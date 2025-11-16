import os
import sys

## ファイルがimport先と同じ階層なら不要
# testsフォルダから1つ上の階層（プロジェクトルート）のパスを作る
app_dir = os.path.join(os.path.dirname(__file__),"..")
# Pythonが「ここからもimportしていいよ」とパスを追加
sys.path.append(app_dir)

import pytest
from database import create_engine,get_db
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from models import Base,Item
from main import app
from fastapi.testclient import TestClient

@pytest.fixture()
def session_fixture():
    engine = create_engine(
        url= "sqlite://", # ← メモリ上のDB
        connect_args={"check_same_thread":False},
        poolclass= StaticPool
    )
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)
    db = SessionLocal()

    try:
        # テストデータ投入
        test_items = [
            Item(
                address1="北海道",
                address2="札幌市中央区",
                address3="大通東",
                kana1="ﾎｯｶｲﾄﾞｳ",
                kana2="ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ",
                kana3="ｵｵﾄﾞｵﾘﾋｶﾞｼ",
                prefcode="01",
                zipcode="0600041"
            ),
            Item(
                
                address1="北海道",
                address2="札幌市中央区",
                address3="旭ケ丘",
                kana1="ﾎｯｶｲﾄﾞｳ",
                kana2="ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ",
                kana3="ｱｻﾋｶﾞｵｶ",
                prefcode="01",
                zipcode="0640941"
            )
        ]
        # limit検証用：同一郵便番号25件
        for i in range(25):
            test_items.append(
                Item(
                    address1="静岡県",
                    address2="磐田市",
                    address3=f"見付{i+1}丁目",
                    kana1="ｼｽﾞｵｶｹﾝ",
                    kana2="ｲﾜﾀｼ",
                    kana3=f"ﾐﾂｹ{i+1}ﾁﾖｳﾒ",
                    prefcode="22",
                    zipcode="4380086"
                )
            )
        for item in test_items:
            db.add(item)
        db.commit()
        yield db
    finally:
        db.close()

@pytest.fixture()
def client_fixture(session_fixture):
    def override_get_db():
        return session_fixture
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()