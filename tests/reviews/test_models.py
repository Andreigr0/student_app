# from reviews.models import MemberReviewModel
# import datetime
#
#
# def test_create_member_review(db_test):
#     review = MemberReviewModel(
#         start_date=datetime.date(2020, 1, 1),
#         finish_date=datetime.date(2020, 2, 1),
#         hours=100,
#         score=5,
#         text='test',
#     )
#     db_test.add(review)
#     db_test.commit()
#
#     assert review.id is not None
#     assert review.start_date == datetime.date(2020, 1, 1)
#     assert review.finish_date == datetime.date(2020, 2, 1)
#     assert review.hours == 100
#     assert review.score == 5
#     assert review.text == 'test'
