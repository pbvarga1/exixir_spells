from sqlalchemy import Column, Boolean, Integer, String, ForeignKey, event  
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from spells_db.session_context import session_context


class ModelMixin(object):

    ID = Column(Integer, primary_key=True, autoincrement=True)
    active = Column(Boolean, default=True, nullable=False)

    @declared_attr
    def __table_args__(cls):
        return {"schema": "spl"}

    def deactivate(self):
        self.active = False

    def to_dict(self):
        return {
            'ID': self.ID,
            'active': self.active
        }


Base = declarative_base(cls=ModelMixin)


class Spell(Base):

    __tablename__ = 'Spells'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(None), nullable=False)
    history = Column(String(None), nullable=True)
    spell_types = relationship('SpellType', secondary='spl.SpellTypeMappings')

    def __init__(self, name, description, history=None, spell_types=None,
                 active=True, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.history = history
        self.active = active
        if not spell_types:
            spell_types = []
        self.spell_types = spell_types

    def to_dict(self, include_spell_types=True):
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
            'history': self.history,
        })
        if include_spell_types:
            data['spell_types'] = [
                spell_type.to_dict(False) for spell_type in self.spell_types
                if spell_type.active
            ]
        return data


class SpellType(Base):

    __tablename__ = 'SpellTypes'

    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(None), nullable=True)
    spells = relationship('Spell', secondary='spl.SpellTypeMappings')

    def __init__(self, name, *args, description=None, active=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.description = description
        self.active = active

    def to_dict(self, include_spells=True):
        data = super().to_dict()
        data.update({
            'name': self.name,
            'description': self.description,
        })
        if include_spells:
            data['spells'] = [
                spell.to_dict(False) for spell in self.spells if spell.active
            ]

        return data


class SpellTypeMapping(Base):

    __tablename__ = 'SpellTypeMappings'

    spell_id = Column(Integer, ForeignKey('spl.Spells.ID'))
    spell_type_id = Column(Integer, ForeignKey('spl.SpellTypes.ID'))

    def __init__(self, spell_id, spell_type_id, *args, active=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.spell_id = spell_id
        self.spell_type_id = spell_type_id
        self.active = active

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'spell_id': self.spell_id,
            'spell_type_id': self.spell_type_id,
        })
        return data


@event.listens_for(Base.metadata, 'before_create')
def receive_before_create(target, connection, **kw):
    with session_context() as session:
        engine = session.bind
        if not engine.dialect.has_schema(engine, 'spl'):
            engine.execute(CreateSchema('spl'))
