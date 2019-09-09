# ragabot
Ragas in Hindustani classical music are characterized by certain structures. The most obvious one is the set of frequencies allowed in a certain raga. Assuming 12 basic frequencies, each raga uses a subset (not necessarily proper subset) of these 12 frequencies. We shall refer to a frequency as a ‘note’. Further, when composing tunes in a raga, there are certain notes that are allowed when notes are increasing in their frequencies (aaroha) and certain other notes when they are decreasing in frequency (avroha). Some ragas are more complicated in that when notes are increasing in frequency there are certain notes from which one must ‘descend’, i.e., use lower frequency notes and then continue the ‘ascent’ of increasing frequency notes. This last structure is also called the ‘chalan’ of the raga. Further, some notes are granted greater relative time than others, often called ‘nyas’ notes.

Given the above structures, an interesting question is the following: are these structures sufficiently well defined for a computer to ‘compose’ tunes in a certain raga?

## A simple usage guide
- Clone the repository
- Create virtual Environment at convenient location using
`python3 -mvenv ragabotvenv`
- Activate virtual Environment using
`source ragabotvenv/bin/activate`
- Install packages using pip and requirements.txt
`pip install -r requirements.txt`
- You can make use of scripts in ragabot/ folder inside repo
```
python train.py bhooptraining.csv --output bhoopmodel.yaml
python bot.py bhoopmodel.yaml bhooptune.csv
python midiconvert.py bhooptune.csv
timidity bhooptune.mid
```
