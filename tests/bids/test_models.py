from bids.models import BidModel, BidStatus


def test_create_model(db_test, faker):
    bid = BidModel(
        status=BidStatus.expired,
        about=faker.text(),
        experience=faker.text(),
        reason=faker.text(),
        refusal_reason=faker.text(),
        is_archival=False,
    )
    db_test.add(bid)
    db_test.commit()

    assert bid.id is not None
    assert bid.status == BidStatus.expired
    assert bid.is_archival is False
    assert bid.about is not None
    assert bid.experience is not None
    assert bid.reason is not None
    assert bid.refusal_reason is not None
