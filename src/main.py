#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    main.py
    This file is part of btptr.

    Copyright (c) 2015 Pietdagamer 
    Copyright (c) 2017 MrTijn

    btptr is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    btptr is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with btptr.  If not, see <http://www.gnu.org/licenses/>.
"""

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
#sock = socket.socket()
#btptr.connect(sock)

time.sleep(5)

while 1:
    data = btptr.sock.recv(512)
    print(data)
    btptr.parse_recv_data(data)

    # Find a better solution to do this
    btptr.check_timed_events()
