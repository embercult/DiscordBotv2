import urllib.parse
import urllib.request
import json

def pastebinpost(user, language, code):  # function to post code on pastebin
    url = "http://pastebin.com/api/api_post.php"
    values = {'api_dev_key': '12efb555d9bb45188ca382e4003df583',  # your api dev key
              'api_paste_code': f'{code}',  # code you wanna post
              'api_paste_private': '1',  # 1 = unlisted 0 = public and 2 = private
              'api_paste_name': f'{user}s{language}code.php',  # name of paste eg. embercultspythoncode.php
              'api_paste_expire_date': 'N',  # N = never expire 10m = expire in 10 mins
              'api_paste_format': f'{language}',  # language the paste is in
              'api_option': 'paste', }  # telling api that we wanna make a paste

    data = urllib.parse.urlencode(values)  # encoding the values into url
    data = data.encode('utf-8')  # pastebin accepts uft 8 only
    req = urllib.request.Request(url, data)  # make the final url

    with urllib.request.urlopen(req) as response:  # ask pastebin to make a paste
        pageurl = response.read()  # pastebin tell you the url of paste
    return pageurl  # return the url
#so i dont like commenting code but when i do i do this


def giphy(tag = None):
    print(tag)
    key = 'LwB4XOaGKkUoD2j6KUNeLvMAz2jbC97S'
    if tag == None:
        url = "http://api.giphy.com/v1/gifs/random?api_key={}&rating=g".format(key)
    else:
        url = "http://api.giphy.com/v1/gifs/random?api_key={}&tag={}&rating=g".format(key, tag)
    with urllib.request.urlopen(url) as response:
        pageurl = response.read().decode()
    pageurl = json.loads(pageurl)
    return (pageurl['data']['embed_url'])