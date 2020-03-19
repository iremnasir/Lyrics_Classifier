import requests
from bs4 import BeautifulSoup
import re
import pickle
import json
import os
from sys import argv
import warnings
warnings.filterwarnings('ignore')


BASE_URL = 'https://www.metrolyrics.com/'


def create_artist_directory(namelist):

    """
    Converts the user input artist name to dash form /
    Creates artist folders in current path

    """

    st_name = []
    for name in namelist:
        artist_name = str(name).lower()
        artist_name_re = re.sub('_', '-', artist_name)
        st_name.append(artist_name_re)
        if not os.path.exists(artist_name_re):
            os.mkdir(artist_name_re)
            print("Directory", artist_name_re, " created ")
        else:
            print("Directory", artist_name_re, " already exists")
    return st_name

def create_artist_url(st_name):
    """
    Takes a list of names
    Generates base url pattern for each name
    Returns artist urls
    """
    artist_link = []
    for artist_st in st_name:
        artist_name_ht = artist_st + '-lyrics.html'
        wbpg = BASE_URL+artist_name_ht
        artist_link.append(wbpg)
    return artist_link

def collect_artist_song_pages(artist_link):
    """
    Parses the collection of urls for each artist_st
    """
    http_links = []
    for link in artist_link:
        song_links = requests.get(link)
        if song_links.status_code == 200:
            print('Access granted')
        else:
            print('Access denied')
        parsed = BeautifulSoup(song_links.text, 'html.parser')
        for i in range(
        len(parsed.find_all(attrs={'class': 'pages'})[0].find_all('a'))):
            http_links.append(parsed.find_all(attrs={'class': 'pages'})[0]
            .find_all('a')[i].get('href'))
    return http_links

def collect_song_urls(http_links):
    """Parse each song url"""
    song_http = []
    for address in http_links:
        songs_pg = requests.get(address)
        pg = BeautifulSoup(songs_pg.text, 'html.parser')
        titles = pg.find_all(
        attrs = {'class': 'page-content tabs-wrapper clearfix'})[0].find_all(attrs = {'class':'title'})
        for i in range(len(titles)):
            song_http.append(titles[i].get('href'))
    return song_http

def song_parsing(song_http):
    """
    Collect artist name again from the url
    Parse the songs
    Omit the songs with non-pattern matching urls
    Write .txt files
    """

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
    return artist_name, song_name
