from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from shorter_app.models import Base

def init_db(app):
    engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"), convert_unicode=True)
    app.db_session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    Base.query = app.db_session.query_property()
