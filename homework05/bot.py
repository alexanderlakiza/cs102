import requests
import telebot
import config
import datetime
import time
from bs4 import BeautifulSoup


telebot.apihelper.proxy = {'https': 'https://141.125.82.106:80'}
bot = telebot.TeleBot(config.access_token)

days = [
        'monday',
        'tuesday',
        'wednesday',
        'thursday',
        'friday',
        'saturday',
        'sunday'
]


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url, verify = False)
    web_page = response.text
    return web_page


'''def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) \
    for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list'''


def parse_schedule(web_page, day):
    soup = BeautifulSoup(web_page, "html5lib")

    week = ['/monday', '/tuesday', '/wednesday',
            '/thursday', '/friday', '/saturday', '/sunday']
    num = 0
    for week_day in range(len(week)):
        if week[week_day] == day:
            num = week_day + 1

    day = '{}day'.format(num)
    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})

    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Номер аудитории
    rooms_list = schedule_table.find_all(
        "dd", attrs={"class": "rasp_aud_mobile"}
    )
    rooms_list = [aud.text for aud in rooms_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info])
                    for lesson_info in lessons_list
                    ]

    return times_list, locations_list, rooms_list, lessons_list


'''@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = \
        parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')'''


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday',
                               'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """
    try:
        received_message = message.text.split()

        if len(received_message) == 2:
            day, group = received_message
            web_page = get_page(group)
        else:
            day, group, week = received_message
            web_page = get_page(group, week)

        if 'Расписание не найдено' in web_page:
            bot.send_message(message.chat.id, 'Такой группы нет')
        else:
            try:
                if day[1:] != "sunday":
                    times_list, locations_list, rooms_list, lessons_list \
                        = parse_schedule(web_page, day)
                    resp = ''
                    for time, location, room, lession in zip(
                            times_list, locations_list, rooms_list,
                            lessons_list):
                        resp += '<b>{}</b>, {}, {}, {}\n'.format(
                            time, location, room, lession)
                    bot.send_message(message.chat.id, resp, parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, "Выходной")
            except AttributeError:
                resp = 'Занятий нет'
                bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный ввод данных. \
            \nВведите команду <b>/help</b> для справки', parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    q = datetime.datetime.today()
    b = datetime.datetime(2019, 9, 2, 0, 0, 0)
    a = q - b
    c = a.days  # Разность дней,начиная со 2 сентября
    n_day = c % 7
    n_week = c // 7

    if n_week % 2 == 0:
        n_week = '2'  # Неделя - нечётная
    else:
        n_week = '1'  # Неделя - чётная

    week = ['/monday', '/tuesday', '/wednesday',
            '/thursday', '/friday', '/saturday', '/sunday']
    week_day = week[n_day]
    hours = datetime.datetime.today().hour
    minutes = datetime.datetime.today().minute
    r_n = hours * 60 + minutes  # Минуты с 0-00 сегодня

    try:
        _, group = message.text.split()

        web_page = get_page(group, n_week)
        if 'Расписание не найдено' in web_page:
            bot.send_message(message.chat.id, 'Такой группы нет')
        else:
            try:
                times_list, locations_list, rooms_list, lessons_list \
                    = parse_schedule(web_page, week_day)
                resp = ''
                q = times_list[-1]
                h = q.split('-')
                start_last = h[0]
                start_last = start_last.split(':')
                start_last_minutes = int(start_last[0])*60 + int(start_last[1])
                for i in range(len(times_list)):
                    k = times_list[i].split('-')
                    start = k[0]
                    start = start.split(':')
                    start_minutes = int(start[0])*60 + int(start[1])
                    if r_n < start_minutes:
                        resp += '<b>{}</b>, {}, {}, {}\n'.format(
                            times_list[i], locations_list[i],
                            rooms_list[i], lessons_list[i])
                        bot.send_message(message.chat.id,
                                         '<b>Сегодня:\n</b>' + resp,
                                         parse_mode='HTML')
                    elif r_n > start_last_minutes:
                        for _ in range(1, 7):
                            n_day += 1
                            if n_day == 7:
                                n_day = 0
                                if n_week == "1":
                                    n_week = "2"
                                else:
                                    n_week = "1"
                            week = ['/monday', '/tuesday', '/wednesday',
                                    '/thursday', '/friday', '/saturday',
                                    '/sunday']
                            week_day = week[n_day]
                            web_page = get_page(group, n_week)
                            try:
                                times_list, locations_list, \
                                    rooms_list, lessons_list \
                                    = parse_schedule(web_page, week_day)
                                resp = ''
                                resp += '<b>{}\n</b><b>{}</b>, {}, {}, {}\n'.format(
                                    week[n_day], times_list[0],
                                    locations_list[0],
                                    rooms_list[0], lessons_list[0])
                                bot.send_message(message.chat.id,
                                                 resp, parse_mode='HTML')
                                break
                            except AttributeError:
                                continue
                    if len(resp) != 0:
                        break
                # bot.send_message(message.chat.id, resp, parse_mode='HTML')
            except AttributeError:
                for _ in range(1, 7):
                    n_day += 1
                    if n_day == 7:
                        n_day = 0
                        if n_week == "1":
                            n_week = "2"
                        else:
                            n_week = "1"
                    week = ['/monday', '/tuesday', '/wednesday',
                            '/thursday', '/friday', '/saturday', '/sunday']
                    week_day = week[n_day]
                    web_page = get_page(group, n_week)
                    try:
                        times_list, locations_list, rooms_list, lessons_list \
                            = parse_schedule(web_page, week_day)
                        resp = ''
                        resp += '<b>{}\n</b><b>{}</b>, {}, {}, {}\n'.format(
                            week[n_day], times_list[0], locations_list[0],
                            rooms_list[0], lessons_list[0])
                        bot.send_message(message.chat.id,
                                         resp, parse_mode='HTML')
                        break
                    except AttributeError:
                        continue

    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный ввод данных. \
            \nВведите команду <b>/help</b> для справки', parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    try:
        q = datetime.datetime.today()
        b = datetime.datetime(2019, 9, 2, 0, 0, 0)
        a = q - b
        c = a.days
        n_day = c % 14

        odd_week = (0, 1, 2, 3, 4, 5, 13)
        even_week = (6, 7, 8, 9, 10, 11, 12)
        week = ['/monday', '/tuesday', '/wednesday',
                '/thursday', '/friday', '/saturday', '/sunday']
        if n_day in odd_week:
            n_day += 1
            n_day %= 7
            week_day = week[n_day]
            command, group = message.text.split()
            web_page = get_page(group, '2')
        else:
            n_day += 1
            n_day %= 7
            week_day = week[n_day]
            command, group = message.text.split()
            web_page = get_page(group, '1')

        if 'Расписание не найдено' in web_page:
            bot.send_message(message.chat.id, 'Такой группы нет')
        else:
            try:
                if week_day != '/sunday':
                    times_list, locations_list, rooms_list, lessons_list \
                        = parse_schedule(web_page, week_day)
                    resp = ''

                    for time, location, room, lession in zip(
                            times_list, locations_list,
                            rooms_list, lessons_list):
                        resp += '<b>{}</b>, {}, {}, {}\n'.format(
                            time, location, room, lession)
                    bot.send_message(message.chat.id, resp, parse_mode="HTML")
                else:
                    bot.send_message(message.chat.id, "Выходной")
            except AttributeError:
                resp = 'Занятий нет'
                bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный ввод данных. \
            \nВведите команду <b>/help</b> для справки', parse_mode='HTML')


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    try:
        received_message = message.text.split()

        if len(received_message) == 2:
            _, group = received_message
            web_page = get_page(group)
        else:
            _, group, week = received_message
            web_page = get_page(group, week)

        if 'Расписание не найдено' in web_page:
            bot.send_message(message.chat.id, 'Такой группы нет')
        else:
            week_resp = ['<b>Понедельник:</b>\n', '<b>Вторник:</b>\n',
                         '<b>Среда:</b>\n', '<b>Четверг:</b>\n',
                         '<b>Пятница:</b>\n', '<b>Суббота:</b>\n',
                         '<b>Воскресенье:</b>\n']
            week = ['/monday', '/tuesday', '/wednesday',
                    '/thursday', '/friday', '/saturday', '/sunday']
            resp = ''
            for i in range(7):
                respond = week_resp[i]
                try:
                    times_list, locations_list, rooms_list, lessons_list \
                        = parse_schedule(web_page, week[i])

                    for time, location, room, lession in zip(
                            times_list, locations_list,
                            rooms_list, lessons_list):
                        respond += '<b>{}</b>, {}, {}, {}\n'.format(
                            time, location, room, lession)
                except AttributeError:
                    respond += 'Занятий нет\n'
                resp += respond
            bot.send_message(message.chat.id, resp, parse_mode='HTML')

    except ValueError:
        bot.send_message(message.chat.id, 'Неправильный ввод данных. \
            \nВведите команду <b>/help</b> для справки', parse_mode='HTML')


@bot.message_handler(commands=['help'])
def get_help(message):
    if message.text[1:] == "help":
        bot.send_message(message.chat.id,
                         '<b>Получить расписание на указанный день</b> \
            \n/WEEK_DAY GROUP WEEK_TYPE \
            \n<b>Получить расписание на завтрашний день</b> \
            \n/TOMMOROW GROUP \
            \n<b>Получить ближайшее занятие</b> \
            \n/NEAR GROUP \
            \n<b>Получить расписание группы на указанную неделю</b> \
            \n/ALL GROUP WEEK_TYPE \
            \n<b>WEEK_TYPES: \
            \n1 - чётная неделя \
            \n2 - нечётная неделя \
            \nWEEK_DAY - День недели по-английски \
            \nGROUP - Название учебной группы</b>', parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)
