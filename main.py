from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import requests
import json
from flask import session as flask_session

engine = create_engine('sqlite:///test.db')
session = Session(engine)
Base = declarative_base()
tm = declarative_base()

class Movie(Base):
    __tablename__ = 'Movie'
    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=True)
    year = Column(Integer, nullable=True)
    description = Column(String(250), nullable=True)
    rating = Column(Float, nullable=True)
    ranking = Column(Integer, nullable=True)
    review = Column(String(200), nullable=True)
    image_url = Column(String(200), nullable=True)

Base.metadata.create_all(engine)

class Tmdb(tm):
    __tablename__ = 'Adding_api'
    id = Column(Integer, primary_key=True)
    movie_title = Column(String(250), nullable=False)
    release_date = Column(Integer, nullable=False)
    overview = Column(String(250), nullable=False)
    poster_image_url = Column(String(200), nullable=False)
        
tm.metadata.create_all(engine)



movie_data = [
    {
        "id":1,
        "title":"The Godfather",
        "year":1972,
        "description":"The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.",
        "rating":9.2,
        "ranking":10,
        "review":"An offer you can't refuse.",
        "image_url":"https://upload.wikimedia.org/wikipedia/en/a/af/The_Godfather%2C_The_Game.jpg"
    },
    {
        "id":2,
        "title":"Phone Booth",
        "year":2002,
        "description":"Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
        "rating":7.3,
        "ranking":9,
        "review":"My favourite character was the caller.",
        "image_url":"https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
    },
]


""" for each in movie_data:
    new_movie = Movie(
        id=each['id'],
        title=each['title'],
        year=each['year'],
        description=each['description'],
        rating=each['rating'],
        ranking=each['ranking'],
        review=each['review'],
        image_url=each['image_url']
    )
    session.add(new_movie)
    session.commit() """
    

# Read a specific value from a specific row:
""" movie_query_data = session.query(Movie).filter_by(title="The Godfather").first()
print(movie_query_data.rating) """


 

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
class CafeForm(FlaskForm):
    id__ = HiddenField('ID')
    rating__ = StringField('Rating', validators=[DataRequired()])
    review__ = StringField('Review', validators=[DataRequired()])
    submit__ = SubmitField('submit')

class add_movie(FlaskForm):
    title_add = StringField('Title', validators=[DataRequired()])
    submit_add= SubmitField('search')

class add_movie_from_api(FlaskForm):
    submit_add_api= SubmitField('add')



@app.route("/")
def home():
    # Read All data
    list_of_movies = []
    all_movies = session.query(Movie).all()
    for movie in all_movies:
        dict_ = {
            "id":movie.id,
            "title":movie.title,
            "year":movie.year,
            "description":movie.description,
            "rating":movie.rating,
            "ranking":movie.ranking,
            "review":movie.review,
            "image_url":movie.image_url
        }
        list_of_movies.append(dict_)

    return render_template("index.html", moviess = list_of_movies)



@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form_ = CafeForm()
    movie_id = request.args.get("id")

    if request.method == 'POST' and form_.validate_on_submit():
        movie = session.query(Movie).filter_by(id=movie_id).first()
        if movie:
            movie.rating = form_.rating__.data
            movie.review = form_.review__.data
            session.commit()
            return redirect(url_for('home'))
        else:
            return "Movie not found"
    
    movie = session.query(Movie).filter_by(id=movie_id).first()

    if movie:
        return render_template("edit.html", movie=movie, form_=form_, title = movie.title)
    else:
        return "Movie not found"
    

@app.route('/delete', methods=['GET', 'POST'])
def delete():
    movie_id = request.args.get("id")
    if request.method == 'GET':
        try:
            movie = session.query(Movie).filter_by(id=movie_id).first()
            if movie:
                session.delete(movie)
                session.commit()
        except Exception as e:
            print(f"An error occurred while trying to delete movie {movie_id}: {e}")
            """ session.rollback() """
    return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    form_add = add_movie()
    if form_add.validate_on_submit():
        title_by_user = form_add.title_add.data
        movies_list_search = []
        url = "https://api.themoviedb.org/3/search/movie?include_adult=false&language=en-US&page=1"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkNDg2NjQ5NDY5NjQ4NWE4NTNjN2M5YTM5ZTk4ZmE3ZiIsInN1YiI6IjY1ZjM1MTk5MDZmOTg0MDE4NTQ3NjY4NiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.an13mjeEfjP_z6vzp64ZZD4930eLz046dD-ELPfNEjE",
        }
        params = {
            "query": title_by_user,
        }
        response = requests.get(url, headers=headers, params=params)
        i=-1
        for _ in range(0, len(response.json()["results"])):
            try:
                i+=1
                title = response.json()['results'][i]["original_title"]
                overview = response.json()['results'][i]["overview"]
                poster_img = response.json()['results'][i]["poster_path"]
                release_date = response.json()['results'][i]["release_date"]
                movie_data_tmdb = {
                    "movie_title": title,
                    "movie_release_date": release_date,
                    "movie_overview": overview,
                    "movie_poster_img": f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_img}",
                }
                movies_list_search.append(movie_data_tmdb)
            except IndexError as e:
                print(e)

        for each in movies_list_search:
            new_movie_api = Tmdb(
                movie_title=each['movie_title'],
                release_date=each['movie_release_date'],
                overview=each['movie_overview'],
                poster_image_url=each['movie_poster_img']
            )
            session.add(new_movie_api)
            session.commit()
            


        return redirect(url_for('select'))
    return render_template("add.html", form_add=form_add)


def delete_all_movies(session):
    session.query(Tmdb).delete()
    session.commit()


@app.route('/select', methods=['GET', 'POST'])
def select():
    list_of_movies_tmdb = []
    all_movies = session.query(Tmdb).all()
    for movie in all_movies:
        dict_added_movies = {
            "id":movie.id,
            "title":movie.movie_title,
            "year":movie.release_date,
            "overview":movie.overview,
            "poster_image_url":movie.poster_image_url
        }
        list_of_movies_tmdb.append(dict_added_movies)

    return render_template("select.html", moviesss = list_of_movies_tmdb)

@app.route('/add_new', methods=['GET', 'POST'])
def add_new():
    form_add_api = add_movie_from_api()
    movie_id_api_table = request.args.get("id")
    movies_api = session.query(Tmdb).filter_by(id=movie_id_api_table).first()

    list_movie_api = {
        "id":movies_api.id,
        "title":movies_api.movie_title,
        "release_date":movies_api.release_date,
        "overview":movies_api.overview,
        "poster_image_url":movies_api.poster_image_url,
    }
    return render_template("add_new.html",form_add_api=form_add_api, movie_new = list_movie_api)

@app.route('/copy', methods=['GET', 'POST'])
def copy_from_api_to_db():
    movie_id_table = request.args.get("id")  # Corrected variable name
    if movie_id_table:
        find_movie_api_db = session.query(Tmdb).filter_by(id=movie_id_table).first()
        print(find_movie_api_db)
        if find_movie_api_db:
            new_movie = Movie(
                title=find_movie_api_db.movie_title,
                year=find_movie_api_db.release_date,
                description=find_movie_api_db.overview,
                image_url=find_movie_api_db.poster_image_url,
            )
            session.add(new_movie)
            session.commit()
            delete_all_movies(session)
            return render_template("index.html")
        else:
            return "Movie not found in the database."
    else:
        return "No movie ID provided."




if __name__ == '__main__':
    app.run(debug=True)
