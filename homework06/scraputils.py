import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []
    
    news = parser.find_all('tr', {'class' : 'athing'})
    news_stat = parser.find_all('td', {'class' : 'subtext'})

    for i in range(len(news_stat)):
        title = (news[i].find('a', {'class' : 'storylink'})).text

        try:
            author = (news_stat[i].find('a', {'class' : 'hnuser'})).text
        except:
            author = 'N/A'

        if (news_stat[i].text).split()[-1] == 'discuss':
            comments = 0
        elif (news_stat[i].text).split()[-2] == '|': # если нет discuss
            comments = 0
        else:
            int((news_stat[i].text).split()[-2])
            comments = int((news_stat[i].text).split()[-2])

        try:
            points = int(news_stat[i].find("span", {"class" : "score"}).text.split()[0])
        except:
            points = 0

        url = (news[i].find('a', {'class' : 'storylink'}))['href']
        if len(url.split(".")) == 1:
            url = "https://news.ycombinator.com/" + url

        news_list.append(
            {'author': author,
            'comments': comments,
            'points': points,
            'title': title,
            'url': url})

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    next_page_beeline = parser.find('a', {'class' : 'morelink'})['href']
    return next_page_beeline


def get_news(url, n_pages=16):
    """ Collect news from a given web page """
    news = []
    k = 1
    while n_pages:
        print("Collecting data from page: {}".format(url))
        print(k)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        if k != 16:
            next_page = extract_next_page(soup)
        else:
            next_page = ''
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
        k += 1
    return news


if __name__ == '__main__':
    print(get_news("https://news.ycombinator.com/"))