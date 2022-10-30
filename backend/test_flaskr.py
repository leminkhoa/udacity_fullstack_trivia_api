import unittest
import json

from unittest.mock import patch
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app

from models.respond_schema import *
from models.request_schema import *
from models.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = 'postgresql://{}/{}'.format('postgres:abc@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'test_question',
            'answer': 'test_answer',
            'category': 3,
            'difficulty': 5,
        }

        self.search_question = {
            'searchTerm': 'what'
        }

        self.quizzes = {
            'quiz_category': {
                'id': 5
            },
            'previous_questions': [2, 4, 6]
        }


        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_get_categories_expect_200(self):
        """
        Test get categories - Expect return status code 200
        """

        res = self.client().get('/categories')
        data = json.loads(res.data)
        schema = GetCategoriesRespondSchema()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(schema.validate(data), {})
        self.assertTrue(data['total_categories'])
        self.assertTrue(len(data['categories']))


    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_get_categories_expect_404(self, mock_query):
        """
        Test get categories - Expect return status code 404
        """

        # setup mock
        mock_query\
            .return_value.filter\
            .return_value.one_or_none\
            .return_value = []
        
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


    def test_get_questions_expect_200(self):
        """
        Test get questions - Expect return status code 200
        """

        res = self.client().get('/questions')
        data = json.loads(res.data)
        schema = GetQuestionRespondSchema()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(schema.validate(data), {})
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))


    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_get_questions_expect_404(self, mock_query):
        """
        Test get categories - Expect return status code 404
        """

        # setup mock
        mock_query\
            .return_value.filter\
            .return_value.one_or_none\
            .return_value = []
        
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


    def test_delete_questions_expect_200(self):
        """
        Test delete question - Expect return status code 200
        """

        test_id = 9
        res = self.client().delete(f'/questions/{test_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], test_id)
        self.assertTrue(data['total_questions'])


    def test_delete_questions_expect_422(self):
        """
        Test delete question - Expect return status code 422
        """

        test_id = 5000
        res = self.client().delete(f'/questions/{test_id}')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == test_id).one_or_none()

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')
        self.assertEqual(question, None)


    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_delete_questions_expect_500(self, mock_query):
        """
        Test delete question - Expect return status code 500
        """

        # setup mock
        mock_query\
            .return_value.filter\
            .return_value.one_or_none\
            .side_effect = Exception("test exception")

        test_id = 5000
        res = self.client().delete(f'/questions/{test_id}')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)


    def test_create_questions_expect_200(self):
        """
        Test create question - Expect return status code 200
        """

        res = self.client().post(f'/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])


    def test_create_questions_expect_400_missing_field(self):
        """
        Test create question with missing
        field(s) - Expect return status code 400
        """
        
        request_missing_field = {
            'question': 'test_question',
            'answer': 'test_answer',
        }

        res = self.client().post(f'/questions', json=request_missing_field)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


    def test_create_questions_expect_400_wrong_datatype(self):
        """
        Test create question with wrong datatype
        in request - Expect return status code 400
        """
        
        request_category_wrong_data_type = {
            'question': 'test_question',
            'answer': 'test_answer',
            'category': 'History',
            'difficulty': 5,
        }

        res = self.client().post(f'/questions', json=request_category_wrong_data_type)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


    def test_create_questions_expect_400_invalid_scale(self):
        """
        Test create question with invalid difficulty
        scale - Expect return status code 400
        """ 

        request_difficulty_invalid_scale = {
            'question': 'test_question',
            'answer': 'test_answer',
            'category': 'History',
            'difficulty': 15,
        }

        res = self.client().post(f'/questions', json=request_difficulty_invalid_scale)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


    def test_create_questions_expect_422(self):
        """
        Test create question with non-exist 
        category - Expect return status code 422
        """

        request_integrity_error = {
            'question': 'test_question',
            'answer': 'test_answer',
            'category': 100,
            'difficulty': 3,
        }

        res = self.client().post(f'/questions', json=request_integrity_error)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')


    @patch.object(Question, "insert")
    def test_create_questions_expect_500(self, mock_query):
        """
        Test create question - Expect return status code 500
        """

        # setup mock
        mock_query\
            .side_effect = Exception("test exception")

        res = self.client().post(f'/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')


    def test_search_questions_expect_200(self):
        """
        Test search question - Expect return status code 200
        """
        
        res = self.client().post(f'/questions/search', json=self.search_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])


    def test_search_questions_expect_400_no_body(self):
        """
        Test search question with no body in 
        request - Expect return status code 400
        """

        res = self.client().post(f'/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


    def test_search_questions_expect_400_wrong_schema(self):
        """
        Test search question with wrong schema in 
        request - Expect return status code 400
        """

        request_wrong_schema = {
            'search_Term': 'something'
        }
        res = self.client().post(f'/questions/search', json=request_wrong_schema)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


    def test_get_questions_from_category_expect_200(self):
        """
        Test get question by category - Expect return status code 200
        """
        
        test_id = 2
        res = self.client().get(f'/categories/{test_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertLessEqual(len(data['questions']), 10)
        self.assertTrue(data['total_questions'])


    def test_get_questions_from_category_expect_404(self):
        """
        Test get question by category with non-exist
        category - Expect return status code 404
        """

        test_id = 500
        res = self.client().get(f'/categories/{test_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')


    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_get_questions_from_category_expect_500(self, mock_query):
        """
        Test get question by category - Expect return status code 500
        """
        
        # setup mock
        mock_query\
            .return_value.filter\
            .return_value.all\
            .side_effect = Exception("test exception")

        test_id = 2
        res = self.client().get(f'/categories/{test_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')


    def test_quizzes_expect_200_one_category(self):
        """
        Test quizzes for one category - Expect return status code 200
        """
        
        # Random 20 times
        for _ in range(1, 20):
            res = self.client().post('/quizzes', json=self.quizzes)
            data = json.loads(res.data)
            schema = QuestionsSchema()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(schema.validate(data['question']), {})
            self.assertEqual(data['question']['category'], 5)


    def test_quizzes_expect_200_multiple_categories(self):
        """
        Test quizzes with category 0 in 
        request (all categories) - Expect return status code 200
        """
        
        request_category_0 = {
            'quiz_category': {
                'id': 0
            },
            'previous_questions': []
        }

        category = set()
        # Random 20 times
        for _ in range(1, 20):
            res = self.client().post('/quizzes', json=request_category_0)
            data = json.loads(res.data)
            schema = QuestionsSchema()

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertEqual(schema.validate(data['question']), {})
            category.add(data['question']['category'])

        self.assertGreater(len(category), 1)


    def test_quizzes_expect_400(self):
        """
        Test quizzes wrong schema - Expect return status code 400
        """
        
        request_wrong_schema = {
            'quiz_category': {
                'wrong_field_name': 5
            },
            'wrong_field_name': [2, 4, 6]
        }
        res = self.client().post('/quizzes', json=request_wrong_schema)
        data = json.loads(res.data)

        schema = QuestionsSchema()

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')


    @patch('flask_sqlalchemy._QueryProperty.__get__')
    def test_quizzes_expect_500(self, mock_query):
        """
        Test quizzes - Expect return status code 500
        """
        
        # setup mock
        mock_query\
            .return_value.filter\
            .return_value.all\
            .side_effect = Exception("test exception")

        res = self.client().post('/quizzes', json=self.quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['error'], 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main(verbosity=2)
