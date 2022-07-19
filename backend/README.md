##Server Setup

###  Step 1: Set up and Populate the Database

With Postgres running, create a trivia database:

`createdb trivia`

From the backend folder in terminal, Populate the database using the trivia.psql file provided.run:

`psql trivia < trivia.psql`

Likewise create the test database trivia_test.psql and populate

`createdb trivia_test`

`psql trivia_test < trivia.psql`

Create a *variables.env* file setting the keys outlined in *variables.env.example* file
### Step 2: Install Dependencies

Once your virtual environment is setup and running, install the required dependencies by navigating to the /backend directory and running:

`pip install -r requirements.txt`

### Step 3: Start the Server

Start the Server

In the backend directory, start the Flask server by running:

```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

### Documentation

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
---

`GET '/questions?page=${integer}'`

- Fetches a paginated set of questions, a total number of questions, all categories and current category string.
- Request Arguments: page - integer
- Returns: An object with 10 paginated questions, total questions, object including all categories

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 2
        }
    ],
    "totalQuestions": 100,
    "categories": { "1" : "Science",
    "2" : "Art",
    "3" : "Geography",
    "4" : "History",
    "5" : "Entertainment",
    "6" : "Sports" }
}
```
---

`GET '/categories/${id}/questions'`

- Fetches questions for a cateogry specified by id request argument
- Request Arguments: id - integer
- Returns: An object with questions for the specified category, total questions, and current category string

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 4
        }
    ],
    "totalQuestions": 1,
    "currentCategory": "History"
}
```
---

`DELETE '/questions/${id}'`

- Deletes a specified question using the id of the question
- Request Arguments: id - integer
- Returns: Returns the appropriate HTTP status code of 200 on success.

---

`POST '/quizzes'`

- Sends a post request in order to get the next question
- Request Body:

```json
{
    "previous_questions": [1, 4, 20, 15],
    "quiz_category": "current category"
}
```


- Returns: a single new question object

```json
{
    "question": {
        "id": 1,
        "question": "This is a question",
        "answer": "This is an answer",
        "difficulty": 5,
        "category": 4
    }
}
```
---

`POST '/questions'`

- Sends a post request in order to add a new question
- Request Body:

```json
{
    "question":  "Heres a new question string",
    "answer":  "Heres a new answer string",
    "difficulty": 1,
    "category": 3
}
```
- Returns: Does not return any new data

---

`POST '/questions'`

- Sends a post request in order to search for a specific question by search term
- Request Body:

```json
{
    "searchTerm": "this is the term the user is looking for"
}
```

- Returns: any array of questions, a number of totalQuestions that met the search term and the current category string

```json
{
    "questions": [
        {
            "id": 1,
            "question": "This is a question",
            "answer": "This is an answer",
            "difficulty": 5,
            "category": 5
        }
    ],
    "totalQuestions": 100
}
```



