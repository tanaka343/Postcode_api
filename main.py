from fastapi import FastAPI
from typing import Optional,List
from schemas import ItemResponse,Address

app = FastAPI()

@app.get("/")
def top():
  return "Postcode_api"

class Postcode:
  def __init__(
      self,
      address1 : str,
			address2: str,
			address3: Optional[str],
			kana1: str,
			kana2: str,
			kana3: Optional[str],
			prefcode: str,
			zipcode: str
      ):
    self.address1=address1
    self.address2=address2
    self.address3=address3
    self.kana1=kana1
    self.kana2=kana2
    self.kana3=kana3
    self.prefcode=prefcode
    self.zipcode=zipcode

Items = [Postcode("北海道","札幌市中央区","","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","","01101","0640941"),
         Postcode("北海道","札幌市中央区","旭ケ丘","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｱｻﾋｶﾞｵｶ","01101","0640941"),
         Postcode("北海道","札幌市中央区","大通東","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾋｶﾞｼ","01101","0600041")]   
 
# row_Postcode = [[01101,"060  ","0600000","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","","北海道","札幌市中央区","",0,0,0,0,0,0],
# [01101,"064  ","0640941","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｱｻﾋｶﾞｵｶ","北海道","札幌市中央区","旭ケ丘",0,0,1,0,0,0],
# [01101,"060  ","0600041","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾋｶﾞｼ","北海道","札幌市中央区","大通東",0,0,1,0,0,0]
# ]

@app.get("/api/search",response_model=ItemResponse[List[Address]])
  for item in Items:
    if item.zipcode == zipcode:
  return {
    "message" : "",
    "result" : limited_list,
    "status" : 200
  }