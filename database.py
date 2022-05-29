import functools
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text


def singleton(cls):
    @functools.wraps(cls)
    def wrapper(*args, **kwargs):
        if not wrapper.instance:
            wrapper.instance = cls(*args, **kwargs)
        return wrapper.instance
    wrapper.instance = None
    return wrapper


@singleton
class Database:
    def __init__(self):
        self.engine = create_engine('sqlite:///idioms.db')
        self.engine.connect()
        self.idioms = None
        self.post_init()

    def create_table_idioms(self):
        metadata = MetaData()

        self.idioms = Table('Idioms', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('phrase', Text, nullable=False),
                            Column('explanation', Text, nullable=False),
                            Column('etymology', Text, nullable=True),
                            sqlite_autoincrement=True
                            )

        metadata.create_all(self.engine)

    def post_init(self):
        import sqlalchemy
        metadata = MetaData()

        if sqlalchemy.inspect(self.engine).has_table("Idioms"):
            self.idioms = Table('Idioms', metadata, autoload_with=self.engine)
        else:
            self.create_table_idioms()
