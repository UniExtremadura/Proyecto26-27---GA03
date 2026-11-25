"""Registro de navegación y buscadores que cada módulo rellena al importarse."""
_NAV = []
_SEARCH = []


def register_nav(label, endpoint, section="Servicios", order=100):
    _NAV.append({"label": label, "endpoint": endpoint, "section": section, "order": order})


def nav_items():
    return sorted(_NAV, key=lambda i: (i["section"], i["order"], i["label"]))


def register_search(provider):
    """provider(q) -> lista de dicts {title, url, section}."""
    _SEARCH.append(provider)


def search_providers():
    return list(_SEARCH)
