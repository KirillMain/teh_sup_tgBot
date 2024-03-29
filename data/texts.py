

txt_main = "Главное меню 📁"

txt_a_main = "Админская панель"


def txt_appeal(appeal: list):
    txt = f"#️⃣Номер обращения - <b>{appeal[0]}</b>\n" \
          f"🗓Дата обращения - <b>{appeal[2]}</b>\n\n" \
          f"◻️Тип: <b>{appeal[3]}</b>\n" \
          f"◻️Содержание: <i>{appeal[4]}</i>"
    return txt


def txt_new_appeal(data: dict):
    txt = f"Тип обращения: {data['type']}\n" \
          f"Содержание: {data['content']}\n\n" \
          f"Вы действительно хотите отправить данное обращение администраторам?" 
    return txt