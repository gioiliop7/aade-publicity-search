def get_key(d: dict, endswith: str):
    for k, v in d.items():
        if k.endswith(endswith):
            return v
    return None


def validate_afm(afm: str) -> bool:
    if not afm.isdigit() or len(afm) != 9 or afm == "000000000":
        return False
    m = 1
    s = 0
    for i in range(7, -1, -1):
        m *= 2
        s += int(afm[i]) * m
    return (s % 11) % 10 == int(afm[8])
