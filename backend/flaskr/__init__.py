import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    cors = CORS(app, resources={r"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', "Content-Type, Authorization, true")
        response.headers.add('Access-Control-Allow-Methods', "GET,POST,DELETE")
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        if categories is None:
            abort(404)

        formatted_categories = [category.get_name() for category in categories]
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start_index = (page - 1) * QUESTIONS_PER_PAGE
        end_index = start_index + QUESTIONS_PER_PAGE

        questions = Question.query.all()

        if questions is None:
            abort(404)

        current_page_questions = questions[start_index:end_index]

        formatted_questions = [question.format() for question in current_page_questions]

        categories = Category.query.all()

        formatted_categories = [category.get_name() for category in categories]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'current_page_total_questions': len(formatted_questions),
            'total_questions': len(questions),
            'current_category': 'All',
            'categories': formatted_categories
        })

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.get(id)

            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True
            })
        except:
            abort(422)

    @app.route('/questions/<int:id>', methods=['GET'])
    def get_question(id):
        question = Question.query.get(id)

        if question is None:
            abort(404)

        return jsonify({
            'id': id,
            'success': True,
            'question': question.format()
        })

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
    @app.route('/questions', methods=['POST'])
    def post_question():
        try:
            form = request.get_json()
            question = create_question_from_form(form)
            question.insert()
            return jsonify({
                'success': True,
                'question': question.format()
            })
        except Exception as exception:
            print(exception)
            abort(422)

    def create_question_from_form(form):
        form_question = form['question']
        answer = form['answer']
        difficulty = form['difficulty']
        category = form['category']
        question = Question(question=form_question, answer=answer, difficulty=difficulty, category=category)
        return question

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
    @app.route('/search', methods=['POST'])
    def search_question():
        return jsonify({
            'success': True
        })

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable Entity"
        }), 422

    return app
