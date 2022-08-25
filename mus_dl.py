#!/usr/bin/env python3
import os, youtube_dl, logging, get_cover_art, json, taglib

def install_ffmpeg(overwrite=False):
    if os.name == 'nt':
        if not os.path.isfile('ffmpeg.exe') or overwrite:
            if not os.path.isdir(os.path.join("resources","ffmpeg","release-full")): os.mkdir(os.path.join("resources","ffmpeg","release-full"))
            resp = requests.get('https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z', allow_redirects=True)
            with open(os.path.join('resources','ffmpeg','ffmpeg-release-full.7z'), "wb") as f:
                f.write(resp.content)
            # os.system('7za x '+os.path.join('resources','ffmpeg','ffmpeg-release-full.7z')+' -o'+os.path.join('resources','ffmpeg'))
            import py7zr
            with py7zr.SevenZipFile(os.path.join('resources','ffmpeg', 'ffmpeg-release-full.7z'), mode='r') as sz:
                sz.extractall(path=os.path.join("resources","ffmpeg","release-full"))
            shutil.copyfile(os.path.join("resources","ffmpeg","release-full","bin","ffmpeg.exe"), 'ffmpeg.exe')
            self.log.debug('copied ffmpeg.exe')

class MusicGetter():
    """docstring for MusicGetter."""

    def __init__(self):
        self.log = logging.getLogger('MusicGetter')
        self.log.setLevel(logging.DEBUG)
        if not self.log.handlers:
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
            ch.setFormatter(formatter)
            self.log.addHandler(ch)

    def dl_file(self, url, filename='', path=''):
        import requests
        headers = requests.utils.default_headers()
        x = requests.get(url, headers=headers, allow_redirects=True)
        if filename =='':
            filename = url.split('/')[-1]
        if path=='':
            with open(filename, 'wb') as file:
                file.write(x.content); file.close()
        else:
            if not os.path.isdir(path): os.makedirs(path)
            with open(os.path.join(path,filename), 'wb') as file:
                file.write(x.content); file.close()

    def dump_json(self, data, filename, path = ""):
        if path != "":
            if not os.path.isdir(path):
                os.makedirs(path)
        with open(os.path.join(path, filename), 'w') as file:
            json.dump(data, file, indent=4, separators=(',', ': '))

    def infoget(self, url):
        ydl_opts = {
        'ignoreerrors': True
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
        self.log.debug(info_dict)
        return info_dict

    def album_art_folder(self, path, force=True, no_embed=False):
        coverdict={'inline':True, 'verbose':True}
        if force:
            coverdict['force']=True
        if no_embed:
            coverdict['no_embed']=True
        finder = get_cover_art.CoverFinder(coverdict)
        finder.scan_folder(path)

    def yt_mp3(self, url, path='downloads', autoplay=True, format='mp3'):
        install_ffmpeg()
        info_dict = infoget(self, url)
        video_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').translate({ord(i): ' ' for i in "<>:\"/\\|?*"})
        filename = video_title + "." + format
        if format=='mp3':
            if not os.path.isdir(path): os.makedirs(path)
            if not os.path.isfile(os.path.join(path, filename)):
                ydl_opts = {
                    'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                    'format': 'bestaudio/best',
                    'ignoreerrors': True,
                    'logger': logger(),
                    'noplaylist': True,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            #clear()
            if info_dict["artist"] != None:
                audiofile = eyed3.load(os.path.join(path, filename))
                audiofile.tag.artist = info_dict["artist"]
                audiofile.tag.album = info_dict["album"]
                audiofile.tag.album_artist = info_dict["uploader"]
                audiofile.tag.title = info_dict["track"]
                audiofile.tag.release_date = info_dict["release_year"]
                audiofile.tag.save()
        elif format=='flac':
            if not os.path.isfile(os.path.join(path, video_title+".flac")):
                ydl_opts = {
                    'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                    'format': 'bestaudio/best',
                    'ignoreerrors': True,
                    'logger': logger(),
                    'noplaylist': True,
                    # 'extract-audio': True,
                    # 'audio-format': 'flac',
                    # 'audio-quality': '0',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'flac',
                        'preferredquality': '300',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                if not os.path.isdir(path): os.mkdir(path)
            else:
                self.log.error('file already exists')
        else:
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'format': format,
                'embed-thumbnail': True,
                'add-metadata': True,
                'ignoreerrors': True,
                'logger': logger(),
                'noplaylist': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        if autoplay: music_player(filename=filename)

    def yt_playlist_mp3(self, url, overwrite=False, path='playlists', format='mp3', askformat=True, enum=False):
        created = False
        if not os.path.isfile('ffmpeg.exe'):
            install_ffmpeg()
        info_dict = self.infoget(url)
        try:
            playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').translate({ord(i): ' ' for i in "<>:\"/\\|?*"})
        except:
            playlist_title = info_dict['id']
        if not os.path.isdir(os.path.join(path, playlist_title)):
            created = True
            os.makedirs(os.path.join(path, playlist_title))
        self.dump_json(info_dict, F"{playlist_title} metadata.json", os.path.join(path, playlist_title))
        if enum:
            filenamefmt='%(playlist_index)s - %(title)s.%(ext)s'
        else:
            filenamefmt='%(title)s.%(ext)s'

        playlist = {}
        if info_dict['extractor_key'] == "YoutubeTab":
            if format=='mp3':
                ydl_opts = {
                    'outtmpl': os.path.join(path, playlist_title, filenamefmt),
                    'ignoreerrors': True,
                    ##'logger': logger(),
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '256',
                    }],
                }
                if created or overwrite:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                for i in info_dict['entries']:
                    if i == None:
                        continue
                    try:
                        metadata = {'artist': i["artist"], 'album': i["album"], 'track': i["track"], 'album_artist': i['creator']}
                    except:
                        metadata = None
                    filename=(i['title']+'.mp3').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','').replace('*','_')
                    playlist[str(i['playlist_index'])] = {'title': i['title'], 'filename': filename, 'filepath': os.path.join('playlists', playlist_title, filename), 'Metadata': metadata, 'duration': i["duration"]};
                    try:
                        if metadata != None:
                            if metadata["album"] == None: Albumname = playlist_title
                            else: Albumname = metadata["album"]
                            audiofile = eyed3.load(playlist[str(i['playlist_index'])]['filepath'])
                            if audiofile.tag == None:
                                audiofile.initTag(version=(2,3,0))
                            audiofile.tag.artist = metadata["artist"]
                            audiofile.tag.album = Albumname
                            audiofile.tag.album_artist = metadata["artist"]
                            audiofile.tag.title = metadata["track"]
                            audiofile.tag.track_num = i['playlist_index']
                            audiofile.tag.release_date = i["release_year"]
                            audiofile.tag.save()
                            del audiofile
                        else:
                            audiofile = eyed3.load(playlist[str(i['playlist_index'])]['filepath'])
                            if audiofile.tag == None:
                                audiofile.initTag(version=(2,3,0))
                            audiofile.tag.album = info_dict['title']
                            audiofile.tag.title = i['title']
                            audiofile.tag.track_num = i['playlist_index']
                            audiofile.tag.save()
                            del audiofile
                    except:
                        self.log.error('could not write metadata to ', i['title'])
                self.album_art_folder(playlist_title=playlist_title, no_embed=True)
            if format=='flac':
                ydl_opts = {
                    'outtmpl': os.path.join(path, playlist_title, filenamefmt),
                    'format': 'bestaudio/best',
                    'ignoreerrors': True,
                    ##'logger': logger(),
                    'noplaylist': False,
                    # 'extract-audio': True,
                    # 'audio-format': 'flac',
                    # 'audio-quality': '0',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'flac',
                        'preferredquality': '300',
                    }],
                }
                if created or overwrite:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                with open(os.path.join(path, playlist_title,'playlist.txt'), 'w') as file:
                    for i in info_dict['entries']:
                        if i == None:
                            continue
                        try:
                            metadata = {'artist': i["artist"], 'album': i["album"], 'track': i["track"], 'album_artist': i['creator']};
                            textmetadata = i["artist"] +' :: '+ i["album"]+' :: '+ i["track"]+' :: '+i['creator']
                        except:
                            metadata = None
                            textmetadata =  ''+' :: '+ info_dict['title']+' :: '+ i['title']+' :: '
                        filename=(i['title']+'.flac').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','')
                        playlist[str(i['playlist_index'])] = {'title': i['title'], 'filename': filename, 'filepath': os.path.join('playlists', playlist_title, filename), 'Metadata': metadata, 'duration': i["duration"]};
                        file.write(filename+' :: '+str(i['title'])+' :: '+str(i['playlist_index'])+' :: '+textmetadata+'\n')
                with open(os.path.join(path, playlist_title,'playlist.txt'), 'r') as f:
                    sortfile = f.readlines()
                sortfile.sort()
                with open(os.path.join(path, playlist_title,'playlist.txt'), 'w') as f:
                    f.writelines(sortfile)
            else:
                ydl_opts = {
                    'outtmpl': os.path.join(path, playlist_title, filenamefmt),
                    'format': format,
                    'ignoreerrors': True,
                    ##'logger': logger(),
                }
                if created or overwrite:
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])

        if info_dict['extractor'] == "soundcloud:set":
            if format=='mp3':
                ydl_opts = {
                    'outtmpl': os.path.join(path, playlist_title, filenamefmt),
                    'ignoreerrors': True,
                    ##'logger': logger(),
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '256',
                    }],
                }
            else:
                ydl_opts = {
                    'outtmpl': os.path.join(path, playlist_title, filenamefmt),
                    'format': format,
                    'ignoreerrors': True,
                    ##'logger': logger(),
                }
            if created or overwrite:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            for i in info_dict['entries']:
                metadata = {'artist': i["uploader"], 'album': info_dict['title'], 'track': i["title"], 'album_artist': i['uploader']}
                filename=(i['title']+'.mp3').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','')
                playlist[str(i['playlist_index'])] = {'title': i['title'], 'filename': filename, 'filepath': os.path.join('playlists', playlist_title, filename), 'Metadata': metadata, 'duration': i["duration"]};
                try:
                    audiofile = eyed3.load(playlist[str(i['playlist_index'])]['filepath'])
                    if audiofile.tag == None:
                        audiofile.initTag(version=(2,3,0))
                    audiofile.tag.artist = i["uploader"]
                    audiofile.tag.album = info_dict['title']
                    audiofile.tag.album_artist = i["uploader"]
                    audiofile.tag.title = i["title"]
                    audiofile.tag.track_num = i['playlist_index']
                    audiofile.tag.release_date = i["upload_date"]
                    audiofile.tag.save()
                    del audiofile
                except:
                    self.log.error('could not write metadata to ', i['title'])
            self.album_art_folder(playlist_title=playlist_title, no_embed=True)

        if info_dict['extractor_key'] == "BandcampAlbum":
            formats = dict()
            for i in info_dict["entries"]:
                for j in i["formats"]:
                    formats[j["format_id"]] = j["ext"]
            if len(formats) > 1 and askformat:
                print()
            elif len(formats)==1 and askformat:
                format = list(format.keys())[0]
            ydl_opts = {
                'outtmpl': os.path.join(path, playlist_title, filenamefmt),
                'format': format,
                'ignoreerrors': True,
                ##'logger': logger(),
            }
            if created or overwrite:
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            for i in info_dict['entries']:
                if i == None:
                    continue
                if i["artist"] != None: metadata = {'artist': i["artist"], 'album': i["album"], 'track': i["track"], 'album_artist': i["uploader"]};
                else: metadata = None
                filename=(i['title']+'.mp3').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','')
                playlist[str(i['playlist_index'])] = {'title': i['track'], 'filename': filename, 'filepath': os.path.join('playlists', playlist_title, filename), 'Metadata': metadata, 'duration': i["duration"]};
                if metadata["album"] == None:
                    Albumname = playlist_title
                else:
                    Albumname = metadata["album"]
                # try:
                self.dl_file(i['thumbnails'][0]['url'], (i['title']+'.'+i['thumbnails'][0]['url'].split('.')[-1]).replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?',''), os.path.join(path, playlist_title, 'thumbnails'))
                if metadata != None:
                    song = taglib.File(playlist[i]['filepath'])
                    if metadata != None:
                        if not song.get("ARTIST"):
                            self.log.debug(F"REPLACING ARTIST IN { playlist[i]['filepath'] }!! { song.get('ARTIST') } TO { [metadata['artist']] }")
                            song["ARTIST"] = [metadata["artist"]]
                        if not song.get("ALBUM"):
                            self.log.debug(F"REPLACING ALBUM IN { playlist[i]['filepath'] }!! {song.get('ALBUM')} TO {[Albumname]}")
                            song["ALBUM"] = [Albumname]
                        if not song.get("ALBUMARTIST"):
                            self.log.debug(F"REPLACING ALBUMARTIST IN { playlist[i]['filepath'] }!! {song.get('ALBUMARTIST')} TO {[metadata['artist']]}")
                            song["ALBUMARTIST"] = [metadata["artist"]]
                        if not song.get("TITLE"):
                            self.log.debug(F"REPLACING TITLE IN { playlist[i]['filepath'] }!! {song.get('TITLE')} TO {[metadata['track']]}")
                            song["TITLE"] = [metadata["track"]]
                        if not song.get("TRACKNUMBER"):
                            self.log.debug(F"REPLACING TRACKNUMBER IN { playlist[i]['filepath'] }!! {song.get('TRACKNUMBER')} TO {[i['playlist_index']]}")
                            song["TRACKNUMBER"] = [i['playlist_index']]
                    else:
                        if not song.get("ALBUM"):
                            self.log.debug(F"REPLACING ALBUM IN { playlist[i]['filepath'] }!! {song.get('ALBUM')} TO {[playlist_title]}")
                            song["ALBUM"] = [playlist_title]
                        if not song.get("TITLE"):
                            self.log.debug(F"REPLACING TITLE IN { playlist[i]['filepath'] }!! {song.get('TITLE')} TO {[i['track']]}")
                            song["TITLE"] = [i['track']]
                        if not song.get("TRACKNUMBER"):
                            self.log.debug(F"REPLACING TRACKNUMBER IN { playlist[i]['filepath'] }!! {song.get('TRACKNUMBER')} TO {[i['playlist_index']]}")
                            song["TRACKNUMBER"] = [i['playlist_index']]
                    song.save()
                # except:
                #     self.log.error('could not write metadata to '+ i['track'])
        self.dump_json(playlist, F"{playlist_title} playlist.json", os.path.join(path, playlist_title))

    def view_playlist_metadata(self, playlist_title=False, url=False, path='playlists'):
        if not playlist_title and not url: return self.log.error('please pass a url or playlist title')
        if playlist_title and url: return self.log.error('please do not pass both a url and playlist title')
        if url:
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','').replace('*','_')
        if playlist_title:
            try:
                with open(os.path.join(path, playlist_title,  F"{playlist_title} playlist.json"), 'r') as file:
                    playlist = json.load(file)
            except:
                return self.log.error(F"could not find {playlist_title} playlist.json")
            try:
                with open(os.path.join(path, playlist_title, F"{playlist_title} metadata.json"), 'r') as file:
                    info_dict = json.load(file)
            except:
                return self.log.error(F"could not find {playlist_title} metadata.json")
            for i in playlist:
                if playlist[i]["Metadata"]["album"] == None:
                    Albumname = playlist_title
                else:
                    Albumname = playlist[i]["Metadata"]["album"]
                song = taglib.File(playlist[i]['filepath'])
                self.log.info(song.tags)

    def playlist_metadata(self, playlist_title=False, url=False, path='playlists'):
        if not playlist_title and not url: return self.log.error('please pass a url or playlist title')
        if playlist_title and url: return self.log.error('please do not pass both a url and playlist title')
        if url:
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','').replace('*','_')
        if playlist_title:
            try:
                with open(os.path.join(path, playlist_title,  F"{playlist_title} playlist.json"), 'r') as file:
                    playlist = json.load(file)
            except:
                return self.log.error(F"could not find {playlist_title} playlist.json")
            try:
                with open(os.path.join(path, playlist_title, F"{playlist_title} metadata.json"), 'r') as file:
                    info_dict = json.load(file)
            except:
                return self.log.error(F"could not find {playlist_title} metadata.json")
            for i in playlist:
                if playlist[i]["Metadata"]["album"] == None:
                    Albumname = playlist_title
                else:
                    Albumname = playlist[i]["Metadata"]["album"]
                song = taglib.File(playlist[i]['filepath'])
                if playlist[i]["Metadata"] != None:
                    song["ARTIST"] = [playlist[i]["Metadata"]["artist"]]
                    song["ALBUM"] = [Albumname]
                    song["ALBUMARTIST"] = [playlist[i]["Metadata"]["album_artist"]]
                    song["TITLE"] = [playlist[i]["Metadata"]["track"]]
                    song["TRACKNUMBER"] = [i]
                else:
                    song["ALBUM"] = [Albumname]
                    song["TITLE"] = [playlist[i]['title']]
                    song["TRACKNUMBER"] = [i]
                song.save()
                # try:
                #     if playlist[i]["Metadata"] != None:
                #         audiofile = eyed3.load(playlist[i]['filepath'])
                #         audiofile.tag.save(version=(2,3,0))
                #         audiofile = eyed3.load(playlist[i]['filepath'])
                #         audiofile.tag.artist = playlist[i]["Metadata"]["artist"]
                #         audiofile.tag.album = Albumname
                #         audiofile.tag.album_artist = playlist[i]["Metadata"]["album_artist"]
                #         audiofile.tag.title = playlist[i]["Metadata"]["track"]
                #         audiofile.tag.track_num = i
                #         audiofile.tag.save()
                #         del audiofile
                #     else:
                #         audiofile = eyed3.load(playlist[i]['filepath'])
                #         audiofile.tag.save(version=(2,3,0))
                #         audiofile = eyed3.load(playlist[i]['filepath'])
                #         audiofile.tag.album = playlist_title
                #         audiofile.tag.title = playlist[i]['title']
                #         audiofile.tag.track_num = i
                #         audiofile.tag.save()
                #         del audiofile
                # except:
                #     self.log.error('could not write metadata to '+ playlist[i]['title'])
        # self.album_art_folder(os.path.join(path, playlist_title))
