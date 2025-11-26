# Postcode_API

郵便番号から住所情報を検索するREST APIです。



## 目的
Udemyで学習したFastAPIの内容をアウトプットする目的で、既存のタスク管理アプリを再構成しました。\
CRUD処理、バリデーション、マイグレーション、テストまでの一連の流れを通して、自分でAPI設計・実装ができるようになることを目指しました。
### ⚠️ 環境変数について

このプロジェクトは**個人学習用・非デプロイ**のため、`.env.*`ファイルをリポジトリに含めています。  
実務環境では`.gitignore`で除外し、`.env.example`をサンプルとして提供します。

## 機能

- 郵便番号（7桁）による住所検索
- 取得件数制限（limitパラメータ）
- バリデーション付きエラーハンドリング
- 統一されたJSONレスポンス形式
- 自動生成されるAPIドキュメント（Swagger UI）
- データベースマイグレーション管理（Alembic）
- APIテスト（pytest）
- envファイルを使った環境の切り分け（開発/本番/テスト）

## 技術スタック

FastAPI\
SQLAlchemy（ORM）\
Alembic（マイグレーション）\
MySQL\
SQLite（開発用）\
Pydantic（バリ.デーション）\
pytest（テスト）\
Docker Compose,Dockerfile（コンテナ）

## コミットメッセージ規約

下記の記事を参考にしました。: <https://qiita.com/konatsu_p/items/dfe199ebe3a7d2010b3e>
### フォーマット
```
<type> : <subject>

<body>（オプション）

<footer>（オプション）
```
### type一覧

| type | 説明 | 例 |
|------|------|-----|
| `feat` | 新機能追加 | `feat: 郵便番号検索API実装` |
| `fix` | バグ修正 | `fix: 7桁以外のエラーメッセージ修正` |
| `docs` | ドキュメント変更 | `docs: README セットアップ手順追記` |
| `style` | コード整形（動作に影響なし） | `style: import文の順序修正` |
| `refactor` | リファクタリング | `refactor: DB接続処理を関数化` |
| `test` | テスト追加・修正 | `test: limit機能のテストケース追加` |
| `chore` | ビルド・設定変更 | `chore: requirements.txt更新` |
## ファイル構成

```python
postcode-api/
├── migrations/          # Alembicマイグレーションファイル
│   ├── env.py
│   └── versions/
├── tests/               # テストファイル
│   ├── conftest.py     # fixtureでテストDB作成
│   └── test_main.py    # API入出力テスト
├── __init__.py
├── .env.development    # 開発用環境変数
├── .env.production     # 本番想定用環境変数
├── .env.test           # テスト用環境変数
├── .gitignore
├── config.py            # 環境変数による設定
├── alembic.ini          # Alembic設定
├── database.py          # データベース接続設定
├── docker-compose.yml   # MySQL + Appコンテナ定義
├── Dockerfile           # MySQL + Appコンテナ定義
├── import_csv.py        # 郵便番号データ投入スクリプト
├── main.py              # FastAPIアプリケーション本体
├── models.py            # SQLAlchemyモデル定義
├── schemas.py           # Pydanticスキーマ定義
├── requirements.txt     # 依存パッケージ
└── x-ken-all.csv        # 郵便番号マスタデータ
```

## セットアップ

このプロジェクトは3つの環境に対応しています：
 環境 | データベース | 用途 |
|------|-------------|------|
| 開発 | SQLite | ローカル開発 |
| テスト | MySQL (Docker) | CI/CD・結合テスト想定 |
| 本番 | MySQL (Docker) | デプロイ想定 |

### 開発環境（SQLite）

#### 1. 依存パッケージのインストール
```bash
pip install -r requirements.txt
```

#### 2. 環境変数の確認
`config.py` でデフォルトがSQLiteになっていることを確認：
```python
database_url : str = "sqlite:///./database.db"　# デフォルト
```

#### 3. データベースのセットアップ
```bash
# マイグレーション実行
alembic upgrade head
# 郵便番号データ投入
python import_csv.py
```

#### 4. サーバー起動
```bash
uvicorn main:app --reload
```

アクセス:
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
---
### 本番テスト環境（MySQL）

#### 初回のみ: テスト用DB作成
```bash
docker compose --env-file .env.production up -d mysql
docker compose exec mysql mysql -u root -prootpass
```
MySQL内で実行:
```sql
CREATE DATABASE postcode_db_test;
GRANT ALL PRIVILEGES ON postcode_db_test.* TO 'appuser'@'%';
exit
```
#### テスト環境
```bash
docker compose --env-file .env.test up --build
docker compose exec api alembic upgrade head
docker compose exec api python import_csv.py
```

#### 本番環境
```bash
docker compose --env-file .env.production up --build
docker compose exec api alembic upgrade head
```
アクセス:
- API: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
---
## テストの実行
```bash
pytest tests/test_main.py -v
```

- **API入出力テスト**: 正常系・異常系のレスポンス検証
- **ビジネスロジックテスト**: limit機能、存在しない郵便番号の
- **fixtureの活用**: テスト用メモリDBのセットアップ


## API仕様

### 郵便番号データ構造
```json
{
  "address1": "北海道",
  "address2": "札幌市中央区",
  "address3": "大通東",
  "kana1": "ﾎｯｶｲﾄﾞｳ",
  "kana2": "ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ",
  "kana3": "ｵｵﾄﾞｵﾘﾋｶﾞｼ",
  "prefcode": "01",
  "zipcode": "0600041"
}
```

### エンドポイント一覧

#### 1. トップページ
```bash
GET /
```

レスポンス: `"Postcode_api"`

#### 2. 郵便番号検索
```bash
GET /api/search?zipcode=0600041&limit=10
```

**クエリパラメータ**
| 名前 | 型 | 必須 | 説明 |
|------|-----|------|------|
| `zipcode` | string | ✓ | 7桁の郵便番号 |
| `limit` | integer | - | 取得件数（デフォルト: 20） |

**リクエスト例**
```bash
curl "http://localhost:8000/api/search?zipcode=0600041"
```

**レスポンス例（正常系）**
```json
{
  "message": "",
  "result": [
    {
      "address1": "北海道",
      "address2": "札幌市中央区",
      "address3": "大通東",
      "kana1": "ﾎｯｶｲﾄﾞｳ",
      "kana2": "ｻｯﾎﾟﾛｼﾁｭｳｵｳｸ",
      "kana3": "ｵｵﾄﾞｵﾘﾋｶﾞｼ",
      "prefcode": "01",
      "zipcode": "0600041"
    }
  ],
  "status": 200
}
```

### エラーハンドリング

#### 400 Bad Request - 桁数エラー
```json
{
  "message": "パラメータ「郵便番号」の桁数が不正です。",
  "result": null,
  "status": 400
}
```

#### 400 Bad Request - 数字以外エラー
```json
{
  "message": "パラメータ「郵便番号」に数字以外の文字が指定されています。",
  "result": null,
  "status": 400
}
```

#### 400 Bad Request - 必須パラメータ不正
```json
{
  "message": "必須パラメータが指定されていません。",
  "result": null,
  "status": 400
}
```

#### 500 Internal Server Error
```json
{
  "message": "データベースエラーの詳細",
  "result": null,
  "status": 500
}
```

## 工夫した点・学んだこと

- 既存機能の模倣
- カスタマイズしたエラーハンドリング
- 環境の切り分け

## 改善点・今後の課題

- 適切に検索できるようにする\
環境の切り分け方法の学習で、やりたいことを適切に検索できないため、結局aiにたより受動的に学習する形になってしまった。

- エラー解決を能動的に解決する\
エラーが出たときにフォーマットを作成して状況を整理しながら質問していたが、自分で解決する能力が身についている感じがしない。工夫が必要。
  - エラーログを出力させる
  - エラーコードを読めるようにして、整理して記録する