from py.client.models import Gift


def get_weight(gift: Gift):
    return gift.weight


def get_volume(gift: Gift):
    return gift.volume


def get_id(gift: Gift):
    return gift.id
