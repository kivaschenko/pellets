from sqlalchemy import (
	Column,
	Integer,
	Numeric,
	String,
	Text
)
from sqlalchemy.orm import relationship
from .meta import Base

class Point(Base):
	__tablename__ = 'point'
	id = Column(Integer, primary_key=True)
	lat = Column(Numeric)
	lng = Column(Numeric)
	address = Column(Text)
	short_name = Column(String(255))
	# relation one-to-many
	offers = relationship("Offer", backref='point')

	def __repr__(self):
		return f'<Point(id={self.id} address={self.address})>'