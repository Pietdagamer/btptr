#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    irc - IRC class
    This file is part of btjchmpie.

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

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    """
    Basic utility methods
    """

    def debug_print(self, msg):
        if self.DEBUG:
            print(msg)

    def sock_send_str(self, msg):
        total_sent = 0
        while total_sent < len(msg):
            sent = self.sock.send(msg[total_sent:].encode())
            total_sent += sent

    """
    Basic connection methods
    """

    def connect(self):
        """Connects to IRC server and sets nickname"""
        self.sock.connect((self.irc_server_address, self.irc_server_port))
        self.sock_send_str("USER " + self.nickname + " 0 * :" + self.realname + "\r\n")
        self.sock_send_str("NICK " + self.nickname + "\r\n")

    def join_channel(self):
        """Join configured channel"""
        self.sock_send_str("MODE " + self.nickname + " +B\r\n")
        self.sock_send_str("JOIN " + self.channel + "\r\n")

    def send_msg(self, msg):
        """Send a string to the configured channel"""
        return self.sock_send_str("PRIVMSG " + self.channel + " :" + msg + "\r\n")

    def send_raw(self, data):
        """Send raw data to irc server"""
        return self.sock_send_str(data + "\r\n")

    def notice(self, msg, nick):
        return self.sock_send_str("NOTICE " + nick + " :" + msg + "\r\n")
