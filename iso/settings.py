import os

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


settings = {
    'DATABASE': {
        'URL': os.environ.get(
            'DATABASE_URL',
            'postgres://iso:iso123@localhost:5432/iso'),
        'METADATA': Base.metadata
    }
}
