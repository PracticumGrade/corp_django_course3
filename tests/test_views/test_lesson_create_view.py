from http import HTTPStatus

from pytest_django.asserts import assertTemplateUsed, assertRedirects
import pytest

from utils import get_response_safely, get_reverse_url

pytestmark = [
    pytest.mark.django_db,
]


def test_get_create_lesson(user_client, user_course):
    url = get_reverse_url("courses:create_lesson", args=(user_course.pk,))

    response = get_response_safely(user_client, url)
    expected_template_name = 'lessons/lesson_form.html'
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `LessonCreateView` в качестве шаблона '
            'используется имя по умолчанию - `название модели_form`'
        )
    )


def test_post_create_lesson(user_client, user_course, lesson_data):
    url = get_reverse_url("courses:create_lesson", args=(user_course.pk,))
    response = user_client.post(url, data=lesson_data)
    expected_url = get_reverse_url("lessons:lesson_detail", args=(1,))
    assertRedirects(
        response, expected_url,
        msg_prefix=(
            'Убедитесь, что после добавления урока происходит '
            'перенаправление на страницу созданного урока.'
        )
    )


def test_get_create_lesson_another_user(another_user_client, user_course):
    url = get_reverse_url("courses:create_lesson", args=(user_course.pk,))

    response = another_user_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что в классе `LessonCreateView`, если автор пытается создать урок не к своему курсу, '
        'то должна возвращаться ошибка 404, с указанием, что запрашиваемый курс не найден'
    )


def test_post_create_lesson_another_user(another_user_client, user_course, lesson_data):
    url = get_reverse_url("courses:create_lesson", args=(user_course.pk,))
    response = another_user_client.post(url, data=lesson_data)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что в классе `LessonCreateView`, если автор пытается создать урок не к своему курсу, '
        'то должна возвращаться ошибка 404, с указанием, что запрашиваемый курс не найден'
    )


def test_login_redirect(unlogged_client, settings, user_course):
    url = get_reverse_url("courses:create_lesson", args=(user_course.pk,))
    response = unlogged_client.get(url)
    expected_url = get_reverse_url(settings.LOGIN_URL) + f'?next={url}'
    assertRedirects(
        response, expected_url,
        msg_prefix=(
            'Убедитесь, что неавторизованный пользователь при попытке добавить урок, '
            'перенаправляется на страницу авторизации.'
        )
    )
