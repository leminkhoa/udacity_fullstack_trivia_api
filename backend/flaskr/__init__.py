import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
import sys

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @cross_origin()
    @app.route('/')
    def hello():      
        return jsonify({'message': 'HELLO WORLD'})
    
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def get_categories():
        error500 = False
        try:
            categories = Category.query.all()
            formatted_categories = [category.format() for category in categories]
        except Exception:
            error500 = True
        if error500:
            abort (500)
        return jsonify({
            'success': True,
            'categories': formatted_categories,
            'total_categories': len(categories)
        })


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        error500 = False
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        try:
            questions = Question.query.all()
            formatted_questions = [question.format() for question in questions]
        except Exception:
            error500 = True
        if error500:
            abort (500)
        return jsonify({
            'success': True,
            'page': page,
            'questions': formatted_questions[start:end],
            'total_questions': len(questions)
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        error500 = False
        question = Question.query.filter(Question.id == question_id).one_or_none()

        if question is None:
            abort(404)
        try:
            question.delete()
        except Exception:
            error500 = True
        if error500:
            abort (500)
        return jsonify({
            'success': True,
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
        error500 = False
        question = request.args.get('question', type=str)
        answer = request.args.get('answer', type=str)
        category = request.args.get('category', type=int)
        difficulty = request.args.get('difficulty', type=int)
        new_question = Question(
            question=question,
            answer=answer,
            category=category,
            difficulty=difficulty,
        )
        try:
            new_question.insert()
        except Exception:
            error500 = True
        if error500:
            abort (500)
        return jsonify({
            'success': True,
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
        error404 = False
        error500 = False
        try:
            search_term = request.args.get('search_term', '')
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]
        except AttributeError:
            error404 = True
            print(sys.exc_info())
        except Exception:
            error500 = True
            print(sys.exc_info())
        if error404:
            abort (404)
        if error500:
            abort (500)
        return jsonify({
            'success': True,
            'results': formatted_questions
        })

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/questions/categories/<int:category_id>', methods=['POST'])
    def question_from_category(category_id):
        error404 = False
        error500 = False
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            formatted_questions = [question.format() for question in questions]
        except AttributeError:
            error404 = True
            print(sys.exc_info())
        except Exception:
            error500 = True
            print(sys.exc_info())
        if error404:
            abort (404)
        if error500:
            abort (500)
        return jsonify({
            'success': True,
            'results': formatted_questions
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
    @app.route('/quiz', methods=['POST'])
    def quiz():
        # error404 = False
        # error500 = False
        # # get the qestion category an the previous question
        # body = request.get_json()
        # quiz_category = body.get('quiz_category')
        # previous_question = body.get('previous_questions')
        
        # random_id = random.randint(0, len(questions))
        return jsonify({
            'success': True,
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
            "message": "Bad request"
        }), 400


    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({
            "success": False,
            'error': 404,
            "message": "Page not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            'error': 422,
            "message": "Unprocessable Entity"
        }), 422
    

    @app.errorhandler(500)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            'error': 500,
            "message": "Internal Server Error"
        }), 500
    return app