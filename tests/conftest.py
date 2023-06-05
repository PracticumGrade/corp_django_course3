import pytest
from mixer.backend.django import mixer as _mixer
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model


User = get_user_model()


N_PER_FIXTURE = 10
N_PER_PAGE = 3

pytest_plugins = [
    'fixtures.lessons',
    'fixtures.categories',
    'fixtures.courses',
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def anonymous_user():
    return AnonymousUser()


@pytest.fixture
def user(mixer):
    user = mixer.blend(User)
    return user


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def another_user(mixer):
    user = mixer.blend(User, username='another_user')
    return user


@pytest.fixture
def another_user_client(another_user, client):
    client.force_login(another_user)
    return client


@pytest.fixture
def unlogged_client(client):
    return client
