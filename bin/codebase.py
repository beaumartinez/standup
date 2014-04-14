#! /usr/bin/env python3

from argparse import ArgumentParser
from sys import path
import logging

path.insert(0, '..')

from codebase import Codebase


if __name__ == '__main__':
    parser = ArgumentParser(description="print today's activity on Codebase.")
    parser.add_argument('username', help='API username')
    parser.add_argument('key', help='API key')
    parser.add_argument('project', help='project name')
    parser.add_argument('--days-ago', default=None, help="show DAYS_AGO days ago's activity", type=int)
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
            print('    {}'.format(ticket))

        print()
