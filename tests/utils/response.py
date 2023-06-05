from http import HTTPStatus
from typing import Optional

from django.test.client import Client
from django.http import HttpResponse
from django.urls import reverse, exceptions


def get_response_safely(
        user_client: Client, url: str, raises: bool = True, err_msg: Optional[str] = None
) -> HttpResponse:
    default_msg = f'Убедитесь, что url `{url}` успешно открывается.'
    response = user_client.get(url)
    if raises:
        assert response.status_code == HTTPStatus.OK, err_msg or default_msg
    return response


def get_reverse_url(viewname, args=None, kwargs=None):
    try:
        url = reverse(viewname, args=args, kwargs=kwargs)
    except exceptions.NoReverseMatch:
        raise AssertionError(
            f'Не удалось найти не одного представления соответствующего названию - `{viewname}`. '
            f'Проверьте, что в файлах `urls.py` есть такое название.'
        )

    return url
