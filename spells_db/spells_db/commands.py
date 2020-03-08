import os
import json
from functools import wraps

from spells_db.session_context import session_context
from spells_db.models import (
    Spell,
    SpellType,
    SpellTypeMapping,
)


def to_elixir(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        resource = func(*args, **kwargs)
        if os.environ.get('SPELLS_ELIXIR'):
            resource = json.dumps(resource)
        return resource
    return wrapper


@to_elixir
def _get_by_id(ID, model):
    with session_context() as session:
        query = session.query(model)
        resource = query.get(ID)
        if resource:
            return resource.to_dict()
        else:
            return {}


@to_elixir
def _get_by_name(name, model):
    with session_context() as session:
        query = session.query(model)
        resources = query.filter(model.name.like(name))
        return [resource.to_dict() for resource in resources]


@to_elixir
def _get_all(model):
    with session_context() as session:
        query = session.query(model)
        resources = query.all()
        return [resource.to_dict() for resource in resources]


def get_spell(ID):
    return _get_by_id(ID, Spell)


def get_spell_type(ID):
    return _get_by_id(ID, SpellType)


def get_spell_mapping(ID):
    return _get_by_id(ID, SpellTypeMapping)


def get_all_spells():
    return _get_all(Spell)


def get_spells(name):
    return _get_by_name(name, Spell)


def get_spell_types(name):
    return _get_by_name(name, SpellType)


@to_elixir
def create_spell(name, description, history=None, spell_type_ids=None):
    if isinstance(name, bytes):
        name = name.decode()
    if isinstance(description, bytes):
        description = description.decode()
    if isinstance(history, bytes):
        history = history.decode()
    with session_context() as session:
        if spell_type_ids:
            query = session.query(SpellType)
            spell_types = [query.get(st_id) for st_id in spell_type_ids]
        else:
            spell_types = None
        spell = Spell(name, description, history=history, spell_types=spell_types)
        session.add(spell)
        session.commit()
        return spell.to_dict()


@to_elixir
def create_spell_type(name, description=None, spell_ids=None):
    with session_context() as session:
        if spell_ids:
            query = session.query(Spell)
            spells = [query.get(spell_id) for spell_id in spell_ids]
        else:
            spells = None
        spell_type = SpellType(name, description=description, spells=spells)
        session.add(spell_type)
        session.commit()
        return spell_type.to_dict()


@to_elixir
def map_spell_to_type(spell_id, spell_type_id):
    with session_context() as session:
        spell_type_mapping = SpellTypeMapping(spell_id, spell_type_id)
        session.add(spell_type_mapping)
        session.commit()
        return spell_type_mapping.to_dict()
