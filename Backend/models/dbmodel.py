from config.database import Base
from sqlalchemy import Column, Integer, String,Numeric,Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship





class Users(Base):
    __tablename__ = 'users'


    # serial_no = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    id = Column(String, unique=True,primary_key=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False, unique=True)
    country = Column(String,nullable=False)
    password = Column(String,nullable=False)
    phone_no = Column(Numeric,nullable=False, unique=True)
    role = Column(String, server_default='Trader',nullable=False)
    capital = Column(String,nullable=False)
    status = Column(String,server_default='Received',nullable=False)
    reason = Column(String,nullable=False,server_default='N/A')
    phase = Column(String, server_default='Evaluation', nullable=False)
    upgrade_to= Column(String,nullable=False,server_default='N/A')
    scale_to= Column(String,nullable=False,server_default='N/A')
    mt_login = Column(String,nullable=False,server_default='N/A')
    metatrader_password= Column(String,nullable=False,server_default='N/A')
    mt_server = Column(String,nullable=False,server_default='N/A')
    analytics = Column(String,nullable=False,server_default='N/A')
    status_upgrade = Column(String,nullable=False,server_default='N/A')
    status_scale = Column(String,nullable=False,server_default='N/A')
    status_payout = Column(String,nullable=False,server_default='N/A')
    upgrading_reason = Column(String,nullable=False,server_default='N/A')
    scaling_reason = Column(String,nullable=False,server_default='N/A')
    account_id_meta = Column(String,nullable=False,server_default='N/A')
    transaction_id =Column(String, unique=True, nullable=False)
    transaction_link  = Column(String, nullable=False)
    profit_split  = Column(Float, nullable=False, default= 0)
    type_meta = Column(String,nullable=False,server_default='N/A')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
    
    

    

class Requests(Base):
    __tablename__ = 'requests'

    serial_no = Column(Integer, primary_key=True, nullable=False)
    id = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    country = Column(String,nullable=False)
    phone_no = Column(Numeric,nullable=False)
    password = Column(String,nullable=False,server_default='N/A')
    transaction_id = Column(String,nullable=False,server_default='N/A')
    transaction_link = Column(String,nullable=False,server_default='N/A')
    role = Column(String,nullable=False)
    capital = Column(String,nullable=False)
    mt_login = Column(String,nullable=False,server_default='N/A')
    metatrader_password= Column(String,nullable=False,server_default='N/A')
    mt_server = Column(String,nullable=False,server_default='N/A')
    analytics = Column(String,nullable=False,server_default='N/A')
    status_upgrade =Column(String,nullable=False, server_default='N/A')
    status_scale =Column(String,nullable=False, server_default='N/A')
    current_phase =Column(String,nullable=False, server_default ="N/A")
    upgrade_to =Column(String,nullable=False, server_default ="N/A")
    current_capital =Column(String,nullable=False, server_default ="N/A")
    scale_to =Column(String,nullable=False,server_default ="N/A")
    analytics_upgrade =Column(String,nullable=False, server_default ="N/A")
    analytics_scale =Column(String,nullable=False, server_default ="N/A")
    type =Column(String,nullable=False, server_default ="N/A")
    reason = Column(String,nullable=False,server_default='N/A')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))







class Payouts(Base):
    __tablename__ = 'payouts'

    serial_no = Column(Integer, primary_key=True, nullable=False)
    id = Column(String, nullable=False)
    first_name = Column(String, nullable=False,server_default="N/A")
    last_name = Column(String,nullable=False,server_default="N/A")
    status =Column(String, nullable=False)
    payment_method = Column(String, nullable=False )
    amount = Column(String, nullable=False)
    analytics = Column(String, nullable=False)
    profit_share = Column(Float, nullable=False, default=0)
    payable_amount= Column(Float, nullable=False, default=0)
    reason = Column(String, nullable=False,server_default="N/A")
    email = Column(String,nullable=False)
    wallet_address = Column(String, nullable=False)
    type = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))




class Admin(Base):
    __tablename__='admin'

    id =Column(Integer, primary_key=True, nullable=False)
    first_name = Column(String, nullable=False )
    last_name  = Column(String, nullable=False )
    email  = Column(String, nullable=False,unique=True)
    phone_no = Column(Numeric, nullable=False,unique=True)
    password = Column(String, nullable=False ,server_default="N/A")
    role  = Column(String, nullable=False, server_default="N/A")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))




class Cryptochil(Base):
    __tablename__='Cryptochil'

    id =Column(Integer, primary_key=True, nullable=False)
    transaction_id =Column(String, unique=True, nullable=False)
    email  = Column(String, nullable=False,unique=True)
    amount = Column(Integer, nullable=False)
    profile_id  = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()'))
