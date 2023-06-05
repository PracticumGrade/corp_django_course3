from pytest_django.asserts import assertTemplateUsed
import pytest

from utils import get_response_safely, get_reverse_url

pytestmark = [
    pytest.mark.django_db,
]


def test_categories(client, categories):
    url = get_reverse_url("courses:category_list")
    response = get_response_safely(client, url)

    expected_template_name = "courses/category_list.html"
    assertTemplateUsed(
        response, expected_template_name,
        msg_prefix=(
            'Убедитесь, что в классе `CategoryListView` в качестве шаблона '
            'используется имя по умолчанию - `название модели_list`'
        )
    )

    context = response.context_data

    assert 'category_list' in context, (
        'Убедитесь, что в классе `LessonDetailView` в качестве имени объекта '
        'для передачи в контекст используется имя по умолчанию'
    )

    category_list = response.context_data['category_list']

    assert len(category_list) == len(categories), (
        'Убедитесь, что при отображении списка категорий, попали все категории.'
    )
