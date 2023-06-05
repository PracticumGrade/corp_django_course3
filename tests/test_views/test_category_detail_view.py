from http import HTTPStatus
from operator import attrgetter

from pytest_django.asserts import assertTemplateUsed, assertQuerysetEqual
from django.test import RequestFactory
import pytest

from utils import get_response_safely, get_reverse_url
from conftest import N_PER_PAGE
from courses.views import CategoryDetailView

pytestmark = [
    pytest.mark.django_db,
]


def test_categories(client, category, courses_with_category):
    url = get_reverse_url("courses:category_detail", args=(category.slug,))
    response = get_response_safely(client, url)

    expected_template_name = "courses/category_detail.html"
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `CategoryDetailView` в качестве шаблона '
            'используется имя по умолчанию - `название модели_detail`'
        )
    )

    context = response.context_data

    assert 'page_obj' in context, (
        'Убедитесь, что в классе `LessonDetailView` в контекст передается значение по ключу `page_obj`'
    )
    page_obj = response.context_data['page_obj']
    assert len(page_obj) <= N_PER_PAGE, (
        f'Убедитесь, что в классе `LessonDetailView` настроена пагинация '
        f'для отображения списка курсов на странице категории и выводится не более {N_PER_PAGE} курсов.'
    )

    assert 'category' in context, (
        'Убедитесь, что в классе `LessonDetailView` в контекст передается значение по ключу `category`'
    )
    actual_category = response.context_data['category']
    assert actual_category == category, (
        f'Убедитесь, что в классе `LessonDetailView` передается категория '
        f'для отображения на странице запрашиваемой категорией.'
    )


def test_does_not_exists_category(client):
    does_not_exists_category = 'does_not_exists_category'
    url = get_reverse_url("courses:category_detail", args=(does_not_exists_category,))

    response = client.get(url)

    assert response.status_code == HTTPStatus.NOT_FOUND


def test_public_course_for_anonymous_user(anonymous_user, category, courses_with_category):
    url = get_reverse_url("courses:category_detail", args=(category.slug,))
    request = RequestFactory().get(url)
    request.user = anonymous_user

    view = CategoryDetailView()
    view.setup(request)
    view.object = category

    public_ordered_courses = sorted(
        (course for course in courses_with_category if course.is_public),
        key=attrgetter('created_at'),
        reverse=True,
    )
    queryset = view.get_queryset()
    assertQuerysetEqual(
        queryset, public_ordered_courses,
        msg=(
            'Убедитесь, что queryset в классе `CategoryDetailView` содержит только опубликованные курсы, '
            'принадлежащие запрашиваемой категории и отсортированные от старых курсов к свежим по времени создания.'
        )
    )


def test_all_course_for_auth_user(user, category, courses_with_category):
    url = get_reverse_url("courses:category_detail", args=(category.slug,))
    request = RequestFactory().get(url)
    request.user = user

    view = CategoryDetailView()
    view.setup(request)
    view.object = category

    ordered_courses = sorted(
        courses_with_category,
        key=attrgetter('created_at'),
        reverse=True,
    )
    queryset = view.get_queryset()
    assertQuerysetEqual(
        queryset, ordered_courses,
        msg=(
            'Убедитесь, что queryset в классе `CategoryDetailView` содержит все курсы для авторизованного пользователя, '
            'принадлежащие запрашиваемой категории и отсортированные от старых курсов к свежим по времени создания.'
        )
    )
