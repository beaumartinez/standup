def _whitelist(keys, dict_):
    return {key: dict_[key] for key in keys}


def parse_ticket(ticket):
    ticket = ticket['ticket']

    return _whitelist((
        'summary',
        'ticket_id',
    ), ticket)


def parse_ticket_note(ticket_note):
    ticket_note = ticket_note['ticket_note']

    return _whitelist((
        'content',
        'created_at',
        'updates',
        'user_id',
    ), ticket_note)
