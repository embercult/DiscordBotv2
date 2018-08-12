import requests
from bs4 import BeautifulSoup as Soup
import re


def timecheck(t):
    t = t.split(' ')
    if t[1] == 'hours' or t[1] == 'days' or (t[1] == 'min' and int(t[0]) >= 3):
        return False
    else:
        return True


def usercheck(user):

    return timecheck(getusers()[user])


def getusers():
    url = 'https://www.codechef.com/status/HS08TEST'
    d = requests.get(url)
    soup = Soup(d.content, 'html.parser')
    x = list(list(soup.find_all(class_='dataTable')[0].children)[3].children)
    z = list()
    y = list()
    q = dict()
    for i in x:
        i = str(i)
        z.append(re.findall('<a href="/users/(.*?)"', i))
        y.append(re.findall('<td width="50">*(.*?)ago',i))
    z.pop()
    z.pop(0)
    y.pop()
    y.pop(0)
    for i in range(len(y)):
        if z[i][0] not in q:
            q[z[i][0]] = y[i][0]
    return q


def userrating(user):
    try:
        url = 'https://www.codechef.com/users/' + user
        d = requests.get(url)
        soup = Soup(d.content, 'html.parser')
        x = soup.find_all('div', {"class": "rating-number"})[0].string
        return x
    except:
        return False


# def userexists(user):
#     if userrating(user):
#         return True
#     else:
#         return False