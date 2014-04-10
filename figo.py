from __future__ import print_function

import logging
from datetime import datetime
from itertools import chain
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
from pprint import pformat
from sys import argv
from sys import exit
from sys import stderr

from requests import Session

from pickle_hack import pickle_hack


log = logging.getLogger(__name__)

log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class Figo(object):

    def __init__(self, username, key):
        self.username = username
        self.key = key

        date = datetime.utcnow()
        self.date = date.strftime('%Y-%m-%d')

        pickle_hack()

    def _create_session(self):
        session = Session()
        session.auth = self.username, self.key

        return session

    def _get_ticket_page(self, page):
        log.debug('Getting ticket page {}.'.format(page))

        session = self._create_session()
        response = session.get((
            'https://api3.codebasehq.com/locus/tickets.json?query=sort:updated_at+update:"{}"&'
            'page={}'
        ).format(self.date, page))

        if response.status_code != 200:
            return tuple()
        else:
            return response.json()

    def _get_tickets(self):
        total_results = []

        core_count = 16
        pool = Pool(core_count)

        offset = 0
        done = False
        while not done:
            pages = range(offset * core_count, (offset + 1) * core_count)
            results = pool.map(self._get_ticket_page, pages)

            total_results.extend(results)

            offset += 1

            result_lengths = map(len, results)
            truncated_results = filter(lambda x: x < 20, result_lengths)
            done = len(truncated_results) != 0

        self.tickets = chain(*total_results)

    def _build_ticket_note_urls(self):
        ticket_ids = map(lambda x: x['ticket']['ticket_id'], self.tickets)
        self.ticket_note_urls = map(
            lambda x: 'https://api3.codebasehq.com/locus/tickets/{}/notes.json'.format(x),
            ticket_ids
        )

    def _get_ticket_note(self, url):
        log.debug('Getting ticket note {}.'.format(url))

        session = self._create_session()
        response = session.get(url)

        return response.json()

    def _get_ticket_notes(self):
        core_count = 16
        pool = Pool(core_count)

        ticket_notes = pool.map(self._get_ticket_note, self.ticket_note_urls)
        self.ticket_notes = chain(*ticket_notes)

    def _filter_todays_ticket_notes(self):
        self.ticket_notes = filter(lambda x: x['ticket_note']['created_at'].startswith(self.date), self.ticket_notes)

    def _get_user_id(self):
        log.debug('Getting user ID.')

        # username is in the format <domain>/<username>, we want just <username>
        simple_username = self.username[self.username.find('/') + 1:]

        session = self._create_session()

        response = session.get('https://api3.codebasehq.com/locus/assignments.json')
        users = response.json()

        current_users = filter(lambda x: x['user']['username'] == simple_username, users)
        current_user = current_users[0]

        self.user_id = current_user['user']['id']

    def _filter_own_ticket_notes(self):
        self.ticket_notes = filter(lambda x: x['ticket_note']['user_id'] == self.user_id, self.ticket_notes)

    def get_own_ticket_notes(self):
        self._get_tickets()
        self._build_ticket_note_urls()
        self._get_ticket_notes()
        self._get_user_id()
        self._filter_todays_ticket_notes()
        self._filter_own_ticket_notes()


if __name__ == '__main__':
    try:
        username, key = argv[1], argv[2]
    except IndexError:
        print('Please pass your username and key', file=stderr)
        exit(1)

    figo = Figo(username, key)
    figo.get_own_ticket_notes()
    notes = map(lambda x: x['ticket_note']['content'], figo.ticket_notes)

    print(pformat(notes))
