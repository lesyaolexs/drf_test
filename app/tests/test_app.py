import django

django.setup()

from typing import Any, Dict

from pytest_assert_utils import assert_model_attrs
from pytest_common_subject import precondition_fixture
from pytest_drf import (Returns200, Returns201, UsesGetMethod,
                        UsesListEndpoint, UsesPostMethod, ViewSetTest)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture, static_fixture

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
    detail_url = lambda_fixture(lambda user: url_for("user-detail", user.pk))

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

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        data = static_fixture(
            {
                "login": "Jes",
                "sex": "female",
                "birth_date": "2022-08-01",
            }
        )

        initial_user_ids = precondition_fixture(
            lambda: set(CustomUser.objects.values_list("id", flat=True)), async_=False
        )

        # def test_sets_expected_attrs(self, data, json):
        #     user = CustomUser.objects.get(pk=json["id"])
        #
        #     expected = data
        #     assert_model_attrs(user, expected)
