import datetime

from users.models import UserModel


def test_create_user_model(db_test):
    now = datetime.datetime.now()
    user = UserModel(
        name='test',
        email='email',
        password='password',
        email_verified_at=now,
    )
    db_test.add(user)
    db_test.commit()

    assert user.id is not None
    assert user.name == 'test'
    assert user.email == 'email'
    assert user.password == 'password'
    assert user.email_verified_at == now
    assert user.created_at is not None
    assert user.updated_at is not None
