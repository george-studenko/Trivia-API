# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET '/categories/<id>/questions'
GET '/questions'  
GET '/questions/<id>'
POST '/questions'
POST '/quizes'
POST '/search'
DELETE '/questios/<id>'

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

- Errors: 404 if the requested category does not exist

{
  "error": 404, 
  "message": "Not found", 
  "success": false
}

GET '/categories/<id>/questions'
- Fetches the questions for a given category
- Request Arguments: Category Id
- Returns: An object with currentCategory, and question objects from the category. 

{
  "currentCategory": 1, 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}

- Errors: 404 if the requested category has no questions or the category does not exist

{
  "error": 404, 
  "message": "Not found", 
  "success": false
}

GET '/questions'  
- Fetches the all questions and categories paginated 10 questions at a time
- Request Arguments: Page, by default page is set to one if not sent
- Returns: An object with all categories, and all question from all categories. 

{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": "All", 
  "current_page_total_questions": 10, 
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
      ], 
  "success": true, 
  "total_questions": 2
}

- Errors: 404 if the page does not exist

{
  "error": 404, 
  "message": "Not found", 
  "success": false
}


GET '/questions/<id>'
- Fetches the all questions and categories
- Request Arguments: None
- Returns: An object with all categories, and all question from all categories. 

{
  "id": 6, 
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }, 
  "success": true
}

POST '/questions'
- Creates a new question
- Request Arguments: question, answer, category and difficulty
- Returns: the created question

{
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }, 
  "success": true
}

- Errors: 422 if the question could not be created

{
  "error": 422, 
  "message": "Unprocessable Entity", 
  "success": false
}

POST '/quizes'
- Requests the questions for the game
- Request Arguments: previous_questions array with the ids of the already played questions, and quiz_category object: 
{'previous_questions': [17], 'quiz_category': {'type': 'Art', 'id': '2'}}
- Returns: a random question from the category requested (if the category requested is 0 then it retrieves questions from all categories)

{
  "question": {
    "answer": "Edward Scissorhands", 
    "category": 5, 
    "difficulty": 3, 
    "id": 6, 
    "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
  }, 
  "success": true
}

POST '/search'
- Searchs for a question
- Request Arguments: searchTerm 
- Returns: an array of questions with the results from the search

{
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "currentCategory": "all", 
  "success": true, 
  "totalQuestions": 2
}

-Errors: 404 if there are no questions for the searched term]

{
  "error": 404, 
  "message": "Not found", 
  "success": false
}

- Errors: 422 if searchTerm as not sent or was miss spelled

{
  "error": 422, 
  "message": "Unprocessable Entity", 
  "success": false
}

DELETE '/questios/<id>'
- Deletes a question given the question id to be deleted
- Request Arguments: searchTerm 
- Returns: an array of questions with the results from the search

{
  "success": true, 
}

- Errors: 404 if the requested question does not exist

{
  "error": 404, 
  "message": "Not found", 
  "success": false
}

- Errors: 422 if something fails

  "error": 422, 
  "message": "Unprocessable Entity", 
  "success": false
}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

** A more convenient way to run the tests is to execute:
```
./run_tests.sh
```

The line above will execute all the 4 lines above in the same order, this way instead of running 4 instructions manually only one line needs to be executed.

If the file does not run because of permissions, execute the following line:
```
chmod +x run_tests.sh
```
