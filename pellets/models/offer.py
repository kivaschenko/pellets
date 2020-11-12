from datetime import date
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
	"""Represents model for table 'offer' """
	__tablename__ = 'offer'
	id = Column(Integer, primary_key=True)
	type_offer = Column(String(10), nullable=False)
	goods = Column(String(55), nullable=False)
	amount = Column(Integer, nullable=False)
	price = Column(Integer, nullable=False)
	incoterms = Column(String(5), nullable=False)
	body = Column(Text)
	creation_date = Column(Date)
	due_date = Column(Date)
	active = Boolean(create_constraint=True)
	user_id = Column(Integer, ForeignKey('user.id'))
	lat = Column(Numeric)
	lng = Column(Numeric)
	address = Column(Text)
	country = Column(String(255))
	# new technical parameters
	diameter = Column(Integer)
	length_min = Column(Numeric)
	length_max = Column(Numeric)
	bulk_density = Column(Integer)
	net_calorific_value = Column(Numeric)
	moisture_content = Column(Integer)
	fines = Column(Integer)
	mechanical_durability = Column(Numeric)
	ash_content = Column(Numeric)
	ash_melting_temp = Column(Integer)
	# chlorine_content = Column(Numeric)
	# sulphur_content = Column(Numeric)
	# nitrogen_content = Column(Numeric)
	# copper_content = Column(Numeric)
	# chromium_content = Column(Numeric)
	# arsenic_content = Column(Numeric)
	# cadmium_content = Column(Numeric)
	# mercury_content = Column(Integer)
	# lead_content = Column(Integer)
	# nickel_content = Column(Integer)
	def __repr__(self):
		return f'<Offer(offer_id={self.id} {self.type_offer} {self.goods}: \
${self.price} - {self.amount} ton)>'

	def __init__(self, *args, **kwargs):
		"""On constraction, set date of creation """
		super().__init__(*args, **kwargs)
		self.creation_date = date.today()


class Goods(Base):
	"""Create table for goods"""
	__tablename__ = 'goods'
	id = Column(Integer, primary_key=True)
	name = Column(String(55), unique=True)
	body = Column(Text)

	def __repr__(self):
		return f'<Goods(id={self.id} - name={self.name})>'
