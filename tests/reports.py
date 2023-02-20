import unittest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker
from db.queries import reports
from db.models.member import Member


class TestReportsQuery(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///base.db', echo=True)
        self.session = scoped_session(sessionmaker(autocommit=False,
                                                   autoflush=False,
                                                   bind=self.engine))

    def test_books_by_year(self):
        member_query = select(Member).where(Member.id == 2)
        member = self.session.execute(member_query).first()[0]

        books_query = reports.books_by_year(member, 2015)
        result = self.session.execute(books_query).all()

        self.assertEqual(result[0][0], 10)
        self.assertEqual(result[0][1], 2)
