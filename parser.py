class Struct(object):

    def __init__(self, **entries): 
        self.__dict__.update(entries)


def _whitelist(keys, dict_):
    return {key: dict_[key] for key in keys}


def _whitelist_as_struct(keys, dict_):
    return Struct(**_whitelist(keys, dict_))


def parse_ticket(ticket):
    ticket = ticket['ticket']

    return _whitelist_as_struct((
        'summary',
        'ticket_id',
    ), ticket)


def parse_ticket_note(ticket_note):
    ticket_note = ticket_note['ticket_note']

    return _whitelist_as_struct((
        'content',
        'created_at',
        'updates',
        'user_id',
    ), ticket_note)


def parse_user(user):
    user = user['user']

    return _whitelist_as_struct((
        'id',
        'username',
    ), user)
