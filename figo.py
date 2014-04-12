from __future__ import print_function

import logging
from collections import defaultdict
from datetime import datetime
from datetime import timedelta
from pprint import pformat
from sys import argv
from sys import exit
from sys import stderr

from requests import Session

from parser import parse_ticket
from parser import parse_ticket_note
from parser import parse_user


log = logging.getLogger(__name__)

log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class Codebase(object):

    def __init__(self, username, key):
        self.username = username
        self.key = key

        date = datetime.utcnow() - timedelta(days=1)
        self.date = date.strftime('%Y-%m-%d')

        self.session = self._create_session()

    def _create_session(self):
        session = Session()
        session.auth = self.username, self.key

        return session

    def _get_users(self):
        log.debug('Getting users.')

        response = self.session.get('https://api3.codebasehq.com/locus/assignments.json')
        self.users = response.json()

    def _parse_users(self):
        self.users = map(parse_user, self.users)

    def _build_user_id_lookup(self):
        user_lookup = {}

        for user in self.users:
            user_lookup[user.id] = user.username

        self.user_lookup = user_lookup

    def _get_tickets(self):
        tickets = []

        page = 0
        done = False
        while not done:
            log.debug('Getting tickets page {}.'.format(page))

            response = self.session.get((
                'https://api3.codebasehq.com/locus/tickets.json?query=sort:updated_at+update:"{}"&'
                'page={}'
            ).format(self.date, page))

            if response.status_code == 200:
                tickets.extend(response.json())

                page += 1
            else:
                done = True

        self.tickets = tickets

    def _parse_tickets(self):
        self.tickets = map(parse_ticket, self.tickets)

    def _build_ticket_note_urls(self):
        for ticket in self.tickets:
            ticket.ticket_note_url = (
                'https://api3.codebasehq.com/locus/tickets/{}/notes.json'
            ).format(ticket.ticket_id)

    def _get_ticket_notes(self):
        for ticket in self.tickets:
            log.debug('Getting notes for ticket {}.'.format(ticket.ticket_id))

            response = self.session.get(ticket.ticket_note_url)

            ticket.ticket_notes = response.json()

    def _parse_ticket_notes(self):
        for ticket in self.tickets:
            ticket.ticket_notes = map(parse_ticket_note, ticket.ticket_notes)

    def _filter_todays_ticket_notes(self):
        for ticket in self.tickets:
            ticket.ticket_notes = filter(
                lambda x: x.created_at.startswith(self.date), ticket.ticket_notes
            )

    def _group_user_ticket_notes(self):
        user_ticket_notes = defaultdict(set)

        for ticket in self.tickets:
            for note in ticket.ticket_notes:
                username = self.user_lookup[note.user_id]

                user_ticket_notes[username].add('{}: {}'.format(ticket.ticket_id, ticket.summary))

        self.user_ticket_notes = dict(user_ticket_notes)

    def get_own_ticket_notes(self):
        self._get_tickets()
        self._parse_tickets()
        self._build_ticket_note_urls()
        self._get_ticket_notes()
        self._parse_ticket_notes()
        self._filter_todays_ticket_notes()
        self._get_users()
        self._parse_users()
        self._build_user_id_lookup()
        self._group_user_ticket_notes()


if __name__ == '__main__':
    log.disabled = True

    try:
        username, key = argv[1], argv[2]
    except IndexError:
        print('Please pass your username and key', file=stderr)
        exit(1)

    codebase = Codebase(username, key)
    codebase.get_own_ticket_notes()

    for user in sorted(codebase.user_ticket_notes):
        print(user)

        tickets = sorted(codebase.user_ticket_notes[user])
        for ticket in tickets:
            print('\t{}'.format(ticket))

        print()
