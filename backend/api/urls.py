from django.urls import path
from . import views

urlpatterns = [
    path('movies/trending/', views.trending_movies, name='trending_movies'),
    path('movies/popular/', views.popular_movies, name='popular_movies'),
    path('movies/top-rated/', views.top_rated_movies, name='top_rated_movies'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/videos/', views.movie_videos, name='movie_videos'),
    path('movies/<int:movie_id>/similar/', views.similar_movies, name='similar_movies'),
    path('movies/<int:movie_id>/recommendations/', views.movie_recommendations, name='movie_recommendations'),
    path('tv/', views.popular_tv, name='popular_tv'),
    path('tv/trending/', views.trending_tv, name='trending_tv'),
    path('tv/top-rated/', views.top_rated_tv, name='top_rated_tv'),
    path('tv/<int:tv_id>/', views.tv_detail, name='tv_detail'),
    path('tv/<int:tv_id>/episodes/', views.tv_episodes, name='tv_episodes'),
    path('tv/<int:tv_id>/videos/', views.tv_videos, name='tv_videos'),
    path('tv/<int:tv_id>/similar/', views.similar_tv, name='similar_tv'),
    path('genres/movies/', views.movie_genres, name='movie_genres'),
    path('genres/tv/', views.tv_genres, name='tv_genres'),
    path('search/', views.search, name='search'),
    path('discover/movies/', views.discover_movies, name='discover_movies'),
    path('discover/tv/', views.discover_tv, name='discover_tv'),
    path('movies/<int:movie_id>/stream/', views.movie_stream, name='movie_stream'),
    path('tv/<int:tv_id>/stream/', views.tv_stream, name='tv_stream'),
]
