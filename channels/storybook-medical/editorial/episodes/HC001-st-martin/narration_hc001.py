"""HC001-L narration: the approved script (script-long-v1.md), one sentence per line, one take per chapter.
Narrator spellings from editorial/pronunciation.csv (Mackinaw, Saint Martin); captions map them back at build."""
import json
from pathlib import Path

P = Path("projects/hc001-window-into-his-stomach/episode.json")

CH = [
 ("ch0", 3.3, """[excited] A doctor ties a piece of beef to a silk string.
Then he lowers it… into a living man's stomach.
He checks his watch.
One hour.
He pulls the string.
Half the food is GONE.
And the man?
He gets up and goes back to work.
[curious] Nobody cut him open.
That opening was already there…
and it had been there for three years.
So how does a man end up with a window into his own stomach?"""),
 ("ch1", 1.2, """Mackinaw Island, eighteen twenty-two.
A fur-trade post on an island between two of the Great Lakes.
Every summer the voyageurs paddled in: the canoe-men who moved the fur trade, one stroke at a time.
One of them is Alexis Saint Martin.
About eighteen.
French-Canadian.
Working for the American Fur Company.
On the sixth of June, a musket goes off.
By accident.
Loaded with powder and duck shot…
fired from less than a METER away.
The army surgeon at the fort, William Beaumont, reaches him in about half an hour.
[whispers] What he sees is something doctors almost never see.
He can look straight into Alexis's stomach.
By every rule of eighteen twenty-two medicine, Alexis should not survive the day.
He does.
And that's where the trouble starts."""),
 ("ch2", 1.2, """For seventeen days, everything he swallows comes back out… through the wound.
Then, slowly, he gets stronger.
Beaumont spends eight, ten months trying to close the opening.
There's one option left: stitch it shut.
Alexis says NO.
We don't know his reasons.
But surgery in the eighteen-twenties meant no anaesthetic.
None.
So his body found another way.
That winter, a fold of the stomach lining grew across the hole… like a little lid.
Press it with a finger, and it opens.
[curious] And Beaumont realised what he was looking at."""),
 ("ch3", 1.2, """Here's the thing.
In the eighteen-twenties, doctors were still arguing about what the stomach actually does.
Some said it grinds food, like a mill.
Others said food just… rots in there.
To settle it, you'd need to watch a living stomach while it worked.
Beaumont had no laboratory.
He was an army doctor at a frontier fort.
What he had… was Alexis."""),
 ("ch4", 1.2, """Remember the string?
That was the first of them: August the first, eighteen twenty-five.
Six foods, from spiced beef to raw cabbage.
After two hours, the cabbage, the bread, the pork and the boiled beef were "cleanly digested, and gone from the string."
[mischievously] The next day Alexis felt unwell.
So Beaumont dropped his medicine straight in.
Through the hole.
No forms.
No ethics board.
Just a doctor, a pocket watch and a notebook.
Then he went further.
He collected some of the stomach's juice, put it in glass vials with pieces of meat… and kept them warm.
The meat dissolved.
Slowly, but it dissolved.
OUTSIDE the body.
A clear, slightly salty, very acid juice was breaking the food down.
Digestion wasn't just grinding, and it wasn't rotting.
It was, in large part, chemistry.
And yes.
Beaumont wrote that he put his own tongue on the inside of Alexis's stomach.
Empty: no acid taste.
With food in it: sour, right away.
He also noted Alexis's "anger and impatience", and believed strong emotion upset digestion.
[curious] Alexis, to be fair, had reasons to be impatient.
In the end there would be two hundred and thirty-eight numbered experiments.
But Beaumont's experiment had one problem.
It could WALK away."""),
 ("ch5", 1.2, """In eighteen twenty-five, Alexis left.
He went home to Canada, "without obtaining my consent," Beaumont wrote.
For four years he lived his own life.
He married.
Had two children.
Paddled for the Hudson's Bay Company.
Then in eighteen twenty-nine, fur-company agents brought him back.
With his wife and children.
Nearly two thousand MILES.
"At great expense to me," Beaumont noted.
Between experiments, Alexis worked as the doctor's servant.
Chopping wood.
Carrying loads.
In eighteen thirty-one the family left again… in an open canoe.
Down the Mississippi, up the Ohio, across the Great Lakes, down the Saint Lawrence, all the way to Montreal.
[curious] Think about that.
A man with an opening in his side, paddling his family across half a continent.
The next year, cholera swept through Canada.
Alexis survived that too.
By eighteen thirty-three he was back with Beaumont, in Washington.
On paper, Alexis was now a SERGEANT in the army.
And there was a contract.
It made him Beaumont's "covenant servant."
He had to submit to experiments "on or in" his stomach.
The pay: board, lodging, and a hundred and fifty dollars a year.
Alexis couldn't read it.
He couldn't read or write at all.
And the contract was drafted by the man paying him.
[whispers] That's the part most versions of this story leave out.
His comrades even had a nickname for him: "the man with a lid on his stomach."
Then, in eighteen thirty-four, a letter came from Canada, written for Alexis.
His wife was not willing to let him go.
He never worked for Beaumont again.
Beaumont never stopped trying."""),
 ("ch6", 1.2, """In eighteen thirty-three, Beaumont had published everything, in a book called "Experiments and Observations on the Gastric Juice, and the Physiology of Digestion."
Doctors in Europe wanted to see Alexis for themselves.
A London society reportedly raised hundreds of pounds to bring him over.
Beaumont kept writing to him.
In eighteen forty-six he sent his own son to fetch Alexis.
By then Alexis had his own farm.
He stayed.
In eighteen fifty-two Beaumont offered five hundred dollars a year.
More than three times the old contract.
His last letter ends: "Don't disappoint me more."
Six months later, Beaumont died after a fall in Saint Louis.
Alexis outlived him by twenty-seven years."""),
 ("ch7", 1.2, """Now, if you've heard this story before, you probably heard a few things that aren't quite right.
It wasn't a shotgun.
Beaumont says a musket, loaded with duck shot.
Alexis wasn't a fur trader.
He was a voyageur: the guy paddling the canoe, not the guy selling the furs.
"The wound never healed"?
It healed around an opening.
Beaumont tried to close it, and Alexis refused the stitches.
[whispers] Even the library that holds Beaumont's own papers says some suspect he left it open on purpose.
Nobody can prove it.
And the strangest bit, the doctor tasting the stomach?
That one's TRUE.
He wrote it down himself.
Even Alexis's age is a puzzle.
The records disagree by years.
Which brings us to the last chapter."""),
 ("ch8", 1.2, """In June eighteen eighty, Alexis Saint Martin died in Quebec.
A young doctor in Montreal, William Osler, later one of the most famous physicians in the world, wrote to the family.
He offered to pay for the stomach.
For a museum.
The family said NO.
According to the parish priest, they kept Alexis's body at home much longer than usual, in the summer heat.
And they had his grave dug eight feet deep.
So that nobody could ever take him.
[whispers] After fifty-eight years of doctors, the last decision about his body was made by the people who loved him."""),
 ("ch9", 0.8, """Every time someone explains how your stomach digests food, part of that story started with a silk string on a frontier island.
It came from a man who was shot by accident, said no to surgery, and kept trying to go home.
Medicine owes a lot to people who never asked to be part of history.
And Alexis wasn't the last person whose body became an experiment.
Some doctors… volunteered their OWN."""),
]

ep = json.load(open(P, encoding="utf-8"))
ep["narration"] = {"chapters": [{"id": i, "gap_after": g, "v3_text": t} for i, g, t in CH],
                   "punch_words": ["gone", "meter", "no", "outside", "walk", "miles", "sergeant", "true", "own"]}
json.dump(ep, open(P, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
chars = sum(len(t) for _, _, t in CH)
print(f"{len(CH)} chapters, {chars} characters, {sum(len(t.split()) for _, _, t in CH)} words")
