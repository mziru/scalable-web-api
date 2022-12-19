from datetime import datetime
from config import db, ma, app
from sqlalchemy import event, DDL


class Person(db.Model):
    __tablename__ = "person"
    name = db.Column(db.String(32), primary_key=True)
    covid_positive = db.Column(db.Boolean)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    results = db.relationship('Result', backref='person', lazy=True)


class Result(db.Model):
    __tablename__ = "result"
    name = db.Column(db.String(32), db.ForeignKey('person.name'), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    covid_positive = db.Column(db.Boolean)
    pcr = db.Column(db.Boolean)
    test_id = db.Column(db.Integer, primary_key=True)


class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True


person_schema = PersonSchema()
people_schema = PersonSchema(many=True)


class ResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True
        sqla_session = db.session
        include_fk = True
        include_relationships = True


result_schema = ResultSchema()
results_schema = ResultSchema(many=True)

trigger_ddl = """
    CREATE OR REPLACE FUNCTION update_covid_status() RETURNS trigger AS $update_covid_status$
        BEGIN
            INSERT INTO person(name, covid_positive, timestamp)
            VALUES(NEW.name, NEW.covid_positive, now())
            ON CONFLICT(name)
            DO
                UPDATE SET covid_positive = NEW.covid_positive,
                           timestamp = now();
            RETURN NEW;
        END
    $update_covid_status$ LANGUAGE plpgsql;
    
    CREATE OR REPLACE TRIGGER update_covid_status
    BEFORE INSERT OR UPDATE ON result
        FOR EACH ROW EXECUTE PROCEDURE update_covid_status();"""


event.listen(
    db.Model.metadata,
    "after_create",
    DDL(trigger_ddl)
)

with app.app_context():
    db.Model.metadata.create_all(db.engine)


