import databases
import sqlalchemy
from sqlalchemy import Boolean, Column, ForeignKey, Integer, MetaData, String, Table

from blogapi.core.config import config

metadata = MetaData()

user_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String, unique=True, nullable=False),
    Column("password", String, nullable=False),
    Column("confirmed", Boolean, default=False),
)

post_table = Table(
    "posts",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("image_url", String),
)

comment_table = Table(
    "comments",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("body", String),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
)

like_table = Table(
    "likes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("users.id"), nullable=False),
    Column("post_id", ForeignKey("posts.id"), nullable=False),
)

connect_args = {"check_same_thread": False} if "sqlite" in config.DATABASE_URL else {}
engine = sqlalchemy.create_engine(config.DATABASE_URL)

metadata.drop_all(engine)
metadata.create_all(engine)

db_args = {"min_size": 1, "max_size": 4} if "postgres" in config.DATABASE_URL else {}
database = databases.Database(
    config.DATABASE_URL, force_rollback=config.DB_FORCE_ROLL_BACK, **db_args
)
