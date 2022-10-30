import random
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from sqlalchemy import exc

from models.request_schema import *
from models.models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    
    @app.route('/categories')
    def get_categories():
        # Get categories
        try:
            categories = Category.query.order_by(Category.id).all()
        except:
            print(sys.exc_info())
            abort (500)
        # If there is no category, return 404
        if len(categories) == 0:
            abort (404)
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        return jsonify({
            'success': True,
            'categories': categories_dict,
            'total_categories': len(categories)
        })


    @app.route('/questions')
    def get_questions():
        # Get questions
        try:
            retrieved_questions = Question.query.order_by(Question.id).all()
        except:
            print(sys.exc_info())
            abort (500)
        # If there is no question, return 404
        if len(retrieved_questions) == 0:
            abort (404)
        # Paginate
        try:     
            categories = Category.query.order_by(Category.id).all()     
            current_questions = paginate_questions(request, retrieved_questions)
        except:
            print(sys.exc_info())
            abort (500)
        # If there is no question, return 404
        if len(categories) == 0:
            abort (404)
        categories_dict = {}
        for category in categories:
            categories_dict[category.id] = category.type
        return jsonify({
            'success': True,
            'questions': current_questions,
            'categories': categories_dict,
            'total_questions': len(retrieved_questions),
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()
        except:
            print(sys.exc_info())
            abort (500)
        # If cannot find requested id, return 404
        if question is None:
            abort (422)
        try:
            question.delete()
        except:
            print(sys.exc_info())
            abort (500)
        return jsonify({
            'success': True,
            'deleted': id,
            'total_questions': len(Question.query.all())
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        # Request input
        body = request.get_json()
        # Validate request
        schema = CreateQuestionRequestSchema()
        try:
            # Validate request body against schema data types
            schema.load(body)
        except ValidationError:
            print(sys.exc_info())
            abort (400)
        # Create a new question
        new_question = Question(
            question=body.get('question'),
            answer=body.get('answer'),
            category=body.get('category'),
            difficulty=body.get('difficulty'),
        )
        # Insert
        try:
            new_question.insert()
        except exc.IntegrityError:
            print(sys.exc_info())
            abort (422)
        except:
            print(sys.exc_info())
            abort (500)
        return jsonify({
            'success': True,
            'created': new_question.id,
            'total_questions': len(Question.query.all())
        })

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        # Validate request
        schema = SearchQuestionRequestSchema()
        try:
            # Validate request body against schema data types
            schema.load(body)
        except ValidationError:
            print(sys.exc_info())
            abort (400)
        # Get search term
        search_term = body.get('searchTerm')
        # Query to find matched questions
        try:
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            current_questions = paginate_questions(request, questions)
        except:
            print(sys.exc_info())
            abort (500)
        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def questions_by_category(category_id):
        try:
            retrieved_questions = Question.query.filter(Question.category == category_id).all()
        except:
            print(sys.exc_info())
            abort (500)
        if len(retrieved_questions) == 0:
            abort (404)
        current_questions = paginate_questions(request, retrieved_questions)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(retrieved_questions),
        })



    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quiz():
        # Request input
        body = request.get_json()
        # Validate request
        schema = QuizzesRequestSchema()
        try:
            # Validate request body against schema data types
            schema.load(body)
        except ValidationError:
            print(sys.exc_info())
            abort (400)
        try:
            # get the qestion category an the previous question
            quiz_category = body.get('quiz_category')
            category_id = quiz_category.get('id')
            previous_questions = body.get('previous_questions')
            # If id is set to zero, show questions of all categories
            if category_id == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions), 
                ).all()
            # Otherwise filter by category id
            else:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions), 
                    Question.category == category_id
                ).all()
            # Randomly pick from the list
            question = random.choice(questions)
        except:
            print(sys.exc_info())
            abort (500)
        return jsonify({
            'success': True,
            'question': question.format(),
        })


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "Bad Request"
        }), 400


    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Not Found"
        }), 404


    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable Entity"
        }), 422
    

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal Server Error"
        }), 500
    return app
