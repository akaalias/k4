# Glossary

Plain definitions of the words the experiment pages use. Each entry is one term, its
other names in brackets, and a definition a newcomer can read without the rest of the
site. The dashboard shows, under each experiment's plain-words text, the entries whose
term or alias appears in that text. Keep entries short; add one whenever a new experiment
uses a word a stranger would not know.

**the message** (also: plaintext, the English, the fourth message): The 97 letters of English that Jim Sanborn wrote and enciphered. Nobody outside a few people has read them. Recovering them, and the method that hides them, is the goal.

**the carved letters** (also: ciphertext, the scrambled text, the carved text, K4): The 97 letters cut into the copper at the CIA, shown at the top of every experiment page. They are the message after the cipher was applied.

**the known letters** (also: cribs, the 24 known letters, the clue words): Sanborn has confirmed that positions 22 to 34 of the message read EASTNORTHEAST and positions 64 to 74 read BERLINCLOCK. These 24 letters are the only hard facts about the message, and every experiment leans on them.

**the secret word** (also: the key, key word, a repeating secret word): The word or string a cipher needs besides the method. In the first two messages on the sculpture the secret words were PALIMPSEST and ABSCISSA, used with the table.

**the table** (also: the tableau, the sculpture's table, the big table): The right-hand half of the sculpture, 26 rows of the alphabet each shifted one place further, starting from the word KRYPTOS. To encipher a letter you find its column, go down to the row of the secret word's letter, and read off the letter there. It is how the first two messages were made.

**the sculpture's alphabet** (also: the KRYPTOS alphabet, the sculpture's two alphabets): The alphabet reordered to begin with KRYPTOS: KRYPTOSABCDEFGHIJLMNQUVWXZ. The table is built from it. "The sculpture's two alphabets" means this one and the ordinary A to Z.

**the plain alphabet** (also: the ordinary alphabet, the standard alphabet): A to Z in the usual order.

**the puzzle's words** (also: the vocabulary, every word the puzzle knows, the puzzle's own world): A list of 62 words tied to the sculpture: the earlier secret words, place names, the names of the people involved, the words in the Morse code, and the themes Sanborn has named. Many experiments try each of these as the secret word or as the word that reorders the alphabet.

**a reordered alphabet** (also: an alphabet built from a word, keyword-mixed alphabet, the table built from another word, every table the puzzle's words can build): An alphabet that starts with a word, dropping repeated letters, followed by the rest of A to Z. KRYPTOS gives the sculpture's alphabet; PALIMPSEST would give PALIMSETBCDFGHJKNOQRUVWXYZ. There are four standard ways of finishing the reordering, and the experiments try all four.

**a repeating secret word** (also: a periodic key, period, the length of the secret word): A secret word written under the message again and again. Its length is the period. Two message letters the same distance apart as the period are enciphered with the same letter of the word, which is what lets the known letters test a period.

**an autokey cipher** (also: autokey, the message as its own key, keyed by itself): A cipher that uses the message itself, or the scrambled text itself, as the secret word, each letter enciphered with the letter a fixed distance before it. That distance is the lag.

**the lag** (also: a fixed distance back): In an autokey cipher, how far back the key letter sits from the letter being enciphered.

**a running key** (also: a book as the key, a long text as the key): A secret word as long as the message, taken from a book or another text. The experiments slide candidate texts along the message at every starting point.

**a grid** (also: a matrix, a scramble, a transposition, a route, a columnar transposition): Writing the message into rows of some width and reading it out in another order, column by column for instance, which shuffles the letters without changing them. The third message on the sculpture was hidden this way. A keyed grid reads the columns in the order given by a word.

**a mask** (also: disguise): Something done to the English before the cipher proper, such as writing it backwards or slipping in meaningless letters, that is not itself a cipher but moves or hides the letters.

**nulls** (also: meaningless letters, padding): Letters inserted into a message that carry no meaning, used to pad it or to disguise it.

**a shift** (also: a nudge, a push along the alphabet): Moving a letter a fixed number of places along an alphabet, A to D for a shift of three.

**the forced letter** (also: forced key letter, what the known letters force, pinned letters): Given a known message letter, its carved letter, and a way of using the table, the one letter of the secret word that would turn the first into the second. The 24 known letters force 24 such letters.

**a slot** (also: a position in the secret word): One letter position of a repeating secret word. Two message positions that share a slot must force the same letter, or that period is dead.

**a collision** (also: two known letters that would use the same letter, a clash): Two known letters that land on the same slot or the same cell and therefore must agree.

**dead** (also: ruled out, ruled that out, killed): Said of a period, grid or method when the known letters contradict it: no secret word of that kind can produce the carved letters.

**the chain** (also: the chain closes, the chain breaks, fills the whole message): In an autokey cipher each known letter reveals the letter one lag later and the letter one lag earlier; those reveal more, and so on. If two revelations disagree the chain breaks; if they never do and reach every position, the chain fills the whole message.

**a way of using the table** (also: a convention, the 24 ways): Whether the message is looked up on the sculpture's alphabet or the plain one, whether the carved letters are, whether the secret word is, and whether letters are added or subtracted. Two choices for each of three alphabets and three rules of arithmetic make 24 ways; most experiments try all of them.

**Vigenere** (also: adding, Beaufort, subtracting): The three rules of arithmetic a table can use: add the key letter to the message letter, subtract the message letter from the key letter, or subtract the key letter from the message letter. Vigenere is the first; the Beauforts are the other two.

**a shuffled control** (also: shuffled K4, random letters, the control, a scrambled version of the carved text): The same experiment run on the carved letters shuffled into a random order. Whatever the experiment finds on the shuffle is what luck alone can produce, so a result on the real text counts only if it beats the shuffles.

**the English score** (also: reads like English, reads most like English, quadgram score): A number saying how much a stretch of letters looks like English, computed from how common each run of four letters is in English text. Real English scores about -3.6, random letters about -6.5; higher is better.

**loss** (also: the loss, the hero number): The single number the loop tries to drive to zero: ten points for each of the 24 known letters a candidate gets wrong, plus how far the other 73 letters are from English, plus a charge for a secret word too long to remember.

**the crib gate** (also: the line at ten): The point on the loss scale below which every one of the 24 known letters is in place.

**the champion** (also: kept): The candidate with the lowest loss so far among those that passed every check. An experiment is kept when it produces a new champion, reverted otherwise. Reverted is the normal outcome; a reverted experiment still leaves a bounded negative.

**a bounded negative** (also: a dead end with a stated reason): The guaranteed product of every experiment: a precise statement of what was tried and found impossible, so nobody has to try it again.

**a Hill cipher** (also: Hill, a mixing table of numbers): A cipher that turns letters into numbers, takes them two, three or four at a time, and mixes each group with a fixed table of numbers. Named for Lester Hill; the sculpture's grid has a column reading HILL.

**Gromark** (also: a growing number stream, a Fibonacci-style stream): A cipher whose secret is a short number that grows into a long stream of digits by adding pairs of earlier digits; each message letter is pushed along the alphabet by the next digit.

**Porta**: An old cipher that cuts the alphabet into two halves and always swaps a letter into the other half, with the secret word choosing one of thirteen swap patterns.

**trifid** (also: the cube): A cipher that turns each letter into three small digits, like floor, row and seat in a 27-seat cube, writes several letters' digits in rows, and regroups them, so each new letter is made from pieces of three old ones.

**the one-to-one mapping** (also: letter for letter, one carved letter stands for one message letter): The idea, attributed to Sanborn, that each carved letter in the clue stretches is the direct image of the message letter in the same position.

**a mirror** (also: backwards, reversed): Reading or writing the text from the end to the start.

**trial and error** (also: simulated annealing, hill-climbing, the computer rearranges, climbed): Letting a program change a key one small step at a time, keeping steps that improve a score and sometimes accepting worse ones to escape a rut. It finds good answers when the score is a smooth guide and fails when it is not.

**the width-21 repeats** (also: letters 21 apart behaving alike, vertical pairs): When the carved letters are written in rows of 21, pairs of letters stacked one above the other repeat more often than chance allows. The same was true at width 19 in the Zodiac killer's 340-letter cipher and turned out to be a trace of its method.

**the doublets** (also: a letter repeating its neighbour, the doublet column): Places where a carved letter is immediately followed by the same letter. K4 has six, and five of them fall in the same column when the text is written in rows of seven.

**the index of coincidence** (also: how evenly the letters are spread): The chance that two letters picked at random from the text are the same. English gives about 0.066, random letters 0.038, K4 0.036, so K4's letters are spread as flat as random.

**the workshop** (also: the simulator, fake K4s): An experiment that builds thousands of pretend K4s by each suspected method and measures them, to learn which methods produce text that looks like the real one. It points, it does not solve.

**the earlier messages** (also: K1, K2, K3, the first three messages, the third message): The three solved parts of the sculpture. K1 and K2 used the table with the secret words PALIMPSEST and ABSCISSA; K3 was a grid scramble. K3 retells Howard Carter opening Tutankhamun's tomb.

**an anagram** (also: shuffled letters, a rearrangement): The same letters in a different order, with none added, removed or changed.
