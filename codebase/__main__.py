from __future__ import print_function

from argparse import ArgumentParser
from sys import argv
from sys import exit
from sys import stderr
import logging

from . import Codebase


if __name__ == '__main__':
    parser = ArgumentParser(description='Print today\'s activity on Codebase.')
    parser.add_argument('username')
    parser.add_argument('key')
    parser.add_argument('project')
    parser.add_argument('--days-ago', default=None, type=int)
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()
    
    if args.debug:
        logger = logging.getLogger('codebase')

        logger.setLevel(logging.DEBUG)

    codebase = Codebase(args.username, args.key, args.project, days_ago=args.days_ago)
    codebase.get_tickets()

    for user in sorted(codebase.user_ticket_lookup):
        print(user)

        tickets = sorted(codebase.user_ticket_lookup[user])
        for ticket in tickets:
            print('\t{}'.format(ticket))

        print()
