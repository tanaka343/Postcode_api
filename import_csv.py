row_Postcode = [["01101","060  ","0600000","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","","北海道","札幌市中央区","",0,0,0,0,0,0],
["01101","064  ","0640941","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｱｻﾋｶﾞｵｶ","北海道","札幌市中央区","旭ケ丘",0,0,1,0,0,0],
["01101","060  ","0600041","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾋｶﾞｼ","北海道","札幌市中央区","大通東",0,0,1,0,0,0]
]
import csv
from models import Item
from sqlalchemy.orm import Session
from database import SessionLocal


# Dbdependency = Depends(get_db)

db = SessionLocal()

def import_csv(row_Postcode :list,db: Session):
  reader = row_Postcode

  for row in reader:
    item = Item(
      address1=row[6],
		  address2=row[7],
		  address3=row[8] if row[8] else None,
		  kana1=row[3],
		  kana2=row[4],
		  kana3=row[5] if row[5] else None,
		  prefcode=str(row[0]).zfill(5)[:2],
		  zipcode=row[2]
    )
    db.add(item)
  db.commit()
  db.close()

import_csv(row_Postcode,db)