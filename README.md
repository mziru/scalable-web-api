
# web-api-with-orm

This repo contains code for an example RESTful web API with create, read, update, and delete (CRUD) operations and data persistence. It is scalable and intended to serve as a foundation for developing more complex database interfaces in Python using Object-Relational Mapping. 

The sample data models represent fictional people and Covid-19 test results, which have a one-to-many relationship. Each person's Covid status is updated automatically based on their most recent test result.

#### Technologies:
-	Google App Engine and Google Cloud SQL for cloud deployment
-	Flask web framework
-	PostgreSQL for RDBMS
-	SQLAlchemy for ORM
-	marshmallow for data object serialization
-	Swagger for API design and documentation (OpenAPI Specification)

#### Database connection:

The app requires a PostgreSQL database connection to run. To set this up, add a file to the base directory called "postgres_uri.txt" containing the URI for the database that you would like to use.

For a local connection, the URI will look something like this:

postgresql://<db_user>:<db_password>@localhost/<db_name>

#### API security:

The example API requires basic authorization for operations that modify the database. To set this up, add a file to the base directory called "auth.txt" containing credentials to be used for authorization, formatted as a dictionary, e.g.

{"<user_1>": "<password_1>", "<user_2>": "<password_2>"}

NOTE: this authorization method is used for testing purposes only and should not be considered secure for use with a production database.


#### Using the API:

Once the database URI and authorization credentials are configured, the app can be tested locally by running "main.py". When the app is run, Swagger will automatically build documentation and a browser interface, which can be used to explore and test the API:

<img src="https://github.com/mziru/scalable-web-api/blob/master/swagger-ui.png?raw=true" style="width: 100%">

