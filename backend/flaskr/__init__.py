import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

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
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Origin", "*"
        )
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type, Authorization, true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET, PUT, POST, DELETE, OPTIONS"
        )
        return response

    @app.route('/categories')
    def retrieve_categories():
        selection = Category.query.order_by(Category.id).all()

        if len(selection) == 0:
            abort(404)

        categories = {category.id: category.type for category in selection}

        return jsonify(
            {
                'success': True,
                'categories': categories
            }
        )

    @app.route('/questions')
    def retrieve_paginated_questions():
        questionSelection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questionSelection)

        categorySelection = Category.query.order_by(Category.id).all()
        categories = {category.id: category.type for category in categorySelection}

        if len(current_questions) == 0 or len(categories) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': current_questions,
                'total_questions': len(Question.query.all()),
                'categories': categories,
                'current_category': None
            }
        )

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify(
                {
                    'success': True
                }
            )
        except:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def create_question():
        body = request.get_json()

        question = body.get('question', None)
        answer = body.get('answer', None)
        difficulty = body.get('difficulty', None)
        category = body.get('category', None)
        searchTerm = body.get('searchTerm', None)

        try:
            if searchTerm:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(searchTerm))
                )
                current_questions = paginate_questions(request, selection)

                return jsonify(
                    {
                        'success': True,
                        'questions': current_questions,
                        'total_questions': len(selection.all())
                    }
                )

            else:

                question = Question(question=question, answer=answer, difficulty=difficulty, category=category)
                question.insert()

                return jsonify(
                    {
                        'success': True
                    }
                )

        except:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route('/categories/<string:category_id>/questions')
    def retrieve_questions_by_category(category_id):
        selection = Question.query.filter_by(category=category_id).all()
        current_questions_by_category = paginate_questions(request, selection)

        if len(current_questions_by_category) == 0:
            abort(404)

        return jsonify(
            {
                'success': True,
                'questions': current_questions_by_category,
                'total_questions': len(Question.query.all()),
                'current_category': Category.query.filter(Category.id == int(category_id)).first().type
            }
        )

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        body = request.get_json()

        previous_quizzes = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            next_question_query = Question.query.filter(~Question.id.in_(previous_quizzes))

            if quiz_category['id'] != 0:
                next_question_query = next_question_query.filter_by(category=quiz_category['id'])

            next_question = next_question_query.first()

            return jsonify(
                {
                    'success': True,
                    'question': next_question.format()
                }
            )

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({'success': False, 'error': 404, 'message': 'resource not found'}),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({'success': False, 'error': 422, 'message': 'unprocessable'}),
            422
        )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (
            jsonify({'success': False, 'error': 405, 'message': 'method not allowed'}),
            405
        )

    return app

