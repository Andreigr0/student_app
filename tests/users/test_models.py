def test_create_user_model(create_user_model):
    user, now = create_user_model()

    assert user.id is not None
    assert user.name == 'test'
    assert user.email is not None
    assert user.password == 'password'
    assert user.email_verified_at == now
    assert user.created_at is not None
    assert user.updated_at is not None
