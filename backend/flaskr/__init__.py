import random
import sys

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from sqlalchemy import exc

from models.request_schema import *
from models.models import setup_db, Question, Category
from . import error_handler

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
    app.register_blueprint(error_handler.blueprint)
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
    
    return app
