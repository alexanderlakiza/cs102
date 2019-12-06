import datetime as dt
from statistics import median
from typing import Optional

from api import get_friends
#from api_models import User
import time

#user_id = 369826180
def age_predict(user_id: int) -> Optional[float]:
    """ Наивный прогноз возраста по возрасту друзей

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: идентификатор пользователя
    :return: медианный возраст пользователя
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    friends = get_friends(user_id,'bdate,sex')
    ages = []
    today = dt.datetime.today()

    for friend in friends:
        try:
            bdate = friend['bdate']
            bdate = dt.datetime.strptime(bdate, "%d.%m.%Y")
            ages.append((today - bdate).days/365)
        except:
            pass

    if len(ages)>0:
        print(ages)
        a = round(median(ages), 1)
        return a
    else:
        return None
        
print('Средний возраст:',age_predict(369826180))