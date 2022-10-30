# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Getting Started

To run this project, developer should install these pre-requisites:
- Python 3.9
- npm 

Both **Backend** and **Frontend** has separate set up process, please follow instructions for each part:
- [Back End](backend/README.md)
- [Front End](frontend/README.md)

## API Documentations
### Endpoints

Below are all endpoints used to run Trivia Project 

* [Get Question Categories](api_documentations/get_categories.md) : `GET /categories`
* [Get Questions](api_documentations/get_questions.md) : `GET /questions`
* [Delete Questions](api_documentations/delete_questions.md) : `DELETE /questions/<int:id>`
* [Create Questions](api_documentations/create_questions.md) : `POST /questions`
* [Search Questions](api_documentations/search_questions.md) : `POST /questions/search`
* [Get Questions By Category](api_documentations/questions_by_category.md) : `POST /categories/<int:category_id>/questions`
* [Play Quizzes](api_documentations/quizzes.md) : `POST /quizzes`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```

The API will return four error types when requests fail:
```
- 400: Bad Request
- 404: Not Found
- 422: Unprocessable Entity
- 500: Internal Server Error
```

