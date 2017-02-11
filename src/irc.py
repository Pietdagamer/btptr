#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    irc - IRC class
    This file is part of btptr.

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

class IRC:
    nickname = None
    channel = None
    realname = None
    irc_server_address = None
    irc_server_port = None
    sock = None
    DEBUG = True

    def __init__(self, nick, channel, realname, irc_server_address, irc_server_port):
        self.nickname = nickname
        self.channel = channel
        self.realname = realname
        self.irc_server_address = irc_server_address
        self.irc_server_port = irc_server_port

        self.sock = socket.socket()

    """
    Basic connection methods
    """

    def connect(self):
        """Connects to IRC server and sets nickname"""
        self.sock.connect((self.irc_server_address, self.irc_server_port))
        self.sock.send("USER " + self.nickname + " 0 * :" + self.realname + "\r\n")
        self.sock.send("NICK " + self.nickname + "\r\n")

    def join_channel(self):
        """Join configured channel"""
        self.sock.send("MODE " + self.nickname + " +B\r\n")
        self.sock.send("JOIN " + self.channel + "\r\n")

    def send_msg(self, msg):
        """Send a string to the configured channel"""
        return self.sock.send("PRIVMSG " + self.channel + " :" + msg + "\r\n")

    def send_raw(self, data):
        """Send raw data to irc server"""
        return self.sock.send(data + "\r\n")

    def notice(self, msg, nick):
        return self.sock.send("NOTICE " + nick + " :" + msg + "\r\n")
