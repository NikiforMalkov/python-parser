from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Text
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from src.post import Post
from src.postPdo import PostPdo
from src.link import Link
from src.linkPdo import LinkPdo

# TODO: нормальное ООП
# пример соединения 'dialect+driver://user:pass@host:port/db'
engine = create_engine('mysql+pymysql://root:@localhost/test2', echo=True)

metadata = MetaData()
post = Table('post', metadata,
             Column('id', Integer, primary_key=True),
             Column('description', Text),
             Column('image_url', Text),
             Column('link', Text),
             Column('date', String(255))
             )

link = Table('link', metadata,
             Column('id', Integer, primary_key=True),
             Column('link', Text),
             )

metadata.create_all(engine)

mapper(Post, post)
mapper(Link, link)

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
