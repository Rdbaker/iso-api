import typing

from apistar import Include, Route, typesystem
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls

from api.authority import (get_authorities, get_authority_generation,
                           get_authority_load, get_authority_lmp,
                           get_authority_trade)


class Authority(typesystem.Object):
    """A balancing authority."""
    properties = {
        'code': typing.Text
    }


def welcome(name=None):
    """This is the welcome docstring."""
    if name is None:
        return {'message': 'Welcome to API Star!'}
    return {'message': 'Welcome to API Star, %s!' % name}


routes = [
    Route('/', 'GET', welcome),
    Route('/authorities/', 'GET', get_authorities),
    Route('/authorities/{authority}/gen/', 'GET', get_authority_generation),
    Route('/authorities/{authority}/load/', 'GET', get_authority_load),
    Route('/authorities/{authority}/lmp/', 'GET', get_authority_lmp),
    Route('/authorities/{authority}/trade/', 'GET', get_authority_trade),
    Include('/docs', docs_urls),
    Include('/static', static_urls)
]

app = App(routes=routes)


if __name__ == '__main__':
    app.main()
