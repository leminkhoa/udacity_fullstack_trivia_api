# Play Quizzes

**Description** : Endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.

**URL** : `/quizzes`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : 
Provide category and previous questions (to be excluded from question generation)
```
{
    "quiz_category": {
        "id": <int: Category ID>
    },
    "previous_questions": [<array of integers>]
}
```

**Data Example** :
Generate random question from category with `id=1` while exclude question 2 and 3
```json
{
    "quiz_category": {
        "id": 1
    },
    "previous_questions": [2, 3]
}
```

Generate random question from all categories with no restriction
```json
{
    "quiz_category": {
        "id": 0
    },
    "previous_questions": []
}
```

## Success Responses

**Code** : `200 OK`

**Content** : 

```json
{
    "question": {
        "answer": "Alexander Fleming",
        "category": 1,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
    },
    "success": true
}
```