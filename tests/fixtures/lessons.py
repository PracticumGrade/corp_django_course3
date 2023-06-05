import pytest
from mixer.backend.django import Mixer

from conftest import N_PER_FIXTURE


@pytest.fixture
def lesson(mixer: Mixer):
    return mixer.blend('lessons.Lesson')


@pytest.fixture
def lesson_with_public_course(mixer: Mixer):
    return mixer.blend('lessons.Lesson', course__is_public=True)


@pytest.fixture
def lesson_with_not_public_course(mixer: Mixer, not_public_course):
    return mixer.blend('lessons.Lesson', course__is_public=False)


@pytest.fixture
def lessons_with_course(mixer: Mixer, public_course):
    return mixer.cycle(N_PER_FIXTURE).blend('lessons.Lesson', course=public_course)


@pytest.fixture
def lesson_with_user_course(mixer: Mixer, user_course):
    return mixer.blend('lessons.Lesson', course=user_course)


@pytest.fixture
def lesson_data(mixer: Mixer):
    with mixer.ctx(commit=False):
        lesson = mixer.blend('lessons.Lesson')
        yield {
            'title': lesson.title,
            'text': lesson.text,
            'type': lesson.type,
            'duration': lesson.duration,
        }
