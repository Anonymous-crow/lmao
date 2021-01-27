import os
def dl_file(url, filename, path=''):
    import requests
    headers = requests.utils.default_headers()
    x = requests.get(url, headers=headers)
    if path=='':
        with open(filename, 'wb') as file:
            file.write(x.content); file.close()
    else:
        if not os.path.isdir(path): os.makedirs(path)
        with open(os.path.join(path,filename), 'wb') as file:
            file.write(x.content); file.close()

def install():
    dl_file(url='https://www.7-zip.org/a/7z1604-extra.7z',path=os.path.join('resources','7z'),filename='7z1604-extra.7z')
    # logging.info('downloaded 7z1604-extra.7z')
    from pyunpack import Archive
    if not os.path.isdir(os.path.join("resources","7z","7z1604-extra")): os.mkdir(os.path.join("resources","7z","7z1604-extra"))
    try:
        Archive(os.path.join('resources','7z','7z1604-extra.7z')).extractall(os.path.join("resources","7z","7z1604-extra"))
    except:
        print('could not extract 7z1604-extra')
    shutil.copyfile(os.path.join("resources","7z","7z1604-extra","7za.exe"), '7za.exe')
    # logging.info('copied 7za.exe')
    dl_file(url='https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-4.3.1-2020-11-19-full_build.7z', filename='ffmpeg-4.3.1-2020-11-19-full_build.7z',path=os.path.join('resources','ffmpeg'))
    os.system('7za x '+os.path.join('resources','ffmpeg','ffmpeg-4.3.1-2020-11-19-full_build.7z')+' -o'+os.path.join('resources','ffmpeg'))
    if not os.path.isfile('ffmpeg.exe'):
        shutil.copyfile(os.path.join("resources","ffmpeg","ffmpeg-4.3.1-2020-11-19-full_build","bin","ffmpeg.exe"), 'ffmpeg.exe')
        # logging.info('copied ffmpeg.exe')
