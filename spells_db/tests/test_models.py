from spells_db.models import Spell, SpellType, SpellTypeMapping


def test_spell():
    spell = Spell('Accio', 'Summaning Charm')
    assert spell.active
    assert spell.to_dict() == {
        'ID': None,
        'active': True,
        'name': 'Accio',
        'description': 'Summaning Charm',
        'history': None,
        'spell_types': [],
    }


def test_spelltype():
    spell_type = SpellType('dark')
    assert spell_type.active
    assert spell_type.to_dict() == {
        'ID': None,
        'active': True,
        'name': 'dark',
        'description': None,
        'spells': [],
    }


def test_spell_type_mapping():
    mapping = SpellTypeMapping(1, 2)
    assert mapping.active
    assert mapping.to_dict() == {
        'ID': None,
        'active': True,
        'spell_id': 1,
        'spell_type_id': 2,
    }
