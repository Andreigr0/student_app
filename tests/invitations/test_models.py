from invitations.models import InvitationModel, InvitationStatus


def test_create_invitation(db_test):
    invitation = InvitationModel(
        status=InvitationStatus.viewed,
        text='test',
        is_archival=True,
    )
    db_test.add(invitation)
    db_test.commit()
    assert invitation.id is not None
    assert invitation.status == InvitationStatus.viewed
    assert invitation.text == 'test'
    assert invitation.is_archival is True
