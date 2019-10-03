from train import train
from bot import bot
from midiconvert import midiconvert
from midiplay import play
import click

@click.command()
@click.argument("inputnotations",nargs=-1,required=True, type= click.File("r"))
def player(inputnotations):
    model = "playermodel.yaml"
    with open(model, "w") as output:
        train(inputnotations, output)
    botoutput = "bottune.csv"
    with open(botoutput, "w") as output:
        with open(model) as mod:
            bot(bitcount=16,
                lines=4,
                startnote="Sa",
                model=mod,
                output=output
                )
    midifile = botoutput.replace(".csv",".mid")
    midiconvert(notation=botoutput, midi=midifile, sa=58, instrument=40)
    print(midifile)
    play(music_file=midifile)

if __name__ == "__main__":
    player()
