
from config.database import Base
from sqlalchemy import Column, Integer, String,Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text




class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False, unique=True)
    country = Column(String,nullable=False)
    phone_no = Column(Integer,nullable=False, unique=True)
    password = Column(String,nullable=False)
    transaction_id = Column(String,nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    is_admin = Column(Boolean, nullable=False, server_default=" False ")