#include <string.h>
#include <stdint.h>
static uint64_t s_; static inline uint64_t rnd(void){ s_^=s_<<13; s_^=s_>>7; s_^=s_<<17; return s_; }
static inline void permute(int *w, int rot, int ext){ int tmp[26]; for(int j=0;j<26;j++) tmp[j]=w[(j+rot)%26];
  int x=tmp[ext]; for(int j=ext;j<13;j++) tmp[j]=tmp[j+1]; tmp[13]=x; memcpy(w,tmp,sizeof tmp); }
/* given L0, the index stream: ridx[t] = original R0 index under the right wheel at step t */
double icstream(const int *L0, const int *ct, int n, int *out){
  int L[26], R[26], pos[26], cnt[26]={0}; memcpy(L,L0,sizeof L); for(int j=0;j<26;j++) R[j]=j;
  for(int s=0;s<n;s++){ for(int j=0;j<26;j++) pos[L[j]]=j; int i=pos[ct[s]]; int r=R[i]; cnt[r]++; if(out) out[s]=r;
    permute(L,i,1); permute(R,(i+1)%26,2); }
  double t=0; for(int j=0;j<26;j++) t+=cnt[j]*(cnt[j]-1.0); return t/(n*(n-1.0)); }
double anneal(const int *ct, int n, long iters, double T0, uint64_t seed, int *best){
  s_=seed*2654435761ULL+1; int L[26]; for(int j=0;j<26;j++) L[j]=j;
  for(int j=25;j>0;j--){int k=rnd()%(j+1); int t=L[j]; L[j]=L[k]; L[k]=t;}
  double cur=icstream(L,ct,n,0), bs=cur; memcpy(best,L,sizeof L);
  for(long it=0;it<iters;it++){ double T=T0*(1.0-(double)it/iters)+1e-6; int a=rnd()%26,b=rnd()%26; if(a==b) continue;
    int t=L[a]; L[a]=L[b]; L[b]=t; double v=icstream(L,ct,n,0);
    if(v>=cur || (rnd()%1000000)/1e6 < __builtin_exp((v-cur)/T)){ cur=v; if(v>bs){bs=v; memcpy(best,L,sizeof L);} }
    else { t=L[a]; L[a]=L[b]; L[b]=t; } }
  return bs; }
