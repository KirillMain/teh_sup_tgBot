import aiosqlite as sq


async def db_start():
    db = await sq.connect("data/tg.db")

    await db.execute('CREATE TABLE IF NOT EXISTS faq('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'question TEXT,'
                'answer TEXT,'
                'img TEXT)')
    await db.execute('CREATE TABLE IF NOT EXISTS appeals('
                'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                'user_id INTEGER,'
                'date TEXT,'
                'type TEXT,'
                'content TEXT,'
                'img TEXT,'
                'answer TEXT,'
                'answer_img TEXT)')
    
    await db.commit()
    await db.close()


# async def db_update(num: int, txt: str):
#     db = await sq.connect("data/tg.db")

#     await db.execute('UPDATE faq SET id = & WHERE question = &', 
#                      (num, txt))
    
#     await db.close()


# ----------------------- FAQ -----------------------
# count
# get question and answer
async def db_faq_count():
    db = await sq.connect("data/tg.db")

    cur = await db.execute('SELECT * FROM faq')
    res = await cur.fetchall()

    await cur.close()
    await db.close()

    return res


async def db_faq_get_qa(question_id: int):
    db = await sq.connect("data/tg.db")

    cur = await db.execute("SELECT question, answer FROM faq WHERE id == {id}".format(id=question_id))
    res = await cur.fetchall()

    await cur.close()
    await db.close()
    
    return res


# ----------------------- APPEAL -----------------------
# new appeal
# get appeal
async def db_appeal_new(data: dict):
    db = await sq.connect("data/tg.db")

    await db.execute("INSERT INTO appeals (type, user_id, date, content, img) VALUES (?, ?, ?, ?, ?)",
                    (data['type'], data['user_id'], data['date'], data['content'], data['img']))

    await db.commit()
    await db.close()


async def db_appeal_get(u_id: int):
    db = await sq.connect("data/tg.db")

    cur = await db.execute("SELECT id, user_id, date, type, content, img, answer, answer_img FROM appeals WHERE user_id == {id}".format(id=u_id))
    res = await cur.fetchall()

    await cur.close()
    await db.close()

    return res


# ----------------------- ADMIN FAQ -----------------------
async def a_db_faq_remove(faq_id: int):
    db = await sq.connect("data/tg.db")

    await db.execute("DELETE FROM faq WHERE id == {id}".format(id=faq_id))

    await db.commit()
    await db.close()


async def a_db_faq_add(que: str, ans: str, img: str):
    db = await sq.connect("data/tg.db")

    await db.execute("INSERT INTO faq (question, answer, img) VALUES (?, ?, ?)",
                     (que, ans, img))
    
    await db.commit()
    await db.close()


# ----------------------- ADMIN APPEAL -----------------------
async def a_db_appeal_get_id(id: int):
    db = await sq.connect("data/tg.db")
    
    cur = await db.execute("SELECT id, user_id, date, type, content, img, answer, answer_img FROM appeals WHERE id == {idd}".format(idd=id))
    res = await cur.fetchone()
    
    await cur.close()
    await db.close()

    return res


async def a_db_appeal_get_no_id():
    db = await sq.connect("data/tg.db")
    
    cur = await db.execute("SELECT id, user_id, date, type, content, img, answer, answer_img FROM appeals")
    res = await cur.fetchall()
    
    await cur.close()
    await db.close()

    return res


async def a_db_appeal_update(id: int, answer: str, img: str):
    db = await sq.connect("data/tg.db")

    await db.execute('UPDATE appeals SET answer = ?, answer_img = ? WHERE id = ?', 
                      (answer, img, id))

    await db.commit()
    await db.close()