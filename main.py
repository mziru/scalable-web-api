from flask import render_template
import config
from models import Person, Result, create_tables

app = config.connex_app
app.add_api(config.basedir / "my_api.yaml")

create_tables()


@app.route('/')
def home_func():
    people = Person.query.all()
    results = Result.query.all()
    return render_template('home.html', people=people, results=results)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)
