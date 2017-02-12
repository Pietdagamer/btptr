#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    main.py
    This file is part of btjchmpie.

    Copyright (c) 2015 Pietdagamer
    Copyright (c) 2017 MrTijn

    btjchmpie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    btjchmpie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with btjchmpie.  If not, see <http://www.gnu.org/licenses/>.
"""

import socket
import time
import ircbot

DEBUG = True

bot_owner = "Meandonlymeandnooneelse"
nick = "btjchmpie"

if DEBUG:
    channel = "#btjchmpy"
else:
    channel = "#eras"

server = "irc.freenode.net"
port = 6667

btjchmpie = ircbot.IRCBot(nick, channel, bot_owner, server, port)
#sock = socket.socket()
#btjchmpie.connect(sock)

time.sleep(5)

while 1:
    data = btjchmpie.sock.recv(512).decode("utf-8")
    print(data)
    btjchmpie.parse_recv_data(data)

    # Find a better solution to do this
    #btjchmpie.check_timed_events()
