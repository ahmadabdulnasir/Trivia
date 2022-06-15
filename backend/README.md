# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.


## Endpoint Documentation

### GET `/categories`
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
- Request arguments: None.
- Returns:  An object with these keys:
  - `success`: The success flag
  - `categories`: Contains a object of `id:category_string` and `key:value pairs`.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET `/questions`
- Returns:
  - A list of questions paginated by 10 questions per page
  - A dictionary of categories
  - The total of questions
  - The current category
- Request arguments:
  - `page` (integer) - The current page (default to 1)
- Response: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions (paginated by 10 items)
  - `categories`: A dictionary of categories
  - `total_questions`: The total of questions
  - `current_category`: The current category

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
  ],
  "success": true,
  "total_questions": 19
}
```

### DELETE `/questions/:question_id/`
- Delete question using the question ID
- Request query params:
  - `question_id` (integer): The question id
- Response: An object with theses keys:
  - `success` flag of success `boolean`.
  - `deleted` ID of the deleted question.

```json
{
  "success": true,
  "deleted": 1,
}
```

### POST `/questions`
- Create a new question.
- Request Body:
  - `question` (char) - The question
  - `answer` (char) - The answer
  - `difficulty` (char) - The question difficulty
  - `category` (char) - The question category
- Response: An object with theses keys:
  - `success` flag of success `boolean`.
  - `created` ID of the created question.

```json
{
  "success": true,
  "created": 1,
}
```

### POST `/search`
- Search a question.
- Request arguments:
  - `search` (char) - The term to search
- Returns: An object with these keys:
  - `success`: The success flag
  - `questions`: A list of questions
  - `total_questions`: The total of questions
  - `current_category`: The current category

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "total_questions": 10,
  "current_category": null,
}
```


### GET `/categories/:category_id/questions`
- Return list of questions based on category.
- Request arguments:
  - `category_id` (integer): The category id
- Response: An object with these keys:
  - `success`: success flag
  - `questions`: List of questions paginated by 10 questions
  - `total_questions`: total of questions
  - `current_category`: current category

```json
{
  "success": true,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "total_questions": 10,
  "current_category": 1,
}
```

### POST `/quizzes`
- Return a question to play the quiz.
- Request body (json):
  - `quiz_category` (dict): quiz category with the `type` and the `id`.
  - `previous_ids` (list): previous questions ids or null
- Response: An object with these keys:
  - `success`: The success flag
  - `question`: The question to play

```json
{
  "success": true,
  "question":{
    "answer": "Apollo 13",
    "category": 5,
    "difficulty": 4,
    "id": 2,
    "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
  }
}
```

## Errors
### Error 400
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 400,
  "message": "Bad request!!!"
}
```

### Error 404
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 404,
  "message": "Not Found!!!"
}
```

### Error 422
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 422,
  "message": "Request Unprocessable!!!"
}
```

### Error 406
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 406,
  "message": "Not Acceptable!!!"
}
```

### Error 500
- Returns an object with these keys: `success`, `error` and `message`.

```json
{
  "success": false,
  "error": 500,
  "message": "Server Error!!!"
}
```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb udacity_test_triviadb
createdb udacity_test_triviadb
psql udacity_test_triviadb < trivia.psql
python test_flaskr.py
```

## Running
```shell
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```