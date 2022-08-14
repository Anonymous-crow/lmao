#from future import unicode_literals
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import logging, random, time, base64, json, youtube_dl, pafy, threading, pygame, eyed3, asyncio, twitchio as tio, shutil, sys

def install_dependencies():
    os.system('python -m pip install -U windows-curses pyunpack mutagen get_cover_art patool pygame gtts curses-menu playsound youtube-dl pafy pyglet opencv-python emoji python-dotenv twitchio eyed3 --user')

def sec_t_timestamp(sec):
    import time
    ty_res = time.gmtime(sec)
    if sec < 3600:
        res = time.strftime("%M:%S",ty_res)
    else:
        res = time.strftime("%H:%M:%S",ty_res)
    return res

def clear():
    if os.name == 'nt': _ = os.system('cls')
    else: _ = os.system('clear')
url = 'https://www.youtube.com/watch?v=BqnG_Ei35JE'

class logger():
    """a simple logger for youtube_dl."""

    def debug(self, msg):
        print(msg)

    def warning(self, msg):
        print(msg)

    def error(self, msg):
        print(msg)

logging.basicConfig(filename="info.log", level=logging.INFO)

def b64_encode_img(imgpth):
    return base64.b64encode(open(imgpth, 'rb').read()).decode('utf-8')

def b64_decode_img(imgencoded, filepath=False):
    decoded_image_data = base64.decodebytes(imgencoded.encode('utf-8'))
    if not filepath:
        return decoded_image_data
    else:
        with open(filepath, 'wb') as file_to_save:
            file_to_save.write(decoded_image_data)

def b64_encode(text):
    return base64.b64encode(text.encode('ascii')).decode('ascii')

def b64_decode(text):
    return base64.b64decode(text.encode('ascii')).decode('ascii')

def downloadfile_curl(url = "https://raw.githubusercontent.com/Anonymous-crow/Disarray/master/image%5B1%5D.png", filename=False, overwrite=False, path='downloads'):
        if not filename:
            if not os.path.isdir(path): os.makedirs(path)
            os.system('cd '+path+'&& curl -OL ' + url + ' --ssl-no-revoke && cd '+ os.path.dirname(os.path.abspath(__file__))); clear();
        else:
            if not os.path.isdir(path): os.makedirs(path)
            if overwrite: os.system('curl ' + url + ' -L --output ' + os.path.join(path, filename)+' --ssl-no-revoke'); clear();
            else:
                while True:
                    if not os.path.isfile(os.path.join(path, filename)): os.system('curl ' + url + ' -L --output ' + os.path.join(path, filename)+' --ssl-no-revoke'); clear(); break
                    else: filename = filename.split('.')[0] + '(1).' + filename.split('.')[1]

def dl_file(url, filename='', path=''):
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

def install_ffmpeg():
    if not os.path.isfile('7za.exe'):
        dl_file(url='https://www.7-zip.org/a/7z1900-extra.7z',path=os.path.join('resources','7z'),filename='7z1900-extra.7z')
        logging.info('downloaded 7z1900-extra.7z')
        import py7zr
        #if not os.path.isdir(os.path.join("resources","7z","7z1900-extra")): os.mkdir(os.path.join("resources","7z","7z1900-extra"))
        try:
            archive = py7zr.SevenZipFile(os.path.join('resources','7z','7z1900-extra.7z'), mode='r')
            archive.extractall(path=os.path.join("resources","7z","7z1900-extra"))
            archive.close()
        except:
            print('could not extract 7z1900-extra')
        try:
            shutil.copyfile(os.path.join("resources","7z","7z1900-extra","7za.exe"), '7za.exe')
        except:
            try:
                dl_file(url='https://crow.epicgamer.org/assets/7za.exe')
            except:
                return -1
        logging.info('copied 7za.exe')
    dl_file(url='https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-full.7z', filename='ffmpeg-release-full.7z',path=os.path.join('resources','ffmpeg'))
    os.system('7za x '+os.path.join('resources','ffmpeg','ffmpeg-release-full.7z')+' -aoa '+os.path.join('resources','ffmpeg'))
    if not os.path.isfile('ffmpeg.exe'):
        for i in os.listdir(os.path.join("resources","ffmpeg")):
            print(i)
            if os.path.isdir(os.path.join("resources","ffmpeg", i)):
                ffmpegdir=i
        shutil.copyfile(os.path.join("resources","ffmpeg",ffmpegdir,"bin","ffmpeg.exe"), 'ffmpeg.exe')
        logging.info('copied ffmpeg.exe')


def infoget(url):
    ydl_opts = {
    'logger': logger(),
    'ignoreerrors': True
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    if not os.path.isdir('downloads'):
        os.mkdir('downloads')
    with open(os.path.join('downloads', info_dict["title"]+' metadata.json'), 'w') as file:
        json.dump(info_dict, file, indent=4, separators=(',', ': '))
    print(info_dict)

def music_playlist_player(playlist_title=False, url=False, path='playlists', askshuffle=True):
    import curses, traceback
    pygame.mixer.init()
    if not playlist_title and not url:
        return print('please pass a url or playlist title')
    if playlist_title and url:
        return print('please do not pass both a url and playlist title')
    if url:
        ydl_opts = {'logger': logger()}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
    if playlist_title:
        if not os.path.isdir(os.path.join(path, playlist_title)):
            return print('folder '+playlist_title+' does not exist')
        with open(os.path.join(path, playlist_title, playlist_title + ' playlist.json'), 'r') as file:
            playlist = json.load(file)


        lmao = 1
        if askshuffle:
            import MenuLibrary as ML
            shufflemenu = ML.makemenu(['Yes', 'No', 'Cancel'],'Shuffle Playlist?')
            if shufflemenu == 'Yes': shuffled = True
            elif shufflemenu == 'No': shuffled = False
            elif shufflemenu == 'Cancel': return 0
        else:
            shuffled = False
        # while True:
        #     resp = input(" shuffle playlist?[y]\n")
        #     if resp == 'y' or resp == '': shuffled = True; break
        #     elif resp == 'n': shuffled = False; break

        try:
            # -- Initialize --
            vol=0.5
            stdscr = curses.initscr()   # initialize curses screen
            x_w, y_w = stdscr.getmaxyx()
            curses.noecho()             # turn off auto echoing of keypress on to screen
            curses.cbreak()             # enter break mode where pressing Enter key
                                        #  after keystroke is not required for it to register
            stdscr.keypad(1)            # enable special Key values such as curses.KEY_LEFT etc
            stdscr.nodelay(True)
        except:
            traceback.print_exc()     # print trace back log of the error
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            return print('error initalising curses')
        songlist=[]
        history=[]
        for i in playlist:
            songlist.append(str(i))
        if shuffled: random.shuffle(songlist)
        while len(songlist) > 0:
            i = songlist.pop(0); history.append(i)
            filename = playlist[i]['filename'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
            title = playlist[i]['title']; legnth_s=playlist[i]['duration']; legnth=sec_t_timestamp(legnth_s)
            if playlist[i]['Metadata'] != None:
                title = playlist[i]['Metadata']['track'] + ' by ' + playlist[i]['Metadata']['artist']

            ##try:
            if lmao:
                pygame.mixer.music.load(os.path.join(path, playlist_title, filename))
                pygame.mixer.music.set_volume(vol)
                pygame.mixer.music.play()
            ##except:
                ##print('There was a problem playing '+title)
            y_w, x_w = stdscr.getmaxyx()
            nopwin = curses.newwin(int(y_w)-3,int(x_w/2)+2)
            playwin = curses.newwin(int(y_w)-3,0,0,int(x_w/2)+2)
            ctrlwin = curses.newwin( 3, 0, int(y_w)-3, 0)
            paused=False; song_playing=True
            while song_playing and lmao:
                stdscr.clear()
                # stay in this loop till the user presses 'q'
                songpos = pygame.mixer.music.get_pos()/1000
                y_wv, x_wv = stdscr.getmaxyx()
                # if not y_wv == y_w or not x_wv == x_w:
                #     y_w = y_wv; x_w = x_wv
                nopwin = curses.newwin(int(y_w)-3,int(x_w/2)+2)
                playwin = curses.newwin(int(y_w)-3,0,0,int(x_w/2)+2)
                ctrlwin = curses.newwin( 3, 0, int(y_w)-3, 0)
                nopwin.clear()
                playwin.clear()
                ctrlwin.clear()
                nopwin.box()
                playwin.box()
                ctrlwin.box()
                lne = 0
                for j in playlist:
                    lne +=1
                    if j == i:
                        np = '*'
                    else:
                        np = ' '
                    try:
                        if playlist[j]["Metadata"] != None:
                            playwin.addstr(lne, 1, np+j+'. '+playlist[j]["Metadata"]["track"], curses.A_NORMAL)
                        else:
                            playwin.addstr(lne, 1, np+j+'. '+playlist[j]["title"], curses.A_NORMAL)
                    except:
                        pass
                nopwin.addstr(1, 2, 'Now Playing Playlist '+playlist_title, curses.A_BOLD)
                nopwin.addstr(2, 2, 'Now Playing Song '+i+':', curses.A_NORMAL)
                nopwin.addstr(3, 2, title, curses.A_NORMAL)
                nopwin.addstr(4, 2, sec_t_timestamp(songpos)+'----'+legnth, curses.A_NORMAL)
                nopwin.addstr(5, 2, 'volume: '+str(int(vol*100))+'%', curses.A_NORMAL)
                if shuffled:
                    shufflestatus = 'ON'
                if not shuffled:
                    shufflestatus = 'OFF'
                # ctrlwin.addstr(1, 1, 'Press q to quit, s to skip, a to go back one song, o to pause, p to play, e to toggle shuffle (shuffle is '+shufflestatus+')', curses.A_NORMAL)
                try:
                    ctrlwin.addstr(1, 1, 'Press q to quit, s to skip, a to go back one song, o to pause, p to play, e to toggle shuffle (shuffle is '+shufflestatus+')', curses.A_NORMAL)
                except:
                    ctrlwin.addstr(1, 1, 'q, s, a, o, p, e, '+shufflestatus, curses.A_NORMAL)

                # # nopwin.addstr(int(x_w-1), 1, 'Press q to quit, s to skip, a to go back one song, o to pause, p to play, e to toggle shuffle (shuffle is '+shufflestatus+')', curses.A_NORMAL)
                ch = stdscr.getch()
                if ch == ord('q'):
                    pygame.mixer.music.stop()
                    lmao=0
                    break
                if ch == ord('s'): pygame.mixer.music.stop(); break
                if ch == ord('a'):
                    if len(history) == 1: songlist.insert(0, history.pop(-1)); break
                    if len(history) >= 2: songlist.insert(0, history.pop(-1)); songlist.insert(0, history.pop(-1)); break
                if ch == ord('p'): pygame.mixer.music.unpause(); paused=False
                if ch == ord('o'): pygame.mixer.music.pause(); paused=True
                if ch == ord('.'): pygame.mixer.music.unpause(); paused=False
                if ch == ord(','): pygame.mixer.music.pause(); paused=True
                if ch == ord('w'): pygame.mixer.music.set_pos(180)
                if ch == ord('e'):
                    if shuffled: shuffled = False; songlist.sort(key = lambda k: int(k)); print(songlist)
                    elif not shuffled: shuffled = True; random.shuffle(songlist); print(songlist)
                if ch == curses.KEY_UP:
                    if vol<1: vol+=0.1
                    pygame.mixer.music.set_volume(vol)
                if ch == curses.KEY_DOWN:
                    if vol>0: vol-=0.1
                    pygame.mixer.music.set_volume(vol)
                if not pygame.mixer.music.get_busy() and not paused:
                    song_playing=False
                else:
                    song_playing=True
                nopwin.refresh()
                playwin.refresh()
                ctrlwin.refresh()
                time.sleep(0.1)
                stdscr.refresh()

        # --- Cleanup on exit ---
        pygame.mixer.music.stop()
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

def music_playlist_player_menu(path='playlists', askshuffle=True):
    path2 = path
    while True:
        Playlists = os.listdir(path2); Playlists.append('Download New Playlist'); Playlists.append('..'); Playlists.append('Cancel')
        import MenuLibrary as ML
        playlist_title = ML.makemenu(Playlists)
        if playlist_title == 'Cancel':
            return 0
        if playlist_title == 'Download New Playlist':
            yt_playlist_mp3_menu()
        if playlist_title == '..':
            path2 = os.path.join(path2, '..')
        elif os.path.isdir(os.path.join(path2, playlist_title)):
            # if os.path.isfile(os.path.join(path2, playlist_title, playlist_title+' playlist.json')):
            if os.path.isfile(os.path.join(path2, playlist_title, playlist_title+' playlist.json')):
                music_playlist_player(playlist_title=playlist_title, path=path2, askshuffle=askshuffle)
                continue
            else:
                path2 = os.path.join(path2, playlist_title)
    # Playlists = os.listdir(path); Playlists.append('Download New Playlist'); Playlists.append('Cancel')
    # import MenuLibrary as ML
    # playlist_title = ML.makemenu(Playlists)
    # if playlist_title == 'Download New Playlist':
    #     yt_playlist_mp3_menu()
    # if playlist_title == 'Cancel':
    #     return 0
    # else:
    #     music_playlist_player(playlist_title=playlist_title, path=path, askshuffle=askshuffle)


def music_player(path='download',filename=False, url=False):
    import curses, traceback
    pygame.mixer.init()


    if not filename and not url:
        return print('please pass a url or filepath')
    if filename and url:
        return print('please do not pass both a url and filepath')
    if url:
        ydl_opts = {'logger': logger()}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            song_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
            filename = song_title+'.mp3'
    if filename:
        if not os.path.isfile(os.path.join(path, filename)):
            return print(filename+' does not exist in downloads')
        lmao = 1
        try:
            # -- Initialize --
            stdscr = curses.initscr()   # initialize curses screen
            x_w, y_w = stdscr.getmaxyx()
            curses.noecho()             # turn off auto echoing of keypress on to screen
            curses.cbreak()             # enter break mode where pressing Enter key
            vol = 0.5
            paused=False                            #  after keystroke is not required for it to register
            stdscr.keypad(1)            # enable special Key values such as curses.KEY_LEFT etc
            stdscr.nodelay(True)
        except:
            traceback.print_exc()     # print trace back log of the error
            stdscr.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()
            return print('error initalising curses')
        try:
            pygame.mixer.music.load(os.path.join(path, filename))
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play()
        except:
            print('There was a problem playing '+filename.split('.')[0])
        while lmao:
            # stay in this loop till the user presses 'q'
            songpos = pygame.mixer.music.get_pos()/1000
            x_w, y_w = stdscr.getmaxyx()
            stdscr.clear()
            stdscr.border(0)
            stdscr.addstr(1, 1, 'Now Playing Song: '+filename.split('.')[0], curses.A_NORMAL)
            stdscr.addstr(2, 1, sec_t_timestamp(songpos), curses.A_NORMAL)
            stdscr.addstr(3, 2, 'volume: '+str(int(vol*100))+'%', curses.A_NORMAL)
            stdscr.addstr(int(x_w-1), 1, 'Press q to quit, o to pause, p to play', curses.A_NORMAL)
            ch = stdscr.getch()
            if ch == ord('q'): pygame.mixer.music.stop(); break
            if ch == ord('s'): pygame.mixer.music.stop(); break
            if ch == ord('p'): pygame.mixer.music.unpause(); paused=False
            if ch == ord('o'): pygame.mixer.music.pause(); paused=True
            if ch == ord('.'): pygame.mixer.music.unpause(); paused=False
            if ch == ord(','): pygame.mixer.music.pause(); paused=True
            if ch == ord('w'): pygame.mixer.music.set_pos(180)
            if ch == curses.KEY_UP:
                if vol<1: vol+=0.1
                pygame.mixer.music.set_volume(vol)
            if ch == curses.KEY_DOWN:
                if vol>0: vol-=0.1
                pygame.mixer.music.set_volume(vol)
            stdscr.refresh()
            if not pygame.mixer.music.get_busy() and not paused:
                lmao=0

        # --- Cleanup on exit ---
        pygame.mixer.music.stop()
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()

def music_player_menu(path='playlists'):
    path2 = path
    while True:
        Playlists = os.listdir(path2); Playlists.append('..'); Playlists.append('Cancel')
        import MenuLibrary as ML
        playlist_title = ML.makemenu(Playlists)
        if playlist_title == 'Cancel':
            break
        if playlist_title == '..':
            path2 = os.path.join(path2, '..')
        elif os.path.isdir(os.path.join(path2, playlist_title)):
            path2 = os.path.join(path2, playlist_title)
        else:
            music_player(filename=playlist_title, path=path2)


def cli_play_playlist(path='playlists', playlist_title=False, url=False):
    clear()
    pygame.mixer.init()
    if not playlist_title and not url:
        return print('please pass a url or playlist title')
    if playlist_title and url:
        return print('please do not pass both a url and playlist title')
    if url:
        ydl_opts = {'logger': logger()}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
    if playlist_title:
        if not os.path.isdir(os.path.join(path, playlist_title)):
            return print('folder '+playlist_title+' does not exist')
        with open(os.path.join(path, playlist_title, playlist_title + ' playlist.json'), 'r') as file:
            playlist = json.load(file)
        print('Now Playing: '+playlist_title)
        lmao = True
        for i in playlist:
            filename = playlist[i]['filename'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
            title = playlist[i]['title']; legnth_s=playlist[i]['duration']; legnth=sec_t_timestamp(legnth_s)
            if playlist[i]["Metadata"] != None:
                title = playlist[i]['title'] + ' by ' + playlist[i]["Metadata"]["artist"]
            clear()
# --------------------------Path of your music
            try:
                if lmao:
                    pygame.mixer.music.load(os.path.join(path, playlist_title, filename))
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play()
                busy = 1;

                while busy and lmao:
                    busy = pygame.mixer.music.get_busy()
                    print('Now Playing Playlist: '+playlist_title)
                    print('Now Playing: ' + title)
                    print("Press 'p' to pause")
                    print("Press 'r' to resume")
                    print("Press 'v' set volume")
                    print("Press 's' to skip")
                    print("Press 'e' to exit")
                    ch = input("['p','r','v','s','e']>>>")
                    busy = pygame.mixer.music.get_busy()
                    clear()
                    if ch == "p":
                        pygame.mixer.music.pause()
                    elif ch == "r":
                        pygame.mixer.music.unpause()
                    elif ch == "v":
                        v = float(input("Enter volume(0 to 1): "))
                        pygame.mixer.music.set_volume(v)
                        clear()
                    elif ch == "s":
                        pygame.mixer.music.stop()
                        break
                    elif ch == "e":
                        pygame.mixer.music.stop()
                        lmao = False
                        break
                    elif ch == "w":
                        pygame.mixer.music.set_pos(200)
                    elif ch == "q":
                        print(pygame.mixer.music.get_pos())
                        print(pygame.mixer.music.get_busy())
            except:
                print('there was an issue playing '+playlist[i][0])

def execute_cmc(command):
    import subprocess
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    # Poll process for new output until finished
    #while True:
    nextline = process.stdout.readline()
    # if nextline == '' and process.poll() != None:
    #     pass
    sys.stdout.write(nextline.decode('utf-8'))
    #sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return str(output).strip("\n","b''")
    else:
        raise ProcessException(command, exitCode, output)

def album_art_folder(playlist_title=False, url=False, path='playlists', force=True, no_embed=False):
    if not playlist_title and not url: return print('please pass a url or playlist title')
    if playlist_title and url: return print('please do not pass both a url and playlist title')
    if url:
        ydl_opts = {'ignoreerrors': True}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
    if playlist_title:
        import get_cover_art
        coverdict={'inline':True, 'verbose':True}
        if force:
            coverdict['force']=True
        if no_embed:
            coverdict['no_embed']=True
        finder = get_cover_art.CoverFinder(coverdict)
        finder.scan_folder(os.path.join(path, playlist_title))

def yt_playlist_mp3(url, autoplay=False, overwrite=False, Truecli=False, path='playlists', format='mp3', enum=False, login=False, passwd=False):
    created = False
    if not os.path.isfile('ffmpeg.exe'):
        install_ffmpeg()
    ydl_opts = {
    'logger': logger(),
    'ignoreerrors': True,
    'verbose': True
    }
    if login:
        ydl_opts.update({"username": login, "password": passwd})
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    try:
        playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').translate({ord(i): ' ' for i in "<>:\"/\\|?*"})
    except:
        playlist_title = info_dict['id']
    if not os.path.isdir(os.path.join(path, playlist_title)):
        created = True
        if not os.path.isdir(path):
            os.mkdir(path)
        os.mkdir(os.path.join(path, playlist_title))
    with open(os.path.join(path, playlist_title, playlist_title + ' metadata.json'), 'w') as file:
        json.dump(info_dict, file, indent=4, separators=(',', ': '))
    if enum:
        filename='%(playlist_index)s - %(title)s.%(ext)s'
    if format == 'mp3':
        ydl_opts = {
            'outtmpl': os.path.join(path, playlist_title, '%(title)s.%(ext)s'),
            'nooverwrites': overwrite,
            'ignoreerrors': True,
            'embed-thumbnail': True,
            'add-metadata': True,
            ##'logger': logger(),
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
        }
    elif format=='flac':
        ydl_opts = {
            'outtmpl': os.path.join(path, playlist_title, '%(title)s.%(ext)s'),
            'format': 'bestaudio/best',
            'embed-thumbnail': True,
            'add-metadata': True,
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
    else:
        ydl_opts = {
            'outtmpl': os.path.join(path, playlist_title, '%(title)s.%(ext)s'),
            'format': format,
            'embed-thumbnail': True,
            'add-metadata': True,
            'ignoreerrors': True,
            ##'logger': logger(),
        }
    if login:
        ydl_opts.update({"username": login, "password": passwd})
    if created:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    else:
        if overwrite:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    playlist = {}
    if info_dict['extractor_key'] == "YoutubeTab":
        if format=='mp3':
            for i in info_dict['entries']:
                if i == None:
                    continue
                try:
                    metadata = {'artist': i["artist"], 'album': i["album"], 'track': i["track"], 'album_artist': i['creator']}; #print(i['creator'].split(','))
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
                    print('could not write metadata to ', i['title'])
        if format=='flac':
            with open(os.path.join(path, playlist_title,'playlist.txt'), 'w') as file:
                for i in info_dict['entries']:
                    if i == None:
                        continue
                    try:
                        metadata = {'artist': i["artist"], 'album': i["album"], 'track': i["track"], 'album_artist': i['creator']};
                        textmetadata = i["artist"] +' :: '+ i["album"]+' :: '+ i["track"]+' :: '+i['creator'] #print(i['creator'].split(','))
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
        album_art_folder(playlist_title=playlist_title, no_embed=True)
    if info_dict['extractor'] == "soundcloud:set":
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
                print('could not write metadata to ', i['title'])
        album_art_folder(playlist_title=playlist_title, no_embed=True)
    if info_dict['extractor_key'] == "BandcampAlbum":
        for i in info_dict['entries']:
            if i == None:
                continue
            if i["artist"] != None: metadata = {'artist': i["artist"], 'album': i["album"], 'track': i["track"], 'album_artist': i["uploader"]};
            else: metadata = None
            filename=(i['title']+'.mp3').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','')
            playlist[str(i['playlist_index'])] = {'title': i['track'], 'filename': filename, 'filepath': os.path.join('playlists', playlist_title, filename), 'Metadata': metadata, 'duration': i["duration"]};
            # print(playlist[i]["Metadata"], playlist[i]["filepath"])
            if metadata["album"] == None:
                Albumname = playlist_title
            else:
                Albumname = metadata["album"]
            try:
                dl_file(i['thumbnails'][0]['url'], (i['title']+'.'+i['thumbnails'][0]['url'].split('.')[-1]).replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?',''), os.path.join(path, playlist_title, 'thumbnails'))
                if metadata != None:
                    audiofile = eyed3.load(os.path.join('playlists', playlist_title, filename))
                    print(audiofile.tag)
                    if audiofile.tag == None:
                        audiofile.initTag(version=(2,3,0))
                        print(audiofile.tag)
                        # audiofile = eyed3.load(os.path.join('playlists', playlist_title, filename))
                        if metadata != None:
                            audiofile.tag.artist = metadata["artist"]
                            audiofile.tag.album = Albumname
                            audiofile.tag.album_artist = metadata["artist"]
                            audiofile.tag.title = metadata["track"]
                            audiofile.tag.track_num = i['playlist_index']
                            audiofile.tag.save()
                            del audiofile
                        else:
                            audiofile.tag.album = playlist_title
                            audiofile.tag.title = i['track']
                            audiofile.tag.track_num = i['playlist_index']
                            audiofile.tag.save()
                            del audiofile
            except:
                logging.error('could not write metadata to '+ i['track'])
    with open(os.path.join(path, playlist_title, playlist_title + ' playlist.json'), 'w') as file:
        json.dump(playlist, file, indent=4, separators=(',', ': '))
    if autoplay:
        if Truecli: cli_play_playlist(path=path, playlist_title=playlist_title)
        else: music_playlist_player(path=path, playlist_title=playlist_title, askshuffle=False)

def yt_playlist_mp3_menu(lmao=''):
    path = 'playlists'; autoplay = True; overwrite = False
    url = input('Enter URL of file: '); path = input('input file path[playlists]: '); autoplay = input('Autoplay?[y]: '); overwrite = input('Overwrite?[n]: ')
    if path == '': path = 'playlists'
    if autoplay == '': autoplay = True
    if autoplay == 'y': autoplay = True
    if autoplay == 'n': autoplay = False
    if overwrite == '': overwrite = False
    if overwrite == 'y': overwrite = True
    if overwrite == 'n': overwrite = False
    yt_playlist_mp3(url, path=path, autoplay=autoplay, overwrite=overwrite)

def playlist_metadata(playlist_title=False, url=False, path='playlists'):
    if not playlist_title and not url: return print('please pass a url or playlist title')
    if playlist_title and url: return print('please do not pass both a url and playlist title')
    if url:
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_').replace('|', '_').replace('//','_').replace('/','_').replace('?','').replace('*','_')
    if playlist_title:
        with open(os.path.join(path, playlist_title, playlist_title + ' playlist.json'), 'r') as file:
            playlist = json.load(file)
        with open(os.path.join(path, playlist_title, playlist_title + ' metadata.json'), 'r') as file:
            info_dict = json.load(file)
        for i in playlist:
            # print(playlist[i]["Metadata"], playlist[i]["filepath"])
            if playlist[i]["Metadata"]["album"] == None:
                Albumname = playlist_title
            else:
                Albumname = playlist[i]["Metadata"]["album"]
            try:
                if playlist[i]["Metadata"] != None:
                    audiofile = eyed3.load(playlist[i]['filepath'])
                    audiofile.tag.save(version=(2,3,0))
                    audiofile = eyed3.load(playlist[i]['filepath'])
                    audiofile.tag.artist = playlist[i]["Metadata"]["artist"]
                    audiofile.tag.album = Albumname
                    audiofile.tag.album_artist = playlist[i]["Metadata"]["album_artist"]
                    audiofile.tag.title = playlist[i]["Metadata"]["track"]
                    audiofile.tag.track_num = i
                    audiofile.tag.save()
                    del audiofile
                else:
                    audiofile = eyed3.load(playlist[i]['filepath'])
                    audiofile.tag.save(version=(2,3,0))
                    audiofile = eyed3.load(playlist[i]['filepath'])
                    audiofile.tag.album = playlist_title
                    audiofile.tag.title = playlist[i]['title']
                    audiofile.tag.track_num = i
                    audiofile.tag.save()
                    del audiofile
            except:
                logging.error('could not write metadata to'+ playlist[i]['title'])
        import get_cover_art
        finder = get_cover_art.CoverFinder({'inline':True, 'verbose':True, 'force':False})
        finder.scan_folder(os.path.join(path, playlist_title))


def yt_mp3(url, path='downloads', autoplay=True, format='mp3'):
    from playsound import playsound;
    if not os.path.isfile('ffmpeg.exe'):
        try:
            install_ffmpeg()
        except:
            return print("could not download ffmpeg.exe")
    ydl_opts={}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title=info_dict['title'].replace(':', ' -')
    filename = video_title + "." + format
    if format=='mp3':
        if not os.path.isdir(path): os.makedirs(path)
        if not os.path.isfile(os.path.join(path, filename)):
            ydl_opts = {
                'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
                'format': 'bestaudio/best',
                'embed-thumbnail': True,
                'add-metadata': True,
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
                'embed-thumbnail': True,
                'add-metadata': True,
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
            print('file already exists')
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

def yt_mp3_menu(lmao=''):
    path = 'downloads'; autoplay = True
    url = input('Enter URL of file: '); path = input('input file path[downloads]: '); autoplay = input('Autoplay? [y]: ')
    if path == '': path = 'downloads'
    if autoplay == '': autoplay = True;
    if autoplay == 'y': autoplay = True
    if autoplay == 'n': autoplay = False
    yt_mp3(url, path, autoplay)

def install_chromium():
    import zipfile
    if not os.path.isdir('resources'):
        os.mkdir('resources')
    if not os.path.isdir('resources\\chromium'):
        os.mkdir('resources\\chromium')
        if os.name == 'nt':
            os.system('cd resources\\chromium && curl -O https://commondatastorage.googleapis.com/chromium-browser-snapshots/Win_x64/813604/chrome-win.zip --ssl-no-revoke')
        if os.name == 'nt':
            with zipfile.ZipFile('resources\\chromium\\chrome-win.zip', 'r') as zip_ref:
                zip_ref.extractall('resources\\chromium')
            os.remove("resources\\chromium\\chrome-win.zip")
        if os.name == 'posix':
            os.system('cd resources\\chromium && curl -O https://commondatastorage.googleapis.com/chromium-browser-snapshots/Linux_x64/813606/chrome-linux.zip --ssl-no-revoke')
        if os.name == 'posix':
            with zipfile.ZipFile(os.path.join('resources','chromium','chrome-linux.zip'), 'r') as zip_ref:
                zip_ref.extractall(os.path.join('resources','chromium'))
            os.remove(os.path.join("resources","chromium","chrome-linux.zip"))

def install_mpv():
    if not os.path.isfile('resources\\mpv\\mpv.exe'):
        dl_file(url='https://pilotfiber.dl.sourceforge.net/project/mpv-player-windows/bootstrapper.zip', path=os.path.join('resources', 'mpv'),filename='bootstrapper.zip')
        import zipfile
        with zipfile.ZipFile(os.path.join('resources', 'mpv','bootstrapper.zip'), 'r') as zip_ref:
            zip_ref.extractall(os.path.join('resources', 'mpv'))
        os.system(os.path.join('resources', 'mpv','updater.bat /WAIT'))


def yt_live(url, autoplay=True, MPV=True, chromechat=False):
    from playsound import playsound; import sys
    if not os.path.isfile('ffmpeg.exe'):
        install_ffmpeg()
    install_chromium()
    ydl_opts={}
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
    except:
        return print(url.split('/')[3]+' is offline or cant be accessed')
    with open(os.path.join('downloads', url.split('/')[3] + ' metadata.json'), 'w') as file:
        json.dump(info_dict, file, indent=4, separators=(',', ': '))
    if autoplay:
        if MPV:
            if chromechat:
                if os.name == 'nt':
                    if info_dict["extractor"]=='twitch:stream':
                        os.system('start resources\\chromium\\chrome-win\\chrome.exe --app=https://www.twitch.tv/popout/'+info_dict['webpage_url_basename']+'/chat?popout=')
                if os.name == 'posix':
                    if info_dict["extractor"]=='twitch:stream':
                        os.system('start resources/chromium/chrome-linux/chrome --app=https://www.twitch.tv/popout/'+info_dict['webpage_url_basename']+'/chat?popout=')
            if os.name == 'nt':
                install_mpv()
                os.system('start resources\\mpv\\mpv.exe '+info_dict["url"])
            else:
                os.system('mpv '+info_dict["url"])
            if not chromechat:
                os.system('start python3 lmao.py --sendtwitchchat channel='+info_dict['webpage_url_basename'])
                import twitchbot
                bot = twitchbot.Bot([info_dict['webpage_url_basename']])
                bot.run()
        if not MPV:
            os.system('start chrome --app='+info_dict['webpage_url'])

def sendtwitchchat(channel):
    import Chatlogger
    Chatlogger.chatmain(channel)

def yt_live_menu():
    autoplay = True; MPV=True; chromechat=False; url=None
    url = input('Enter URL of livestream: '); MPV = input('MPV?[y]: '); chromechat = input('Chromechat?[n]: '); autoplay = input('Autoplay?[y]: ')
    if autoplay == '': autoplay = True
    elif autoplay == 'y': autoplay = True
    elif autoplay == 'n': autoplay = False
    if MPV == '': MPV = True
    elif MPV == 'y': MPV = True
    elif MPV == 'n': MPV = False
    if chromechat == '': chromechat = False
    elif chromechat == 'y': chromechat = True
    elif chromechat == 'n': chromechat = False
    yt_live(url, autoplay, MPV, chromechat)

def Followinge(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    yes=True
    client = tio.client.Client()
    while yes:
        following = asyncio.run(client.get_following(user_id=info_dict['display_id']))
        print(following)

def parseimages(folder = '\\'):
    if not os.path.isdir(folder + '/'): return None
    import cv2
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None: images.append(filename)
    if len(images) == 0: return None
    else: return images

def parseimages_dict(folder = '\\'):
    if not os.path.isdir(folder + '/'): return None
    import cv2; images = {}
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename))
        if img is not None: images[str(filename.split('.')[0])]=os.path.join(folder,filename)
    if len(images) == 0: return None
    else: return images




def tts(lmao = 'lmao'):
    from gtts import gTTS; from playsound import playsound
    if lmao == '': lmao = 'lmao'
    tts = gTTS(text = lmao, lang = 'en'); tts.save("TTS.mp3"); playsound("TTS.mp3"); os.remove("TTS.mp3")
def yanderesim():
    import random as cock, time as dio
    clear()
    x = ['sixty nine','four twenty','666','cum','tiddies lol','please','weed','Creep by','by LMFAO','verb noun','bro','gayve strider dick rider','society','gamer','m i n o r i t i e s','Cum Univeristy'] #cum haha
    while len(x) > 1:
        z = cock.randint(0,len(x)-1);p = cock.randint(0,len(x)-1); newstring = x[z]+' '+x[p]; print(newstring); tts(newstring)
def consoleTTS():
    while True:
        lmao = input('\n');
        if lmao == 'exit': break
        else: tts(lmao)
def typetext():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame, time, random
    pygame.init(); pygame.display.set_caption('tts machine');
    screen = pygame.display.set_mode((640, 240), pygame.RESIZABLE); text = 'type something and press enter'; font = pygame.font.SysFont(None, 48); img = font.render(text, True, (0, 0, 0)); rect = img.get_rect(); rect.topleft = (20, 20); cursor = pygame.Rect(rect.topright, (3, rect.height))
    images = parseimages('downloads'); imgnames = []; imgpath = [];
    if images is not None:
        randimg = random.randint(0, len(images)-1)
        for i in images:
            imgnames.append(i.split('.')[0]); imgpath.append(os.path.join('downloads',i))
        lmao2 = pygame.image.load(imgpath[randimg]); pygame.display.set_icon(lmao2)
        lmao2 = pygame.transform.scale(lmao2, (640, 240))
    bksp = 0; bkspcnt = 0
    lmao = True
    while lmao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: lmao = False; break
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if images is not None:
                    lmao2 = pygame.image.load(imgpath[randimg]); lmao2 = pygame.transform.scale(lmao2, (event.w, event.h))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: lmao = False; break
                if images is not None:
                    if event.key == pygame.K_SPACE: randimg = random.randint(0, len(images)-1); lmao2 = pygame.image.load(imgpath[randimg]); lmao2 = pygame.transform.scale(lmao2, screen.get_size())
                if event.key == pygame.K_RETURN: img = font.render(text, True, (255, 0, 0)); screen.blit(img, rect); pygame.display.update(); tts(text)
                if event.key == pygame.K_BACKSPACE: bksp = 1; text = text[:-1]; bkspt0 = time.time()
                else:
                    if event.key != pygame.K_RETURN: text += event.unicode
                img = font.render(text, True, (0, 0, 0))
                rect.size=img.get_size()
                cursor.topleft = rect.topright
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE: bksp = 0; bkspt0 = 0; bkspcnt = 0; rect.size=img.get_size(); cursor.topleft = rect.topright
        if bksp:
            if time.time()-bkspt0 > 0.5:
                bkspcnt += 1
                if bkspcnt > 15: bkspcnt = 0; text = text[:-1]; img = font.render(text, True, (0, 0, 0)); rect.size=img.get_size(); cursor.topleft = rect.topright; pygame.draw.rect(screen, (0, 0, 0), cursor); screen.blit(img, rect); pygame.display.update()
        screen.fill((255, 255, 255))
        if images is not None:
            screen.blit(lmao2, (0,0))
            #for i in imgpath:
                #screen.blit(pygame.image.load(i), (0,0))
        screen.blit(img, rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, (0, 0, 0), cursor)
        pygame.display.update()
    pygame.quit()

def typetext2():
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
    import pygame, time, random
    pygame.init(); pygame.display.set_caption('tts machine');
    screen = pygame.display.set_mode((640, 240), pygame.RESIZABLE); text = 'type something and press enter'; font = pygame.font.SysFont(None, 48); img = font.render(text, True, (0, 0, 0)); rect = img.get_rect(); rect.topleft = (20, 20); cursor = pygame.Rect(rect.topright, (3, rect.height))
    images = parseimages('downloads'); imgnames = []; imgpath = [];
    #lmao3 = pygame.image.frombuffer(b64_decode_img(b64_encode_img('downloads\\alice.png')), (218,218), 'RGBA')
    if images is not None:
        randimg = random.randint(0, len(images)-1)
        for i in images:
            imgnames.append(i.split('.')[0]); imgpath.append(os.path.join('downloads',i))
        lmao2 = pygame.image.load(imgpath[randimg]); pygame.display.set_icon(lmao2)
        lmao2 = pygame.transform.scale(lmao2, (640, 240))

    bksp = 0; bkspcnt = 0
    lmao = True
    while lmao:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: lmao = False; break
            if event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                if images is not None:
                    lmao2 = pygame.image.load(imgpath[randimg]); lmao2 = pygame.transform.scale(lmao2, (event.w, event.h))
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: lmao = False; break
                if images is not None:
                    if event.key == pygame.K_SPACE: randimg = random.randint(0, len(images)-1); lmao2 = pygame.image.load(imgpath[randimg]); lmao2 = pygame.transform.scale(lmao2, screen.get_size())
                if event.key == pygame.K_RETURN: text = b64_encode(text)
                if event.key == pygame.K_BACKSPACE: bksp = 1; text = text[:-1]; bkspt0 = time.time()
                else:
                    if event.key != pygame.K_RETURN: text += event.unicode
                img = font.render(text, True, (0, 0, 0))
                rect.size=img.get_size()
                cursor.topleft = rect.topright
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_BACKSPACE: bksp = 0; bkspt0 = 0; bkspcnt = 0; rect.size=img.get_size(); cursor.topleft = rect.topright
        if bksp:
            if time.time()-bkspt0 > 0.5:
                bkspcnt += 1
                if bkspcnt > 15: bkspcnt = 0; text = text[:-1]; img = font.render(text, True, (0, 0, 0)); rect.size=img.get_size(); cursor.topleft = rect.topright; pygame.draw.rect(screen, (0, 0, 0), cursor); screen.blit(img, rect); pygame.display.update()
        screen.fill((255, 255, 255))
        if images is not None:
            screen.blit(lmao2, (0,0))
            #for i in imgpath:
                #screen.blit(pygame.image.load(i), (0,0))
        screen.blit(img, rect)
        if time.time() % 1 > 0.5:
            pygame.draw.rect(screen, (0, 0, 0), cursor)
        pygame.display.update()
    pygame.quit()

def menu():
    import sys
    arg = None; arglist = []; argopts = []
    for i in sys.argv[1:]:
        if i[0] == '-': arg = i[1:]; arglist.append(arg)
        else: argopts.append((arg, i))
    if 'h' in arglist:
        return print('LMAO.PY\n\nuhhhhhh cant help you just look in the code or something, just run with -i to install dependencies')
    if 'i' in arglist:
        install_dependencies()
    if 'g' in arglist:
        ytargopts = []
        for i in argopts:
            if i[0] == 'g': ytargopts.append(i[1])
        return infoget(ytargopts[0])
    if 'yt' in arglist or '-youtube_mp3' in arglist:
        ytargopts = []; ytarguments = {'path':'downloads', 'autoplay':True}
        for i in argopts:
            if i[0]=='yt' or i[0]=='-youtube_mp3': ytargopts.append(i[1])
        if len(ytargopts)==0: return yt_mp3_menu()
        for i in ytargopts:
            if i[:4] == "http":
                ytarguments['url']=i
                continue
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            ytarguments[k] = v
        return yt_mp3(**ytarguments)
    if 'yp' in arglist or '-youtube_mp3_playlist' in arglist:
        ypargopts = []; yparguments = {'autoplay':False, 'overwrite':False, 'Truecli':False, 'path':'playlists'}
        for i in argopts:
            if i[0]=='yp' or i[0]=='-youtube_mp3_playlist': ypargopts.append(i[1])
        if len(ypargopts)==0: return yt_playlist_mp3_menu()
        for i in ypargopts:
            if i[:4] == "http":
                yparguments['url']=i
                continue
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            yparguments[k] = v
        return yt_playlist_mp3(**yparguments)
    if 'pm' in arglist or '-playlist_metadata' in arglist:
        pmargopts = []; pmarguments = {'playlist_title':False, 'url':False, 'path':'playlists'}
        for i in argopts:
            if i[0]=='pm' or i[0] == '-playlist_metadata': pmargopts.append(i[1])
        for i in pmargopts:
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            pmarguments[k] = v
        return playlist_metadata(**pmarguments)
    if 'aa' in arglist:
        aaargopts = []; aaarguments = {'playlist_title':False, 'url':False, 'path':'playlists'}
        for i in argopts:
            if i[0] == 'aa': aaargopts.append(i[1])
        for i in aaargopts:
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            aaarguments[k] = v
        return album_art_folder(**aaarguments)
    if 'pp' in arglist:
        ppargopts = []; pparguments = {'playlist_title':False, 'url':False, 'path':'playlists', 'askshuffle':True}
        for i in argopts:
            if i[0] == 'pp': ppargopts.append(i[1])
        if len(ppargopts)==0: return music_playlist_player_menu()
        for i in ppargopts:
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            pparguments[k] = v
            if not pparguments['playlist_title'] and not pparguments['url']:
                music_playlist_player_menu(path=pparguments['path'], askshuffle=pparguments['askshuffle'])
        return music_playlist_player(**pparguments)
    if 'mp' in arglist:
        mpargopts = []; mparguments = {'filename':False, 'url':False, 'path':'playlists'}
        for i in argopts:
            if i[0] == 'mp': mpargopts.append(i[1])
        if len(mpargopts)==0: return music_player_menu()
        for i in mpargopts:
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            mparguments[k] = v
            if not mparguments['filename'] and not mparguments['url']:
                music_player_menu(path=mparguments['path'])
        return music_player(**mparguments)
    if 'yl' in arglist:
        ylargopts = []; ylarguments = {'autoplay':True, 'MPV':True, 'chromechat':False}
        for i in argopts:
            if i[0] == 'yl': ylargopts.append(i[1])
        if len(ylargopts)==0: return yt_live_menu()
        for i in ylargopts:
            if i[:4] == "http":
                ylarguments['url']=i
                continue
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            ylarguments[k] = v
        return yt_live(**ylarguments)
    if '-sendtwitchchat' in arglist:
        sendtwitchchatargopts = []; sendtwitchchatarguments = {}
        for i in argopts:
            if i[0] == '-sendtwitchchat': sendtwitchchatargopts.append(i[1])
        for i in sendtwitchchatargopts:
            k,v = i.split('=',1)
            if v == 'True': v=True
            if v == 'False': v=False
            sendtwitchchatarguments[k] = v
        return sendtwitchchat(**sendtwitchchatarguments)
    if len(arglist) == 0:
        import MenuLibrary
        MenuLibrary.main()



def main():
    import os
    os.system('color a')
    #typetext()
    #videoplayer('https://www.youtube.com/watch?v=BqnG_Ei35JE')
    #downloadfile()
    #yt_playlist_mp3('https://www.youtube.com/playlist?list=OLAK5uy_m0caEe_OxtoII-A3qucyav_776n7-HQ7M', autoplay=True)
    #downloadfile("https://raw.githubusercontent.com/Anonymous-crow/Disarray/master/image%5B1%5D.png", overwrite=True, filename="alice.png")
    '''
    downloadfile(b64_decode('aHR0cHM6Ly9jcm93LmVwaWNnYW1lci5vcmcvYXNzZXRzL2xtYW8uZXhl'))
    '''
    #music_playlist_player('ZABA')
    #yt_playlist_mp3_menu()
    #download_url(base64.b64decode('aHR0cHM6Ly9jcm93LmVwaWNnYW1lci5vcmcvYXNzZXRzL2xtYW8uZXhl'.encode('ascii')).decode('ascii'))

if __name__ == "__main__":
    main()
    menu()
