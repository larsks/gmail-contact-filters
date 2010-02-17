#!/bin/sed -f
#
# Pass this script a list of addresses and it will generate
# a Gmail filter string to match email sent by anyone in
# the list.

s/^/from:(/
:a
$!N
s/\n/|/
ta
s/$/)/

