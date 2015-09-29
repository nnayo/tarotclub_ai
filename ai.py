#! /usr/bin/env python3

"""
tarotclub game python AI

this is the try to make a python AI for the tarotclub game
"""

import sys
import getopt

import protocol

SERVER_DEFAULT_IP = '127.0.0.1'
SERVER_DEFAULT_PORT = 4269
SERVER_DEFAULT_TABLE = 0

def usage():
    """
    usage:
    ai.py [-s <game server IP>] [-p <game server port>] [-t <table number to join>]
    """

    print(usage.__doc__)
    sys.exit()

def main():
    # suppress prog name from arg list
    optlist, args = getopt.getopt(sys.argv[1:], 'hs:p:t:')

    if not optlist:
        usage()

    server_ip = SERVER_DEFAULT_IP
    server_port = SERVER_DEFAULT_PORT
    table = SERVER_DEFAULT_TABLE

    for o, a in optlist:
        if o == '-h':
            usage()
        elif o == '-s':
            server_ip = a
        elif o == '-p':
            server_port = int(a, 10)
        elif o == '-t':
            table = int(a, 10)

    protocol.Protocol(server_ip, server_port, table).run()

if __name__ == '__main__':
    main()

