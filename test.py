import os
import unittest

from config import basedir
from app import app, db
from app.models import User, Expense, Tag

class TestCase(unittest.TestCase):
    def setup(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://" + os.environ['PG_user'] + ":" + os.environ['PG_pass'] + "@localhost:5432/testdb"
        self.app = app.test_client()
        db.create_all()

    def test_make_userexpensetag(self):
        u = User(nickname="john", social_id="johndoe")
        db.session.add(u)
        db.session.commit()
        e = Expense(description="Lehenga", amount=7000.0, spender=u)
        db.session.add(e)
        db.session.commit()
        t = Tag(body="marriage", for_expense=e)
        db.session.add(t)
        db.session.commit(t)
        u = User.query.get(nickname="john")
        assert u.social_id == "johndoe"
        flag = False
        for e in u.expenses.all():
            if e.description == "Lehenga":
                flag = True
                break
        assert flag == True

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
