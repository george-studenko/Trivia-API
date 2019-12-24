from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random, json

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
        formatted_categories = dict()

        for category in categories:
            formatted_categories[category.id] = category.type

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

        categories = get_categories()
        content = json.loads(categories.data)
        formatted_categories = content['categories']

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

    @app.route('/search', methods=['POST'])
    def search_question():
        try:
            form = request.get_json()
            search_term = form['searchTerm']

            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            if len(questions) is 0:
                abort(404)

            formatted_questions = [question.format() for question in questions]
            total_questions = len(questions)
            return jsonify({
                'questions': formatted_questions,
                'success': True,
                'totalQuestions': total_questions,
                'currentCategory': 'all'
            })
        except KeyError:
            abort(422)

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        questions = Question.query.filter_by(category=id).all()
        formatted_questions = [question.format() for question in questions]
        if len(questions) is 0:
            abort(404)

        return jsonify({
            'currentCategory': id,
            'success': True,
            'questions': formatted_questions,
            'totalQuestions': len(formatted_questions)
        })

    @app.route('/quizzes', methods=['POST'])
    def get_next_question():
        form = request.get_json()
        category_id = form['quiz_category']['id']
        answered_questions = form['previous_questions']

        questions = get_quizz_questions(category_id)
        remaining_questions = filter_remaining_questions(answered_questions, questions)
        question = get_random_question(remaining_questions)

        return jsonify({
            'success': True,
            'question': question.format()
        })

    def get_random_question(remaining_questions):
        question = random.choice(remaining_questions)
        return question

    def filter_remaining_questions(answered_questions, questions):
        remaining_questions = [q for q in questions if q.id not in answered_questions]
        return remaining_questions

    def get_quizz_questions(category_id):
        if category_id is not 0:
            return Question.query.filter_by(category=category_id).all()
        return Question.query.all()

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

    # @app.errorhandler(500)
    # def unprocessable_entity(error):
    #     return jsonify({
    #         "success": False,
    #         "error": 500,
    #         "message": "Internal server error",
    #         "exception_message": error
    #     }), 500
    return app
