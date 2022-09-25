'''新增功能: 非同步下載圖片，加快下載速度，如果程式失敗檢查cookie、x-csrf-token'''

import requests as req
import json
import os
from concurrent.futures import ThreadPoolExecutor

def main():
    global link_d, cookie, x_csrf_token, authorization, username, date_l, num_of_img
    link_d = {}
    date_l = []
    num_of_img = 0
    username = input("input username: ")
    cookie = 'dnt=1; kdt=uYacsFQtPPu2ewMWCy9SbT7UOTsz8ylFtfpaGmYD; lang=zh-tw; guest_id_marketing=v1%3A163196644910095243; guest_id_ads=v1%3A163196644910095243; at_check=true; _ga_ZJQNEMXF73=GS1.1.1656313049.1.0.1656313052.0; _ga=GA1.2.217593482.1631966454; mbox=PC#b8e36639a5b9405196d03aff04a26273.32_0#1719647075|session#bdbf0161b9f64c9ebc647f0e0534ae02#1656404135; personalization_id="v1_qcVwTkLBxukIKxiLpAbogw=="; guest_id=v1%3A165683370566240393; _twitter_sess=BAh7CSIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCFQe%252FMKBAToMY3NyZl9p%250AZCIlZjRhZDQzNTY2NjczZDdmNDgwY2QzZThiZGFkZWE3ZGU6B2lkIiU4MzQw%250AYWU5MTcwZDFmMjA4NTc5OTc3ZDUwMGU0YWZmYg%253D%253D--2cb56f087a37a30548cc5dd26347150e81d98c46; external_referer=padhuUp37zilt9KL9%2B5PERZx%2FM6mz60u2uqd6t%2FHycQ%3D|0|8e8t2xd8A2w%3D; gt=1545413474721087489; _gid=GA1.2.190581732.1657290261; g_state={"i_p":1657376711446,"i_l":2}; auth_token=4344d2ba4d1f9c69a5ce65a4146ff8e9489bf18f; ct0=a327728e541227d93f3ded6c7ce6a1f0bfa929081252c147e17cb1ad2e90742e70bb18f1d8f59c5fcc2e2982eb60c834798942ffd6c87671bebc833d5642d3012220060abeed5f4f4fac109d835deee0; twid=u%3D935863469999407105; att=1-3Cr5pEuaelLhkTo9znms0x7UVn7gGIlblSzQjLm7'
    x_csrf_token ='a327728e541227d93f3ded6c7ce6a1f0bfa929081252c147e17cb1ad2e90742e70bb18f1d8f59c5fcc2e2982eb60c834798942ffd6c87671bebc833d5642d3012220060abeed5f4f4fac109d835deee0'
    authorization = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'
    
    get_user_id(username)
    get_req_url(user_id)
    get_img_url(request_url)
    download_images()

def get_user_id(username):#從UserByScreenName取得user-id以取得request url
    global user_id
    #try:
    req_url_of_user_id = f'https://twitter.com/i/api/graphql/mCbpQvZAw6zu_4PvuAUVVQ/UserByScreenName?variables=%7B%22screen_name%22%3A%22{username}%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%7D'
    response = req.get(req_url_of_user_id, headers = {
        'cookie':cookie, 'x-csrf-token':x_csrf_token, 'authorization':authorization,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44'
        })
    data = json.loads(response.text)
    #print(data)
    user_id = data['data']['user']['result']['rest_id']
    print(f"\n{username}'s id is {user_id}")
    #except:
        #print('Fail to get user id, plz check if there is any typo.')
        #return

def get_req_url(user_id):
    global request_url
    request_url = f'https://twitter.com/i/api/graphql/ZlD_vJnCST1I6eHMCSPOOg/UserMedia?variables=%7B%22userId%22%3A%22{user_id}%22%2C%22count%22%3A20%2C%22includePromotedContent%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withClientEventToken%22%3Afalse%2C%22withBirdwatchNotes%22%3Afalse%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Atrue%7D&features=%7B%22dont_mention_me_view_api_enabled%22%3Atrue%2C%22interactive_text_enabled%22%3Atrue%2C%22responsive_web_uc_gql_enabled%22%3Afalse%2C%22vibe_tweet_context_enabled%22%3Afalse%2C%22responsive_web_edit_tweet_api_enabled%22%3Afalse%2C%22standardized_nudges_misinfo%22%3Afalse%2C%22responsive_web_enhance_cards_enabled%22%3Afalse%7D'

def get_img_url(url):
    global link_d, cookie, x_csrf_token, authorization, date_l
    res = req.get(url, headers = {
        'cookie':cookie, 'x-csrf-token':x_csrf_token, 'authorization':authorization,
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'
        })

    data = json.loads(res.text)
    #print(data)
    entries = data['data']['user']['result']['timeline_v2']['timeline']['instructions'][0]['entries']
    #print(entries)
    month = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    
    i, v = 0, 0
    for entry in entries:
        i += 1

        try:
            imgs = entry['content']['itemContent']['tweet_results']['result']['legacy']['entities']['media']
            date_all = entry['content']['itemContent']['tweet_results']['result']['legacy']['created_at']
            date_all = date_all.split(' ')
            date = f'{month.get(date_all[1]):02}{date_all[2]}'
            date_l.append(date)
            #print(date)
                
            for img in imgs:
                url = img['media_url_https']
                if link_d.get(date)==None:
                    link_d[date]=[]
                link_d[date].append(url)
                #print(link_d)
            
        except:
            print(f"fail to get the {i}th tweet's url...")
            v += 1
            
    print(f'{i-v} valid urls are finded.')
    

def download_images():
    global link_d, username, date_l, num_of_img
    print('\nDownloading...')
    os.chdir('C:\Downloads\\twitter')
    if not os.path.exists(username):
        os.mkdir(username)
    os.chdir(f'C:\Downloads\\twitter\{username}')
    with ThreadPoolExecutor(max_workers=5) as exe:
        exe.map(download, date_l)
    print(f'finished\n{num_of_img} imges are saved.')

def download(date):
    global num_of_img
    i = 1
    for url in link_d[date]:
        print(f'{date}_{i:02}.jpg downloading...')
        img = req.get(url)
        with open(f'{date}_{i:02}.jpg' , 'wb') as f:
            f.write(img.content)
            i += 1
            num_of_img += 1
    print(f'{date} Download finish\n')

if __name__ == '__main__':
    main()