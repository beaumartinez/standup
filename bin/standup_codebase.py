#! /usr/bin/env python3

def build_parser():
    from argparse import ArgumentParser

    parser = ArgumentParser(description="print today's activity on Codebase.")
    parser.add_argument('project', help='project name')
    parser.add_argument('-u', '--username', help='API username')
    parser.add_argument('-k', '--key', help='API key')
    parser.add_argument('-a', '--all-users', action='store_true', help="print all user's activity")
    parser.add_argument('-d', '--days-ago', default=None, help="show DAYS_AGO days ago's activity", type=int)
    parser.add_argument('--debug', action='store_true')

    args = parser.parse_args()

    return args


def build_codebase(args):
    if args.debug:
        import logging

        logger = logging.getLogger('standup.codebase')
        logger.setLevel(logging.DEBUG)

    from standup.codebase import Codebase

    if None not in (args.username, args.key):
        codebase = Codebase(args.username, args.key, args.project, days_ago=args.days_ago)
    else:
        codebase = Codebase.from_credentials_file(args.project, days_ago=args.days_ago)

    return codebase


def print_tickets(args, codebase):
    codebase.get_tickets()

    users = sorted(codebase.user_ticket_lookup, key=lambda x: x.first_name)

    if not args.all_users:
        raw_username = codebase.username.split('/')[1]
        users = tuple(filter(lambda x: x.username == raw_username, users))

    for index, user in enumerate(users):
        print(user.first_name)

        def _get_ticket_id(ticket):
            colon_index = ticket.find(':')
            ticket_id = ticket[:colon_index]
            ticket_id = int(ticket_id)

            return ticket_id

        tickets = sorted(codebase.user_ticket_lookup[user], key=_get_ticket_id)
        for ticket in tickets:
            print('  {}'.format(ticket))

        if index + 1 != len(users):  # Not last iteration
            print()


if __name__ == '__main__':
    args = build_parser()
    codebase =  build_codebase(args)

    print_tickets(args, codebase)
