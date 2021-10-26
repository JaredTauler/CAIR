
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session

DBstr = "sqlite:///database.db"
engine = db.create_engine(DBstr, echo=True)

Base = declarative_base()
metadata = MetaData()

user = Table('user', metadata,
    Column('id', Integer, primary_key=True),
    Column('password', String(32), nullable=False),
	Column('salt', String(32), nullable=False),
    Column('email', String(60)),
    Column('fname', String(50), nullable=False),
	Column('lname', String(50), nullable=False),
	Column('username', String(50), nullable=False)
)
class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	password = Column(String)
	salt = Column(String)
	email = Column(String)
	fname = Column(String)
	lname = Column(String)
	username = Column(String)

query = db.select([user])
connection = engine.connect()
ResultProxy = connection.execute(query)
ResultSet = ResultProxy.fetchall()
with Session(engine) as session:
	session.add(User(id=2))
	session.commit()
print(ResultSet)
# class User(Base):
# 	__tablename__ = 'users'
#
# 	id = Column(Integer, primary_key=True)
# 	password = Column(String)
# 	salt = Column(String)
# 	email = Column(String)
# 	fname = Column(String)
# 	lname = Column(String)
# 	username = Column(String)
#
#
# 	def __repr__(self):
# 		return "<User(name='%s', fullname='%s', nickname='%s')>" % (
# 						 self.name, self.fullname, self.nickname)
#
# user = Table('User', metadata_obj,
#     Column('id', Integer, primary_key=True),
#     Column('password', String(32), nullable=False),
# 	Column('salt', String(32), nullable=False),
#     Column('email', String(60)),
#     Column('fname', String(50), nullable=False),
# 	Column('lname', String(50), nullable=False),
# 	Column('username', String(50), nullable=False)
# )
#
# User.create(bind=engine)
#
#
# metadata_obj.create_all(engine)
# session = sessionmaker()
# # Bind the sessionmaker to engine
# session.configure(bind=engine)
# s = session()
#
# ed_user = User(fname="er")
# session.add(ed_user)
