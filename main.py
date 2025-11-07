from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from typing import Optional,List
from schemas import ItemResponse,Address
from fastapi.exceptions import RequestValidationError

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

@app.exception_handlers(RequestValidationError)




@app.get("/api/search",response_model=ItemResponse[List[Address]])
def find_by_zipcode(zipcode :str,limit :Optional[int]=None):

  if limit is None:
    limit == 20
  else:
    limit == limit
  
    
    
  if len(str(zipcode))!=7:
    raise HTTPException(status_code=400,
                        detail={
                          "message" :"パラメータ「郵便番号」の桁数が不正です。",
                          "result" :"",
                          "status" : 400
                        })
  try:
    int(zipcode)
  except ValueError:
    raise HTTPException(status_code=400,
                        detail={
                          "message" :"パラメータが数字以外です。",
                          "result" :"",
                          "status" : 400
                        })
    
    # if zipcode is None:
    #   raise HTTPException(status_code=400,detail="リクエストパラメータが不正です")

  try:
    item_list = []
    for item in Items:
      if item.zipcode == zipcode:
        item_list.append(item)
    limited_list = item_list[:limit]  
    return {
      "message" : "",
      "result" : limited_list,
      "status" : 200
    }
  except Exception as e:
   raise HTTPException(
     status_code=500,
     detail={
       "message" : str(e),
       "result" : "",
       "status" :500
     }
   )
   