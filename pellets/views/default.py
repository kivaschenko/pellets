# built-in imports
import logging
import secrets
from datetime import datetime, date

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

@view_config(route_name="offers",
             renderer='pellets:templates/offers.jinja2')
def offers(request):
    try:
        query = request.dbsession.query(models.Offer).all()
    except DBAPIError:
        return Response(db_err_msg, content_type='text/plain', status=500)
    print(query)
    return {'offers': query}


@view_config(route_name='offer_action', match_param='action=create',
             renderer='pellets:templates/offer_edit.jinja2',
             permission='create')
def offer_create(request):
    user = request.user
    # creator = request.dbsession.query(models.User).filter_by(id=user.id).first()
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
    class OfferSchema(colander.Schema):
        '''create schema form for view
        '''
        token = secrets.token_urlsafe(16)
        csrf_token = colander.SchemaNode(colander.String(),
            widget=deform.widget.HiddenWidget(), default=token)
        latitude = colander.SchemaNode(colander.String(),
            widget=deform.widget.HiddenWidget())
        longitude = colander.SchemaNode(colander.String(),
            widget=deform.widget.HiddenWidget())
        goods = colander.SchemaNode(colander.String(),
            widget=deform.widget.SelectWidget(values=goods_choice),
            validator=colander.Length(max=50), title="Goods")
        type_offer = colander.SchemaNode(colander.String(),
            widget=deform.widget.RadioChoiceWidget(values=type_offer_choice),
            validator=colander.OneOf(('sell', 'buy')), title='Type offer')
        amount = colander.SchemaNode(colander.Integer(), title='Amount, m ton')
        price = colander.Schema(colander.Integer(), title='Price, $',
            validator=colander.Range(1,100000))
        incoterms = colander.SchemaNode(colander.String(encoding='utf-8'),
            widget=deform.widget.RadioChoiceWidget(values=incoterms_choice),
            validator=colander.OneOf(x[0] for x in incoterms_choice),
            title='Incoterms 2020')
        body = colander.SchemaNode(colander.String(encoding='utf-8'),
            widget=deform.widget.TextAreaWidget(cols=5, rows=5),
            validator=colander.Length(max=255),title='Short description')
        due_date = colander.SchemaNode(colander.Date(),
            widget=deform.widget.DateInputWidget(),
            validator=colander.Range(min=date.today(),
            min_err=('${val} earler than today ${min}')),
            title='Due date offer')
        active = colander.SchemaNode(colander.Boolean(), default=True,
            title='Offer is active')
    schema = OfferSchema().bind(request=request)
    button = deform.form.Button(name='submit', title="Add the offer",
        type='submit')
    form = deform.Form(schema, buttons=(button,), autocomplete='off')
    if request.method == 'POST':
        if 'submit' in request.POST:
            appstruct = form.validate(request.POST.items())
            print(appstruct)
            goods_id = request.dbsession.query(models.Goods.id).filter_by(
                     name=appstruct['goods']).first()
            print('goods_id', goods_id)
            location = geolocator.reverse((appstruct['latitude'],
                                           appstruct['longitude']))
            print('location', location)
            offer = models.Offer(
                goods_id=goods_id,
                type_offer=appstruct['type_offer'],
                amount=appstruct['amount'],
                price=appstruct['price'],
                incoterms=appstruct['incoterms'],
                body=appstruct['body'],
                due_date=appstruct['due_date'],
                active=appstruct['active'],
                user_id=user.id,
                lat=appstruct['latitude'],
                lng=appstruct['longitude'],
                address=location.address
            )
            print(offer)
            request.dbsession.add(offer)
            next_url = request.route_url('offers')
            return HTTPFound(location=next_url)
    return {'form': form}
