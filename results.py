from flask import make_response, abort
from config import db
from models import Result, result_schema, results_schema


def read_all_results():
    results = Result.query.all()
    return results_schema.dump(results)


def read_results_one_person(name):
    results = Result.query.filter(Result.name == name)
    result_list = results_schema.dump(results)
    if len(result_list) > 0:
        return result_list
    else:
        abort(
            404,
            f"{name} not found."
        )


def create_result(result):
    new_result = result_schema.load(result, session=db.session)
    db.session.add(new_result)
    db.session.commit()
    return result_schema.dump(new_result), 201
