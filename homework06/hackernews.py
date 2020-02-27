from bottle import (
    route, run, template, request, redirect
)

from scraputils import get_news
from db import News, session
from bayes import NaiveBayesClassifier
from stop_words import get_stop_words
import string

stop_words = get_stop_words('english')

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def del_stops(s):
    s = s.split()
    k = []
    for i in range(len(s)):
        if s[i] not in stop_words:
            k.append(s[i])
    s=''
    for i in range(len(k)):
        if i!=len(k)-1:
            s+=(k[i]+' ')
        else:
            s+=(k[i])
    return s


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route("/add_label/")
def add_label():
    s = session()

    news_id = request.query['id']
    label  = request.query['label']

    news = s.query(News).filter(News.id == news_id).one()
    news.label = label

    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 10)
    top_news = get_news("https://news.ycombinator.com/", 11)
    news.extend(top_news)
    for n in range(len(news)):
        row = News(title=news[n]["title"],
                   author=news[n]["author"],
                   url=news[n]["url"],
                   comments=news[n]["comments"],
                   points=news[n]["points"])
        if s.query(News).filter(News.title == row.title and News.author == row.author).all():
            continue
        s.add(row)
        s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    s = session()
    labeled_news = s.query(News).filter(News.label != None).filter(News.id < 1001).all()
    x = [clean(news.title) for news in labeled_news]
    x = [del_stops(news) for news in x]
    y = [news.label for news in labeled_news]
    classifier = NaiveBayesClassifier(1)
    classifier.fit(x, y)

    rows = s.query(News).filter(News.label == None).all()
    good, maybe, never = [], [], []
    for row in rows:
        row.title = clean(row.title)
        row.title = del_stops(row.title)

        prediction = classifier.predict([row.title])
        print(prediction)
        
        if prediction == ['good']:
            good.append(row)
        elif prediction == ['maybe']:
            maybe.append(row)
        else:
            never.append(row)

    return template('news_recs', good=good, maybe=maybe, never=never)


@route("/update_recs")
def update_recs():
    s = session()
    news = get_news("https://news.ycombinator.com/newest", 4)
    top_news = get_news("https://news.ycombinator.com/", 2)
    news.extend(top_news)
    for n in range(len(news)):
        row = News(title=news[n]["title"],
                   author=news[n]["author"],
                   url=news[n]["url"],
                   comments=news[n]["comments"],
                   points=news[n]["points"])
        if s.query(News).filter(News.title == row.title and News.author == row.author).all():
            continue
        s.add(row)
        s.commit()
    redirect("/classify")


if __name__ == "__main__":
    run(host="localhost", port=8080)
