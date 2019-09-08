import click
import yaml
import stats

def read_notations(files):
    for f in files:
        for line in f:
            yield line.strip().split(",")

@click.command()
@click.option("--output", default="model.yaml", type=click.File("w"))
@click.argument("notations", nargs=-1,required=True,
                type= click.File("r"))
def train(notations, output):
    hist = stats.histogram(read_notations(notations))
    yaml.dump(hist, output)

if __name__ == "__main__":
    train()
