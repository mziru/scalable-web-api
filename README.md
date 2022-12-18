# web-api-example

This project contains code for an example RESTful web API with create, read, update, and delete (CRUD) operations and data persistence. It is intended to serve as a foundation for developing more complex database interfaces in Python. The sample data models represent fictional people and Covid-19 test results, which have a one-to-many relationship. Each person's Covid status is updated automatically based on their most recent test result.

Technologies:
-	PostgreSQL for RMDBS
-	Flask web framework
-	SQLAlchemy for ORM
-	marshmallow for data object serialization
-	Swagger for API design and documentation (OpenAPI Specification)
