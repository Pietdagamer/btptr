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
nick = "btptr" + str(nicknumb)

if DEBUG:
    channel = "#btjchmpy"
else:
    channel = "#eras"
server = "irc.freenode.net"
port = 6667

btptr = ircbot.ircbot(nick, channel, bot_owner, server, port)

sock = socket.socket()
btptr.connect(sock)
time.sleep(5)
btptr.send_msg("TEST", sock)
#sock.connect(("irc.freenode.net",6667))
#sock.send("USER " + nick + " 0 * :" + bot_owner + "\r\n")
#sock.send("NICK " + nick + "\r\n")
"""
def msg(msg):
    return sock.send("PRIVMSG " + channel + " :" + msg + "\r\n")

def notice(msg, nick):
    return sock.send("NOTICE " + nick + " :" + msg + "\r\n")

def getsender(data):
    senderTemp = data.split("!")[0]
    sender = senderTemp.split(":")[1]
    print "Sender: " + sender
    return sender

def say(data):
    message = data.split(":")[2]
    msg(message)

def choose(args):
    msg(random.choice(args))
"""

def parseArgs(data):
    argstr = ""
    if len(data.split(" ")) > 3:
        for i in range(4, len(data.split(" "))):
            argstr += data.split(" ")[i] + " "

    args = []
    
    quoteArgs = argstr.split('"')
    spaceArgstr = ""

    for i in range(0, len(quoteArgs)):
        if i % 2 == 1:
            args.append(quoteArgs[i])
        else:
            spaceArgstr += quoteArgs[i] + " "

    spaceArgs = spaceArgstr.split(" ")
    for i in range(0, len(spaceArgs)):
        args.append(spaceArgs[i])

    #clean up the empty strings and other nonsense
    cleanArgs = []
    
    i = len(args) - 1 
    while(i >= 0):
        if args[i] != '':
            cleanArgs.append(args[i])
        #elif args[i].endswith("\r\n"): #Might not work on linux!!
        #    print args[i]

        i -= 1
            
    return cleanArgs

while 1:
    data = sock.recv(512)
    print data
    if data[0:4] == "PING":
        sock.send(data.replace("PING", "PONG"))
    if data[0]!=':':
        continue
    if data.split(" ")[1] == "001":
        sock.send("MODE " + nick + " +B\r\n")
        sock.send("JOIN " + channel + "\r\n")
    elif data.split(" ")[1] == "PRIVMSG":
        command = data.split(" ")[3]
        if command.startswith(":!"):
            args = parseArgs(data)
                
            if command == ":!say":
                btptr.command_say(data, sock)
            elif command == ":!choose":
                btptr.command_choose(args, sock)            
