from dotenv import load_dotenv
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

# test_database = f"sqlite:///{os.path.join(basedir, 'database.db')}"
# TEST_DB_NAME = os.environ.get("TEST_DB_NAME")
# TEST_DB_USERNAME = os.environ.get("TEST_DB_USERNAME")
# TEST_DB_PASSWORD = os.environ.get("TEST_DB_PASSWORD")
# TEST_DB_HOST = os.environ.get("TEST_DB_HOST", "localhost")
# TEST_DB_PORT = os.environ.get("TEST_DB_PORT", 5432)
TEST_DB_NAME = os.getenv("TEST_DB_NAME")
TEST_DB_USERNAME = os.getenv("TEST_DB_USERNAME")
TEST_DB_PASSWORD = os.getenv("TEST_DB_PASSWORD")
TEST_DB_HOST = os.getenv("TEST_DB_HOST")
TEST_DB_PORT = os.getenv("TEST_DB_PORT")

database_path = f"postgres://{TEST_DB_USERNAME}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}:{TEST_DB_PORT}/{TEST_DB_NAME}"


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        # self.database_name = "udacity_test_triviadb"
        # self.database_path = "postgres://{}/{}".format(
        #     'localhost:5432', self.database_name)
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        ##
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        # new question
        self.sample_question = {
            "question": "How many legs does a cow have?",
            "answer": "Four",
            "difficulty": 2,
            "category": 1,
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Done 
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_category_list(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_question_list(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])

    def test_question_delete(self):
        res = self.client().delete("questions/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 1)

    def test_question_create(self):
        res = self.client().post("/questions", json=self.sample_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsInstance(data["created"], int)

    def test_question_create_400(self):
        incomplete_question = {
            "question": "What is Python?",
            "category": "",
            "answer": "Python is Programming language",
            "difficulty": 1,
        }

        res = self.client().post("/questions", json=incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 400)
        self.assertEqual(data["message"], "Bad request!!!")

    def test_question_create_406(self):
        incomplete_question = {
            "question": "What is Python?",
            "category": "1",
            "answer": "Python is Programming language",
        }

        res = self.client().post("/questions", json=incomplete_question)
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["error"], 406)
        self.assertEqual(data["message"], "Not Acceptable!!!")

    def test_question_search(self):
        res = self.client().post("questions/search", json={"searchTerm": "kano"})
        data = json.loads(res.data)

        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])

    def test_question_search_404(self):
        res = self.client().post("questions/search", json={"searchTerm": ""})
        data = json.loads(res.data)

        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found!!!")
        self.assertEqual(res.status_code, 404)

    def test_category_questions_list(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

        self.assertTrue(data["questions"])
        self.assertIsInstance(data["questions"], list)
        self.assertEqual(data["current_category"], 1)

    def test_trivia_quiz(self):
        sample_request = {
            "quiz_category": {"id": 1, "type": "science"},
            "previous_questions": None,
        }
        res = self.client().post("/quizzes", json=sample_request)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertEqual(data["question"]["category"], 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    # print("*"*40)
    # print(database_path)
    # print("*"*40)
    unittest.main()
