from covidmap import app
from covidmap.utils import populate_db

if __name__ == "__main__":
    populate_db()
    app.run(debug=True)
