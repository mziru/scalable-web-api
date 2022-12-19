from datetime import datetime
from config import db, ma, app
from sqlalchemy import event, DDL


# object data model for Person table
class Person(db.Model):
    __tablename__ = "person"
    name = db.Column(db.String(32), primary_key=True)
    covid_positive = db.Column(db.Boolean)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    # persons and results have a one-to-many relationship
    results = db.relationship('Result', backref='person', lazy=True)


# object data model for Result table
class Result(db.Model):
    __tablename__ = "result"
    name = db.Column(db.String(32), db.ForeignKey('person.name'), nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    covid_positive = db.Column(db.Boolean)
    pcr = db.Column(db.Boolean)
    test_id = db.Column(db.Integer, primary_key=True)


# serialization schema for Person
class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True


# create distinct data serialization schema objects for a single person and multiple people
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)


# serialization schema for Result
class ResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Result
        load_instance = True
        sqla_session = db.session
        include_fk = True
        include_relationships = True


# create distinct data serialization schema objects for a single result and multiple results
result_schema = ResultSchema()
results_schema = ResultSchema(many=True)

# add custom SQL to execute after "person" and "result" table creation.
# creates a trigger to execute upserts on the "person" table based inserts or updates on the "result" table.
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

# call SQLAlchemy event lister function to issue custom SQL after tables are created based on model metadata
event.listen(
    db.Model.metadata,
    "after_create",
    DDL(trigger_ddl)
)

# the SQLAlchemy create_all() method will issue queries that first check for the existence of each individual table
# defined in the model metadata, and if not found will issue the CREATE statements
with app.app_context():
    db.Model.metadata.create_all(db.engine)
