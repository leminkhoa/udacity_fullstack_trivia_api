# Create A Question

**Description** : Endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.

**URL** : `/questions`

**Method** : `POST`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : 
Provide question, answer text, category and difficulty score to create a new question
```
{
    "question": <str: Question Content>,
    "answer": <str: Answer>,
    "category": <int: Categort Name>,
    "difficulty": <int: Difficulty in number (1-5)>
}
```

**Data Example** :
```json
{
    "question": "Which metal was invented by British metallurgist Harold Brearley in 1912?",
    "answer": "Stainless Steel",
    "category": 1,
    "difficulty": 5
}
```

## Success Responses

**Code** : `200 OK`

**Content** : 

```json
{
    "created": 55,
    "success": true,
    "total_questions": 49
}
```
hn