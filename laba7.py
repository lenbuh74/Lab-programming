import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp


r = requests.get("https://news.ycombinator.com/newest")


def get_news(site_text):
    page = BeautifulSoup(site_text, 'html.parser')
    tbl = page.find('table').findAll('table')[1]
    news_list = []
    for i in range(30):
        tit = tbl.findAll('tr')[i*3]('td')[2].text.split('(')[0]
        aut = tbl.findAll('tr')[i*3+1]('td')[1].findAll('a')[0].text #('td')[1], т.к. автор идет в маленькой таблице с 0 индексом
        poin = tbl.findAll('tr')[i*3+1]('td')[1].findAll('span')[0].text[:-6] # первой таблице по тегу span
        com = tbl.findAll('tr')[i*3+1]('td')[1].findAll('a')[3].text[:-9]
        url = tbl.findAll('tr')[i*3]('td')[2].findAll('a')[0]['href']
        news = {'title' : tit, 'author' : aut, 'points' : poin, 'comments' : com, 'url' : url}
        news_list.append(news)
    return (news_list)


pp(get_news(r.text))


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, String, Integer
class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)

from sqlalchemy import create_engine
engine = create_engine("sqlite:///news.db")
Base.metadata.create_all(bind=engine)

from sqlalchemy.orm import sessionmaker
session = sessionmaker(bind=engine)
s = session()

news = News(title='Lab 7',
                author='dementiy',
                url='https://dementiy.gitbooks.io/-python/content/lab7.html',
                comments=0,
                points=0)
print (news.id, news.title)
s.add(news)
s.commit()
print(news.id, news.title)