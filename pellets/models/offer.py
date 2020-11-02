from datetime import datetime
from sqlalchemy import (
	Column,
	Integer,
	Numeric,
	String,
	Text,
	Date,
	DateTime,
	Boolean,
	ForeignKey
)
from sqlalchemy.orm import relationship
from .meta import Base


class Offer(Base):
	"""Represents model for table 'offers' """
	__tablename__ = 'offers'
	offer_id = Column(Integer, primary_key=True)
	goods_id = Column(Integer, ForeignKey(column='goods.id'))
	type_offer = Column(String(10), nullable=False)
	amount = Column(Integer)
	price = Column(Integer)
	incoterms = Column(String(5), nullable=False)
	calorific = Column(Numeric)
	ash = Column(Numeric)
	humidity = Column(Numeric)
	sulfur = Column(Numeric)
	description = Column(Text)
	creation_date = Column(DateTime)
	due_date = Column(Date)
	active = Boolean(create_constraint=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	point_id = Column(Integer, ForeignKey(column='point.id'), nullable=False)

	def __repr__(self):
		return f'<Offer(offer_id={self.offer_id} name={self.name} - price={self.price})>'
	
	def __init__(self, *args, **kwargs):
		"""On constraction, set date of creation """
		super().__init__(*args, **kwargs)
		self.creation_date = datetime.now()


class Goods(Base):
	"""Create table for goods"""
	__tablename__ = 'goods'
	id = Column(Integer, primary_key=True)
	name = Column(String(55), unique=True)
	body = Column(Text)
	offers = relationship("Offer", backref='goods')

	def __repr__(self):
		return f'<Goods(id={self.id} - name={self.name})>'

