from __future__ import print_function

from sys import argv
from sys import exit
from sys import stderr
import logging

from . import Codebase


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)

    try:
        username, key = argv[1], argv[2]
    except IndexError:
        print('Please pass your username and key', file=stderr)
        exit(1)

    codebase = Codebase(username, key, 'locus')
    codebase.get_tickets()

    for user in sorted(codebase.user_tickets):
        print(user)

        tickets = sorted(codebase.user_tickets[user])
        for ticket in tickets:
            print('\t{}'.format(ticket))

        print()
