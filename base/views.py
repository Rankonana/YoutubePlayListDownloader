from django.shortcuts import render
from pytube import YouTube, Playlist
from .form import UrlForm
from django.conf import settings
import shutil
import string
import random
import os
import re
from django.http import HttpResponse


def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    
def home(request):
    request.session[0]='var'
    if request.method == 'POST':
        x = id_generator()
        form = UrlForm(request.POST)
        if form.is_valid():
            #Downloading a song song
            url = form.cleaned_data['url']
            regex = r'^(http(s)?:\/\/)?((w){3}.)?youtu(be|.be)?(\.com)?\/.+'
            if not re.match(regex,url):
                return HttpResponse('Enter correct url.')


            if('list' in url):
                #Downloading a PlayList song
                p = Playlist(url)
                thumb =''
                Duration = 0
                title = ''
                for v in p.videos:
                   saveTo = str(settings.MEDIA_ROOT) + '\\'+ x
                   yt = YouTube(v.watch_url)
                   yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(saveTo)
                   Duration += yt.length
                   if len(thumb)  <5 :
                    thumb = yt.thumbnail_url 
                    title = 'Playlist for : ' + yt.title + ' video with :\n\n ' + str(p.length) + '  videos'
                shutil.make_archive(saveTo, 'zip', saveTo)
                context = {
                     'downloadlink' : settings.MEDIA_URL + x+ '.zip',
                     'form': form,
                     'extension': '.zip',
                     'thumb': thumb,
                     'title': title,
                     'Duration': str(round(((Duration)/60),2)) + ' Minutes'
                      }
                return render(request, 'home.html',context)

            else:
                yt = YouTube(url)
                saveTo = str(settings.MEDIA_ROOT) + '\\'+ x
                yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(saveTo)
                
                arr = os.listdir(saveTo)
                for file_n in arr:
                    filename = file_n
                context = {
                    'downloadlink' : settings.MEDIA_URL +  x +'\\'+ filename,
                    'form': form,
                    'title': yt.title ,
                    'extension': '.mp4',
                    'thumb': yt.thumbnail_url,
                    'Duration': str(round(((yt.length)/60),2)) + ' Minutes'

                    }
                return render(request, 'home.html',context)



    else:
        form = UrlForm
    return render(request, 'home.html',{'form': form})