import os

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


settings = {
    'DATABASE': {
        'URL': os.environ.get('DATABASE_URL'),
        'METADATA': Base.metadata
    }
}
