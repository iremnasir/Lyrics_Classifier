import requests
from bs4 import BeautifulSoup
import re
import pickle
import json
import os
from sys import argv
import warnings
warnings.filterwarnings('ignore')

namelist = argv[1:]
# Build this in somehow
#if len(namelist)<3:
#    print('You need to pass in at least two artists')
#else:
###
def create_artist_directory(namelist):
    """ Converts the user input artist name to dash form /
    Creates artist folders in current path """

    st_name = []
    for name in namelist:
        artist_name = str(name).lower()
        artist_name_re = re.sub('_','-',artist_name)
        st_name.append(artist_name_re)
        if not os.path.exists(artist_name_re):
            os.mkdir(artist_name_re)
            print("Directory " , artist_name_re ,  " Created ")
        else:
            print("Directory " , artist_name_re ,  " already exists")
    return st_name

#Build a pattern for HTTP fetch
def song_parsing(st_name):
    """ Collects the number of pages for individual artist's lyrics /
    Fetching each link for each song /
    Writing songs into .txt files """

    links = []
    for artist_st in st_name:
        artist_name_ht = artist_st + '-lyrics.html'
        wbpg = 'https://www.metrolyrics.com/'+artist_name_ht
        links.append(wbpg)
    http_range = [] # List of HTTPs for different artist pages
    for link in links:
        song_links = requests.get(link)
        if song_links.status_code == 200:
            print('Fetching the songs')
        else:
            print('Access denied')
        parsed = BeautifulSoup(song_links.text, 'html.parser')
        for i in range(
        len(parsed.find_all(attrs={'class': 'pages'})[0].find_all('a'))):
            http_range.append(parsed.find_all(attrs={'class': 'pages'})[0]
            .find_all('a')[i].get('href'))
    song_http = []
    for address in http_range:
        songs_pg = requests.get(address)
        pg = BeautifulSoup(songs_pg.text, 'html.parser')
        titles = pg.find_all(
        attrs = {'class': 'page-content tabs-wrapper clearfix'})[0].find_all(attrs = {'class':'title'})
        for i in range(len(titles)):
            song_http.append(titles[i].get('href'))
    for link in song_http:
        artistpre = link.split('.html')[0].split('lyrics')[-1]
        artist_name = artistpre[1:]
        song_name = link.split('/')[3].split('.htm')[0]
        ind_song = requests.get(link)
        parser = BeautifulSoup(ind_song.text, 'html.parser')
        lyrics = parser.find_all(attrs = {'id':'lyrics-body-text'})[0]
        verse = lyrics.find_all(attrs = {'class' : 'verse'})
        lyrics_text = []
        for i in range(len(verse)):
            v = verse[i].get_text()
            lyrics_text.append(v)
        try:
            with open(f'./{artist_name}/{song_name}.txt', 'w') as f:
                json.dump(lyrics_text, f)
        except Exception:
                print('Defective link name, cannot fetch the song')
