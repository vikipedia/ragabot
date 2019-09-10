import click
import yaml
from stats import transition_probability, sample
import random

def aalap(initial, histogram):
    transition_prob = transition_probability(histogram)
    current = initial

    while True:
        yield current
        if current not in transition_prob:
            current = random.choice(list(transition_prob.keys()))
            yield current
        probs = transition_prob[current]
        items = [i for i in probs.keys()]
        pvalues = [probs[item] for item in items]
        current = sample(items, pvalues)

def take(seq, n):
    return [next(seq) for i in range(n)]

@click.command()
@click.option("--bitcount", default=16, help="Number of notes to be produced per line")
@click.option("--lines", default=4, help="Number of lines in the tune")
@click.option("--startnote", default='Sa', help="Define a note where tune should start")
@click.argument("model", required=True, type=click.File("r"))
@click.argument("output", default="bottune.csv",type=click.File("w"))
def bot(bitcount, lines, startnote, model, output):
    histogram  = yaml.safe_load(model)
    raga = aalap(startnote, histogram)
    for i in range(lines):
        items = take(raga, bitcount)
        output.write(",".join(items))
        output.write("\n")

if __name__ == "__main__":
    bot()
