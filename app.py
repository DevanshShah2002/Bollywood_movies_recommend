from flask import Flask,render_template,request
import pickle
import pandas as pd
popular_df=pickle.load(open('popular_movies.pkl','rb'))
kids_movies=pickle.load(open('kids_movie.pkl','rb'))
movie_dict=pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movie_dict)
similarity_score=pickle.load(open('similar (1).pkl','rb'))
filter_df=pickle.load(open('filtere.pkl','rb'))
app= Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           movie_name= list(popular_df['title'].values),
                           image=list(popular_df['poster_path'].values),
                           votes=list(popular_df['imdb_votes'].values),
                           rating=list(popular_df['imdb_rating'].values),
                           )
@app.route('/kids_content')
def kids_ui():
    return render_template('kids_content.html',
                           movie_name= list(kids_movies['title'].values),
                           image=list(kids_movies['poster_path'].values),
                           genres=list(kids_movies['genres'].values),
                           )


@app.route('/recommend')
def recommend_ui():
    movie_name = list(movies['title'].values)
    movie_name.sort()
    return render_template('recommend.html',
                           movie_name=movie_name
                           )
@app.route('/recommend_movie',methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    movie_index = movies[movies["title"] == user_input].index[0]
    distances = similarity_score[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    data = []
    for i in movies_list:
        item = []
        item.append((movies.iloc[i[0]].title))
        item.append((movies.iloc[i[0]].poster_path))
        data.append(item)

    return render_template('recommend.html', data=data)




@app.route('/filters')
def filters_ui():
    return render_template('filters.html')
@app.route('/filter_movie',methods=['POST'])
def filter_result():
    t = request.form.get('user_input')
    y1= request.form.get('year1')
    y2= request.form.get('year2')
    movie_index = filter_df.loc[
        (filter_df["runtime"] <= float(t)) & (filter_df["year_of_release"] >= float(y1)) & (filter_df["year_of_release"] <= float(y2)) & (filter_df["imdb_rating"] >= 5 ) & (filter_df["imdb_votes"] >= 1000)].index
    data = []
    for i in movie_index:
        item = []
        item.extend(filter_df.loc[[i]].original_title)
        item.extend(filter_df.loc[[i]].poster_path)
        item.extend(filter_df.loc[[i]].year_of_release)
        item.extend(filter_df.loc[[i]].runtime)
        item.extend(filter_df.loc[[i]].imdb_rating)
        item.extend(filter_df.loc[[i]].imdb_votes)
        data.append(item)
    return render_template('filters.html', data=data)



@app.route('/contact')
def contact_ui():
    return render_template('contact.html')

if __name__=='__main__':
    app.run(debug=True)