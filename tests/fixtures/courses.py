import pytest
from mixer.backend.django import Mixer

from conftest import N_PER_FIXTURE


@pytest.fixture
def course(mixer: Mixer, category):
    return mixer.blend('courses.Course')


@pytest.fixture
def courses_with_category(mixer: Mixer, category):
    public_courses = N_PER_FIXTURE // 2
    not_public_courses = N_PER_FIXTURE - public_courses

    return (
        mixer.cycle(public_courses).blend('courses.Course', category=category, is_public=True) +
        mixer.cycle(not_public_courses).blend('courses.Course', category=category, is_public=False)
    )


@pytest.fixture
def public_course(mixer: Mixer):
    return mixer.blend('courses.Course', is_public=True)


@pytest.fixture
def not_public_course(mixer: Mixer):
    return mixer.blend('courses.Course', is_public=False)


@pytest.fixture
def user_course(mixer: Mixer, user):
    return mixer.blend('courses.Course', author=user)


@pytest.fixture
def user_courses(mixer: Mixer, user):
    public_courses = N_PER_FIXTURE // 2
    not_public_courses = N_PER_FIXTURE - public_courses

    return (
        mixer.cycle(public_courses).blend('courses.Course', author=user, is_public=True) +
        mixer.cycle(not_public_courses).blend('courses.Course', author=user, is_public=False)
    )
