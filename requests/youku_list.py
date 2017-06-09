# coding: utf-8

import random
import time
import requests
import xmltodict
from pyquery import PyQuery as pq
douban_movie_query="https://movie.douban.com/subject_search?search_text={}"
film_scores={
}

parsed_yk_urls=[]
output_file = 'yk_douban_score_{}.csv'
parsing_yk_page=0
count=1
headers={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

proxies={
'http':'http://36.81.184.89:80',
'http':'http://36.81.184.94:80',
'http':'http://36.81.185.136:80',
'http':'http://144.140.127.136:8090',
'http':'http://36.81.184.83:80',
'http':'http://36.81.185.9:80',
'http':'http://89.38.149.185:8080',
'http':'http://213.136.77.246:80',
'http':'http://36.81.185.181:80',
'http':'http://36.81.185.73:80',
'http':'http://35.185.72.195:80',
'http':'http://36.81.184.149:80',
'http':'http://36.81.185.138:80',
'http':'http://104.196.58.39:80',
'http':'http://158.69.77.48:8080',
'http':'http://36.81.185.245:80',
'http':'http://36.81.185.8:80',
'http':'http://94.177.190.67:80',

}
time_count=0


def parse_youku_films(url, filename):
    current_page=pq(requests.get(url, headers=headers,  timeout=5).text)
    # print(current_page)
    global parsing_yk_page
    global time_count
    parsing_yk_page+=1
    print("parsing page: {}".format(parsing_yk_page))
    next_url=current_page("li.next")('a').attr('href')
    next_url='http:'+next_url
    current_films=current_page("div.box-series")("ul.panel").children()
    with open(filename,'a+') as f:
        for _ in current_films[:]:
            film = pq(_)
            yk_url, name =film("a").attr('href'), film("a").attr('title')
            douban_url = douban_movie_query.format(name)
            if yk_url in parsed_yk_urls:
                continue
            parsed_yk_urls.append(yk_url)
            # result = parse_mtime_movies( yk_url, name)
            result = parse_douban_movies( yk_url, name)
            if result:
                f.write(result+"\n")
            sleep_time = random.randint(1, 3)
            print("Sleeping:{}".format(sleep_time))
            time.sleep(sleep_time)
            time_count+=sleep_time

    if count % 200 == 0:
        st = random.randint(100, 200)
    else:
        st = random.randint(time_count, 75)

    print("Sleeping {}".format(st))
    time.sleep(st)
    time_count=0
    parse_youku_films(next_url,filename)



def parse_douban_movies(yk_url, name):
    global count
    url="https://movie.douban.com/subject_search?search_text={}".format(name)
    print(url)
    response = requests.get(url, headers=headers,proxies=proxies, timeout=5)
    retries = 0
    print(response.status_code)
    while response.status_code != 200:
        if retries>10:
            break
        try:
            response = requests.get(url, headers=headers,proxies=proxies, timeout=5)
        except:
            retries+=1
            continue

    movies = pq(response.text)
    m_list = movies("tr.item")
    for m in m_list:
        movie=pq(m)
        m_name = movie('a').attr('title')
        stars = movie("div.pl2")("div.star")
        rating=stars('span.rating_nums').text()
        rating = rating if rating else 0
        if m_name==name:
            result = "{},{},{},{}".format(count,'http:'+yk_url, m_name,rating)
            count+=1
            print(result)
            return result

def parse_mtime_movies(yk_url, name):
    url='http://search.mtime.com/search/?q={}&t=1'.format(name)
    global count
    print(url)
    movies = pq(requests.get(url, timeout=5, proxies=proxies, headers=headers).text)
    print(movies)
    error_box = movies("span.edit_color")
    print(len(error_box.children()))
    print(error_box)
    if error_box:
        print("Did not found film:{}".format(name))
        return None

    m_list=movies("div#downRegion")("div.main")("ul.other_list")("li")
    for m in m_list:
        movie = pq(m)
        m_name = movie("h3")("a").text()
        rating = movie("div.filmscore")('p').text()
        print(m_name, rating)
        if name in m_name:
            result = "{}, {}, {}, {}".format(count,'http:'+yk_url, name, rating )
            count+=1
            print(result)
            return result

youku_movie_url="http://list.youku.com/category/show/c_96_r_{}_u_1_s_4_d_1_p_1.html"
# parse_youku_films("http://list.youku.com/category/show/c_96_r_2015_u_1_s_4_d_1_p_1.html")

if __name__ == '__main__':
    import sys
    years = sys.argv[1:] if len(sys.argv)>=2 else 2017
    for year in years:
        filename=output_file.format(year)
        url = youku_movie_url.format(year)
        print(url, filename)
        parse_youku_films(url, filename)
# # films  =  requests.get("http://list.youku.com/category/show/c_96_r_2015_u_1_s_4_d_1_p_29.html")
# d=pq(url="http://list.youku.com/category/show/c_96_r_2015_u_1_s_4_d_1_p_18.html")
# film_div=d("div.box-series")
# # print(type(film_div))
# film_list = film_div("ul.panel").children()
# print(dir(film_list))