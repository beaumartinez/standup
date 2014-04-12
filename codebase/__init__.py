import logging
from collections import defaultdict
from datetime import datetime
from datetime import timedelta

from requests import Session

from .parser import parse_ticket
from .parser import parse_ticket_note
from .parser import parse_user


log = logging.getLogger(__name__)

log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class Codebase(object):

    def __init__(self, username, key, project):
        self.username = username
        self.key = key

        self.project = project

        date = datetime.utcnow() - timedelta(days=1)
        self.date = date.strftime('%Y-%m-%d')

        self.session = self._create_session()

    def _create_session(self):
        session = Session()
        session.auth = self.username, self.key

        return session

    def _get_tickets(self):
        tickets = []

        page = 0
        done = False
        while not done:
            log.debug('Getting tickets page {}.'.format(page))

            response = self.session.get((
                'https://api3.codebasehq.com/{}/tickets.json?query=sort:updated_at+update:"{}"&'
                'page={}'
            ).format(self.project, self.date, page))

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
                'https://api3.codebasehq.com/{}/tickets/{}/notes.json'
            ).format(self.project, ticket.ticket_id)

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

    def _get_users(self):
        log.debug('Getting users.')

        response = self.session.get('https://api3.codebasehq.com/{}/assignments.json'.format(self.project))
        self.users = response.json()

    def _parse_users(self):
        self.users = map(parse_user, self.users)

    def _build_user_id_lookup(self):
        user_lookup = {}

        for user in self.users:
            user_lookup[user.id] = user.username

        self.user_lookup = user_lookup

    def _set_ticket_note_usernames(self):
        for ticket in self.tickets:
            for note in ticket.ticket_notes:
                note.username = self.user_lookup[note.user_id]

    def _group_user_ticket_lookup(self):
        user_ticket_lookup = defaultdict(set)

        for ticket in self.tickets:
            for note in ticket.ticket_notes:
                user_ticket_lookup[note.username].add('{}: {}'.format(ticket.ticket_id, ticket.summary))

        self.user_ticket_lookup = user_ticket_lookup

    def get_tickets(self):
        self._get_tickets()
        self._parse_tickets()
        self._build_ticket_note_urls()
        self._get_ticket_notes()
        self._parse_ticket_notes()
        self._filter_todays_ticket_notes()
        self._get_users()
        self._parse_users()
        self._build_user_id_lookup()
        self._set_ticket_note_usernames()
        self._group_user_ticket_lookup()
