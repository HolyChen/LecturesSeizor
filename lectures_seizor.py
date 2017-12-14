#! /usr/bin/python3
# -*- coding: utf-8 -*-

"""Main module of Lectures Serzor.
    Author: Holy Chen
    Create Time: 2017-12-14
    Last Update Time: 2017-12-14
    License: GPL v3
"""

import argparse

import colorama

from model.seizor import LecturesSeizor

DESCRIPTION = \
    'Auto seize lectures held by School of Information and Engineering, Xiamen University.\n' \
    'Input the website, your student id, password. Just for fun.'

def main():
    """Program entrance
    """
    
    colorama.init()

    args_parser = argparse.ArgumentParser(description=DESCRIPTION)

    args_parser.add_argument('website', metavar='website',
                        help='the website of the system, start with "http://"')
    args_parser.add_argument('username', metavar='username', help='your student ID')
    args_parser.add_argument('password', metavar='password', help='your password')
    
    args = args_parser.parse_args()

    lec_seizor = LecturesSeizor(args.website, args.username, args.password)
    lec_seizor.start()

if __name__ == '__main__':
    main()
