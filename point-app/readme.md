# シンプルなポイント送金アプリ

Python（FastAPI）と素のJavaScript（Vanilla JS）を使用した、シンプルなポイント送金Webアプリケーションです。

## 概要
ユーザー間でポイントを送金できるシステムです。バックエンドにはFastAPIを使用し、データベース（SQLite）のトランザクション処理を用いて、安全な残高の引き算・足し算を実装しています。

## 使用技術
* **バックエンド**: Python 3 / FastAPI
* **データベース**: SQLite
* **フロントエンド**: HTML / CSS / Vanilla JavaScript

## ファイル構成
* `main.py` : バックエンドのAPIサーバーとデータベース処理
* `index.html` : フロントエンドのユーザー画面

## 動かし方（ローカル環境）

1. 必要なライブラリをインストールします。
   ```bash
   pip install fastapi "uvicorn[standard]"