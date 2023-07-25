from django.shortcuts import render
from django.http import HttpResponse
import pickle
import requests
import pandas as pd


# Create your views here.

def index(request):
    
    # similaity=pickle.load(open('movierecommend/static/movierecommend/similaity.pkl','rb'))
    similaity = pd.read_pickle('movierecommend/static/movierecommend/similaity.pkl')
    # newdf=pickle.load(open('movierecommend/static/movierecommend/movies.pkl','rb'))
    newdf = pd.read_pickle('movierecommend/static/movierecommend/movies.pkl')
    print("reched here.")
    if request.method=='POST':
        movie = request.POST.get('movie','')
        # movie_index=newdf[newdf['title']==movie].index[0]
        recommend_movies,recommend_posters=recommend(movie)
        thank=True
        recommended=[[recommend_posters[i],recommend_movies[i]] for i in range(len(recommend_movies)) ]
        params={'movie':movie,'recommended':recommended,'thank':thank}
        return render(request,'movierecommend/index.html',params)
    return render(request,'movierecommend/index.html')

def fetchposter(movie_id):
    url=f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=73ea8b3ecf4e69a185157298d93f8b48'
    # print(type(movie_id),"the index of the current",url)
    response=requests.get(url)
    data=response.json()
    return "https://image.tmdb.org/t/p/w500"+data['poster_path']

def recommend(movie):
    similaity = pd.read_pickle('movierecommend/static/movierecommend/similaity.pkl')
    newdf = pd.read_pickle('movierecommend/static/movierecommend/movies.pkl')
    movie_index=newdf[newdf['title']==movie].index[0]
    similar=similaity[movie_index]
    movies_list=sorted(list(enumerate(similar)),reverse=True,key=lambda x:x[1])[1:6]
    # movie_id=sorted(list(enumerate(similar)),reverse=True,key=lambda x:x[0])[1:6]
    # print(movies_list)
    recommend_movies=[]
    recommend_posters=[]
    for el in movies_list:
        recommend_movies.append(newdf.iloc[el[0]].title)
        recommend_posters.append(fetchposter(newdf.iloc[el[0]].movie_id))
    return (recommend_movies,recommend_posters)






