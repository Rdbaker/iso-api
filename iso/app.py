"""An application factory pattern to create a new APIStar application."""
from apistar import Include, Route
from apistar.backends import sqlalchemy_backend
from apistar.frameworks.wsgi import WSGIApp as App
from apistar.handlers import docs_urls, static_urls
from apistar_alembic_migrations import commands

from iso.api.authority import (get_authorities, get_authority_generation,
                               get_authority_load, get_authority_lmp,
                               get_authority_trade)
from iso.settings import settings


def create_app(config=None):
    """Create an apistar app from this factory."""
    routes = create_routes()
    app = App(
        routes=routes,
        commands=commands,
        components=sqlalchemy_backend.components,
        settings=settings,
    )
    return app


def welcome(name=None):
    """Return the welcome docstring."""
    if name is None:
        return {'message': 'Welcome to the ISO API!'}
    return {'message': 'Welcome to the ISO API, %s!' % name}


def create_routes():
    """Create the routes for the application."""
    return [
        Route('/', 'GET', welcome),
        Route('/authorities/', 'GET', get_authorities),
        Route('/authorities/{authority}/gen/', 'GET', get_authority_generation),
        Route('/authorities/{authority}/load/', 'GET', get_authority_load),
        Route('/authorities/{authority}/lmp/', 'GET', get_authority_lmp),
        Route('/authorities/{authority}/trade/', 'GET', get_authority_trade),
        Include('/docs', docs_urls),
        Include('/static', static_urls)
    ]


if __name__ == '__main__':
    app = create_app()
    app.main()
