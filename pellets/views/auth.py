from pyramid.httpexceptions import HTTPFound
from deform.exception import ValidationFailure
from pyramid.view import (
    view_config,
    forbidden_view_config
)
from pyramid.security import (
    remember,
    forget
    )
import colander
import deform

from ..models import User

class LoginSchema(colander.MappingSchema):
    username = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(max=100),
            widget=deform.widget.TextInputWidget())
    password = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(min=5, max=100),
            widget=deform.widget.PasswordWidget(redisplay=True))
schema = LoginSchema()
button = deform.form.Button(name='submit', title='Додати пропозицію',
        type='submit')


@view_config(renderer='../templates/login.jinja2', route_name='login')
def login(request):
    message = ''
    next_url = request.route_url('home')
    form = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            username = appstruct['username']
            password = appstruct['password']
            user = request.dbsession.query(User).filter_by(nickname=username).first()
            # check password
            if user is not None and user.check_password(password):
                headers = remember(request, user.id)
                return HTTPFound(location=next_url, headers=headers)
            else:
                message = 'Failed login or password!'
        except ValidationFailure as e:
            return dict(
                form=e,
                message=message
            )
    return dict(
        form=form,
        message=message
        )


@view_config(route_name='logout')
def logout(request):
    headers = forget(request)
    next_url = request.route_url('home')
    return HTTPFound(location=next_url, headers=headers)


@forbidden_view_config()
def forbidden_view(request):
    next_url = request.route_url('login', _query={'next': request.url})
    return HTTPFound(location=next_url)


@view_config(renderer='../templates/signup.jinja2', route_name='signup')
def signup(request):
    next_url = request.route_url('home')
    message = ''
    class SignupSchema(colander.MappingSchema):
        username = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(max=100),
            widget=deform.widget.TextInputWidget()
        )
        email = colander.SchemaNode(
            colander.String(),
            validator=colander.Email(msg="Введіть дійсний email"),
        )
        password = colander.SchemaNode(
            colander.String(),
            validator=colander.Length(min=5),
            widget=deform.widget.CheckedPasswordWidget(),
            description="Type your password and confirm it",
        )
    schema = SignupSchema()
    button = deform.form.Button(name='submit', title='Реєстрація',type='submit')
    form = deform.Form(schema, buttons=('submit',))
    if 'submit' in request.POST:
        controls = request.POST.items()
        try:
            appstruct = form.validate(controls)
            username = appstruct['username']
            email = appstruct['email']
            password = appstruct['password']
            nick_check = request.dbsession.query(User).\
                filter_by(nickname=username).first()
            email_check = request.dbsession.query(User).\
                filter_by(email=email).first()
            if nick_check is None and email_check is None:
                new_user = User(nickname=username, email=email, role='base')
                new_user.set_password(password)
                # add new user to db
                request.dbsession.add(new_user)
                # get user id
                user = request.dbsession.query(User).\
                    filter_by(nickname=username).first()
                # check password
                if user is not None and user.check_password(password):
                    headers = remember(request, user.id)
                    return HTTPFound(location=next_url, headers=headers)
            else:
                message = 'Такий користувач або емайл вже зареєстрований'
        except ValidationFailure as e:
            return dict(
                form=e,
                message=message
            )
    return dict(
        form=form,
        message=message
    )
