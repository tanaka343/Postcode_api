from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def top():
  return "Postcode_api"