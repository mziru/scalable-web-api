from flask import make_response, abort
from config import db
from models import Person, person_schema, people_schema


def read_all_people():
    people = Person.query.all()
    return people_schema.dump(people)


def create_person(person):
    name = person.get('name')
    existing_person = Person.query.filter(Person.name == name).one_or_none()

    if existing_person is None:
        new_person = person_schema.load(person, session=db.session)
        db.session.add(new_person)
        db.session.commit()
        return person_schema.dump(new_person), 201
    else:
        abort(
            406,
            f'A person named {name} already exits in the database.'
        )


def read_one_person(name):
    person = Person.query.filter(Person.name == name).one_or_none()

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(
            404,
            f"{name} not found."
        )


def update_covid_status(name, person):
    existing_person = Person.query.filter(Person.name == name).one_or_none()

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.covid_positive = update_person.covid_positive
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(
            404,
            f"{name} not found."
        )


def delete_person(name):
    existing_person = Person.query.filter(Person.name == name).one_or_none()

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{name} successfully deleted", 200)
    else:
        abort(404, f"Person with name {name} not found")
