import logging
import typing
from datetime import datetime as dt, timedelta as td

import dateutil.parser
import pytz
from apistar.backends.sqlalchemy_backend import Session
from apistar import http
from pyiso import BALANCING_AUTHORITIES, client_factory

from iso.models.authority import GenerationDatum, DatumMeta
from iso.schema.authority import Authority, GenerationDatum as GenerationDatumSchema


def jsonify_data(gen):
    if 'timestamp' in gen:
        gen['timestamp'] = str(gen['timestamp'])
    return gen


def pull_gen_data(gen_data):
    """Essentially just turn the 'ba_name' key into 'authority_code'."""
    def transform(g):
        g['authority_code'] = g['ba_name']
        g['frequency'] = g['freq']
        del g['ba_name']
        del g['freq']
        return g
    return [transform(g) for g in gen_data]


def get_dt_from_string(date_string, default_dt=None):
    """Return a datetime either from the coerced date string or the default."""
    try:
        date = dateutil.parser.parse(date_string)
        if date.tzinfo is None:
            return default_dt
        return date
    except:
        return default_dt


def get_authorities() -> typing.List[Authority]:
    """Get a list of the balancing authorities."""
    return [Authority(code=code) for code in BALANCING_AUTHORITIES.keys()]


def get_authority_generation(
        session: Session, authority: typing.Text, start_at: http.QueryParam,
        end_at: http.QueryParam) -> typing.List[GenerationDatumSchema]:
    """Get a timeseries of energy generation for a balancing authority."""
    start_dt = get_dt_from_string(
        start_at,
        default_dt=pytz.utc.localize(dt.utcnow() - td(days=1))
    )
    end_dt = get_dt_from_string(
        end_at,
        default_dt=pytz.utc.localize(dt.utcnow())
    )

    meta = session.query(DatumMeta).filter_by(
        authority_code=authority,
        data_type=GenerationDatum.__tablename__
    ).first()
    new_meta = False
    # we might not have the metadata for this authority/data_type combo
    if meta is None:
        new_meta = True
        meta = DatumMeta(
            authority_code=authority,
            most_recent=end_dt,
            least_recent=start_dt,
            data_type=GenerationDatum.__tablename__,
        )
    if not new_meta and \
            (meta.most_recent + td(minutes=5)) >= end_dt and \
            meta.least_recent <= start_dt:
        logging.info('requested data is stored in database')
    elif meta.most_recent >= end_dt and not (meta.least_recent <= start_dt):
        logging.info('requested data is strictly older than stored data')
        auth_client = client_factory(authority)
        new_data = auth_client.get_generation(
            start_at=start_dt, end_at=meta.least_recent)
        gen_models = [GenerationDatum(**g) for g in pull_gen_data(new_data)]
        meta.least_recent = start_dt
        session.add_all(gen_models + [meta])
        session.flush()
    elif not (meta.most_recent >= end_dt) and meta.least_recent <= start_dt:
        logging.info('requested data is strictly newer than stored data')
        auth_client = client_factory(authority)
        new_data = auth_client.get_generation(
            start_at=meta.most_recent, end_at=end_dt)
        gen_models = [GenerationDatum(**g) for g in pull_gen_data(new_data)]
        meta.most_recent = end_dt
        session.add_all(gen_models + [meta])
        session.flush()
    else:
        logging.info('requested data is a superset of stored data')
        auth_client = client_factory(authority)
        left_hand_data = auth_client.get_generation(
            start_at=meta.least_recent, end_at=end_dt)
        right_hand_data = auth_client.get_generation(
            start_at=start_dt, end_at=meta.most_recent)
        gen_models = list(set([
            GenerationDatum(**g)
            for g in pull_gen_data(left_hand_data + right_hand_data)
        ]))
        meta.most_recent = end_dt
        meta.least_recent = start_dt
        session.add_all(gen_models + [meta])
        session.flush()

    filter_set = [
        GenerationDatum.authority_code == authority,
        GenerationDatum.timestamp <= end_dt,
        GenerationDatum.timestamp >= start_dt,
    ]
    query_set = session.query(GenerationDatum).filter(*filter_set).all()
    return [GenerationDatumSchema(g) for g in query_set]


def get_authority_load(
        session: Session, authority: typing.Text, start_at: http.QueryParam,
        end_at: http.QueryParam):
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


def get_authority_trade(
        session: Session, authority: typing.Text, start_at: http.QueryParam,
        end_at: http.QueryParam):
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


def get_authority_lmp(
        session: Session, authority: typing.Text, start_at: http.QueryParam,
        end_at: http.QueryParam):
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
