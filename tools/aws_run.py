"""Run one experiment's search on a throwaway AWS machine instead of the laptop (issue #115).

    uv run --with boto3 python tools/aws_run.py ATTACK RAW_OUT BUDGET

run_experiment.py calls this in place of _runner.py when data/compute.json says {"where": "aws"}. Same contract as
tools/remote_run.py (Modal): exit 0 = the search ran there (the attack itself may still have failed; raw.json says
so); exit 75 = AWS could not run it (no credentials, budget reached, no capacity, a lost machine), and
run_experiment.py runs it on the laptop.

The pattern is ballpark's infra/aws_train.py:
- One one-time spot machine per experiment (c8g.8xlarge: Graviton4, 32 cores, ARM like the M1), cheapest zone first,
  then c7g.8xlarge. No on-demand: without spot capacity the laptop runs it.
- The machine gets a tarball of the repository without .env, .git and the large folders. It has no git, no AWS
  credentials and no open ports; it reads and writes only through presigned S3 links in its boot script.
- The judge's ANTHROPIC_API_KEY sits in its own S3 object, deleted as soon as the machine has fetched it.
- It cannot be forgotten: it shuts itself down (= terminates) when the run ends and at AWS_MAX_MINUTES whatever
  happens, and this script terminates it on every exit path, a stop included.
- Progress, a heartbeat and the checkpoint file come home while it runs; 15 min of silence hands the run back.
- A spot interruption launches once more; the synced checkpoint means finished units are not redone.
- Spend guard: AWS has no hard limit, so once this month's recorded AWS spend reaches budget_dollars in
  data/compute.json, runs go to the laptop.

Credentials: AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY (and optionally AWS_DEFAULT_REGION, default eu-central-1)
in .env, for this project's own IAM user. Env (optional): AWS_INSTANCE_TYPES ("c8g.8xlarge c7g.8xlarge"),
AWS_MAX_MINUTES (1440), K4_REMOTE_TEST=DIR (parity tests: marker, progress and checkpoint go to DIR and changed
files are not written back).
"""
import io
import json
import os
import signal
import sys
import tarfile
import time
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

UNAVAILABLE = 75
TYPES = (os.environ.get("AWS_INSTANCE_TYPES") or "c8g.8xlarge c7g.8xlarge").split()
CORES = {"c8g.8xlarge": 32, "c7g.8xlarge": 32, "c8g.16xlarge": 64, "c7g.16xlarge": 64}
MAX_MINUTES = int(os.environ.get("AWS_MAX_MINUTES", 24 * 60))   # a guard against a forgotten machine, not a budget
BOOT_SILENCE = 15 * 60     # seconds from launch to the first word from the machine
SILENCE = 15 * 60          # seconds without a heartbeat once it runs
TEST_DIR = os.environ.get("K4_REMOTE_TEST")
MARKER = Path(TEST_DIR) / f"remote-run-{os.getpid()}.json" if TEST_DIR else ROOT / "data" / "remote-run.json"
# Never shipped: secrets, version control, and the folders no attack reads (they are large). As tools/remote_run.py.
SKIP_TOP = {".env", ".git", ".venv", "transcripts", "logs", "figures", "design", "Kryptos Blender Model",
            "Unsolved Book Kryptos Chapter", "drafts", ".pytest_cache", "dashboard"}
SKIP_FILES = {"data/remote-run.json", "data/running-experiment.json", "data/experiment-progress.json",
              "data/loop.pid", "data/loop-stop-request"}


def log(msg):
    print(f"[aws] {msg}", flush=True)


def env_file():
    out = {}
    try:
        for line in (ROOT / ".env").read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                out[k.strip()] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def setting():
    try:
        return json.loads((ROOT / "data" / "compute.json").read_text())
    except (OSError, ValueError):
        return {}


def spend_this_month(where="aws"):
    """Dollars this month's runs on `where` cost, from each record's raw.json (as the loop TUI counts them)."""
    month, total = time.strftime("%Y-%m"), 0.0
    for raw in (ROOT / "experiments").glob("*/raw.json"):
        if time.strftime("%Y-%m", time.localtime(raw.stat().st_mtime)) != month:
            continue
        try:
            c = json.loads(raw.read_text()).get("compute") or {}
        except (OSError, ValueError):
            continue
        if c.get("where") == where:
            total += float(c.get("dollars") or 0)
    return total


class Unavailable(Exception):
    pass


# ---------------------------------------------------------------- packaging

def package_code():
    """tar.gz of the working tree without SKIP_TOP / SKIP_FILES / __pycache__. data/checkpoints goes along, so a
    rerun or a relaunch after a spot interruption resumes the units already finished."""
    buf = io.BytesIO()

    def keep(ti):
        parts = Path(ti.name).parts
        if len(parts) > 1 and parts[1] in SKIP_TOP:
            return None
        rel = "/".join(parts[1:])
        if "__pycache__" in parts or ti.name.endswith(".pyc") or rel in SKIP_FILES or ".DS_Store" in parts:
            return None
        return ti
    with tarfile.open(fileobj=buf, mode="w:gz") as t:
        t.add(ROOT, arcname="repo", filter=keep)
    return buf.getvalue()


# ---------------------------------------------------------------- boot script

def boot_script(urls, max_minutes):
    return f"""#!/bin/bash
# Hard deadline first: whatever happens below, this machine is gone by then.
shutdown -h +{max_minutes}
exec > /var/log/k4.log 2>&1
push_log() {{ curl -s -m 60 -X PUT --upload-file /var/log/k4.log '{urls["log"]}' -o /dev/null; }}
( while sleep 30; do push_log; done ) &
done_() {{ echo "[box] $1"; push_log; sync; shutdown -h now; exit 0; }}
echo "[box] boot $(date -u +%FT%TZ) $(nproc) cores"
mkdir -p /opt/job && cd /opt/job
curl -fsS --retry 5 -o secret.env '{urls["secret"]}' || done_ "secret download failed"
curl -fsS --retry 5 -X PUT --data-binary '{{"booted": true}}' '{urls["status"]}' -o /dev/null
set -a; . /opt/job/secret.env; set +a; rm -f /opt/job/secret.env
curl -fsS --retry 5 -o code.tgz '{urls["code"]}' && tar xzf code.tgz -C /opt || done_ "code download failed"
dnf install -y -q gcc tar >/dev/null || done_ "gcc install failed"
export HOME=/root UV_INSTALL_DIR=/usr/local/bin UV_PYTHON_INSTALL_DIR=/opt/python
curl -LsSf https://astral.sh/uv/install.sh | sh >/dev/null || done_ "uv install failed"
cd /opt/repo && uv sync --frozen --python 3.14 -q || done_ "uv sync failed"
echo "[box] $(uv --version)"
echo "[box] ready $(date -u +%FT%TZ) $(.venv/bin/python --version)"
.venv/bin/python tools/aws_box.py /opt/job/job.json
done_ "finished $(date -u +%FT%TZ)"
"""


# ---------------------------------------------------------------- EC2

def find_ami(ec2):
    imgs = ec2.describe_images(Owners=["amazon"], Filters=[
        {"Name": "name", "Values": ["al2023-ami-2023.*-kernel-*-arm64"]},
        {"Name": "architecture", "Values": ["arm64"]},
        {"Name": "state", "Values": ["available"]}])["Images"]
    imgs = [i for i in imgs if "minimal" not in i["Name"]]
    if not imgs:
        raise Unavailable("no Amazon Linux 2023 arm64 image found")
    best = max(imgs, key=lambda i: i["CreationDate"])
    return best["ImageId"], best["Name"], best["RootDeviceName"]


def launch(ec2, ami, root_dev, user_data, tag):
    """Spot only: each type in TYPES, each zone cheapest first. -> (instance id, type, zone, $/h)."""
    from botocore.exceptions import ClientError
    subnets = {s["AvailabilityZone"]: s["SubnetId"] for s in ec2.describe_subnets(
        Filters=[{"Name": "default-for-az", "Values": ["true"]}])["Subnets"]}
    for itype in TYPES:
        prices = {}
        for p in ec2.describe_spot_price_history(
                InstanceTypes=[itype], ProductDescriptions=["Linux/UNIX"],
                StartTime=datetime.now(timezone.utc) - timedelta(hours=1))["SpotPriceHistory"]:
            prices.setdefault(p["AvailabilityZone"], float(p["SpotPrice"]))
        for zone in sorted((z for z in subnets if z in prices), key=prices.get):
            try:
                inst = ec2.run_instances(
                    ImageId=ami, InstanceType=itype, MinCount=1, MaxCount=1, SubnetId=subnets[zone],
                    UserData=user_data, InstanceInitiatedShutdownBehavior="terminate",
                    MetadataOptions={"HttpTokens": "required"},
                    BlockDeviceMappings=[{"DeviceName": root_dev, "Ebs": {"VolumeSize": 16, "VolumeType": "gp3",
                                                                          "DeleteOnTermination": True}}],
                    InstanceMarketOptions={"MarketType": "spot", "SpotOptions": {
                        "SpotInstanceType": "one-time", "InstanceInterruptionBehavior": "terminate"}},
                    TagSpecifications=[{"ResourceType": "instance", "Tags": [
                        {"Key": "Name", "Value": f"k4-{tag}"}, {"Key": "Project", "Value": "cryptos"}]}])["Instances"][0]
            except ClientError as e:
                code = e.response["Error"]["Code"]
                if "Capacity" in code or "Spot" in code or "Unsupported" in code or "MaxSpot" in code:
                    log(f"{itype} {zone}: no capacity ({code})")
                    continue
                raise
            log(f"launched {inst['InstanceId']} {itype} spot in {zone} at ${prices[zone]:.3f}/h")
            return inst["InstanceId"], itype, zone, prices[zone]
    raise Unavailable(f"no spot capacity for {' / '.join(TYPES)} in {ec2.meta.region_name}")


# ---------------------------------------------------------------- one machine

def run_once(sess, attack_rel, budget, ckpt, progress, attempt):
    """-> ("ok", result dict) | ("interrupted", None). Raises Unavailable."""
    from botocore.config import Config
    from botocore.exceptions import ClientError, ConnectionError as BotoConnectionError, HTTPClientError
    region = sess.region_name
    # Regional endpoint + SigV4 + virtual addressing: presigned links to a new bucket on the global endpoint answer
    # 307 for hours, and curl on the box does not follow them (ballpark, 2026-10).
    s3 = sess.client("s3", region_name=region, config=Config(signature_version="s3v4",
                                                             s3={"addressing_style": "virtual"}))
    ec2 = sess.client("ec2")
    account = sess.client("sts").get_caller_identity()["Account"]
    bucket = f"k4-runs-{account}-{region}"
    try:
        s3.head_bucket(Bucket=bucket)
    except ClientError:
        log(f"creating bucket {bucket}")
        s3.create_bucket(Bucket=bucket, CreateBucketConfiguration={"LocationConstraint": region})
        s3.put_public_access_block(Bucket=bucket, PublicAccessBlockConfiguration={
            "BlockPublicAcls": True, "IgnorePublicAcls": True, "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True})
        s3.put_bucket_lifecycle_configuration(Bucket=bucket, LifecycleConfiguration={"Rules": [
            {"ID": "expire-jobs", "Status": "Enabled", "Filter": {"Prefix": "jobs/"}, "Expiration": {"Days": 3}}]})

    tag = f"{Path(attack_rel).parent.name or 'attack'}-{time.strftime('%Y%m%d-%H%M%S')}-{attempt}"[-60:]
    job = f"jobs/{tag}"
    code = package_code()
    s3.put_object(Bucket=bucket, Key=f"{job}/code.tgz", Body=code)
    key = env_file().get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY", "")
    s3.put_object(Bucket=bucket, Key=f"{job}/secret.env", Body=f"ANTHROPIC_API_KEY={key}\n".encode(),
                  ServerSideEncryption="AES256")
    ttl = MAX_MINUTES * 60 + 3600
    sign = lambda op, k, t=ttl: s3.generate_presigned_url(op, Params={"Bucket": bucket, "Key": k}, ExpiresIn=t)
    urls = {"code": sign("get_object", f"{job}/code.tgz"), "secret": sign("get_object", f"{job}/secret.env", 1800),
            "status": sign("put_object", f"{job}/status.json"), "checkpoint": sign("put_object", f"{job}/checkpoint"),
            "log": sign("put_object", f"{job}/box.log"), "result": sign("put_object", f"{job}/result.tgz")}
    itype0 = TYPES[0]
    job_json = json.dumps({"attack": attack_rel, "budget": budget, "workers": CORES.get(itype0, 32),
                           "urls": {k: urls[k] for k in ("status", "checkpoint", "result")}})
    # job.json travels inside the boot script, next to the links it already holds
    user_data = boot_script(urls, MAX_MINUTES).replace(
        "mkdir -p /opt/job && cd /opt/job\n",
        "mkdir -p /opt/job && cd /opt/job\ncat > /opt/job/job.json <<'JOBJSON'\n" + job_json + "\nJOBJSON\n")
    if len(user_data.encode()) > 16000:
        raise Unavailable("boot script over EC2's 16 KB user-data limit")
    ami, ami_name, root_dev = find_ami(ec2)
    log(f"code {len(code) / 1e6:.1f} MB, image {ami} {ami_name}")
    iid, itype, zone, price = launch(ec2, ami, root_dev, user_data, tag)
    t_launch = time.time()
    MARKER.write_text(json.dumps({"pid": os.getpid(), "attack": attack_rel, "where": "aws", "instance": itype,
                                  "cpu": CORES.get(itype, 32), "zone": zone, "dollars_per_hour": price,
                                  "url": f"https://{region}.console.aws.amazon.com/ec2/home?region={region}"
                                         f"#InstanceDetails:instanceId={iid}", "started": t_launch}))
    heard, status_etag, ck_etag, secret_gone, shown, last_state = None, None, None, False, 0, 0.0
    result = None
    try:
        while True:
            time.sleep(15)
            now = time.time()
            try:
                try:
                    o = s3.get_object(Bucket=bucket, Key=f"{job}/status.json", IfNoneMatch=status_etag or "*none*")
                    status_etag, body = o["ETag"], json.loads(o["Body"].read() or b"{}")
                    heard = now
                    if not secret_gone:
                        s3.delete_object(Bucket=bucket, Key=f"{job}/secret.env")
                        secret_gone = True
                        log(f"machine up after {now - t_launch:.0f}s; key fetched and deleted from S3")
                    if body.get("progress"):
                        progress.write_text(body["progress"])
                except ClientError as e:
                    if e.response["Error"]["Code"] not in ("304", "NoSuchKey", "NotModified"):
                        raise
                try:
                    o = s3.get_object(Bucket=bucket, Key=f"{job}/checkpoint", IfNoneMatch=ck_etag or "*none*")
                    ck_etag, data = o["ETag"], o["Body"].read()
                    if not ckpt.exists() or len(data) >= ckpt.stat().st_size:
                        ckpt.parent.mkdir(parents=True, exist_ok=True)
                        ckpt.write_bytes(data)
                except ClientError as e:
                    if e.response["Error"]["Code"] not in ("304", "NoSuchKey", "NotModified"):
                        raise
                try:
                    o = s3.get_object(Bucket=bucket, Key=f"{job}/box.log", Range=f"bytes={shown}-")
                    chunk = o["Body"].read()
                    sys.stdout.write(chunk.decode(errors="replace")); sys.stdout.flush()
                    shown += len(chunk)
                except ClientError:
                    pass
                try:
                    o = s3.get_object(Bucket=bucket, Key=f"{job}/result.tgz")
                    result = o["Body"].read()
                    break
                except ClientError as e:
                    if e.response["Error"]["Code"] != "NoSuchKey":
                        raise
                if now - last_state > 60:
                    last_state = now
                    st = ec2.describe_instances(InstanceIds=[iid])["Reservations"][0]["Instances"][0]
                    if st["State"]["Name"] in ("shutting-down", "terminated", "stopping", "stopped"):
                        time.sleep(60)    # grace for a late upload
                        try:
                            result = s3.get_object(Bucket=bucket, Key=f"{job}/result.tgz")["Body"].read()
                            break
                        except ClientError:
                            pass
                        reason = st.get("StateReason", {}).get("Message", "?")
                        log(f"machine {st['State']['Name']} without a result: {reason}")
                        if "Spot" in reason or "spot" in reason:
                            return "interrupted", None
                        raise Unavailable(f"machine ended without a result ({reason})")
            except (OSError, BotoConnectionError, HTTPClientError) as e:   # laptop network trouble: the machine keeps running
                log(f"network trouble ({type(e).__name__}); still waiting")
            if heard is None and now - t_launch > BOOT_SILENCE:
                raise Unavailable(f"no word from the machine {BOOT_SILENCE // 60} min after launch")
            if heard is not None and now - heard > SILENCE:
                raise Unavailable(f"no heartbeat for {SILENCE // 60} min")
    finally:
        MARKER.unlink(missing_ok=True)
        for attempt_ in range(10):     # the machine also shuts itself down; this is the belt to its braces
            try:
                ec2.terminate_instances(InstanceIds=[iid])
                break
            except Exception as e:  # noqa: BLE001
                log(f"terminate {iid} failed ({e!r}), retrying")
                time.sleep(20)
        try:
            s3.delete_object(Bucket=bucket, Key=f"{job}/secret.env")
        except Exception:  # noqa: BLE001
            pass
        machine_s = time.time() - t_launch
        log(f"machine {iid} terminated after {machine_s / 60:.1f} min, about ${price * machine_s / 3600:.2f}")
    with tarfile.open(fileobj=io.BytesIO(result)) as t:
        files = {m.name: t.extractfile(m).read() for m in t.getmembers() if m.isfile()}
    meta = json.loads(files.pop("meta.json"))
    return "ok", {"raw": files.pop("raw.json", None), "files": {k[6:]: v for k, v in files.items()
                                                                if k.startswith("files/")},
                  "seconds": meta["seconds"], "exit": meta["exit"], "instance": itype, "zone": zone,
                  "machine_seconds": machine_s, "dollars": price * machine_s / 3600}


def main(attack, raw_out, budget):
    attack_rel = str(Path(attack).resolve().relative_to(ROOT))
    env = env_file()
    for k in ("AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_DEFAULT_REGION"):
        if env.get(k):
            os.environ.setdefault(k, env[k])
    os.environ.setdefault("AWS_DEFAULT_REGION", "eu-central-1")
    if not os.environ.get("AWS_ACCESS_KEY_ID"):
        print("aws_run: no AWS credentials in .env; running locally")
        return UNAVAILABLE
    limit = setting().get("budget_dollars")
    spent = spend_this_month()
    if limit is not None and spent >= float(limit):
        print(f"aws_run: this month's AWS spend ${spent:.2f} has reached the budget ${float(limit):.2f}; running locally")
        return UNAVAILABLE
    from kryptos import checkpoint
    ckpt = checkpoint.path_for(attack, root=TEST_DIR)
    progress = Path(TEST_DIR) / f"progress-{os.getpid()}.json" if TEST_DIR else ROOT / "data" / "experiment-progress.json"

    def stop(signum, frame):
        """Stopped (tools/stop_experiment.sh): unwinding terminates the machine. uv passes the signal on too, so
        a second one is ignored rather than cutting the cleanup short."""
        signal.signal(signal.SIGTERM, signal.SIG_IGN)
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    try:
        import boto3
        sess = boto3.session.Session()
        for attempt in range(2):
            state, final = run_once(sess, attack_rel, budget, ckpt, progress, attempt)
            if state == "ok":
                break
            log("spot interruption; launching once more (finished units are kept)")
        else:
            raise Unavailable("spot machine interrupted twice")
    except KeyboardInterrupt:
        print("aws_run: stopped; machine terminated")
        return 130
    except Exception as e:  # noqa: BLE001  (no capacity, credentials, network, lost machine)
        print(f"aws_run: AWS could not run the experiment: {e!r}")
        return UNAVAILABLE
    if final["raw"] is None:
        print(f"aws_run: the run on AWS ended without raw.json (exit {final['exit']})")
        return UNAVAILABLE
    for rel, data in ({} if TEST_DIR else final["files"]).items():
        dest = ROOT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
    raw = json.loads(final["raw"])
    cores = CORES.get(final["instance"], 32)
    raw["compute"] = {"where": "aws", "instance": final["instance"], "zone": final["zone"], "market": "spot",
                      "cpu": cores, "workers": cores, "python": "3.14", "seconds": round(final["seconds"], 1),
                      "machine_seconds": round(final["machine_seconds"], 1), "dollars": round(final["dollars"], 3)}
    Path(raw_out).write_text(json.dumps(raw, indent=1))
    print(f"aws_run: done on AWS in {final['seconds'] / 60:.1f} min (machine {final['machine_seconds'] / 60:.1f} min, "
          f"${final['dollars']:.2f}); {len(final['files'])} files returned")
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:4]))
