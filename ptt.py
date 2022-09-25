import requests as req
import bs4
def get_data(url):
    
    res = req.get(url, headers = {
        'cookie':'over18=1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
    })
    data = bs4.BeautifulSoup(res.text, 'html.parser')

    titles = data.find_all('div', attrs={'class':'title'})
    for title in titles:
        if title.a != None:
            print(title.text)
            print(title.a["href"])
    next_page = data.find('a', string='‹ 上頁')
    return next_page['href']

url = 'https://www.ptt.cc/bbs/Gossiping/index.html'
count = 0
while count<5:
    url ='https://www.ptt.cc' + get_data(url)
    count += 1
