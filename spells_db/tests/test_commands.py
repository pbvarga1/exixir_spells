import pytest

from spells_db.models import Spell, SpellType, SpellTypeMapping
from spells_db import commands


@pytest.fixture(autouse=True)
def spell(session):
    resource = Spell('Accio', 'Summaning Charm')
    session.add(resource)
    session.commit()
    yield resource


@pytest.fixture(autouse=True)
def spell_type(session):
    resource = SpellType('Everyday')
    session.add(resource)
    session.commit()
    yield resource


@pytest.fixture(autouse=True)
def spell_type_mapping(session, spell, spell_type):
    resource = SpellTypeMapping(1, 1)
    session.add(resource)
    session.commit()
    yield resource


def test_get_spell(spell):
    assert commands.get_spell(1) == {
        'ID': 1,
        'active': True,
        'name': 'Accio',
        'description': 'Summaning Charm',
        'history': None,
        'spell_types': [
            {'ID': 1, 'active': True, 'name': 'Everyday', 'description': None}
        ]
    }


def test_get_spell_type(spell_type):
    assert commands.get_spell_type(1) == {
        'ID': 1,
        'active': True,
        'name': 'Everyday',
        'description': None,
        'spells': [
            {
                'ID': 1,
                'active': True,
                'name': 'Accio',
                'description': 'Summaning Charm',
                'history': None,
            }
        ]
    }


def test_get_spell_mapping(spell_type_mapping):
    assert commands.get_spell_mapping(1) == {
        'ID': 1,
        'active': True,
        'spell_id': 1,
        'spell_type_id': 1
    }


def test_get_spells(spell):
    assert commands.get_spells('Accio') == [{
        'ID': 1,
        'active': True,
        'name': 'Accio',
        'description': 'Summaning Charm',
        'history': None,
        'spell_types': [
            {'ID': 1, 'active': True, 'name': 'Everyday', 'description': None}
        ]
    }]
    assert commands.get_spells('foo') == []


def test_get_spell_type_by_name(spell_type):
    assert commands.get_spell_types('Everyday') == [{
        'ID': 1,
        'active': True,
        'name': 'Everyday',
        'description': None,
        'spells': [
            {
                'ID': 1,
                'active': True,
                'name': 'Accio',
                'description': 'Summaning Charm',
                'history': None,
            }
        ]
    }]
    assert commands.get_spell_types('foo') == []


def test_create_spell():
    spell = commands.create_spell(
        'Duro',
        'Hardens materials',
        spell_type_ids=[1],
    )
    assert spell == {
        'ID': 2,
        'active': True,
        'name': 'Duro',
        'description': 'Hardens materials',
        'history': None,
        'spell_types': [
            {'ID': 1, 'active': True, 'name': 'Everyday', 'description': None}
        ]
    }


def test_create_spell_type():
    spell_types = commands.create_spell_type(
        'Fourth Year',
        spell_ids=[1]
    )
    assert spell_types == {
        'ID': 2,
        'active': True,
        'name': 'Fourth Year',
        'description': None,
        'spells': [
            {
                'ID': 1,
                'active': True,
                'name': 'Accio',
                'description': 'Summaning Charm',
                'history': None,
            }
        ]
    }


def test_map_spell_to_type(session):
    resource = SpellType('Fourth Year')
    session.add(resource)
    session.commit()
    mapping = commands.map_spell_to_type(1, 2)
    assert mapping == {
        'spell_id': 1,
        'spell_type_id': 2,
        'active': True,
        'ID': 2,
    }
