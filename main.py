from fastapi import FastAPI,HTTPException,Request,status,Depends
from fastapi.responses import JSONResponse
from typing import Optional,List,Annotated
from schemas import ItemResponse,Address
from fastapi.exceptions import RequestValidationError
from database import get_db
from sqlalchemy.orm import Session
from models import Item
DbDependency = Annotated[Session,Depends(get_db)]
app = FastAPI()

@app.get("/")
def top():
  return "Postcode_api"

#仮データ
# class Postcode:
#   def __init__(
#       self,
#       address1 : str,
# 			address2: str,
# 			address3: Optional[str],
# 			kana1: str,
# 			kana2: str,
# 			kana3: Optional[str],
# 			prefcode: str,
# 			zipcode: str
#       ):
#     self.address1=address1
#     self.address2=address2
#     self.address3=address3
#     self.kana1=kana1
#     self.kana2=kana2
#     self.kana3=kana3
#     self.prefcode=prefcode
#     self.zipcode=zipcode

# Items = [Postcode("北海道","札幌市中央区","","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","","01101","0640941"),
#          Postcode("北海道","札幌市中央区","旭ケ丘","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｱｻﾋｶﾞｵｶ","01101","0640941"),
#          Postcode("北海道","札幌市中央区","大通東","ﾎｯｶｲﾄﾞｳ","ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ","ｵｵﾄﾞｵﾘﾋｶﾞｼ","01101","0600041")]   
 

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request,exc: RequestValidationError):
  return JSONResponse(
    status_code = 400,
    content={
      "message" :"必須パラメータが指定されていません。",
      "result" :None,
      "status" : 400
    }
  )

@app.exception_handler(HTTPException)
async def HTTPException_handler(request: Request,exc: HTTPException):
  return JSONResponse(
    status_code= exc.status_code,
    content={
      "message" : exc.detail,
      "result" : None,
      "status" : exc.status_code
    }
  )


@app.get("/api/search",response_model=ItemResponse[List[Address]],status_code=status.HTTP_200_OK)
def find_by_zipcode(db : DbDependency,zipcode :str,limit :Optional[int]=None):

  if limit is None:
    limit = 20
  else:
    limit = limit
    
  if len(str(zipcode))!=7:
    raise HTTPException(status_code=400,
                        detail="パラメータ「郵便番号」の桁数が不正です。")
  try:
    int(zipcode)
  except ValueError:
    raise HTTPException(status_code=400,
                        detail="パラメータ「郵便番号」に数字以外の文字が指定されています。")
  try:
    found_items = db.query(Item).filter(Item.zipcode == zipcode).order_by(Item.zipcode).limit(limit).all()
    return {
      "message" : "",
      "result" : found_items,
      "status" : 200
    }
  except Exception as e:
   raise HTTPException(
     status_code=500,
     detail=str(e)
    )
   