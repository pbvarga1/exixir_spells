from spells_db.session_context import session_context
from spells_db.models import Base

if __name__ == "__main__":
    with session_context() as session:
        engine = session.get_bind()
        metadata = Base.metadata
        metadata.bind = engine
        # metadata.drop_all()
        metadata.create_all()
