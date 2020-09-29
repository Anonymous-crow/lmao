import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import lmao
lmao.downloadmp3('https://www.youtube.com/watch?v=EHMCwwtPnV0&feature=youtu.be&t=276')
lmao.consoleTTS()
