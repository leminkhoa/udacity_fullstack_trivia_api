import flask 
from flask import jsonify

blueprint = flask.Blueprint('error_handler', __name__)


@blueprint.app_errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        'error': 400,
        "message": "Bad Request"
    }), 400


@blueprint.app_errorhandler(404)
def page_not_found(error):
    return jsonify({
        "success": False,
        'error': 404,
        "message": "Not Found"
    }), 404


@blueprint.app_errorhandler(422)
def unprocessable_entity(error):
    return jsonify({
        "success": False,
        'error': 422,
        "message": "Unprocessable Entity"
    }), 422


@blueprint.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        'error': 500,
        "message": "Internal Server Error"
    }), 500
