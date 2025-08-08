import json
import re


_NOTE = "[A-G](#?)(-?)[0-9]"
MATCH_RANGE = re.compile(fr' (\*\*\*|{_NOTE} - {_NOTE}) ')


def read(lines):
    result = {}
    for i, line in enumerate(lines):
        number, _, rest = line.strip().partition(" ")
        assert int(number) - 1 == i % 128, (i, number)

        bank = "B" if (i // 128) % 2 else "A"
        if i < 256:
            name, range, _, _, _, _, desc = MATCH_RANGE.split(rest)
            instrument = "stock"
            parts = [name, range, desc]
        else:
            instrument = "patchman"
            parts = [rest]

        result.setdefault(instrument, {}).setdefault(bank, {})[number] = parts
    return result


def read_original():
    with open("all-vl70.txt") as fp_in, open('all-vl70.json', 'w') as fp_out:
        json.dump(read(fp_in), fp_out, indent=2)


def compute_genres():
    with open("all-vl70.json") as fp_in, open('categories.json', 'w') as fp_out:
        genres = {}
        for instrument, a in json.load(fp_in).items():
            for bank, b in a.items():
                for number, desc in b.items():
                    msg = f"{instrument}:{bank}:{number}: {desc[0]}"
                    genres.setdefault(find_category(desc), []).append(msg)
        json.dump(genres, fp_out, indent=2)



def find_category(desc):
    for cat in _CATEGORIES:
        if any(c in d for c in cat for d in desc):
            return cat[0]
    return "none"


_CATEGORIES = (
    ("reed", "Reed", "oboe", "Oboe", "Chanter", "Bassoon"),
    ("flute", "flute", "pipe"),
    ("clarinet", "Cla", "inet"),
    ("bass", 'Ba', 'Slap', 'Bs', 'Upright', 'Fnground', 'Fretles', 'Frtles', 'Chamlion'),
    ("violin", "Viol", "viol", "Bow", "Vln"),
    ("cello", "Cell"),
    ("trombone", "Bone", "bone", "Tb"),
    ("trumpet", "Trump", "Tpt"),
    ("guitar", "Guit"),
    ("synth", "Syn"),
)

compute_genres()
