from http import HTTPStatus

from pytest_django.asserts import assertTemplateUsed
import pytest

from utils import get_response_safely, get_reverse_url

pytestmark = [
    pytest.mark.django_db,
]


def test_exists_lesson(client, lesson_with_public_course):
    url = get_reverse_url("lessons:lesson_detail", args=(lesson_with_public_course.pk,))
    response = get_response_safely(client, url)

    expected_template_name = "lessons/lesson_detail.html"
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `LessonDetailView` в качестве шаблона '
            'используется имя по умолчанию - `название модели_detail`'
        )
    )

    context = response.context_data

    assert 'lesson' in context, (
        'Убедитесь, что в классе `LessonDetailView` в качестве имени объекта '
        'для передачи в контекст используется имя по умолчанию'
    )


def test_does_not_exists_lesson(client):
    does_not_exists_pk = 1
    url = get_reverse_url("lessons:lesson_detail", args=(does_not_exists_pk,))

    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_lesson_with_not_public_course_for_anonymous_user(unlogged_client, lesson_with_not_public_course):
    url = get_reverse_url("lessons:lesson_detail", args=(lesson_with_not_public_course.pk,))

    response = unlogged_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_lesson_with_not_public_course_for_auth_user(user_client, lesson_with_not_public_course):
    url = get_reverse_url("lessons:lesson_detail", args=(lesson_with_not_public_course.pk,))
    response = user_client.get(url)

    assert response.status_code == HTTPStatus.OK


def test_num_queries(unlogged_client, django_assert_max_num_queries, lesson_with_public_course):
    try:
        with django_assert_max_num_queries(2):
            url = get_reverse_url("lessons:lesson_detail", args=(lesson_with_public_course.pk,))
            get_response_safely(unlogged_client, url)
    except pytest.fail.Exception as e:
        raise AssertionError(
            'Убедитесь, что при выводе урока выполнена оптимизация запроса для связанного поля `course`'

        ) from e
