import json
import re
import sys


def dump(d, f):
    with open(f, 'w') as fp:
        json.dump(d, fp, indent=2)
        print('wrote', f, file=sys.stderr)


def load(f):
    with open(f) as fp:
        return json.load(fp)


VL70_DATA =  load("all-vl70.json")

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
    with open("all-vl70.txt") as fp:
        dump(read(fp), "all-vl70.json")


def compute_genres():
    genres = {}
    for instrument, a in VL70_DATA.items():
        for bank, b in a.items():
            for number, desc in b.items():
                msg = f"{instrument}:{bank}:{number}: {desc[0]}"
                genres.setdefault(find_category(desc), []).append(msg)
    dump(genres, "genres.json")



def find_category(desc):
    for cat in _CATEGORIES:
        if any(c in d for c in cat for d in desc):
            return cat[0]
    return "none"


def read_ranges():
    res = {}
    for instrument, r in _RANGES.items():
        for bank, rr in r.items():
            i = 1
            ib = f"{instrument}:{bank}"
            for cat, index in rr:
                cats = res.setdefault(cat, [])
                for i in range(i, index + 1):
                    pc = f"{i:03}"
                    name = VL70_DATA[instrument][bank][pc][0]
                    cats.append(f"{ib}:{pc}: {name}")

    dump(res, "ranges.json")


_CATEGORIES = (
    ("fx", "Mad Tube"),
    ("guitar", "Guit", "Gt"),
    ("sax", "Sax", "Tenr", "Tenor", "Alto", "Bari", "Sop", "Ken", ),
    ("reed", "Reed", "oboe", "Oboe", "Chanter", "Bassoon"),
    ("flute", "Flut", "Picco"),
    ("pipe", "Pipe", "Shak"),
    ("clarinet", "Cla", "inet"),
    ("bass", 'Ba', 'Slap', 'Bs', 'Upright', 'Fnground', 'Fretles', 'Frtles', 'Chamlion'),
    ("violin", "Viol", "viol", "Bow", "Vln"),
    ("cello", "Cell"),
    ("trombone", "Bone", "bone", "Tb"),
    ("trumpet", "Trump", "Tpt", "Flug", "Mangione", "Alpert", "Maynard", "Cornet"),
    ("horn", "Horn", "Hrn"),
    ("synth", "Syn", "Sqr"),
    ("tuba", "Tuba", "Euph"),
)

_RANGES = {
    "stock": {
        "A": (
            ("fx", 1),
            ("synth", 2),
            ("fx", 3),
            ("electric guitar", 4),
            ("synth", 5),
            ("bass", 10),
            ("synth", 26),
            ("bass", 57),
            ("keyboard", 58),
            ("plucked", 60),
            ("percussion", 61),
            ("fx", 71),
            ("acoustic guitar", 72),
            ("electric guitar", 81),
            ("synth", 109),
            ("drone", 109),
            ("clarinet", 110),
            ("pipe", 115),
            ("synth", 118),
            ("sax", 119),
            ("reed", 120),
            ("brass", 121),
            ("sax", 122),
            ("clari", 124),
            ("reed", 125),
            ("guitar", 126),
            ("pipe", 127),
            ("clarinet", 128),
        ),
        "B": (
            ("flute", 2),
            ("sax", 3),
            ("reed", 4),
            ("trumpet", 5),
            ("sax", 7),
            ("trombone", 8),
            ("flute", 9),
            ("sax", 11),
            ("pipe", 12),
            ("violin", 14),
            ("trumpet", 15),
            ("strings", 16),
            ("trumpet", 25),
            ("trombone", 26),
            ("brass", 31),
            ("tuba", 32),
            ("violin", 38),
            ("cello", 43),
            ("strings", 46),
            ("flute", 54),
            ("pipe", 59),
            ("clarinet", 61),
            ("reed", 64),
            ("synth", 65),
            ("sax", 89),
            ("reed", 98),
            ("clarinet", 102),
            ("flute", 103),
            ("reed", 105),
            ("pipe", 106),
            ("reed", 107),
            ("pipe", 108),
            ("synth", 109),
            ("pipe", 110),
            ("synth", 114),
            ("strings", 115),
            ("reed", 116),
            ("strings", 117),
            ("accordion", 118),
            ("harmonica", 122),
            ("pipe", 123),
            ("synth", 124),
            ("tuba", 125),
            ("reed", 125),
        ),
    },
    "patchman": {
        "A": (
            ("trumpet", 16),
            ("trombone", 24),
            ("brass", 30),
            ("tuba", 32),
            ("sax", 61),
            ("flute", 72),
            ("pipe", 94),
            ("clarinet", 99),
            ("reed", 108),
            ("drone", 109),
            ("pipe", 112),
            ("violin", 122),
            ("cello", 126),
            ("strings", 128),
        ),
        "B": (
            ("harmonica", 5),
            ("accordion", 7),
            ("keyboard", 10),
            ("percussion", 12),
            ("plucked", 18),
            ("acoustic guitar", 24),
            ("electric guitar", 49),
            ("synth", 108),
            ("sax", 111),
            ("bass", 128),
        ),
    },
}

read_ranges()
