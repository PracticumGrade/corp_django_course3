from operator import attrgetter

from pytest_django.asserts import assertTemplateUsed, assertQuerysetEqual
from django.test import RequestFactory
import pytest

from utils import get_response_safely, get_reverse_url
from conftest import N_PER_PAGE
from courses.views import CourseListView


pytestmark = [
    pytest.mark.django_db,
]


def test_courses(client, categories):
    url = get_reverse_url("courses:index")
    response = get_response_safely(client, url)

    expected_template_name = "courses/index.html"
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `CourseListView` в качестве шаблона '
            f'используется шаблон `{expected_template_name}`'
        )
    )

    context = response.context_data

    assert 'page_obj' in context, (
        'Убедитесь, что в классе `CourseListView` в контекст передается значение по ключу `page_obj`'
    )
    page_obj = response.context_data['page_obj']
    assert len(page_obj) <= N_PER_PAGE, (
        f'Убедитесь, что в классе `CourseListView` настроена пагинация '
        f'для отображения списка курсов на странице категории и выводится не более {N_PER_PAGE} курсов.'
    )


def test_public_courses_for_anonymous_user(anonymous_user, courses_with_category):
    url = get_reverse_url("courses:index")
    request = RequestFactory().get(url)
    request.user = anonymous_user

    view = CourseListView()
    view.setup(request)

    public_ordered_courses = sorted(
        (course for course in courses_with_category if course.is_public),
        key=attrgetter('created_at'),
        reverse=True,
    )
    queryset = view.get_queryset()
    assertQuerysetEqual(
        queryset, public_ordered_courses,
        msg=(
            'Убедитесь, что queryset в классе `CourseListView` содержит только опубликованные курсы, '
            'отсортированные от старых курсов к свежим по времени создания.'
        )
    )


def test_all_courses_for_auth_user(user, courses_with_category):
    url = get_reverse_url("courses:index")
    request = RequestFactory().get(url)
    request.user = user

    view = CourseListView()
    view.setup(request)

    ordered_courses = sorted(
        courses_with_category,
        key=attrgetter('created_at'),
        reverse=True,
    )
    queryset = view.get_queryset()
    assertQuerysetEqual(
        queryset, ordered_courses,
        msg=(
            'Убедитесь, что queryset в классе `CourseListView` содержит все курсы для авторизованного пользователя, '
            'отсортированные от старых курсов к свежим по времени создания.'
        )
    )
