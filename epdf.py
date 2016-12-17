#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Copyright (C) 2016 Tomas Meszaros <exo [at] tty [dot] sk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# --------------------------------------------------------------------
#
# DESCRIPTION:
#
# epdf is a simple program which can extract pages from pdf
#
#
# --------------------------------------------------------------------
#
# DEPENDENCES:
#
#   PyPDF2
#
# PyPDF2 can be found at http://mstamy2.github.io/PyPDF2/
#
# --------------------------------------------------------------------
#
# USAGE:
#
# $ python spdf.py source.pdf startpage-endpage
#
# e.g. $ ./spdf.py source.pdf 10-23

from PyPDF2 import PdfFileWriter, PdfFileReader
from sys import argv, exit
from getpass import getpass

def main():
    # try load source.pdf to source[]
    source = []
    try:
        source.append(PdfFileReader(file(argv[1], "rb")))
    except IOError:
        exit("error: file \"%s\" does not exist" % argv[1])

    # check if is source.pdf encrypted
    if (source[0].getIsEncrypted()):
        print "warrning: file \"%s\" is encrypted" % argv[1]
        pw = getpass("decrypt %s, password: " % argv[1])
        if (source[0].decrypt(pw) == 0):
            exit("error: sorry, wrong passowrd")
        else: print "%s has been dencrypted, processing..." % argv[1]

    # make names for both parts
    pg_start = int(argv[2].split('-')[0])-1
    pg_end = int(argv[2].split('-')[1])-1

    output = PdfFileWriter()

    # take source.pdf and split it
    for i in range(1, source[0].getNumPages()):
        # split source.pdf into two parts & save it
        if i >= pg_start and i <= pg_end:
            output.addPage(source[0].getPage(i))

    # save extracted pages
    outputStream = file(argv[2] + "_" + argv[1], "wb")
    output.write(outputStream)
    outputStream.close()

    print "done!"

def show_help():
    print "USAGE: $ python epdf.py source.pdf startpage-endpage"
    print
    print "e.g. $ ./spdf.py source.pdf 10-23"

if __name__ == "__main__":
    if (len(argv) == 3):
        main()
    else:
        show_help()

# vim: set ts=4 sts=4 sw=4 :
