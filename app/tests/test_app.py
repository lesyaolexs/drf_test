import django

django.setup()

from typing import Any, Dict

from pytest_drf import Returns200, UsesGetMethod, UsesListEndpoint, ViewSetTest
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture

from app.models import CustomUser


def express_key_value(user: CustomUser) -> Dict[str, Any]:
    return {
        "id": user.id.__str__(),
        "login": user.login,
        "sex": user.sex,
        "birth_date": user.birth_date,
    }


class TestCustomUserViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for("user-list"))

    class TestList(UsesGetMethod, UsesListEndpoint, Returns200):
        users = lambda_fixture(
            lambda: [
                CustomUser.objects.create(**user)
                for user in [
                    {"login": "Tes", "sex": "female", "birth_date": "2022-08-01"},
                    {"login": "Кes", "sex": "female", "birth_date": "2022-08-01"},
                    {"login": "Аes", "sex": "male", "birth_date": "2022-08-01"},
                ]
            ],
            autouse=True,
        )

        def test_users_list(self, users, json):
            actual = json
            expected = [express_key_value(i) for i in users]
            assert expected == actual
