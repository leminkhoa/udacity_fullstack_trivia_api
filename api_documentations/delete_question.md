# Delete A Question

**Description** : Endpoint to DELETE question using a question ID.

**URL** : `/questions/<int:id>`

**Method** : `DELETE`

**Auth required** : NO

**Permissions required** : None

**Data constraints** : `{}`

**Example** :
This request will delete a question with id=10
```
/questions/10
```
## Success Responses

**Code** : `200 OK`

**Content** : 

```json
{
    "deleted": 10,
    "success": true,
    "total_questions": 48
}
```
