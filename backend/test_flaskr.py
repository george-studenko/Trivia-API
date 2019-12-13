import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
import warnings



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        warnings.filterwarnings("ignore")
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_OK_response(self):
        # Arrange
        expected_status_code = 200

        # Act
        result = self.client().get('/categories')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_get_categories_success_True(self):
        # Arrange
        expected_value = True

        # Act
        result = self.client().get('/categories')
        content = json.loads(result.data)
        actual_value = content['success']

        # Assert
        self.assertEqual(actual_value, expected_value)

    def test_get_categories_has_content(self):
        # Arrange
        expected_categories = 6

        # Act
        result = self.client().get('/categories')
        content = json.loads(result.data)
        actual_categories = len(content['categories'])

        # Assert
        self.assertEqual(actual_categories ,expected_categories)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(verbosity=2)
    unittest.main()