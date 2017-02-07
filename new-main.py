#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
List of commands:

     !tell [Sends a message to a user when they return]
     !afk [Marks a user Away From Keyboard]
     !back [Marks a user back]
     !where [Checks where a user is (AFK or Back)]
DONE !choose [Chooses one of the given options]
     !answer (kindof)
     !remind [Reminds a user of something after a given amount of time]
     !waitforit [stupid reference joke command]
     !whatsnew [New functions in the bot
DONE !say [Make the bot send a message]
     !rejoin [Rejoins the channelnel]
     !ascii [Turns a string into ASCII-art]
     !ok [Prints "OK" in ASCII-art]
     !pls [Prints "PLS" in ASCII-art]
     n1 [Prints "N1" in ASCII-art]
"""

import socket
import time
import random
import ircbot

DEBUG = True

nicknumb = random.randint(0,999)

bot_owner = "Meandonlymeandnooneelse"
#nick = "btptr" + str(nicknumb)
nick = "btjchmpy"

if DEBUG:
    channel = "#btjchmpy"
else:
    channel = "#eras"
server = "irc.freenode.net"
port = 6667

btptr = ircbot.IRCBot(nick, channel, bot_owner, server, port)

sock = socket.socket()
btptr.connect(sock)

while 1:
    data = sock.recv(512)
    print(data)
    btptr.parse_recv_data(data, sock)
