#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
    ascii_art - Class for ascii art letter translation
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

class AsciiArt:

    """
    Characters
    """

    a = [ "     "
        , " /\\  "
        , "/--\\ "]
    b = [ " _  "
        , "|_) "
        , "|_) "]
    c = [ " __ "
        , "|   "
        , "|__ "]
    d = [ "__  "
        , "| \\ "
        , "|_/ "]
    e = [ " __ "
        , "|__ "
        , "|__ "]
    f = [ " __ "
        , "|__ "
        , "|   "]
    g = [ " __ "
        , "/   "
        , "\\_] "]
    h = [ "    "
        , "|_| "
        , "| | "]
    i = [ "   "
        , " | "
        , " | "]
    j = [ "    "
        , " |  "
        , "_/  "]
    k = [ "   "
        , "|/ "
        , "|\\ "]
    l = [ "    "
        , "|   "
        , "|__ "]
    m = [ " _    _  "
        , "| \\  / | "
        , "|  \\/  | "]
    n = [ " _    "
        , "| \\ | "
        , "|  \\| "]
    o = [ " _  "
        , "/ \\ "
        , "\\_/ "]
    p = [ " _  "
        , "|_) "
        , "|   "]
    q = [ " _  "
        , "(_| "
        , "  | "]
    r = [ " _  "
        , "|_) "
        , "|\\  "]
    s = [ " __  "
        , "(__  "
        , " __) "]
    t = [ "___ "
        , " |  "
        , " |  "]
    u = [ "     "
        , "|  | "
        , "|__| "]
    v = [ "    "
        , "\\ / "
        , " V  "]
    w = [ "         "
        , "\\  /\\  / "
        , " \\/  \\/  "]
    x = [ "    "
        , " \\/ "
        , " /\\ "]
    y = [ "    "
        , " \\/ "
        , " /  "]
    z = [ "__ "
        , " / "
        , "/_ "]
    space = [ "  ", "  ", "  "]
    period = [ "  ", "  ", ". "]
    exclamation_mark = [ " |  "
        , " |  "
        , " .  "]
    question_mark = [ " /\\ "
        , "  / "
        , "  . "]
    n1 = [ "    "
        , "  | "
        , "  | "]
    n2 = [ " _  "
        , " _| "
        , "|_  "]
    n3 = [ " _  "
        , " _| "
        , " _| "]
    n4 = [ "    "
        , "|_| "
        , "  | "]
    n5 = [ " _  "
        , "|_  "
        , " _| "]
    n6 = [ " _  "
        , "|_  "
        , "|_| "]
    n7 = [ " _  "
        , "  | "
        , "  | "]
    n8 = [ " _  "
        , "|_| "
        , "|_| "]
    n9 = [ " _  "
        , "|_| "
        , " _| "]
    n0 = [ " _  "
        , "| | "
        , "|_| "]
    plus = [ "    "
        , "_|_ "
        , " |  "]
    dash = [ "    "
        , "___ "
        , "    "]
    underscore = [ "    "
        , "    "
        , "___ "]
    equals = [ "    "
        , "--- "
        , "--- "]
    parenthesis_open = [ " / "
        , "|  "
        , " \\ "]
    parenthesis_close = [ " \\ "
        , "  |"
        , " / "]
    percentage = [ " O / "
        , "  /  "
        , " / O "]
    double_quote = [ "|| "
        , "   "
        , "   "]
    quote = [ "| "
        , "  "
        , "  "]
    larger_than = [ "    "
        , " \\  "
        , " /  "]
    smaller_than = [ "    "
        , " /  "
        , " \\  "]
    forward_slash = [ "  / "
        , " /  "
        , "/   "]
    bar = [ " | "
        , " | "
        , " | "]
    colon = [ "   "
        , " . "
        , " . "]
    semicolon = [ "   "
        , " . "
        , " , "]

    characters = {'a' : a, 'b' : b, 'c' : c, 'd' : d, 'e' : e, 'f' : f, 'g' : g,
        'h' : h, 'i' : i, 'j' : j, 'k' : k, 'l' : l, 'm' : m, 'n' : n, 'o' : o,
        'p' : p, 'q' : q, 'r' : r, 's' : s, 't' : t, 'u' : u, 'v' : v, 'w' : w,
        'x' : x, 'y' : y, 'z' : z, ' ' : space, '.' : period, '!' : exclamation_mark,
        '?' : question_mark, '1' : n1, '2' : n2, '3' : n3, '4' : n4, '5' : n5,
        '6' : n6, '7' : n7, '8' : n8, '9' : n9, '0' : n0, '+' : plus, '-' : dash,
        '_' : underscore, '=' : equals, '(' : parenthesis_open, ')' : parenthesis_close,
        '%' : percentage, '"' : double_quote, '\'' : quote, '>' : larger_than,
        '<' : smaller_than, '/' : forward_slash, '|' : bar, ':' : colon, ';' : semicolon }
