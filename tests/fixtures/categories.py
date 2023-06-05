import pytest
from mixer.backend.django import Mixer

from conftest import N_PER_FIXTURE


@pytest.fixture
def categories(mixer: Mixer):
    return mixer.cycle(N_PER_FIXTURE).blend('courses.Category')


@pytest.fixture
def category(mixer: Mixer):
    return mixer.blend('courses.Category')
