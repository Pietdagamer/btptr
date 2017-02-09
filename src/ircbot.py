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

    btptr is distributed in the hope that it will be useful,
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
import csv
import sys
from ascii_art import AsciiArt
import utils

class IRCBot:
    DEBUG = True

    nickname = None
    channel = None
    owner = None
    irc_server_address = None
    irc_server_port = None
    sock = None

    online_users = []

    command_re = re.compile('PRIVMSG \#\S+ \:\!.*')
    status_chars_re = re.compile(r"@|\+")

    # Magical regex sponsored by Fredrik
    quoted_arguments_re = re.compile(r'((?:")[^"]+(?:")|[\S]+)')

    def __init__(self, nickname, channel, owner, irc_server_address, irc_server_port):
        self.nickname = nickname
        self.channel = channel
        self.owner = owner
        self.irc_server_address = irc_server_address
        self.irc_server_port = irc_server_port

        self.sock = socket.socket()
        self.connect()

    def version(self):
        """Returns current version"""
        return "btptr v0.1"

    def license(self):
        """Returns license information"""
        with open("license_information.txt") as f:
            return f.read()

    def connect(self):
        """Connects to IRC server and sets nickname"""
        self.sock.connect((self.irc_server_address, self.irc_server_port))
        self.sock.send("USER " + self.nickname + " 0 * :" + self.owner + "\r\n")
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

    def get_sender(self, msg):
        """Parse sender from given message"""
        # Maybe use a regex for this?
        return msg.split("!")[0].split(':')[1]

    def get_online_users(self):
        """Request userlist from server"""
        self.sock.send("NAMES " + self.channel + "\r\n")
        # So this is kinda risky, because we could miss a user message if this
        # isn't the server response of our NAMES command. But let's just hope
        # that'll never happen.
        answer = self.sock.recv(512)
        if answer.split(' ')[1] == "353":
            self.parse_userlist(answer)
            return True
        else:
            return False

    """
    Parsers
    """

    def parse_userlist(self, data):
        """Reads received userlist and saves to online_users list"""
        # Example data:
        # :niven.freenode.net 353 btjchmpy @ #btjchmpy :btjchmpy MrTijn

        # Remove unnecessary server information
        data = data.split(':')[2]

        # Remove status chars
        data = self.status_chars_re.sub('', data)
        data = data.rstrip('\n').rstrip('\r')
        data = data.split(' ')
        self.online_users = data

    def parse_arguments(self, data):
        """Parse all the arguments of an user-issued command

        Returns [command, [arguments]]
        data -- received raw data
        """

        # Example data:
        # :MrTijn!~MrTijn@unaffiliated/tijndagamer PRIVMSG #btjchmpy :!say this is a command

        # Retrieve the command and its arguments from the data
        data = data.rstrip("\r\n")
        command_and_args = self.command_re.findall(data)[0].lstrip("PRIVMSG " + self.channel + ":")
        command = command_and_args.split(' ')[0]

        # Second lstrip is to remove trailing whitespace
        arguments = command_and_args.lstrip(command).lstrip()
        arguments = self.quoted_arguments_re.findall(arguments)

        return [command, arguments]

    def parse_recv_data(self, data):
        if data.startswith("PING"):
            self.sock.send(data.replace("PING", "PONG"))
        if data[0] != ':':
            pass
        if (self.nickname + " :End of /MOTD") in data:
            self.join_channel()
        if data.split(' ')[1] == "353":
            if self.DEBUG:
                print("Parsing userlist!")
            self.parse_userlist(data)
        elif data.split(' ')[1] == "PRIVMSG":
            msg = data.split(' ')[3]
            if msg.startswith(":!"):
                command_and_args = self.parse_arguments(data)
                command = command_and_args[0]
                args = command_and_args[1]
                if self.DEBUG:
                    print(command_and_args)

                if command == "!say":
                    self.cmd_say(args)
                elif command == "!choose":
                    self.cmd_choose(args)
                elif command == "!ascii":
                    self.cmd_ascii(args)
                elif command == "!afk":
                    self.cmd_afk(self.get_sender(data), args)
                elif command == "!back" or command == "!rug" or command == "!brak":
                    self.cmd_back(self.get_sender(data))
                elif command == "!where":
                    self.cmd_where(args)

                # Debug-only commands
                if self.DEBUG:
                    print("Executing a debug-only command")
                    if command == "!stop":
                        if self.get_sender(data) == "MrTijn":
                            print("Stopping...")
                            sys.exit(0)
                    elif command == "!send_raw":
                        print("!send_raw")
                        print(self.send_raw(utils.list_to_str(args)))

    """
    User command methods
    """

    def cmd_say(self, msg):
        """Say what the user told us to say"""
        return self.send_msg(utils.list_to_str(msg))

    def cmd_choose(self, args):
        """Choose one of the arguments randomly"""
        self.send_msg(random.choice(args))

    def cmd_ascii(self, msg):
        """Print msg in big ascii art letters"""
        # Convert msg to string
        msg = utils.list_to_str(msg)

        line1 = ""
        line2 = ""
        line3 = ""

        for char in msg:
            char = char.lower()
            line1 += AsciiArt.characters[char][0]
            line2 += AsciiArt.characters[char][1]
            line3 += AsciiArt.characters[char][2]

        self.send_msg(line1)
        self.send_msg(line2)
        self.send_msg(line3)

    def cmd_afk(self, user, away_msg):
        """Marks a user afk

        user: username of the user who issued the command, string
        away_msg: away msg to be set, list of strings
        """
        away_msg = utils.list_to_str(away_msg)

        users_afk = []
        with open("users_afk.csv", 'r') as f:
            users_afk.extend(csv.reader(f))

        if self.DEBUG:
            print(users_afk)

        # Hacky fix for bug when no one is afk
        if users_afk == []:
            users_afk.append(['',''])
            if self.DEBUG:
                print("Added empty row for users_afk")

        set_afk = False
        for row in users_afk:
            if user == row[0]:
                row[1] = away_msg
                self.send_msg("You were already away, Your new afk message is: " + away_msg)
                set_afk = True
        if set_afk == False:
            users_afk.append([user, away_msg])
            self.send_msg("You are now afk.")

        if self.DEBUG:
            print(users_afk)

        with open("users_afk.csv", 'w') as f:
            csv.writer(f).writerows(users_afk)

    def cmd_back(self, user):
        """Removes afk marking for a given user"""
        users_afk = []
        with open("users_afk.csv", 'r') as f:
            users_afk.extend(csv.reader(f))

        if self.DEBUG:
            print(users_afk)

        state_changed = False
        if users_afk != []:
            for row in users_afk:
                if user == row[0]:
                    users_afk.remove(row)
                    self.send_msg("Welcome back!")
                    state_changed = True
        if state_changed == False:
            self.send_msg("You weren't afk, but welcome back!")

        # Write changes to database
        with open("users_afk.csv", 'w') as f:
            csv.writer(f).writerows(users_afk)

    def cmd_where(self, args):
        """Sends given user state to channel

        The possible states are: online, offline and afk.
        """

        user = args[0]

        # First check if AFK
        users_afk = []
        with open("users_afk.csv", 'r') as f:
            users_afk.extend(csv.reader(f))

        if users_afk != []:
            for row in users_afk:
                if user == row[0]:
                    self.send_msg(user + ": " + user + " is afk: " + row[1])
                    return

        result = self.get_online_users()

        if self.DEBUG:
            print(result)
            print(self.online_users)

        if user in self.online_users:
            self.send_msg(user + ": " + user + " is online.")
            return

        self.send_msg(user + ": " + user + " is offline.")
