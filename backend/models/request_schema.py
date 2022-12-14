from marshmallow import Schema, fields, ValidationError
from marshmallow import ValidationError

class CreateQuestionRequestSchema(Schema):
    def validate_difficulty_scale(difficulty: int):
        if difficulty < 1 or difficulty > 5:
            raise ValidationError("Difficulty must be from 1 to 5.")
    question = fields.String(required=True)
    answer = fields.String(required=True)
    category = fields.Integer(required=True)
    difficulty = fields.Integer(required=True, validate=validate_difficulty_scale)


class SearchQuestionRequestSchema(Schema):
    searchTerm = fields.String(required=True)


class QuizzesRequestSchema(Schema):
    # Schema of quiz_category
    class QuizCategorySchema(Schema):
        type = fields.String()
        id = fields.Integer(required=True)
    quiz_category = fields.Nested(QuizCategorySchema)
    previous_questions = fields.List(fields.Int, required=True)
