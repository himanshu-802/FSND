# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7
# GIT CLONE DEMO
Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
```bash
pip install virtualenv 
virtualenv myenv
myenv\Scripts\activate
```
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
psql -U postgres trivia< trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:
```bash
set FLASK_APP=flaskr
set FLASK_ENV=development
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

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

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

```


DELETE `/questions/<question_id>`
Delete an existing questions from the repository of available questions
- *Request arguments:* question_id:int 
- *Example response:* 
```
{
  "deleted": "28", 
  "success": true
}
```
POST `/quizzes`
Fetches one random question within a specified category. Previously asked questions are not asked again. 
- *Request body:* {previous_questions: arr, quiz_category: {id:int, type:string}}
- *Example response*: 
```
{
  "question": {
    "answer": "The Liver", 
    "category": 1, 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```
GET `/categories/<int:category_id>/questions`
Fetches a dictionary of questions for the specified category
- *Request argument:* category_id:int
- *Example response:*
```
{
  "current_category": 1, 
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
    }, 
  ], 
  "success": true, 
  "total_questions": 2
}
```
##API DOCUMENTATION

##BASE URL

Since this API is not hosted on a specific domain, it can only be accessed when
`flask` is run locally. To make requests to the API via `curl` or `postman`,
you need to use the default domain on which the flask server is running.

**_http://127.0.0.1:5000/_**


Here is a short table about which ressources exist and which method you can use on them.

                          Allowed Methods
       Endpoints    |  GET |  POST |  DELETE | 
                    |------|-------|---------|
      /questions    |  [x] |  [x]  |   [x]   |         
      /categories   |  [x] |  [x]  |   [x]   |           
      /quizzes      |      |  [x]  |         | 


### 1. GET /questions

Fetch paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/questions?page=1
```

- Fetches a list of dictionaries of questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.
- Returns: 
  1. List of dict of questions with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **list** `categories`
  3. **list** `current_category`
  4. **integer** `total_questions`
  5. **boolean** `success`



### 2. POST /questions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{"searchTerm" : "test"}' -H 'Content-Type: application/json'
```

Create new Question
```bash
curl -X POST http://127.0.0.1:5000/questions -d '{ "question" : "Is this a test question?", "category" : "1" , "answer" : "Yes it is!", "difficulty" : 1 }' -H 'Content-Type: application/json'
```
- Searches database for questions with a search term, if provided. Otherwise,
it will insert a new question into the database.
- Request Arguments: **None**
- Request Headers :
  - if you want to **search** (_application/json_)
       1. **string** `searchTerm` (<span style="color:red">*</span>required)
  - if you want to **insert** (_application/json_) 
       1. **string** `question` (<span style="color:red">*</span>required)
       2. **string** `answer` (<span style="color:red">*</span>required)
       3. **string** `category` (<span style="color:red">*</span>required)
       4. **integer** `difficulty` (<span style="color:red">*</span>required)
- Returns: 
  - if you searched:
    1. List of dict of `questions` which match the `searchTerm` with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. List of dict of ``current_category`` with following fields:
        - **integer** `id`
        - **string** `type`
    3. **integer** `total_questions`
    4. **boolean** `success`
  - if you inserted:
    1. List of dict of all questions with following fields:
        - **integer** `id` 
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. **integer** `total_questions`
    3. **integer** `created`  id from inserted question
    4. **boolean** `success`



### 3. DELETE /questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/questions/10
```
- Deletes specific question based on given id
- Request Arguments: 
  - **integer** `question_id`
- Request Headers : **None**
- Returns: 
    - **integer** `deleted` Id from deleted question.
    - **boolean** `success`


#### Example response
```js
{
  "deleted": 10,
  "success": true
}
```

### Errors

If you try to delete a `question` which does not exist, it will throw an `400` error:

```bash
curl -X DELETE http://127.0.0.1:5000/questions/7
```
will return
```js
{
  "error": 400,
  "message": "Question with id 7 does not exist.",
  "success": false
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql -U postgres trivia_test < trivia.psql
python test_flaskr.py
```




### 4. POST /quizzes

Play quiz game.
```bash
curl -X POST http://127.0.0.1:5000/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Headers : 
     1. **list** `previous_questions` with **integer** ids from already asked questions
     1. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **integer** id from category
- Returns: 
  1. Exactly one `question` as **dict** with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **boolean** `success`

#### Example response
```js
{
  "question": {
    "answer": "Jup",
    "category": 1,
    "difficulty": 1,
    "id": 24,
    "question": "Is this a test question?"
  },
  "success": true
}

```
### Errors

If you try to play the quiz game without a a valid JSON body, it will response with an  `400` error.

```bash
curl -X POST http://127.0.0.1:5000/quizzes
```
will return
```js
{
  "error": 400,
  "message": "Please provide a JSON body with previous question Ids and optional category.",
  "success": false
}

```


### 5. GET /categories

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/categories
```

- Fetches a list of all `categories` with its `type` as values.
- Request Arguments: **None**
- Request Headers : **None**
- Returns: A list of categories with its `type` as values
and a `success` value which indicates status of response. 

#### Example response
```js
{
  "categories": [
    "Science",
    "Art",
    "Geography",
    "History",
    "Entertainment",
    "Sports"
  ],
  "success": true
}
```

# <a name="get-categories-questions"></a>
### 6. GET /categories/<category_id>/questions

Get all questions from a specific `category`.
```bash
curl -X GET http://127.0.0.1:5000/categories/2/questions?page=1
```
- Fetches all `questions` (paginated) from one specific category.
- Request Arguments:
  - **integer** `category_id` (<span style="color:red">*</span>required)
  - **integer** `page` (optinal, 10 questions per Page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. **integer** `current_category` id from inputted category
  2. List of dict of all questions with following fields:
     - **integer** `id` 
     - **string** `question`
     - **string** `answer`
     - **string** `category`
     - **integer** `difficulty`
  3. **integer** `total_questions`
  4. **boolean** `success`

#### Example response

```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "total_questions": 4
}

````
### 7. POST /categories

Create new category.
```bash
curl -X POST http://127.0.0.1:5000/categories -d '{ "type" : "Nerd Stuff"}' -H 'Content-Type: application/json'
```

- Inserts a new `category` to extend gameplay with new kind of questions.
- Request Arguments: **None**
- Request Headers : (_application/json_) 
   1. **string** type (<span style="color:red">*</span>required)
- Returns: 
  1. List of dict of all existing `categories` with following fields:
      - **integer** `id` 
      - **string** `type`
  2. **integer** `total_categories` number of all `categories`
  3. **integer** `created`  id from inserted `category`
  4. **boolean** `success`

#### Example response
```js
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    {
      "id": 3,
      "type": "Geography"
    },
    {
      "id": 4,
      "type": "History"
    },
    {
      "id": 5,
      "type": "Entertainment"
    },
    {
      "id": 6,
      "type": "Sports"
    },
    {
      "id": 7,
      "type": "Nerd Stuff"
    }
  ],
  "created": 7,
  "success": true,
  "total_categories": 7
}
```
