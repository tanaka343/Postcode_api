from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url : str = "sqlite:///./database.db" # デフォルトでローカル開発環境に接続
    environment : str = "development" # デフォルト値
    debug : bool = True

   

settings = Settings()



