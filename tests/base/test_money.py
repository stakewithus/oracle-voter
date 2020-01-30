from oracle_voter.base.money import Note


def test_note_operations():
    a = Note("145.66")
    b = Note("10")
    c = a * b
    assert(str(c) == "1456.600000000000000000000000")
