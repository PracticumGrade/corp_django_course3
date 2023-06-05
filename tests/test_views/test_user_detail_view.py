from http import HTTPStatus
from operator import attrgetter

from pytest_django.asserts import assertTemplateUsed, assertQuerysetEqual
import pytest

from utils import get_response_safely, get_reverse_url


pytestmark = [
    pytest.mark.django_db,
]


def test_user_profile(client, user, user_courses):
    url = get_reverse_url("users:profile", args=(user.username,))
    response = get_response_safely(client, url)

    expected_template_name = "users/profile.html"
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            f'Убедитесь, что в классе `UserProfileDetailView` в качестве шаблона '
            f'используется шаблон `{expected_template_name}`'
        )
    )

    context = response.context_data

    assert 'profile' in context, (
        'Убедитесь, что в классе `UserProfileDetailView` в контекст объект передаётся по ключу `profile`'
    )
    actual_profile = response.context_data['profile']
    assert actual_profile == user, (
        f'Убедитесь, что в классе `UserProfileDetailView` передается пользователь, '
        f'для которого запрашивалась страница.'
    )


def test_all_course_for_auth_user(user_client, user, user_courses):
    url = get_reverse_url("users:profile", args=(user.username,))
    response = get_response_safely(user_client, url)
    context = response.context_data

    assert 'courses' in context, (
        'Убедитесь, что в классе `UserProfileDetailView` в контекст передается значение по ключу `courses`'
    )
    actual_courses = response.context_data['courses']
    assert len(actual_courses) == len(user_courses), (
        f'Убедитесь, что в классе `UserProfileDetailView` для авторизованных пользователей передаются все курсы автора.'
    )

    ordered_courses = sorted(
        user_courses,
        key=attrgetter('created_at'),
        reverse=True,
    )
    assertQuerysetEqual(
        actual_courses, ordered_courses,
        msg=(
            'Убедитесь, что queryset со списком курсов в классе `UserProfileDetailView` содержит курсы, '
            'принадлежащие пользователю и отсортированные от старых курсов к свежим по времени создания.'
        )
    )


def test_public_course_for_anonymous_user(client, user, user_courses):
    url = get_reverse_url("users:profile", args=(user.username,))
    response = get_response_safely(client, url)
    context = response.context_data

    assert 'courses' in context, (
        'Убедитесь, что в классе `UserProfileDetailView` в контекст передается значение по ключу `courses`'
    )
    public_ordered_courses = sorted(
        (course for course in user_courses if course.is_public),
        key=attrgetter('created_at'),
        reverse=True,
    )
    actual_courses = response.context_data['courses']
    assert len(actual_courses) == len(public_ordered_courses), (
        f'Убедитесь, что в классе `UserProfileDetailView` для неавторизованных пользователей '
        f'передаются только публичные курсы автора.'
    )

    assertQuerysetEqual(
        actual_courses, public_ordered_courses,
        msg=(
            'Убедитесь, что queryset со списком курсов в классе `UserProfileDetailView` содержит публичные курсы, '
            'принадлежащие пользователю и отсортированные от старых курсов к свежим по времени создания.'
        )
    )


def test_does_not_exists_user(client):
    slug = "does_not_exists_user"
    url = get_reverse_url("users:profile", args=(slug,))

    response = client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_count_courses(client, user, user_courses):
    url = get_reverse_url("users:profile", args=(user.username,))
    response = get_response_safely(client, url)
    context = response.context_data

    assert 'courses_count' in context, (
        'Убедитесь, что в классе `UserProfileDetailView` в контекст передается значение по ключу `courses_count` '
        'с количеством публичных и непубличных курсов.'
    )

    public_course = {'is_public': True, 'count': len([course for course in user_courses if course.is_public])}
    not_public_course = {'is_public': True, 'count': len([course for course in user_courses if not course.is_public])}

    actual_courses_count = response.context_data['courses_count']

    for count_course in (public_course, not_public_course):
        assert count_course in actual_courses_count, (
            'Убедитесь, что в queryset со списком курсов в классе `UserProfileDetailView` '
            'верно посчитаны публичные курсы, и значения содержатся с нужными ключами.'
        )
