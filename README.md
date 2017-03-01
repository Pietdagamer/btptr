# btjchmpie

An IRC bot written in python

# Commands

| Command    | Description                                               | Implemented |
|------------|-----------------------------------------------------------|-------------|
| !tell      | Sends a message to a user when they return                |N			   |
| !afk       | Marks a user Away From Keyboard                           |Y			   |
| !back      | Marks a user back                                         |Y		       |
| !where     | Checks where a user is (AFK or Back)                      |Y     	   |
| !choose    | Chooses one of the given options                          |Y			   |
| !answer    | (kindof)                                                  |N			   |
| !remind    | Reminds a user of something after a given amount of time  |WIP		   |
| !waitforit | stupid reference joke command                             |N			   |
| !whatsnew  | New functions in the bot                                  |N		  	   |
| !say       | Make the bot send a message                               |Y	   		   |
| !rejoin    | Rejoins the channel                                       |N		       |
| !ascii     | Turns a string into ASCII-art                             |Y 		   |
| !ok        | Prints "OK" in ASCII-art                                  |N		       |
| !pls       | Prints "PLS" in ASCII-art                                 |N		       |
| n1         | Prints "N1" in ASCII-art                                  |N		       |
| !lenny     | Prints a lenny face:  ( ͡° ͜ʖ ͡°)                            |Y	    	   |
| !tableflip | Prints a table flip: (╯°□°）╯︵ ┻━┻                        |Y  	      |
| !quote     | Quote system                                              |N            |
| !help      | Prints help                                               |WIP          |
| !version   | Prints IRCBot class version                               |Y            |
| !license   | Prints license information                                |Y            |
| !featurerequest | Requests a fueture to be implemented | N |

# Todo

- Add IRC text color class/utils
- Maintain AFK user list in memory, next to csv file?
~- Check if making the socket a class variable doesn't break things~
