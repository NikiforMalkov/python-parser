from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from post import Post
from postPdo import PostPdo


# пример соединения 'dialect+driver://user:pass@host:port/db'
engine = create_engine('mysql+pymysql://root:@localhost/test', echo=True)

metadata = MetaData()
post = Table('post', metadata,
             Column('id', Integer, primary_key=True),
             Column('description', Text),
             Column('image_url', String(1024)),
             Column('link', Text),
             Column('date', String(255))
             )

metadata.create_all(engine)

mapper(Post, post)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# TODO: выпилить тесты
# newPost = PostPdo(session)
# newPost.add_post("test", "test")

# print(type(smth))
# if newPost.one_by_link("lol") is None:
#    print("non is here")
#    newPost.add_post("lol", "lol", "lol", "lol")
#     print(newPost.one_by_link("lol"))
