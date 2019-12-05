import requests
import time

import config


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    # PUT YOUR CODE HERE
    for i in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=5)
            print('hold on')
            if response.status_code == 200:
                return response
        except:
            if i == max_retries - 1:
                raise
            print('hold on')
            backoff = backoff_factor * (2 ** i)
            time.sleep(backoff)


def get_friends(user_id, fields):
    """ Вернуть данные о друзьях пользователя

    :param user_id: идентификатор пользователя, список друзей которого нужно получить
    :param fields: список полей, которые нужно получить для каждого пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    # PUT YOUR CODE HERE

    #domain = "https://api.vk.com/method"
    #access_token = "669863d9d522ee2802f23585902c0448c8f2ade42913e5b752806f4ce7a1f797fb1af72a688cba5cdced5"
    #v = "5.103"
    #user_id = "410364115"

    #fields = ''

    query = (f"{config.VK_CONFIG['domain']}/" +
             f"friends.get?" +
             f"user_id={user_id}&" +
             f"fields={fields}&" +
             f"access_token={config.VK_CONFIG['access_token']}&" +
             f"v={config.VK_CONFIG['version']}")

    response = get(url=query)
    
    try:
        return response.json()['response']['items']
    except:
        return None

if __name__ == "__main__":
    print(get_friends(369826180,'bdate,sex'))