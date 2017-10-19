import pytest
from django.contrib.auth import get_user_model
from model_mommy import mommy


@pytest.fixture
def user():
    User = get_user_model()
    return mommy.make(User, username='diegoponciano')
