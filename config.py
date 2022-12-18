import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import MetaData

metadata_obj = MetaData()

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir,
                           options={"swagger_ui": True})

with open("local_postgres_uri.txt", "r") as file:
    postgres_uri = file.read()

# with open("postgres_uri.txt", "r") as file:
#     postgres_uri = file.read()

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = postgres_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

