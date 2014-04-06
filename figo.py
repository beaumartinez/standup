from __future__ import print_function

from multiprocessing import Pool
from multiprocessing import cpu_count
from sys import argv
from sys import exit
from sys import stderr

from requests import Session

from pickle_hack import pickle_hack


class Figo(object):

    def __init__(self, username, key):
        self.username = username
        self.key = key

        pickle_hack()

    def _create_session(self):
        session = Session()
        session.auth = self.username, self.key

        return session

    def _get_ticket_page(self, page):
        session = self._create_session()
        response = session.get((
            'https://api3.codebasehq.com/locus/tickets.json?query=sort:updated_at&'
            'page={}'
        ).format(page))

        if response.status_code != 200:
            return None
        else:
            return response.json()

    def _get_tickets(self):
        total_results = []

        core_count = cpu_count()

        offset = 0
        done = False
        while not done:
            pages = range(offset * core_count, (offset + 1) * core_count)

            pool = Pool()
            results = pool.map(self._get_ticket_page, pages)

            total_results.extend(results)

            offset += 1
            done = None in results

        self.total_results = filter(lambda x: x is not None, total_results)


if __name__ == '__main__':
    try:
        username, key = argv[1], argv[2]
    except IndexError:
        print('Please pass your username and key', file=stderr)
        exit(1)

    figo = Figo(username, key)
    figo._get_tickets()

    print(figo.total_results)
