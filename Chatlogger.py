import socket, logging, re, os, sys
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


def get_chat(nickname, token, channel, printchat=True):
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
                    msg=[''.join(msg[0:])]
                    if printchat: print('<'+user+'> '+msg[0])

    except KeyboardInterrupt:
        sock.close()
        exit()

def send_chat(nickname, token, channel):
    sock = socket.socket()
    sock.connect(('irc.chat.twitch.tv', 6667))
    sock.send(f"PASS {token}\r\n".encode('utf-8'))
    sock.send(f"NICK {nickname}\r\n".encode('utf-8'))
    sock.send(f"JOIN #{channel}\r\n".encode('utf-8'))
    while True:
        sock.send((f'PRIVMSG #'+channel+' :'+input('message chat:\n')+'\r\n').encode('utf-8'))

def chatmain(channel):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    nickname=os.getenv('NICKNAME')
    token=os.getenv('TOKEN')
    print(nickname, channel)
    send_chat(nickname, token, channel)

if __name__ == '__main__':
    chatmain(sys.argv[1])
