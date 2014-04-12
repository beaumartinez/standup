class Struct(object):

    def __init__(self, **entries): 
        self.__dict__.update(entries)


def _whitelist(keys, dict_):
    return {key: dict_[key] for key in keys}


def parse_ticket(ticket):
    ticket = ticket['ticket']

    return Struct(**_whitelist((
        'summary',
        'ticket_id',
    ), ticket))


def parse_ticket_note(ticket_note):
    ticket_note = ticket_note['ticket_note']

    return Struct(**_whitelist((
        'content',
        'created_at',
        'updates',
        'user_id',
    ), ticket_note))
