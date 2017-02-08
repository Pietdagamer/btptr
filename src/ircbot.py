#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    ircbot - irc bot class
    This file is part of btptr.

    Copyright (c) 2017 MrTijn

    btptr is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Foobar is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with btptr.  If not, see <http://www.gnu.org/licenses/>.
"""

import socket
import time
import random
import re

class IRCBot:
    nickname = None
    channel = None
    owner = None
    irc_server_address = None
    irc_server_port = None

    # compiled regexes for optimisation
    command_regex = re.compile('PRIVMSG \#\S+ \:\!.*')
    
    # Magical regex sponsored by Fredrik
    quoted_arguments_regex = re.compile(r'((?:")[^"]+(?:")|\b[^\s]+\b)')

    def __init__(self, nickname, channel, owner, irc_server_address, irc_server_port):
        self.nickname = nickname
        self.channel = channel
        self.owner = owner
        self.irc_server_address = irc_server_address
        self.irc_server_port = irc_server_port

    def connect(self, sock):
        sock.connect((self.irc_server_address, self.irc_server_port))
        sock.send("USER " + self.nickname + " 0 * :" + self.owner + "\r\n")
        sock.send("NICK " + self.nickname + "\r\n")

    def join_channel(self, sock):
        sock.send("MODE " + self.nickname + " +B\r\n")
        sock.send("JOIN " + self.channel + "\r\n")

    def send_msg(self, msg, sock):
        """Send a string to the configured channel"""
        return sock.send("PRIVMSG " + self.channel + " :" + msg + "\r\n")

    def notice(self, msg, nick, sock):
        return sock.send("NOTICE " + nick + " :" + msg + "\r\n")

    def get_sender(self, msg):
        """Parse sender from given message"""
        # Maybe use a regex for this?
        return msg.split("!")[0].split(':')[1]

    def parse_arguments(self, data):
        """Parse all the arguments of an user-issued command

        Returns [command, [arguments]]
        data -- received raw data
        """

        # Example data:
        # :MrTijn!~MrTijn@unaffiliated/tijndagamer PRIVMSG #btjchmpy :!say this is a command

        # Retrieve the command and its arguments from the data
        data = data.rstrip("\r\n")
        command_and_args = self.command_regex.findall(data)[0].lstrip("PRIVMSG " + self.channel + ":")
        command = command_and_args.split(' ')[0]

        # Second lstrip is to remove trailing whitespace
        arguments = command_and_args.lstrip(command).lstrip()
        arguments = self.quoted_arguments_regex.findall(arguments) 

        return [command, arguments]

    def parse_recv_data(self, data, sock):
        if data[0:4] == "PING":
            sock.send(data.replace("PING", "PONG"))
        if data[0] != ':':
            pass
        if (self.nickname + " :End of /MOTD comm") in data:
            self.join_channel(sock)
        elif data.split(' ')[1] == "PRIVMSG":
            msg = data.split(' ')[3]
            if msg.startswith(":!"):
                command_and_args = self.parse_arguments(data)
                command = command_and_args[0]
                args = command_and_args[1]
                print(command_and_args)

                if command == "!say":
                    self.command_say(args, sock)
                elif command == "!choose":
                    self.command_choose(args, sock)

    # Methods for user-commands

    def command_say(self, msg, sock):
        """Say what the user told us to say"""
        return self.send_msg(' '.join(msg), sock)

    def command_choose(self, args, sock):
        """Choose one of the arguments randomly"""
        self.send_msg(random.choice(args), sock)
