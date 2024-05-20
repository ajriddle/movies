import pandas as pd
import os
from flask import Flask, request, render_template, flash, redirect
from wtforms import Form, StringField, SelectField

movies = pd.read_csv('data/Movies.csv')

class MovieSearchForm(Form):
    choices = [('title', 'title'),
               ('digital', 'digital'),
               ('genre', 'genre'),
               ('rating', 'rating'),
               ('actor', 'actor')]
    field = SelectField('Search for movies:', choices=choices)
    search = StringField('')
    
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
@app.route('/movies', methods=['GET', 'POST'])
def index():
    search = MovieSearchForm(request.form)
    if request.method == 'POST':
        if not search.data['search']:
            return render_template('index.html', form=search, movies=movies.to_dict('records'))
        else:
            field = search.data['field']
            value = search.data['search']
            if field == 'title':
                filtered_movies = movies[movies.title.str.contains(value, case=False)]
            elif field == 'digital':
                filtered_movies = movies[movies.digital == value]
            elif field == 'rating':
                filtered_movies = movies[movies.rating > float(value)]
            elif field == 'genre':
                filtered_movies = movies[movies.genres.str.contains(value, case=False)]
            else:
                filtered_movies = movies[movies.actors.str.contains(value, case=False)]
        if len(filtered_movies) == 0:
            flash('No results found!')
            return redirect('/movies')
        else:
            return render_template('index.html', form=search, movies=filtered_movies.to_dict('records'))
    return render_template('index.html', form=search, movies=movies.to_dict('records'))

@app.route('/movies/<id>', methods=['GET'])
def show_movie(id):
    movie = movies[movies.id == id].to_dict('records')[0]
    return render_template('show.html', movie=movie)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    # app.run()