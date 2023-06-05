import pytest


pytestmark = [
    pytest.mark.django_db,
]


def test_lesson_get_absolute_url(lesson):
    model = "Lesson"
    assert hasattr(lesson, 'get_absolute_url'), (
        f"Убедитесь, что в модели `{model}` объявлен метод `get_absolute_url`"
    )

    expected_url = f"/lessons/{lesson.pk}/"
    actual_url = lesson.get_absolute_url()
    assert actual_url == expected_url, (
        f"Убедитесь, что в модели `{model}` метод `get_absolute_url` "
        f"возвращает абсолютный url объекта согласно заданию."
    )


def test_category_get_absolute_url(category):
    model = "Category"
    assert hasattr(category, 'get_absolute_url'), (
        f"Убедитесь, что в модели `{model}` объявлен метод `get_absolute_url`"
    )

    expected_url = f"/courses/category/{category.slug}/"
    actual_url = category.get_absolute_url()
    assert actual_url == expected_url, (
        f"Убедитесь, что в модели `{model}` метод `get_absolute_url` "
        f"возвращает абсолютный url объекта согласно заданию."
    )


def test_course_get_absolute_url(course):
    model = "Course"
    assert hasattr(course, 'get_absolute_url'), (
        f"Убедитесь, что в модели `{model}` объявлен метод `get_absolute_url`"
    )

    expected_url = f"/courses/{course.pk}/"
    actual_url = course.get_absolute_url()
    assert actual_url == expected_url, (
        f"Убедитесь, что в модели `{model}` метод `get_absolute_url` "
        f"возвращает абсолютный url объекта согласно заданию."
    )
