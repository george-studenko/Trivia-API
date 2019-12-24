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

    def test_get_questions_OK_response(self):
        # Arrange
        expected_status_code = 200

        # Act
        result = self.client().get('/questions')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_get_questions_success_True(self):
        # Arrange
        expected_value = True

        # Act
        result = self.client().get('/questions')
        content = json.loads(result.data)
        actual_value = content['success']

        # Assert
        self.assertEqual(actual_value, expected_value)

    def test_get_questions_has_content(self):
        # Arrange
        expected_questions = 10

        # Act
        result = self.client().get('/questions?page=1')
        content = json.loads(result.data)
        actual_questions = content['current_page_total_questions']

        # Assert
        self.assertEqual(actual_questions, expected_questions)

    def test_delete_question_has_OK_response(self):
        # Arrange
        expected_status_code = 200

        # Act
        result = self.client().delete('/questions/5')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_delete_question_has_unprocessable_response(self):
        # Arrange
        expected_status_code = 422

        # Act
        result = self.client().delete('/questions/999')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_question_has_been_deleted(self):
        # Arrange
        expected_result = True

        # Act
        result = self.client().delete('/questions/4')
        content = json.loads(result.data)
        actual_value = content['success']

        # Assert
        self.assertEqual(actual_value, expected_result)

    def test_post_question_OK_response(self):
        # Arrange
        expected_status_code = 200
        data = dict(question='q1', answer='a1', category=1, difficulty=1)

        # Act
        result = self.client().post('/questions', data= json.dumps(data), content_type='application/json')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_search_question_OK_response(self):
        # Arrange
        expected_status_code = 200
        data = dict(searchTerm='1990')

        # Act
        result = self.client().post('/search',data= json.dumps(data), content_type='application/json')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_search_question_has_results(self):
        # Arrange
        expected_results = 1
        data = dict(searchTerm='1990')

        # Act
        result = self.client().post('/search',data= json.dumps(data), content_type='application/json')
        content = json.loads(result.data)
        actual_results = len(content['questions'])

        # Assert
        self.assertEqual(actual_results, expected_results)

    def test_search_not_found_result(self):
        # Arrange
        expected_status_code = 404
        data = dict(searchTerm='Non_existing_term')

        # Act
        result = self.client().post('/search', data=json.dumps(data), content_type='application/json')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_search_unprocessable_result(self):
        # Arrange
        expected_status_code = 422
        data = dict(bad_argument='Non_existing_term')

        # Act
        result = self.client().post('/search', data=json.dumps(data), content_type='application/json')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_get_question_by_category_OK_response(self):
        # Arrange
        expected_status_code = 200

        # Act
        result = self.client().get('/categories/1/questions')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_get_question_by_category_not_found_response(self):
        # Arrange
        expected_status_code = 404

        # Act
        result = self.client().get('/categories/182/questions')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_get_question_by_category_has_correct_id(self):
        # Arrange
        expected_id = 1

        # Act
        result = self.client().get('/categories/1/questions')
        content = json.loads(result.data)
        actual_id = content['currentCategory']

        # Assert
        self.assertEqual(actual_id, expected_id)

    def test_get_next_question_OK_response(self):
        # Arrange
        expected_status_code = 200

        # Act
        result = self.client().post('/quizzes')
        actual_status_code = result.status_code

        # Assert
        self.assertEqual(actual_status_code, expected_status_code)

    def test_get_next_question_has_content(self):
        # Arrange
        expected_number_of_questions = 1
        data = dict(previous_questions=[], quiz_category={'type': 'Geography', 'id': '3'})

        # Act
        result = self.client().post('/quizzes',  data=json.dumps(data), content_type='application/json')
        content = json.loads(result.data)
        actual_number_of_questions = len(content['questions'])

        # Assert
        self.assertEqual(expected_number_of_questions, actual_number_of_questions)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(verbosity=2)
    unittest.main()