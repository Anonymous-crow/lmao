#from future import unicode_literals
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import base64, json, youtube_dl, pafy, threading, pygame

def install_dependencies():
    os.system('python -m pip install gtts playsound youtube-dl pafy pyglet opencv-python --user')

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

def downloadfile(url = "https://raw.githubusercontent.com/Anonymous-crow/Disarray/master/image%5B1%5D.png", filename = False, overwrite = False, path = 'downloads'):
        if not filename:
            os.system('curl -O ' + url); clear();
        else:
            if overwrite: os.system('curl ' + url + ' --output ' + os.path.join(path, filename)); clear();
            else:
                while True:
                    if not os.path.isfile(os.path.join(path, filename)): os.system('curl ' + url + ' --output ' + os.path.join(path, filename)); clear(); break
                    else: filename = filename.split('.')[0] + '(1).' + filename.split('.')[1]

def download_video(url):
    for i in pafy.new(url).streams:
        print(i)
    pafy.new(url).getbest(preftype ="mp4").download()

def music_player():
    import curses
    s = curses.initscr()
    curses.curs_set(0)
    sh, sw = s.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.keypad(1)
    w.timeout(100)

def cli_play_playlist(playlist_title=False, url=False):
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
        if not os.path.isdir(playlist_title):
            return print('folder '+playlist_title+' does not exist')
        with open(os.path.join(playlist_title, playlist_title + ' playlist.json'), 'r') as file:
            playlist = json.load(file)
        print('Now Playing: '+playlist_title)
        lmao = True
        for i in playlist:
            filename = playlist[i][1].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
            title = playlist[i][0]
            if playlist[i][3] != 'null':
                title = playlist[i][0] + ' by ' + playlist[i][3]
            clear()
# --------------------------Path of your music
            try:
                if lmao:
                    pygame.mixer.music.load(os.path.join(playlist_title, filename))
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




def yt_playlist_mp3(url, autoplay=False, overwrite=False):
    from playsound import playsound
    created = False
    if not os.path.isfile('ffmpeg.exe'):
        os.system('curl https://crow.epicgamer.org/assets/ffmpeg.exe --output ffmpeg.exe')
        clear()
    ydl_opts = {'logger': logger()}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        playlist_title = info_dict['title'].replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')
        if not os.path.isdir(playlist_title):
            created = True
            os.mkdir(playlist_title)
        with open(os.path.join(playlist_title, playlist_title + ' metadata.json'), 'w') as file:
            json.dump(info_dict, file, indent=4, separators=(',', ': '))
    ydl_opts = {
        'outtmpl': os.path.join(playlist_title, '%(title)s.%(ext)s'),
        'nooverwrites': overwrite,
        'logger': logger(),
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    if created:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    else:
        if overwrite:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
    playlist = {}
    for i in info_dict['entries']:
        if i["creator"] != None: creator = i["creator"]
        else: creator = "null"
        playlist[str(i['playlist_index'])] = [i['title'], (i['title']+'.mp3').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_'), os.path.join(playlist_title, (i['title']+'.mp3').replace(':', ' -').replace('"', '\'').replace("'", "\'").replace('|', '_')), creator];
    with open(os.path.join(playlist_title, playlist_title + ' playlist.json'), 'w') as file:
        json.dump(playlist, file, indent=4, separators=(',', ': '))
    if autoplay: cli_play_playlist(playlist_title)

def yt_mp3(url, path='downloads', autoplay=True):
    from playsound import playsound;
    if not os.path.isfile('ffmpeg.exe'):
        os.system('curl https://crow.epicgamer.org/assets/ffmpeg.exe --output ffmpeg.exe')
        clear()
    ydl_opts={}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        video_title=info_dict['title'].replace(':', ' -')
    filename = video_title + ".mp3"
    if not os.path.isfile(os.path.join(path, filename)):
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'bestaudio/best',
            'logger': logger(),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        #clear()
        if os.path.isdir(path): os.rename(filename, os.path.join(path, filename))
        else: os.mkdir(path); os.rename(filename, os.path.join(path, filename))
    if autoplay:
        if os.name == 'nt': _ = playsound(os.path.join(path, filename), False)
        else: _ = playsound(os.path.join(path, filename))

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




def videoplayer_no_sound(url):
    if not os.path.isfile('ffmpeg.exe'):
        os.system('curl https://crow.epicgamer.org/assets/ffmpeg.exe --output ffmpeg.exe')
        clear()
    video=pafy.new(url); ash=url.split('=')[1]
    video.getbest(preftype ="mp4").download()
    import cv2
    import numpy as np
    cap = cv2.VideoCapture(video.title+'.mp4')
    if (cap.isOpened()== False):
      print("Error opening video  file")
    while(cap.isOpened()):
      ret, frame = cap.read()
      if ret == True:
        cv2.imshow('Frame', frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
          break
      else:
        break
    cap.release()
    cv2.destroyAllWindows()

def videoplayer(url):
    import pyglet
    video=pafy.new(url); ash=url.split('=')[1]
    video.getbest(preftype ="mp4").download()
    vidPath = video.title+'.mp4'
    window= pyglet.window.Window()
    player = pyglet.media.Player()
    source = pyglet.media.StreamingSource()
    MediaLoad = pyglet.media.load(vidPath)
    player.queue(MediaLoad)
    player.play()
    @window.event
    def on_draw():
        if player.source and player.source.video_format:
            player.get_texture().blit(0,0)
    pyglet.app.run()

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

def main():
    clear()
    os.system('color a')
    #yt_mp3()
    #videoplayer('https://www.youtube.com/watch?v=BqnG_Ei35JE')
    #downloadfile()
    downloadfile("https://raw.githubusercontent.com/Anonymous-crow/Disarray/master/image%5B1%5D.png", overwrite=True, filename="alice.png")
    '''
    downloadfile(b64_decode('aHR0cHM6Ly9jcm93LmVwaWNnYW1lci5vcmcvYXNzZXRzL2xtYW8uZXhl'))
    '''
    #download_url(base64.b64decode('aHR0cHM6Ly9jcm93LmVwaWNnYW1lci5vcmcvYXNzZXRzL2xtYW8uZXhl'.encode('ascii')).decode('ascii'))
    #os.system(b64_decode('c3RhcnQgbG1hby5leGU='))
    #yt_mp3('https://www.youtube.com/watch?v=qQzdAsjWGPg')
    #t2 = threading.Thread(target=yt_mp3, args = ('https://www.youtube.com/watch?v=THpt6ugy_8E',)); t2.start();
    #print(parseimages_dict('downloads'))
    #typetext()
    #typetext2()
    #yt_mp3('https://www.youtube.com/watch?v=iGGVWGJ0ZiM')
    #yt_playlist_mp3('https://www.youtube.com/playlist?list=OLAK5uy_mrQpw7Bipv-a7DFFerdXeLe-Ll4yxdE6U', autoplay=True)
    #play_playlist('Creatures of Habit')
    yt_playlist_mp3('https://www.youtube.com/playlist?list=PLLGT0cEMIAzf5fP-GYGzFGDXheR3Vn45v', autoplay=False)
    #consoleTTS()
    #t1 = threading.Thread(target=downloadallaudio2,args = ('https://www.youtube.com/watch?v=dpAvnPI04-s',)); t1.start(); t1.join()
    cli_play_playlist('Mogul Grooves')
    #music_player()
if __name__ == "__main__":
    install_dependencies()
    main()
