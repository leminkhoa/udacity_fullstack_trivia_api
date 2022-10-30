from marshmallow import Schema, fields, ValidationError
from marshmallow import validate, ValidationError

class QuestionsSchema(Schema):
        answer = fields.String()
        category = fields.Integer()
        difficulty = fields.Integer()
        id = fields.Integer()
        question = fields.String()


class GetQuestionRespondSchema(Schema):

    success = fields.Boolean()
    categories = fields.Dict(keys=fields.Str(), values=fields.Str())
    questions = fields.List(fields.Nested(QuestionsSchema))
    total_questions = fields.Integer()


class GetCategoriesRespondSchema(Schema):
    success = fields.Boolean()
    categories = fields.Dict(keys=fields.Str(), values=fields.Str())
    total_categories = fields.Integer()
