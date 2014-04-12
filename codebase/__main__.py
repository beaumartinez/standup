from __future__ import print_function

from sys import argv
from sys import exit
from sys import stderr
import logging

from . import Codebase


if __name__ == '__main__':
    logging.disable(logging.CRITICAL)

    try:
        username, key, project = argv[1], argv[2], argv[3]
    except IndexError:
        print('Please pass your username, key, and project', file=stderr)
        exit(1)

    codebase = Codebase(username, key, project)
    codebase.get_tickets()

    for user in sorted(codebase.user_ticket_lookup):
        print(user)

        tickets = sorted(codebase.user_ticket_lookup[user])
        for ticket in tickets:
            print('\t{}'.format(ticket))

        print()
