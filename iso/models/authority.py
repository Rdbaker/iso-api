from sqlalchemy import Column, Integer, String, DateTime

from iso.settings import Base


class GenerationDatum(Base):
    """A model for a single point of generation data."""

    __tablename__ = "generation"
    authority_code = Column(String, primary_key=True)
    timestamp = Column(DateTime(timezone=True), primary_key=True)
    fuel_name = Column(String, primary_key=True)
    gen_MW = Column(Integer, nullable=False)
    frequency = Column(String, nullable=False)
    # not sure what this means...but it's in the data, so I'm keeping it!
    market = Column(String, nullable=False)

    def __hash__(self):
        return hash("{0}{1}{2}".format(
            self.authority_code,
            self.timestamp,
            self.fuel_name)
        )

    def __eq__(self, other):
        return isinstance(other, GenerationDatum) and \
            self.__hash__() == other.__hash__()


class DatumMeta(Base):
    """A representation of the range of local data."""

    __tablename__ = "authority_metadata"
    authority_code = Column(String, primary_key=True)
    most_recent = Column(DateTime(timezone=True), primary_key=True)
    least_recent = Column(DateTime(timezone=True), primary_key=True)
    data_type = Column(String, primary_key=True)  # this is the other table name
