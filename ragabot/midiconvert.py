from mido import Message, MidiFile, MidiTrack
import sys
import re
import click

def notations():
    saptak  = ['Sa','Re_',"Re","Ga_","Ga","Ma","Ma__","Pa","Dha_","Dha","Ni_","Ni"]
    return [s.lower() for s in saptak] + saptak + [s.upper() for s in saptak]

def get_regex():
    notes = ['Sa','Re_',"Re","Ga_","Ga","Ma__","Ma","Pa","Dha_","Dha","Ni_","Ni"]
    allnotes = [s.lower() for s in notes] + notes + [s.upper() for s in notes] + ["\$"]
    return "|".join([ "({0})".format(i) for i in allnotes])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield m.group()


def midi_for_pauses(p, note, timeslot):
    subnotes = list(generate_tokens(p, note))
    pauses = subnotes.count("$")
    scopy = subnotes[:-pauses]
    t = len(subnotes[:-pauses])
    for item in subnotes[:-pauses][:-1]:
            yield from get_midi_message(item, timeslot=timeslot//t)
    yield from get_midi_message(subnotes[:-pauses][-1], timeslot=timeslot//t+timeslot*pauses)

def get_midi_message(note, velocity=64,timeslot=128, sa=58):
    p = re.compile(get_regex())
    stdnotes = notations()
    start = sa #mandra Sa , c# -> 58
    if note in stdnotes:
        i = stdnotes.index(note)
        s = Message('note_on', note=i+start, channel=0, velocity=velocity, time=4)
        e = Message('note_off', note=i+start, channel=0, velocity=velocity//16, time=timeslot*3)
        yield from [s,e]
    elif "$" in note:
        yield from midi_for_pauses(p, note, timeslot)
    else:
        yield from midi_for_subnotes(p, note, timeslot)

def midi_for_subnotes(p, note, timeslot):
    subnotes = list(generate_tokens(p, note))
    for n in subnotes:
        yield from get_midi_message(n, timeslot=timeslot//len(subnotes))

def test_get_midi_message():
    notes = notations()
    m1,m2 = list(get_midi_message("Sa"))
    assert m1.note == 30 + notes.index("Sa")
    m = list(get_midi_message("SaMa__"))
    assert len(m) == 4
    assert m[0].note == 30 + notes.index("Sa")
    assert m[2].note == 30 + notes.index("Ma__")


def create_midi(seq, filename="tune.mid", program=40, sa=58):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    track.append(Message('program_change', channel=0, program=program, time=0))#grand piono
    for i in seq:
        for m in get_midi_message(i, sa=sa):
            track.append(m)

    mid.save(filename)


def tune_notations(file):
    with open(file) as f:
        for line in f:
            yield from line.strip().split(",")

def midiconvert(notation, midi, sa, instrument):
    if not midi:
        midi = ".".join(notation.split(".")[:-1]+["mid"])
    create_midi(tune_notations(notation), filename=midi, program=instrument, sa=sa)

@click.command()
@click.option("--sa", default=58, help="Mandra sa location on piono, by default c#")
@click.option("--instrument", default=40, help="Instrument, default is violin")
@click.argument("notation", required=True)
@click.argument("midi", default=None , required=False)
def midiconvert_(notation, midi, sa, instrument):
    midiconvert(notation, midi, sa, instrument)

if __name__ == "__main__":
    midiconvert_()
