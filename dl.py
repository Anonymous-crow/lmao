
def dl_file(url, filename):
    import requests
    x = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(x.content); file.close()

if __name__ == "__main__":
    dl_file('https://crow.epicgamer.org/assets/ffmpeg.exe', 'ffmpeg2.exe')
