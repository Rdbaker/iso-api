"""The authority schema."""
import typing

from apistar import typesystem


class Authority(typesystem.Object):
    """A balancing authority."""

    properties = {
        'code': typing.Text
    }


class GenerationDatum(typesystem.Object):
    """A generation datum from an authority."""
    properties = {
        'authority_code': typesystem.String,
        'frequency': typesystem.String,
        'timestamp': typesystem.String,
        'fuel_name': typesystem.String,
        'gen_MW': typesystem.Integer,
        'market': typesystem.String,
    }
