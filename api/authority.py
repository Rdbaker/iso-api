import typing
from datetime import datetime as dt, timedelta as td

import dateutil.parser
import pytz
from apistar import http
from pyiso import BALANCING_AUTHORITIES, client_factory


def jsonify_data(gen):
    if 'timestamp' in gen:
        gen['timestamp'] = str(gen['timestamp'])
    return gen


def get_dt_from_string(date_string, default_dt=None):
    """Return a datetime either from the coerced date string or the default."""
    try:
        date = dateutil.parser.parse(date_string)
        if date.tzinfo is None:
            return default_dt
        return date
    except:
        return default_dt


def get_authorities() -> typing.List[typing.Text]:
    """Get a list of the balancing authorities."""
    return [dict(code=code) for code in BALANCING_AUTHORITIES.keys()]


def get_authority_generation(authority: typing.Text, start_at: http.QueryParam, end_at: http.QueryParam):
    """Get a timeseries of energy generation for a balancing authority."""
    start_dt = get_dt_from_string(
        start_at,
        default_dt=pytz.utc.localize(dt.utcnow() - td(days=1))
    )
    end_dt = get_dt_from_string(
        end_at,
        default_dt=pytz.utc.localize(dt.utcnow())
    )
    auth_client = client_factory(authority)
    gen = auth_client.get_generation(start_at=start_dt, end_at=end_dt)
    return [jsonify_data(g) for g in gen]


def get_authority_load(authority: typing.Text, start_at: http.QueryParam, end_at: http.QueryParam):
    """Get a timeseries of energy load for a balancing authority."""
    start_dt = get_dt_from_string(
        start_at,
        default_dt=pytz.utc.localize(dt.utcnow() - td(days=1))
    )
    end_dt = get_dt_from_string(
        end_at,
        default_dt=pytz.utc.localize(dt.utcnow())
    )
    auth_client = client_factory(authority)
    gen = auth_client.get_load(start_at=start_dt, end_at=end_dt)
    return [jsonify_data(g) for g in gen]


def get_authority_trade(authority: typing.Text, start_at: http.QueryParam, end_at: http.QueryParam):
    """Get a timeseries of energy trade data for a balancing authority."""
    start_dt = get_dt_from_string(
        start_at,
        default_dt=pytz.utc.localize(dt.utcnow() - td(days=1))
    )
    end_dt = get_dt_from_string(
        end_at,
        default_dt=pytz.utc.localize(dt.utcnow())
    )
    auth_client = client_factory(authority)
    gen = auth_client.get_trade(start_at=start_dt, end_at=end_dt)
    return [jsonify_data(g) for g in gen]


def get_authority_lmp(authority: typing.Text, start_at: http.QueryParam, end_at: http.QueryParam):
    """Get a timeseries of energy lmp for a balancing authority."""
    start_dt = get_dt_from_string(
        start_at,
        default_dt=pytz.utc.localize(dt.utcnow() - td(days=1))
    )
    end_dt = get_dt_from_string(
        end_at,
        default_dt=pytz.utc.localize(dt.utcnow())
    )
    auth_client = client_factory(authority)
    gen = auth_client.get_lmp(start_at=start_dt, end_at=end_dt)
    return [jsonify_data(g) for g in gen]
