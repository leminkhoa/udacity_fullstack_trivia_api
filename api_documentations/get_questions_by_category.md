# Get Questions Based On Category

**Description** : Endpoint to get questions based on category.

**URL** : `/categories/<int:category_id>/questions`

**Method** : `GET`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : `{}`

**Example** :
This request will return all questions belong to category that has `id=5`
```
/categories/5/questions
```

## Success Responses

**Code** : `200 OK`

**Content** : 

```json
{
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
        {
            ...
        }
    ],
    "success": true,
    "total_questions": 8
}
```
