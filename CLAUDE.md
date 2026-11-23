# CLAUDE.md

This file gives Claude Code guidance for working in this repository.

## What this is

Ragabot composes tunes in a Hindustani classical raga. It reads example tunes written in sargam notation, learns a first-order Markov chain of note-to-note transitions, samples new tunes from that chain, converts them to MIDI and plays them. It was presented at PyCon India 2019 (`notebooks/Ragabot-pycon2019.ipynb`).

## Setup

```bash
python3 -m venv ragabotvenv && source ragabotvenv/bin/activate
pip install -r requirements.txt          # click, mido, pygame, PyYAML
sudo apt-get install freepats timidity   # Linux only, for MIDI playback
```

## Running

The modules use flat imports (`import stats`, `from bot import bot`), not package-relative ones. Run them as scripts from inside `ragabot/`:

```bash
cd ragabot
python train.py ../data/bhooptraining.csv --output bhoopmodel.yaml  # notation CSV(s) -> model YAML
python bot.py bhoopmodel.yaml bhooptune.csv                         # model -> generated notation CSV
python midiconvert.py bhooptune.csv [out.mid] --sa 58 --instrument 40
python midiplay.py bhooptune.mid
python botplayer.py ../data/tilakkamod*.csv                         # all four steps at once
```

`botplayer.py` always writes `playermodel.yaml`, `bottune.csv` and `bottune.mid` to the current directory. It uses 4 lines of 16 notes, starts on `Sa`, and plays violin (program 40).

`ragabot/__init__.py` does `from . import stats`. Only `stats` can be imported as `ragabot.stats`. The other modules break when imported through the package, because their flat imports only work with `ragabot/` on `sys.path`.

## Tests

There is no test suite. A few `test_*` functions sit next to the code: `stats.test_histogram`, `stats.test_sample` and `midiconvert.test_get_midi_message`. Run them with `cd ragabot && python -m pytest stats.py midiconvert.py`.

`test_sample` is statistical. It draws 10,000 samples and allows 1% tolerance, so it can fail now and then.

## Architecture

The pipeline is train → bot → midiconvert → midiplay. Each stage is a plain function plus a Click wrapper whose name ends in `_` (for example `bot_`). `botplayer.py` chains the plain functions.

- **`stats.py`**: `histogram(lines)` builds `{note: {next_note: count}}`, counting transitions within each line only, never across lines. `transition_probability` normalises those counts. `sample` draws from them using cumulative weights.
- **`train.py`**: reads one or more CSVs (one tune line per row) and dumps the histogram as YAML. The model file holds raw counts, not probabilities.
- **`bot.py`**: `aalap()` is an infinite generator that walks the Markov chain from `startnote`. When it reaches a note with no outgoing transitions, it jumps to a random known note. `bot()` writes `lines` rows of `bitcount` tokens.
- **`midiconvert.py`**: tokenises each notation cell with a regex and emits mido `note_on`/`note_off` messages. `sa` is the MIDI number of mandra Sa (default 58). Pitch is `sa + index` into `notations()`.
- **`midiplay.py`**: plays a MIDI file with blocking `pygame.mixer.music` playback.

## Notation format

- **Swaras:** `Sa Re Ga Ma Pa Dha Ni`.
  - A `_` suffix means komal (flat), for example `Re_` or `Ni_`.
  - `Ma__` is tivra (sharp) Ma.
- **Octave is set by case:**
  - lowercase is mandra (low), for example `dha`.
  - Titlecase is madhya (middle), for example `Dha`.
  - UPPERCASE is taar (high), for example `DHA`.
- **One CSV cell is one beat.**
  - Several notes joined in one cell (`GaRe`, `DhaSA`) split the beat equally.
  - Each trailing `$` adds one beat of sustain to the last note in the cell, so `Pa$$` lasts three beats.
- **Model tokens:** the Markov model treats every cell string as an opaque token, so `Pa`, `Pa$` and `GaPa` are three different states. Only `midiconvert` parses inside a cell.
- **Order matters in two lists:**
  - In `notations()`, the list order is chromatic and sets pitch, so `Ma` comes before `Ma__`.
  - In `get_regex()`, `Ma__` must come before `Ma` so that it matches the longer token first.
  - Keep both lists in sync if you change either one.

## Data and gitignore

- `data/` holds the training tunes (raga Bhoop, Tilak Kamod, Vande Mataram), along with MIDI and MP3 renders.
- `.gitignore` excludes `*.csv`, `*.yaml` and `*.mid`, so the tracked data files were force-added. Use `git add -f` to commit a new training CSV.
- Generated files such as `bottune.*` and `playermodel.yaml` should stay untracked.
