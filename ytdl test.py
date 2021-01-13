import lmao, os, youtube_dl, eyed3
def yt_mp3(url, path='downloads', autoplay=True, format='mp3'):
    from playsound import playsound;
    if not os.path.isfile('ffmpeg.exe'):
        try:
            lmao.install_ffmpeg()
        except:
            return print("could not download ffmpeg.exe")
        clear()
    ydl_opts={}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title=info_dict['title'].replace(':', ' -')
    filename = video_title + ".mp3"
    if not os.path.isdir(path): os.mkdir(path)
    if format=='mp3':
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'ignoreerrors': True,
            'logger': lmao.logger(),
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
            'format': format,
            #'ignoreerrors': True,
            'logger': lmao.logger(),
            'noplaylist': True,
        }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    #clear()
    # if info_dict["artist"] != None:
    #     audiofile = eyed3.load(os.path.join(path, filename))
    #     audiofile.tag.artist = info_dict["artist"]
    #     audiofile.tag.album = info_dict["album"]
    #     audiofile.tag.album_artist = info_dict["uploader"]
    #     audiofile.tag.title = info_dict["track"]
    #     audiofile.tag.release_date = info_dict["release_year"]
    #     audiofile.tag.save()
    # if autoplay: lmao.music_player(filename=filename)

yt_mp3('https://youtu.be/jjHMB1mTzZc')
