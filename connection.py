from dotenv import load_dotenv
import asyncpg
import os

load_dotenv()
pasw  = os.getenv("PASSWORD_DB")


async def connection_db():
    try:
        conn = await asyncpg.connect(
            host="localhost",
            port=5432,
            user="salim",
            database="tg_bot",
            password=pasw
        )
        return conn
    except Exception as error:
        print(f"{type(error)}: {error} con.py")
    
        
async def create_table():
    try:
        conn = await connection_db()
        await conn.execute("""
Create table if not exists users(
    user_id serial primary key,
    username varchar(100),
    full_name varchar(100),
    telegram_id varchar(200),
    balance numeric(5,2),
    created_at timestamp default now(),
    is_active boolean default true
)   """)
        print("Table created")
    except Exception as error:
        print(f"{type(error)}: {error} con.py")
    finally:
        await conn.close()

async def create_missions():
    try:
        conn = await connection_db()
        await conn.execute("""
create table if not exists missions(
    id serial primary key,
    mission text,
    hint varchar(100),
    answer_format varchar(100),
    created_at timestamp deafult now(),
    level varchar(50)
)
""")
        print("Missions table created")
    except Exception as error:
        print(f"{type(error)}: {error} con.py")
    finally:
        await conn.close()