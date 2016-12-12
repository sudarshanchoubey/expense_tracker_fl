import os
import datetime
import unittest

from config import basedir
from app import app, db
from app.models import User, Expense, Tag

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + os.environ['PG_user'] + ":" + os.environ['PG_pass'] + "@localhost:5432/testdb"
        self.app = app.test_client()
        db.create_all()

    def test_make_userexpensetag(self):
        u = User(nickname="john", social_id="johndoe")
        db.session.add(u)
        db.session.commit()
        e = Expense(description="Lehenga", amount=7000.0, spender=u, timestamp=datetime.datetime.now())
        db.session.add(e)
        db.session.commit()
        t1 = Tag(body="marriage", for_expense=e)
        t2 = Tag(body="clothes", for_expense=e)
        db.session.add(t1)
        db.session.add(t2)
        db.session.commit()
        u = User.query.filter_by(nickname="john").first()
        assert u.social_id == "johndoe"
        flag = False
        for e in u.expenses.all():
            if e.description == "Lehenga":
                for tg in e.tags.all():
                    if tg.body == "marriage":
                        flag = True
                break
        assert flag == True

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
