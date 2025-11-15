from sqlalchemy import Integer,String,Column
from database import Base


class Item(Base):
  __tablename__ = "Postcode"
  id = Column(Integer,primary_key=True,)
  address1 = Column(String(255))
  address2 = Column(String(255))
  address3 = Column(String(255),nullable=True)
  kana1 = Column(String(255))
  kana2 = Column(String(255))
  kana3 = Column(String(255),nullable=True)
  prefcode = Column(String(255))
  zipcode = Column(String(255))