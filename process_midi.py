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


def main():
    with open("all-vl70.txt") as fp_in, open('all-vl70.json', 'w') as fp_out:
        json.dump(read(fp_in), fp_out, indent=2)


main()
