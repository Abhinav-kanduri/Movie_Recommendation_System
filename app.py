import flask
import csv
from flask import Flask, render_template, request
import difflib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

app = flask.Flask(__name__, template_folder='templates')

df2 = pd.read_csv('./data/metadata_final.csv')
count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['combine'])

cosine_sim2 = cosine_similarity(count_matrix)

df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['movie_title'])
all_titles = [df2['movie_title'][i] for i in range(len(df2['movie_title']))]

def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    tit = df2['movie_title'].iloc[movie_indices]
    director = df2['director_name'].iloc[movie_indices]
    actor1 = df2['actor_1_name'].iloc[movie_indices]
    actor2 = df2['actor_2_name'].iloc[movie_indices]
    actor3 = df2['actor_3_name'].iloc[movie_indices]
    genre = df2['genres'].iloc[movie_indices]


    return_df = pd.DataFrame(columns=['movie_title','genres'])
    return_df['movie_title'] = tit
    return_df['director_name'] = director
    return_df['actor_1_name'] = actor1
    return_df['actor_2_name']= actor2
    return_df['actor_3_name']= actor3
    return_df['genres']= genre
    return return_df

def get_suggestions():
    data = pd.read_csv('metadata_final.csv')
    return list(data['movie_title'].str.capitalize())

app = Flask(__name__)
@app.route("/")
@app.route("/index")
def index():
    NewMovies=[]
    with open('movie.csv','r') as csvfile:
        readCSV = csv.reader(csvfile)
        NewMovies.append(random.choice(list(readCSV)))
    m_name = NewMovies[0][0]
    m_name = m_name.title()
    
    with open('movie.csv', 'a',newline='') as csv_file:
        fieldnames = ['Movie']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writerow({'Movie': m_name})
        result_final = get_recommendations(m_name)
        names = []
        director = []
        actor1 = []
        actor2 = []
        actor3 = []
        genre = []
        for i in range(len(result_final)):
            names.append(result_final.iloc[i][0])
            director.append(result_final.iloc[i][1])
            actor1.append(result_final.iloc[i][2])
            actor2.append(result_final.iloc[i][3])
            actor3.append(result_final.iloc[i][4])
            genre.append(result_final.iloc[i][5])
    suggestions = get_suggestions()
    
    return render_template('index.html', suggestions=suggestions, genre = genre[5:], actor3=actor3, actor2 = actor2, actor1 = actor1, director = director, movies_names = names, search_name = m_name)

# Set up the main route
@app.route('/positive', methods=['GET', 'POST'])

def main():
    if flask.request.method == 'GET':
        return(flask.render_template('index.html'))

    if flask.request.method == 'POST':
        m_name = flask.request.form['movies_name']
        m_name = m_name.title()
        if m_name not in all_titles:
            return(flask.render_template('negative.html',name=m_name))
        else:
            with open('movie.csv', 'a',newline='') as csv_file:
                fieldnames = ['Movie']
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                writer.writerow({'Movie': m_name})
            result_final = get_recommendations(m_name)
            names = []
            director = []
            actor1 = []
            actor2 = []
            actor3 = []
            genre = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                director.append(result_final.iloc[i][1])
                actor1.append(result_final.iloc[i][2])
                actor2.append(result_final.iloc[i][3])
                actor3.append(result_final.iloc[i][4])
                genre.append(result_final.iloc[i][5])
               
            return flask.render_template('positive.html',genre = genre[5:], actor3=actor3, actor2 = actor2, actor1 = actor1, director = director, movies_names = names, search_name = m_name)

if __name__ == '__main__':
    app.run()
