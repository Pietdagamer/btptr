#!/usr/bin/python3
# -*- encoding: utf-8 -*-

import socket
import time
import ircbot

DEBUG = True

bot_owner = "Meandonlymeandnooneelse"
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
