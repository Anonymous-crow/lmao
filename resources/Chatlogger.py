import socket, logging, re, os
from datetime import datetime
from emoji import demojize
from dotenv import load_dotenv

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s — %(message)s',
                    datefmt='%Y-%m-%d_%H:%M:%S',
                    handlers=[logging.FileHandler('chat.log', encoding='utf-8')])
"""
Get token here: https://twitchapps.com/tmi/
"""


def get_chat(nickname, token, channel):
    sock = socket.socket()
    sock.connect(('irc.chat.twitch.tv', 6667))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))

    try:
        while True:
            resp = sock.recv(2048).decode('utf-8')

            if resp.startswith('PING'):
                # sock.send("PONG :tmi.twitch.tv\n".encode('utf-8'))
                sock.send("PONG\n".encode('utf-8'))
            elif len(resp) > 0:
                logging.info(demojize(resp))
                if resp[0]==':':
                    user=resp.split('!')[0][1:]
                    msg=resp.split(':')[2:]
                    msg = [''.join(msg[0:])]
                    print('<'+user+'>  '+msg[0])

    except KeyboardInterrupt:
        sock.close()
        exit()

def chatmain():
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    load_dotenv(dotenv_path)
    nickname=os.getenv('nickname'); token=os.getenv('token')
    print(nickname); print(token)
    channel = 'jerma985'
    get_chat(nickname, token, channel)
if __name__ == '__main__':
    chatmain()
