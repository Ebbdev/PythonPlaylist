from __future__ import unicode_literals
from pytube import YouTube
from bs4 import BeautifulSoup
import time
import urllib
import os
import youtube_dl
import pyautogui
import speedtest
s = speedtest.Speedtest()
a = s.download()/(1024*1024)


def playlist_GUI():
    print("Do You Want to Download all Playlist ? Yes/No ")
    yes_no = input()
    if(yes_no == "Yes"):
        return [0,0]
    elif(yes_no =="No"):
        try:
            print("Enter starting video index : ")
            starting = int(input())-1
            print("Enter finishing video index : ")
            finishing = int(input())-1
        except:
            print("Enter integer value !!!")
            playlist_GUI()
        if(starting > finishing | starting<0 | finishing<0):
            print(" !!! Changed starting and finishing index !!!")
            return [finishing,starting]
        return [starting,finishing]
    else:
        print("Wrong !!! Enter valid input")
        playlist_GUI()

def audio_dowload(url):
    ydl_opts = {
        'format' : 'bestaudio/best',
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec' : 'mp3' ,
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg':True,
        'keepvideo':False
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_video(url,path):
    yt = YouTube(url)
    yt = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
    if not os.path.exists(path):
        os.makedirs(path)
    yt.download(path)


def get_data_playlist(url):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page,'html.parser')
    playlist_url_array = []
    for link in soup.find_all('a'):
        playlist =  link.get('href')
        if(playlist.find("index") != -1):
            playlist = "youtube.com"+playlist
            playlist_url_array.append(playlist)
    del playlist_url_array[0],playlist_url_array[0]
    return playlist_url_array


while(True):
   
    print(" *** Welcome Youtube Simply Video - Audio Downloader *** \n")
    print('          Options      \n '+
          '  1- Video Download    \n '+
          '  2- Playlist Download \n '+
          '  3- Audio Download    \n '+
          '          Exit Q          '
        )
    choosing_options = input().strip()
    if(choosing_options=="q"):
        print("Exit ... ")
        time.sleep(2)
        break;
    print("&&&&&  Enter URL address  &&&&& ")
    user_url = input()
    if(choosing_options == "1"):
        tube = YouTube(user_url)
        video = tube.streams.filter(progressive=True, file_extension='mp4').first()
        size_video = int(round(video.filesize/(1024*1024)))
        download_video(user_url,'./testvideo')
        time.sleep(size_video/a)
        print("Download finished ^_^  ")
    elif(choosing_options == "2"):
        playlist_arr = get_data_playlist(user_url)
        temp = playlist_GUI()
        start = temp [0]
        finish = temp[1]
        if(start > len(playlist_arr) | finish>len(playlist_arr)):
            print(" Wrong index number range !!! ")
            playlist_GUI()
        else:
            while(start<=finish):
                tube = YouTube(playlist_arr[start])
                video = tube.streams.filter(progressive=True, file_extension='mp4').first()
                size_video = int(round(video.filesize/(1024*1024)))
                download_video(playlist_arr[start],'./testvideoplaylist')
                start += 1
                time.sleep(size_video/a)
            print("Download all videos '_' ")
    elif(choosing_options == "3"):
        audio_dowload(user_url)
        time.sleep(10)
   
    else:
        print("Please enter valid options !!!")





