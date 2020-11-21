import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lmao
lmao.yt_playlist_mp3('https://www.youtube.com/playlist?list=PL8tkzXKlhGxltZh_s3jGtrJgoVHb0lbKt', overwrite=True)
