from http import HTTPStatus

from pytest_django.asserts import assertTemplateUsed, assertRedirects
import pytest

from utils import get_response_safely, get_reverse_url

pytestmark = [
    pytest.mark.django_db,
]


def test_get_update_lesson(user_client, user_course, lesson_with_user_course):
    url = get_reverse_url("courses:edit_lesson", args=(user_course.pk, lesson_with_user_course.pk))

    response = get_response_safely(user_client, url)
    expected_template_name = 'lessons/lesson_form.html'
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `LessonUpdateView` в качестве шаблона '
            'используется имя по умолчанию - `название модели_form`'
        )
    )


def test_post_update_lesson(user_client, user_course, lesson_with_user_course, lesson_data):
    url = get_reverse_url("courses:edit_lesson", args=(user_course.pk, lesson_with_user_course.pk))
    response = user_client.post(url, data=lesson_data)
    expected_url = get_reverse_url("lessons:lesson_detail", args=(1,))
    assertRedirects(
        response, expected_url,
        msg_prefix=(
            'Убедитесь, что после обновления урока происходит '
            'перенаправление на страницу обновленного урока.'
        )
    )


def test_get_update_lesson_another_user(another_user_client, user_course, lesson_with_user_course):
    url = get_reverse_url("courses:edit_lesson", args=(user_course.pk, lesson_with_user_course.pk))

    response = another_user_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что в классе `LessonUpdateView`, если автор пытается создать урок не к своему курсу, '
        'то должна возвращаться ошибка 404, с указанием, что запрашиваемый курс не найден'
    )


def test_post_update_lesson_another_user(another_user_client, user_course, lesson_with_user_course, lesson_data):
    url = get_reverse_url("courses:edit_lesson", args=(user_course.pk, lesson_with_user_course.pk))
    response = another_user_client.post(url, data=lesson_data)
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Убедитесь, что в классе `LessonUpdateView`, если автор пытается создать урок не к своему курсу, '
        'то должна возвращаться ошибка 404, с указанием, что запрашиваемый курс не найден'
    )


def test_login_redirect(unlogged_client, settings, user_course, lesson_with_user_course,):
    url = get_reverse_url("courses:edit_lesson", args=(user_course.pk, lesson_with_user_course.pk))
    response = unlogged_client.get(url)
    expected_url = get_reverse_url(settings.LOGIN_URL) + f'?next={url}'
    assertRedirects(
        response, expected_url,
        msg_prefix=(
            'Убедитесь, что неавторизованный пользователь при попытке обновить урок, '
            'перенаправляется на страницу авторизации.'
        )
    )
