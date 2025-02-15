import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    """Pagination helper of questions

    Args:
        request: current request
        questions: questions query objects

    Returns:
        list: list of formatted question
    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in questions]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # db.init_app(app)

    """
    Done Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        """
            after_request decorator to set Access-Control-Allow
        """
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/categories")
    def category_list():
        """
        Return All available categories
        """
        categories = Category.query.order_by(Category.type).all()
        # categories = Category.query.all()
        if len(categories) == 0:
            abort(404)
        all_categories = {}
        for category in categories:
            all_categories[category.id] = category.type

        # category.format()
        return jsonify({"success": True, "categories": all_categories})

    @app.route("/questions")
    def question_list():
        page = request.args.get("page", default=1, type=int)
        questions = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, questions)
        if len(current_questions) == 0:
            # query return empty
            abort(404)

        categories = Category.query.order_by(Category.type).all()
        all_categories = {}
        for category in categories:
            all_categories[category.id] = category.type

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": all_categories,
            }
        )

    @app.route("/questions/<question_id>", methods=["DELETE"])
    def question_delete(question_id):
        """
            Delete a single question by the question_id
        """
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({"success": True, "deleted": question_id})
        except Exception as exp:
            print(f"Error: {exp}")
            abort(422)

    @app.route("/questions", methods=["POST"])
    def question_create():
        """
            Create a new Question
        """
        body = request.get_json()
        question = body.get("question")
        answer = body.get("answer")
        difficulty = body.get("difficulty")
        category = body.get("category")

        error_list = []
        required_info = {
            "question": question,
            "answer": answer,
            "difficulty": difficulty,
            "category": category,
        }
        for entry in required_info.keys():
            if not required_info.get(entry):
                error_list.append(f"Invalid Entry of: {entry}")
        if error_list:
            # return jsonify({
            #     'success': False,
            #     "detail": "Fail to Create Question, Non or Partial Data Received.",
            #     "errors": error_list,
            # })
            abort(406)

        try:
            target_question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category,
            )
            target_question.insert()

            return jsonify({"success": True, "created": target_question.id})

        except Exception as exp:
            print(f"Error: {exp}")
            abort(422)

    @app.route("/questions/search", methods=["POST"])
    def question_search():
        body = request.get_json()
        search_term = body.get("searchTerm", None)
        # search_term_dump = request.form.get('searchTerm', None)
        if search_term:
            search_term = search_term.strip()
            search_results = Question.query.filter(
                Question.question.ilike(f"%{search_term}%")
            ).all()

            paginated_search_results = paginate_questions(request, search_results)

            return jsonify(
                {
                    "success": True,
                    "questions": [question for question in paginated_search_results],
                    "total_questions": len(search_results),
                    "current_category": None,
                }
            )
        else:
            print("No search term!!!")
            abort(404)

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def category_questions_list(category_id):
        """
            Return questions based on category
        """
        try:
            questions = Question.query.filter(
                Question.category == int(category_id)
            ).all()
            paginated_category_questions = paginate_questions(request, questions)
            return jsonify(
                {
                    "success": True,
                    "questions": paginated_category_questions,
                    "total_questions": len(questions),
                    "current_category": category_id,
                }
            )
        except Exception as exp:
            print(f"Error: {exp}")
            abort(422)

    @app.route("/quizzes", methods=["POST"])
    def trivia_quiz():
        """
            Play the Trivia Quiz
        """
        try:
            body = request.get_json()
            quiz_category = body.get("quiz_category")
            previous_questions = body.get("previous_questions", [])
            # To handle when previous_questions was sent as null
            if not previous_questions:
                previous_questions = []
            required_info = {
                "quiz_category": quiz_category,
                # "previous_questions": previous_questions,
            }
            error_list = []
            for entry in required_info.keys():
                if not required_info.get(entry):
                    error_list.append(f"Invalid Entry of: {entry}")
            if error_list:
                print(
                    {
                        "success": False,
                        "detail": "Fail to start Quiz, Non or Partial Data Received.",
                        "errors": error_list,
                    }
                )
                abort(406)
            print(quiz_category)
            print(previous_questions)
            # get
            all_questions = Question.query.filter(
                Question.id.notin_((previous_questions))
            ).all()
            if quiz_category["type"] == "click":
                target_questions = all_questions
            else:
                target_questions = (
                    Question.query.filter_by(category=quiz_category["id"])
                    .filter(Question.id.notin_((previous_questions)))
                    .all()
                )
            if len(target_questions) > 0:
                target_question = random.choice(target_questions).format()
            else:
                target_question = None
            return jsonify({"success": True, "question": target_question})
        except Exception as exp:
            print(f"Error: {exp}")
            abort(422)

    @app.errorhandler(404)
    def not_found_error(error):
        # return render_template('errors/404.html'), 404
        return jsonify({"success": False, "error": 404, "message": "Not Found!!!"}), 404

    @app.errorhandler(406)
    def not_found_error(error):
        return (
            jsonify({"success": False, "error": 406, "message": "Not Acceptable!!!"}),
            406,
        )

    @app.errorhandler(422)
    def unprocessable_error(error):
        print(error)
        return (
            jsonify(
                {"success": False, "error": 422, "message": "Request Unprocessable!!!"}
            ),
            422,
        )

    @app.errorhandler(400)
    def bad_request_error(error):
        return (
            jsonify({"success": False, "error": 400, "message": "Bad request!!!"}),
            400,
        )

    @app.errorhandler(500)
    def server_error(error):
        # return render_template('errors/500.html'), 500
        return (
            jsonify({"success": False, "error": 500, "message": "Server Error!!!"}),
            500,
        )

    return app
