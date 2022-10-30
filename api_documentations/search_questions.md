# Search Questions

**Description** : Endpoint to get questions based on a search term.It should return any questions for whom the search term is a substring of the question.


**URL** : `/questions/search`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : 
Provide question, answer text, category and difficulty score to create a new question
```
{
    "searchTerm": <str: Search Term>,
}
```

**Data Example** :
```json
{
    "searchTerm": "what is",
}
```

## Success Responses

**Code** : `200 OK`

**Content** : 

```json
{
    "questions": [
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            ...
        }
    ],
    "success": true,
    "total_questions": 4
}
```
