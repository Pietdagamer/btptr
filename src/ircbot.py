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

    # Currently not used, will change into a timed sync to .csv for performance

    # Format: [[str user, str afk_msg], ...]
    afk_users = []

    # Format: [[str t, str list args], ...]
    # t format: "%Y-%m-%d %H:%M:%S"
    # args format: [str action]
    # args format for reminder: [str action, str user, str remind_msg]
    # Actions: reminder, sync, ignore
    timed_events = []

    preset_text_cmds = {}

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

        # Connect to the IRC server
        self.sock = socket.socket()
        self.connect()

        # Initialize print commands information
        self.preset_text_cmds = { "!lenny" : "( ͡° ͜ʖ ͡°)", "!version" : self.version(), "!license" : self.license(),
                "!help" : "TODO: Add help", "!tableflip" : "(╯°□°）╯︵ ┻━┻ " }

        # Make sure all .csv files exist
        utils.touch_files()

    def version(self):
        """Returns current version"""
        return "btptr v0.1"

    def license(self):
        """Returns license information"""
        with open("license_information.txt") as f:
            return f.read().replace('\n','-')

    def debug_print(self, msg):
        if self.DEBUG:
            print(msg)

    """
    Basic connection methods
    """

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

    """
    get_ methods
    """

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
    Timed events methods
    """

    def add_timed_event(self, action_time, args):
        """Sets a timed event

        time - struct_time
        action - list of string
        """

        timed_events = []
        with open("timed_events.csv", 'r') as f:
            timed_events.extend(csv.reader(f))

        if self.DEBUG:
            print(timed_events)

        timed_events.append([time.strftime("%Y-%m-%d %H:%M:%S", action_time), args])

        if self.DEBUG:
            print(timed_events)

        with open("timed_events.csv", 'w') as f:
            csv.writer(f).writerows(timed_events)

    def check_timed_events(self):
        """Checks and executes timed events"""
        timed_events = []
        with open("timed_events.csv", 'r') as f:
            timed_events.extend(csv.reader(f))

        if self.DEBUG:
            print(timed_events)

        if timed_events == []:
            timed_events.append([time.localtime(), 'ignore'])

        cur_time = time.localtime()
        launch_event = None
        for event in timed_events:
            for i in range(6):
                if event[0][i] == cur_time[i]:
                    if self.DEBUG:
                        print('equal')
                    pass
                else:
                    if self.DEBUG:
                        print('not equal')
                    break
            launch_event = event

        if self.DEBUG:
            print(launch_event)

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
            self.get_online_users()
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

                if command in self.preset_text_cmds:
                    self.send_msg(self.preset_text_cmds[command])

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
                elif command == "!remind":
                    self.cmd_remind(args)

                # Debug-only commands
                if self.DEBUG:
                    if command == "!stop":
                        if self.get_sender(data) == "MrTijn":
                            print("Stopping...")
                            sys.exit(0)
                    elif command == "!send_raw":
                        print("!send_raw")
                        print(self.send_raw(utils.list_to_str(args)))

    """
    Other user commands
    """

    def cmd_say(self, msg):
        """Say what the user told us to say

        msg - list of strings
        """
        return self.send_msg(utils.list_to_str(msg))

    def cmd_choose(self, args):
        """Choose one of the arguments randomly

        args - list of strings
        """
        self.send_msg(random.choice(args))

    def cmd_ascii(self, msg):
        """Print msg in big ascii art letters

        msg - list of strings
        """
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


    '''
    AFK / Back related commands
    '''

    def cmd_afk(self, user, away_msg):
        """Marks a user afk

        user: username of the user who issued the command, string
        away_msg: away msg to be set, list of strings
        """
        away_msg = utils.list_to_str(away_msg)

        afk_users = []
        with open("afk_users.csv", 'r') as f:
            afk_users.extend(csv.reader(f))

        if self.DEBUG:
            print(afk_users)

        # Hacky fix for bug when no one is afk
        if afk_users == []:
            afk_users.append(['',''])
            if self.DEBUG:
                print("Added empty row for afk_users")

        set_afk = False
        for row in afk_users:
            if user == row[0]:
                row[1] = away_msg
                self.send_msg("You were already away, Your new afk message is: " + away_msg)
                set_afk = True
        if set_afk == False:
            afk_users.append([user, away_msg])
            self.send_msg("You are now afk.")

        if self.DEBUG:
            print(afk_users)

        with open("afk_users.csv", 'w') as f:
            csv.writer(f).writerows(afk_users)

    def cmd_back(self, user):
        """Removes afk marking for a given user"""
        afk_users = []
        with open("afk_users.csv", 'r') as f:
            afk_users.extend(csv.reader(f))

        if self.DEBUG:
            print(afk_users)

        state_changed = False
        if afk_users != []:
            for row in afk_users:
                if user == row[0]:
                    afk_users.remove(row)
                    self.send_msg("Welcome back!")
                    state_changed = True
        if state_changed == False:
            self.send_msg("You weren't afk, but welcome back!")

        # Write changes to database
        with open("afk_users.csv", 'w') as f:
            csv.writer(f).writerows(afk_users)

    def cmd_where(self, args):
        """Sends given user state to channel

        The possible states are: online, offline and afk.
        """

        user = args[0]

        # First check if AFK
        afk_users = []
        with open("afk_users.csv", 'r') as f:
            afk_users.extend(csv.reader(f))

        if afk_users != []:
            for row in afk_users:
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

    """
    Tell / Remind & related commands
    """

    def cmd_remind(self, args):
        """Sets a reminder"""
        self.debug_print(args)
        reminder = ["reminder"] + args
        self.debug_print(reminder)
        self.add_timed_event(time.localtime(), reminder)
