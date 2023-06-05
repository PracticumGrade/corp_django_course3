from http import HTTPStatus

from pytest_django.asserts import assertTemplateUsed
import pytest

from utils import get_response_safely, get_reverse_url


pytestmark = [
    pytest.mark.django_db,
]


def test_course(client, public_course, lessons_with_course):
    url = get_reverse_url("courses:course_detail", args=(public_course.pk,))
    response = get_response_safely(client, url)

    expected_template_name = "courses/course_detail.html"
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `CourseDetailView` в качестве шаблона '
            'используется имя по умолчанию - `название модели_detail`'
        )
    )

    context = response.context_data

    assert 'course' in context, (
        'Убедитесь, что в классе `CourseDetailView` в контекст передается значение по ключу `course`'
    )
    actual_course = response.context_data['course']
    assert actual_course == public_course, (
        f'Убедитесь, что в классе `CourseDetailView` передается курс '
        f'для отображения на странице запрашиваемого курса.'
    )

    assert 'lessons' in context, (
        'Убедитесь, что в классе `CourseDetailView` в контекст передается значение по ключу `lessons`'
    )
    lessons = response.context_data['lessons']
    assert len(lessons) == len(lessons_with_course), (
        f'Убедитесь, что в классе `CourseDetailView` настроена передача всех уроков запрашиваемого курса.'
    )


def test_does_not_exists_course(client):
    does_not_exists_pk = 1
    url = get_reverse_url("courses:course_detail", args=(does_not_exists_pk,))

    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_not_public_course_for_anonymous_user(unlogged_client, not_public_course):
    url = get_reverse_url("courses:course_detail", args=(not_public_course.pk,))

    response = unlogged_client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_not_public_course_for_auth_user(user_client, not_public_course):
    url = get_reverse_url("courses:course_detail", args=(not_public_course.pk,))
    response = user_client.get(url)

    assert response.status_code == HTTPStatus.OK


def test_num_queries(client, django_assert_num_queries, public_course, lessons_with_course):
    try:
        with django_assert_num_queries(2):
            url = get_reverse_url("courses:course_detail", args=(public_course.pk,))
            get_response_safely(client, url)
    except pytest.fail.Exception as e:
        raise AssertionError(
            'Убедитесь, что при выводе курса выполнена оптимизация запроса для связанного поля `author` и `category`.'
        ) from e
