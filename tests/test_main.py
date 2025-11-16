from fastapi.testclient import TestClient

# API入出力テスト

def test_find_by_zipcode_正常系(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zipcode=0600041")
    assert response.status_code == 200
    item = response.json()
    
    assert item["result"][0]["address1"] == "北海道"
    assert item["result"][0]["address2"] == "札幌市中央区"
    assert item["result"][0]["address3"] == "大通東"
    assert item["result"][0]["kana1"] == "ﾎｯｶｲﾄﾞｳ"
    assert item["result"][0]["kana2"] == "ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ"
    assert item["result"][0]["kana3"] == "ｵｵﾄﾞｵﾘﾋｶﾞｼ"
    assert item["result"][0]["prefcode"] == "01"
    assert item["result"][0]["zipcode"] == "0600041"

def test_find_by_zipcode_桁数エラー(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zipcode=06000411")
    assert response.status_code == 400
    assert response.json()["message"] == "パラメータ「郵便番号」の桁数が不正です。"

def test_find_by_zipcode_数字以外エラー(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zipcode=kkkkkkk")
    assert response.status_code == 400
    assert response.json()["message"] == "パラメータ「郵便番号」に数字以外の文字が指定されています。"

def test_find_by_zipcode_必須パラメータ不正エラー(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zip=06000411")
    assert response.status_code == 400
    assert response.json()["message"] == "必須パラメータが指定されていません。"

# ビジネスロジックテスト

def test_find_by_zipcode_limitデフォルト制限(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zipcode=4380086")
    assert response.status_code == 200
    item = response.json()
    assert len(item["result"]) == 20

def test_find_by_zipcode_limit引数制限(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zipcode=4380086&limit=5")
    assert response.status_code == 200
    item = response.json()
    assert len(item["result"]) == 5

def test_find_by_zipcode_存在しないzipcode(client_fixture : TestClient):
    response = client_fixture.get("/api/search/?zipcode=1111111")
    assert response.status_code == 200
    item = response.json()
    assert len(item["result"]) == 0




