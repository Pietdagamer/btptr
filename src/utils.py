#!/usr/bin/python
"""
    utils - Some small utility functions
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

def list_to_str(l):
    """Converts list to a normal string without square brackets and quotes"""
    return ' '.join(l)

def touch_files():
    files = ["timed_events.csv", "afk_users.csv"]
    for fn in files:
        open(fn, 'a').close()

def represents_int(i):
    """Checks if a string can be converted to an integer"""
    try:
        int(i)
        return True
    except ValueError:
        return False
