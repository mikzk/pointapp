# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# HTMLファイルからの通信を許可する設定（CORS）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# データベースの初期設定（AさんとBさんを作成）
def init_db():
    conn = sqlite3.connect("points.db")
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, balance INTEGER)")
    c.execute("INSERT OR IGNORE INTO users (id, name, balance) VALUES (1, 'Aさん', 1000)")
    c.execute("INSERT OR IGNORE INTO users (id, name, balance) VALUES (2, 'Bさん', 500)")
    conn.commit()
    conn.close()

init_db()

# 送金時に受け取るデータの形を定義
class TransferRequest(BaseModel):
    sender_id: int
    receiver_id: int
    amount: int

# 送金API（トランザクション処理）
@app.post("/transfer")
def transfer_points(req: TransferRequest):
    if req.amount <= 0:
        raise HTTPException(status_code=400, detail="1以上のポイントを指定してください")

    conn = sqlite3.connect("points.db")
    c = conn.cursor()
    try:
        c.execute("BEGIN") # トランザクション開始
        
        # 送り主の残高確認
        c.execute("SELECT balance FROM users WHERE id = ?", (req.sender_id,))
        sender = c.fetchone()
        if not sender or sender[0] < req.amount:
            raise Exception("残高が足りません")

        # 残高の引き算と足し算
        c.execute("UPDATE users SET balance = balance - ? WHERE id = ?", (req.amount, req.sender_id))
        c.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (req.amount, req.receiver_id))

        conn.commit() # 成功したらデータを確定
        return {"message": "送金成功！"}
    except Exception as e:
        conn.rollback() # エラーが起きたら処理を取り消す
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        conn.close()

# ユーザー情報取得API
@app.get("/users")
def get_users():
    conn = sqlite3.connect("points.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = [{"id": row[0], "name": row[1], "balance": row[2]} for row in c.fetchall()]
    conn.close()
    return users