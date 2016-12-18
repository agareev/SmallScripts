from config import *

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from_engine = create_engine('postgresql://{}:{}@localhost:5432/notabenoid'.format(from_user, from_password), echo=False)
to_engine = create_engine('postgresql://{}:{}@localhost:5432/kursomir_production'.format(to_user, to_password),
                          echo=False)

Base = declarative_base()


class BaseBook:
    id = Column(Integer, primary_key=True)
    eng_title = Column('s_title', String)
    translated_title = Column('t_title', String)


class NotabenoidBook(Base, BaseBook):
    __tablename__ = 'books'
    translated_paragraph_count = Column('d_vars', Integer)
    paragraph_count = Column('n_verses', Integer)


class UploadedBook(Base, BaseBook):
    __tablename__ = 'some_name'
    translated_ratio = Column(Float)


from_session = sessionmaker(bind=from_engine)()
to_session = sessionmaker(bind=to_engine)()

books = from_session.query(NotabenoidBook).filter(NotabenoidBook.paragraph_count > 0).all()
to_upload = (
    UploadedBook(
        eng_title=book.eng_title,
        translated_title=book.translated_title,
        translated_ratio=(book.translated_paragraph_count / book.paragraph_count) * 100,
    )
    for book in books
)
to_session.bulk_save_objects(to_upload)
