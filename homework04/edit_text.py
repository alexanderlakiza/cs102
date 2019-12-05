import pandas as pd
import requests
import textwrap

import config

from pandas.io.json import json_normalize
from string import Template
#from tqdm import tqdm
from stop_words import get_stop_words

stop_words = get_stop_words('russian')
stop_symbols = (',:!?;.\n-_+="()[]}*^%$#><{')
digits = ('0123456789')

"""def get_wall(
    owner_id: str='',
    domain: str='',
    offset: int=0,
    count: int=13,
    filter: str='',
    extended: int=0,
    fields: str='',
    v: str='5.103'
):
    
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param v: Версия API.""
    
    
    code = ("return API.wall.get({" +
        f"'owner_id': '{owner_id}'," +
        f"'domain': '{domain}'," +
        f"'offset': {offset}," +
        f"'count': {count}," +
        f"'filter': '{filter}'," +
        f"'extended': {extended}," +
        f"'fields': '{fields}'," +
        f"'v': {v}," +
    "});")

    response = requests.post(
        url="https://api.vk.com/method/execute",
            data={
                "code": code,
                "access_token": config.VK_CONFIG["access_token"],
                "v": "5.103"
            }
    )

    posts = []
    for i in range(count):
        try:
            posts.append(response.json()['response']['items'][i]['text'])
        except:
            break

    return posts"""


posts = ['https://github.com/alexanderlakiza\nИтмо', 'Антоха!Поля!Арсенал!Итмо!Прога!Колени', 'кек лол Арсенал!😇', 'Программирование губит мою нервную систему...\nалло', 'Вы тоже хотите поступить в итмо?', 'Антоха сегодня помог с графами, он красавчик\n\nЗабыл ему сегодня сказать, что мне Полина сказала', 'скоро начну разговаривать с самим собой\n\nа пока думаю о футболе и об итмо!', 'Что еще сюда написать?\n\nПривет!', 'ИТМО. ИКТ. РОФЛАНПРОГА, лол', 'мне бы хотелось научиться программировать((((', 'сегодня мой темнокожий учитель английского был в футболочке "Россия" с гербом РФ\nлол', 'надеюсь, Арсенал поднимется с колен\n\nхотя бы пока мои дети будут живы🤣🤣', 'единственное,что у меня появилось новое - пара проблем с прогой']


def delete_dig_sym():
	for i in range(len(posts)):  # убираем символы
		for ch in range(len(posts[i])):
			if posts[i][ch] in stop_symbols:
				posts[i] = posts[i].replace(posts[i][ch],' ')

	for i in range(len(posts)):  # убираем цифры
		for ch in range(len(posts[i])):
			if posts[i][ch] in digits:
				posts[i] = posts[i].replace(posts[i][ch],' ')


	
	return posts


upd_posts = delete_dig_sym()

old_new_posts=[]


def delete_words():
	posts = [upd_posts[i].split() for i in range(len(upd_posts))]
	posts = [[j for j in posts[k] if j not in stop_words] for k in range(len(posts))]
	print(posts)
	return


if __name__ == '__main__':
	delete_words()
	#print(stop_words)

	#print(delete_things())
