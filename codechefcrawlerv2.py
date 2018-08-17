import requests
from bs4 import BeautifulSoup as Soup
import re


def get_users(): #Gets the users who have submitted solutions(in past minute?)
    url = 'https://www.codechef.com/status/HS08TEST'
    d = requests.get(url)
    soup = Soup(d.content, 'html.parser')
    x = list(list(soup.find_all(class_='dataTable')[0].children)[3].children)
    z = list()
    y = list()
    for i in x:
        i = str(i)
        z.append([re.findall('<a href="/users/(.*?)"', i),re.findall('<td width="50">*(.*?)ago', i)])
    for i in range(len(z)):
        try:
            if (z[i][1][0].split()[1] == 'sec' or (int(z[i][1][0].split()[0]) < 1 and z[i][1][0].split()[1] == 'min')):
                y.append(z[i])
        except IndexError:
            a = 0
    return y


def user_rating(user):
    try:
        url = 'https://www.codechef.com/users/' + user
        d = requests.get(url)
        soup = Soup(d.content, 'html.parser')
        x = soup.find_all('div', {"class": "rating-number"})[0].string
        return x
    except:
        return False

def live_contest():
    url = 'https://www.codechef.com/contests'
    d = requests.get(url)
    soup = Soup(d.content, 'html.parser')
    soup = soup.find_all(class_='dataTable')[:2]
    for i in range(len(soup)):
     soup[i] = soup[i].find_all('tr')[1:]
    present = len(soup[0])
    x = []
    y = []
    q = []
    w = []
    for j in range(len(soup)):
        for i in range(len(soup[j])):
            x.append(soup[j][i].find_all('td'))
    for j in range(len(x)):
        for i in range(len(x[i])):
            y.append(x[j][i].contents)
        q.append(y)
        y = []

    for i in range(len(q)):
        w.append([q[i][0][0], re.findall('">(.*?)</a>', str(q[i][1][0]))[0], re.findall('<a href="(.*?)"', str(q[i][1][0]))[0],q[i][2][0],q[i][2][2],q[i][3][0],q[i][3][2]])
    return w, present


def verify_user(user):
    for i in get_users():
        if user in i[0]:
            return True
    return False