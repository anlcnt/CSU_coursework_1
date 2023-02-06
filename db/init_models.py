from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def init(path: str):
    from db.models import base
    from db.models import author
    from db.models import book
    from db.models import hall
    from db.models import field
    from db.models import member
    from db.models import publisher
    from db.models import lending

    engine = create_engine(path, echo=True)
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
    base.Base.query = session.query_property()
    base.Base.metadata.create_all(bind=engine)
