# built-in imports
import logging
import secrets
import decimal
from datetime import datetime, date, timedelta

import colander
import deform
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPFound,
    HTTPNotFound
)
from pyramid.csrf import check_csrf_token, get_csrf_token

from geopy.geocoders import Nominatim
from .. import models

# define log
log = logging.getLogger(__name__)
# define parameters for geolocator
geolocator = Nominatim(timeout=7, user_agent='offer')

@view_config(route_name='home')
def my_view(request):
    renderer='../templates/home.jinja2'
    return render_to_response(renderer, {}, request)

db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for descriptions and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


@view_config(route_name='create_offer',
             renderer='pellets:templates/offer_edit.jinja2')
def create_offer(request):
    user = request.user
    message = ''
    csrf_token = request.session.get_csrf_token()
    def validate_csrf(node, value):
        if value != csrf_token:
            raise ValueError("Bad CSRF token")
    class CSRFSchema(colander.Schema):
        csrf = colander.SchemaNode(
            colander.String(),
            default=csrf_token,
            validator=validate_csrf,
            widget=deform.widget.HiddenWidget()
        )
    if user is None or user.role not in ('editor', 'base'):
        raise HTTPForbidden
    goods_query = request.dbsession.query(models.Goods.name).all()
    goods_choice = [(item[0], item[0]) for item in goods_query]
    sorted(goods_choice)
    type_offer_choice = (('sell', 'Sell'), ('buy', 'Buy'))
    incoterms_choice = (
        ('EXW', 'EXW - Ex Works'),
        ('FCA', 'FCA - Free Carrier'),
        ('CPT', 'CPT - Carriage Paid To'),
        ('CIP', 'CIP - Carriage and Insurance Paid To'),
        ('DAP', 'DAP - Delivered At Place'),
        ('DPU', 'DPU - Delivered At Place Unloaded'),
        ('DDP', 'DDP - Delivered Duty Paid'),
        ('FAS', 'FAS - Free Alongside Ship'),
        ('FOB', 'FOB - Free On Board'),
        ('CFR', 'CFR - Cost and Feight'),
        ('CIF', 'CIF - Cost Insurance and Freight')
    )
    class OfferSchema(CSRFSchema):
        '''create schema form for view
        '''
        latitude = colander.SchemaNode(colander.String(),
            widget=deform.widget.HiddenWidget())
        longitude = colander.SchemaNode(colander.String(),
            widget=deform.widget.HiddenWidget())
        type_offer = colander.SchemaNode(colander.String(),
            widget=deform.widget.RadioChoiceWidget(values=type_offer_choice),
            validator=colander.OneOf(('sell', 'buy')), title='Type offer')
        goods = colander.SchemaNode(colander.String(),
            widget=deform.widget.SelectWidget(values=goods_choice),
            validator=colander.Length(max=50), title="Goods")
        amount = colander.SchemaNode(colander.Integer(), title='Amount, m ton',
            validator=colander.Range(1,100000))
        price = colander.Schema(colander.Integer(), title='Price, $',
            validator=colander.Range(1,100000))
        incoterms = colander.SchemaNode(colander.String(encoding='utf-8'),
            widget=deform.widget.RadioChoiceWidget(values=incoterms_choice),
            validator=colander.OneOf(x[0] for x in incoterms_choice),
            title='Incoterms 2020')
        body = colander.SchemaNode(colander.String(encoding='utf-8'),
            widget=deform.widget.TextAreaWidget(cols=5, rows=5),
            validator=colander.Length(max=255),title='Short description')
        def default_due_date():
            today = date.today()
            days = timedelta(days=30)
            return today + days
        due_date = colander.SchemaNode(colander.Date(),
            widget=deform.widget.DateInputWidget(),
            default=default_due_date(),
            validator=colander.Range(min=date.today(),
            min_err=('${val} earler than today ${min}')),
            title='Due date offer')
        active = colander.SchemaNode(colander.Boolean(), default=True,
            widget=deform.widget.HiddenWidget())
        diameter = colander.SchemaNode(colander.Integer(), title='Diameter mm',
            default=6, validator=colander.Range(1,120))
        length_min = colander.SchemaNode(colander.Decimal(),
            title="Length minimum, mm", default=3.15,
            validator=colander.Range(min=0, max=decimal.Decimal("99.99")),
            widget=deform.widget.TextInputWidget(
                attributes={
                    "type": "number",
                    "inputmode": "decimal",
                    "step": "0.01",
                    "min": "0",
                    "max": "99.99",
                }
            ),
        )
        length_max = colander.SchemaNode(colander.Decimal(),
            title="Length maximum, mm", default=40.00,
            validator=colander.Range(min=0, max=decimal.Decimal("99.99")),
            widget=deform.widget.TextInputWidget(
                attributes={
                    "type": "number",
                    "inputmode": "decimal",
                    "step": "0.01",
                    "min": "0",
                    "max": "99.99",
                }
            ),
        )
        bulk_density = colander.SchemaNode(colander.Integer(),
            title="Bulk density, kg/m3", default=651,
            validator=colander.Range(0, 1000))
        net_calorific_value = colander.SchemaNode(colander.Decimal(),
            title="Net calorific value, MJ/kg", default=18.4,
            validator=colander.Range(min=1, max=decimal.Decimal("99.99")),
            widget=deform.widget.TextInputWidget(
                attributes={
                    "type": "number",
                    "inputmode": "decimal",
                    "step": "0.1",
                    "min": "1",
                    "max": "99.99",
                }
            ),
        )
        moisture_content = colander.SchemaNode(colander.Integer(),
            title="Moisture content, less than, wt%", default=10,
            validator=colander.Range(1,99))
        fines = colander.SchemaNode(colander.Integer(),
            title="Fines (<3.15 mm), less than, wt%", default=1,
            validator=colander.Range(1,99))
        mechanical_durability = colander.SchemaNode(colander.Decimal(),
            title="Mechanical durability, more than, wt%", default=97.5,
            validator=colander.Range(min=1, max=decimal.Decimal("99.99")),
            widget=deform.widget.TextInputWidget(
                attributes={
                    "type": "number",
                    "inputmode": "decimal",
                    "step": "0.1",
                    "min": "0",
                    "max": "99.99",
                }
            ),
        )
        ash_content = colander.SchemaNode(colander.Decimal(),
            title="Ash content, less than, wt%", default=0.7,
            validator=colander.Range(min=0, max=decimal.Decimal("99.99")),
            widget=deform.widget.TextInputWidget(
                attributes={
                    "type": "number",
                    "inputmode": "decimal",
                    "step": "0.1",
                    "min": "0",
                    "max": "99.99",
                }
            ),
        )
        ash_melting_temp = colander.SchemaNode(colander.Integer(),
            title="Ash melting temperature, more than, K", default=1473,
            validator=colander.Range(1000,10000))
    schema = OfferSchema().bind(request=request)
    button = deform.form.Button(name='submit', title="Add the offer",
        type='submit')
    form = deform.Form(schema, buttons=(button,), autocomplete='off')
    if request.method == 'POST' and 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            location = geolocator.reverse((appstruct['latitude'],
                     appstruct['longitude']))
            offer = models.Offer(
                type_offer=appstruct['type_offer'],
                goods=appstruct['goods'],
                amount=appstruct['amount'],
                price=appstruct['price'],
                incoterms=appstruct['incoterms'],
                body=appstruct['body'],
                due_date=appstruct['due_date'],
                active=appstruct['active'],
                user_id=user.id,
                lat=appstruct['latitude'],
                lng=appstruct['longitude'],
                address=location.address,
                country=location.address.split(',')[-1],
                length_min=appstruct['length_min'],
                length_max=appstruct['length_max'],
                bulk_density=appstruct['bulk_density'],
                net_calorific_value=appstruct['net_calorific_value'],
                moisture_content=appstruct['moisture_content'],
                fines=appstruct['fines'],
                mechanical_durability=appstruct['mechanical_durability'],
                ash_content=appstruct['ash_content'],
                ash_melting_temp=appstruct['ash_melting_temp']
            )
            request.dbsession.add(offer)
            next_url = request.route_url('home')
            return HTTPFound(location=next_url)
        except deform.exception.ValidationFailure as e:
            return dict(
                form=e,
                message=message
            )
    return dict(
        message=message,
        form=form
    )


@view_config(route_name='offers', renderer='../templates/offers.jinja2')
def offers(request):
    query = request.dbsession.query(models.Offer).all()
    offers = [q.__dict__ for q in query]
    return dict(offers=offers)

@view_config(route_name='view_offer',
             renderer='../templates/offer_detail.jinja2')
def view_offer(request):
    offer_id = request.matchdict['offer_id']
    query = request.dbsession.query(models.Offer).get(offer_id)
    offer = query.__dict__
    title_offer = ' '.join([offer['type_offer'], offer['goods']]).title()
    autor = request.dbsession.query(models.User).get(offer['user_id'])
    owner_offer = autor.__dict__
    message = ''
    csrf_token = request.session.get_csrf_token()
    def validate_csrf(node, value):
        if value != csrf_token:
            raise ValueError("Bad CSRF token")
        return
    class CSRFSchema(colander.Schema):
        csrf = colander.SchemaNode(
            colander.String(),
            default=csrf_token,
            validator=validate_csrf,
            widget=deform.widget.HiddenWidget(),
        )
    class MySchema(CSRFSchema):
        text = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(max=255),
            widget=deform.widget.TextInputWidget()
        )
    schema = MySchema().bind(request=request)
    form = deform.Form(schema, buttons=("submit",))
    if request.method == 'POST' and 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            letter = appstruct['text']
            print(letter)
            return HTTPFound(location=request.url)
        except deform.exception.ValidationFailure as e:
            return dict(
                form=e,
                message=message,
                offer=offer,
                owner_offer=owner_offer,
                title_offer=title_offer
            )
    return dict(
        offer=offer,
        message=message,
        form=form,
        owner_offer=owner_offer,
        title_offer=title_offer
    )
