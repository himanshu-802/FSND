import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    question_list = [question.format() for question in selection]
    temp = question_list[start:end]
    return temp


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,PATCH,DELETE,OPTIONS')
        return response

    @app.route('/categories')
    def get_categories():
        try:
            categories = Category.query.order_by(Category.type).all()
            temp = {i.id: i.type for i in categories}
            if len(categories) == 0:
                abort(404)
            return jsonify({"success": True, "categories": temp})
        except BaseException:
            abort(500)

    @app.route('/questions', methods=['GET'])
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        question_list = pagination(request, selection)

        categories = Category.query.order_by(Category.type).all()
        category_dict = {i.id: i.type for i in categories}
        # arr = [i['type'] for i in categories]

        if len(question_list) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': question_list,
            'total_questions': len(selection),
            'categories': category_dict,
            'current_category': None
        })

    @app.route('/questions/<int:ques_id>', methods=['DELETE'])
    def delete_question(ques_id):
        try:
            question = Question.query.get(ques_id)
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.all()
            current_ques = pagination(request, selection)
            return jsonify({
                'success': True,
                'deleted': ques_id
            })
        except BaseException:
            abort(422)

    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        if not (
                'question' in body and 'answer' in body and
                'difficulty' in body and 'category' in body):
            abort(422)

        new_quest = body.get('question')
        new_ans = body.get('answer')
        new_diff = body.get('difficulty')
        new_cat = body.get('category')

        try:
            question = Question(
                question=new_quest,
                answer=new_ans,
                difficulty=new_diff,
                category=new_cat)
            question.insert()

            return jsonify({
                'success': True,
                'created': question.id
            })
        except BaseException:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        if search_term:
            search_results = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            temp = [i.format() for i in search_results]

            return jsonify({
                'success': True,
                'questions': temp,
                'total_questions': len(search_results),
                'current_category': None
            })
        abort(404)

    @app.route('/categories/<int:cat_id>/questions', methods=['GET'])
    def get_category_questions(cat_id):
        questions = Question.query.filter(
            Question.category == str(cat_id)).all()
        question_list = pagination(request, questions)

        if len(question_list) == 0:
            abort(404)
        return jsonify({
            'success': True,
            'questions': question_list,
            'total_questions': len(questions),
            'categories': Category.query.get(cat_id).format(),
            'current_category': cat_id
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:

            body = request.get_json()

            if not ('quiz_category' in body and 'previous_questions' in body):
                abort(422)

            category = body.get('quiz_category')
            previous_questions = body.get('previous_questions')

            if category['type'] == 'click':
                arr = Question.query.filter(
                    Question.id.notin_((previous_questions))).all()
            else:
                arr = Question.query.filter_by(
                    category=category['id']).filter(
                    Question.id.notin_(
                        (previous_questions))).all()

            new_ques = arr[random.randrange(
                0, len(arr))].format() if len(arr) > 0 else None

            return jsonify({
                'success': True,
                'question': new_ques
            })
        except BaseException:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad_request"
        }), 400

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "server_error"
        }), 500

    return app
