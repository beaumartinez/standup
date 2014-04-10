from __future__ import print_function

import logging
from datetime import datetime
from pprint import pformat
from sys import argv
from sys import exit
from sys import stderr

from requests import Session


log = logging.getLogger(__name__)

log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class Figo(object):

    def __init__(self, username, key):
        self.username = username
        self.key = key

        date = datetime.utcnow()
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

    def _get_tickets(self):
        tickets = []

        page = 0
        done = False
        while not done:
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

    def _build_ticket_note_urls(self):
        for ticket in self.tickets:
            ticket['ticket']['ticket_note_url'] = (
                'https://api3.codebasehq.com/locus/tickets/{}/notes.json'
            ).format(ticket['ticket']['ticket_id'])

    def _get_ticket_notes(self):
        for ticket in self.tickets:
            response = self.session.get(ticket['ticket']['ticket_note_url'])

            ticket['ticket']['ticket_notes'] = response.json()

    def _filter_todays_ticket_notes(self):
        for ticket in self.tickets:
            ticket['ticket']['ticket_notes'] = filter(
                lambda x: x['ticket_note']['created_at'].startswith(self.date), ticket['ticket']['ticket_notes']
            )

    def get_own_ticket_notes(self):
        self._get_tickets()
        self._build_ticket_note_urls()
        self._get_ticket_notes()
        self._filter_todays_ticket_notes()


if __name__ == '__main__':
    try:
        username, key = argv[1], argv[2]
    except IndexError:
        print('Please pass your username and key', file=stderr)
        exit(1)

    figo = Figo(username, key)
    figo.get_own_ticket_notes()

    print(pformat(figo.tickets))
