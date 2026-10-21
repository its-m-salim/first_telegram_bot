from connection import *



async def create_user(username, full_name, tg_id, balance):
    try:
        conn = await connection_db()
        await conn.execute("""
    Insert into users(username, full_name, telegram_id, balance) values
    ($1, $2, $3, $4)
    """, username, full_name, str(tg_id), balance)
    except Exception as error:
        print(f"{type(error).__name__}: {error}s.py")
    finally:
        await conn.close()



async def user_by_id(tg_id):
    try:
        conn = await connection_db()
        user = await conn.fetch("""
select * from users where telegram_id = $1
""", str(tg_id))
        return user
    except Exception as error:
        print(f"{type(error).__name__}: {error}s.py")    
    finally:
        await conn.close()




SCAN_PRICE = 100
DATABASE_PRICE = 500


async def get_random_user(tg_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
select * from users
where telegram_id != $1 and is_active = true
order by random()
limit 1
""", str(tg_id))
        return user
    except Exception as error:
        print(f"{type(error).name}: {error}s.py")
    finally:
        await conn.close()


async def get_all_users(tg_id):
    try:
        conn = await connection_db()
        users = await conn.fetch("""
    select * from users
    where telegram_id != $1 and is_active = true
    order by balance desc
    limit 10
    """, str(tg_id))
        return users
    except Exception as error:
        print(f"{type(error).name}: {error}s.py")
    finally:
        await conn.close()


async def sudo_cmall(tg_id):
    try:
        conn = await connection_db()
        users = await conn.fetch("""
    select * from users
    where telegram_id != $1
    order by balance desc
    limit 10
    """, str(tg_id))
        return users
    except Exception as error:
        print(f"{type(error).name}: {error}s.py")
    finally:
        await conn.close()



async def sudo_cmone(tg_id):
    try:
        conn = await connection_db()
        user = await conn.fetchrow("""
select * from users
where telegram_id != $1
order by random()
limit 1
""", str(tg_id))
        return user
    except Exception as error:
        print(f"{type(error).name}: {error}s.py")
    finally:
        await conn.close()



async def update_balance(tg_id, amount):
    try:
        conn = await connection_db()
        await conn.execute("""
    update users set balance = balance + $1
    where telegram_id = $2
    """, amount, str(tg_id))
    except Exception as error:
        print(f"{type(error).name}: {error}s.py")
    finally:
        await conn.close()





async def get_status(balance):
    if balance < 100:
        return "🪙 Новичок"
    elif balance < 500:
        return "💰 Трейдер"
    elif balance < 1000:
        return "💎 Эксперт"
    else:
        return "👑 Легенда"
