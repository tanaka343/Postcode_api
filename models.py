from sqlalchemy import Integer,String,Column
from database import Base


class Item(Base):
  __tablename__ = "Postcode"
  id = Column(Integer,primary_key=True,)
  address1 = Column(String)
  address2 = Column(String)
  address3 = Column(String,nullable=True)
  kana1 = Column(String)
  kana2 = Column(String)
  kana3 = Column(String,nullable=True)
  prefcode = Column(String)
  zipcode = Column(String)