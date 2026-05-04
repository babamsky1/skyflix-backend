import requests
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

TMDB_BASE = settings.TMDB_BASE_URL


def tmdb_get(endpoint, params=None):
    """Helper to call TMDb API."""
    api_key = settings.TMDB_API_KEY
    if not api_key:
        return None, "TMDb API key not configured. Set TMDB_API_KEY in .env"
    
    url = f"{TMDB_BASE}{endpoint}"
    default_params = {'api_key': api_key, 'language': 'en-US'}
    if params:
        default_params.update(params)
    
    try:
        response = requests.get(url, params=default_params, timeout=10)
        response.raise_for_status()
        return response.json(), None
    except requests.exceptions.Timeout:
        return None, "TMDb API request timed out"
    except requests.exceptions.RequestException as e:
        return None, str(e)


@api_view(['GET'])
def trending_movies(request):
    page = request.GET.get('page', 1)
    data, error = tmdb_get('/trending/movie/week', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def popular_movies(request):
    page = request.GET.get('page', 1)
    data, error = tmdb_get('/movie/popular', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def top_rated_movies(request):
    page = request.GET.get('page', 1)
    data, error = tmdb_get('/movie/top_rated', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def movie_detail(request, movie_id):
    data, error = tmdb_get(f'/movie/{movie_id}', {'append_to_response': 'credits,videos,similar,recommendations'})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def movie_videos(request, movie_id):
    data, error = tmdb_get(f'/movie/{movie_id}/videos')
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    # Filter only YouTube trailers
    if data and 'results' in data:
        trailers = [v for v in data['results'] if v.get('site') == 'YouTube' and v.get('type') in ['Trailer', 'Teaser']]
        data['results'] = trailers
    return Response(data)


@api_view(['GET'])
def similar_movies(request, movie_id):
    page = request.GET.get('page', 1)
    data, error = tmdb_get(f'/movie/{movie_id}/similar', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def movie_recommendations(request, movie_id):
    page = request.GET.get('page', 1)
    data, error = tmdb_get(f'/movie/{movie_id}/recommendations', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def popular_tv(request):
    page = request.GET.get('page', 1)
    data, error = tmdb_get('/tv/popular', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def trending_tv(request):
    page = request.GET.get('page', 1)
    data, error = tmdb_get('/trending/tv/week', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def top_rated_tv(request):
    page = request.GET.get('page', 1)
    data, error = tmdb_get('/tv/top_rated', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def tv_detail(request, tv_id):
    data, error = tmdb_get(f'/tv/{tv_id}', {'append_to_response': 'credits,videos,similar,recommendations'})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def tv_videos(request, tv_id):
    data, error = tmdb_get(f'/tv/{tv_id}/videos')
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    if data and 'results' in data:
        trailers = [v for v in data['results'] if v.get('site') == 'YouTube' and v.get('type') in ['Trailer', 'Teaser']]
        data['results'] = trailers
    return Response(data)


@api_view(['GET'])
def similar_tv(request, tv_id):
    page = request.GET.get('page', 1)
    data, error = tmdb_get(f'/tv/{tv_id}/similar', {'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def movie_genres(request):
    data, error = tmdb_get('/genre/movie/list')
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def tv_genres(request):
    data, error = tmdb_get('/genre/tv/list')
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def search(request):
    query = request.GET.get('query', '').strip()
    if not query:
        return Response({'error': 'query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    page = request.GET.get('page', 1)
    media_type = request.GET.get('type', 'multi')  # multi, movie, tv
    
    endpoint = f'/search/{media_type}'
    data, error = tmdb_get(endpoint, {'query': query, 'page': page})
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def discover_movies(request):
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort_by', 'popularity.desc')
    page = request.GET.get('page', 1)
    year = request.GET.get('year', '')
    
    params = {'sort_by': sort_by, 'page': page, 'include_adult': 'false'}
    if genre:
        params['with_genres'] = genre
    if year:
        params['primary_release_year'] = year
    
    data, error = tmdb_get('/discover/movie', params)
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def discover_tv(request):
    genre = request.GET.get('genre', '')
    sort_by = request.GET.get('sort_by', 'popularity.desc')
    page = request.GET.get('page', 1)
    
    params = {'sort_by': sort_by, 'page': page}
    if genre:
        params['with_genres'] = genre
    
    data, error = tmdb_get('/discover/tv', params)
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def movie_stream(request, movie_id):
    """Get streaming embed URL for a movie."""
    provider = request.GET.get('provider', 'vidsrc')
    
    if provider == 'vidsrc':
        embed_url = f"{settings.VIDSRC_BASE_URL}/{movie_id}"
    elif provider == 'vidsrc_to':
        embed_url = f"{settings.VIDSRC_TO_BASE_URL}/{movie_id}"
    elif provider == 'embed2':
        embed_url = f"{settings.EMBED2_BASE_URL}/{movie_id}"
    elif provider == 'vidsrc_me':
        embed_url = f"{settings.VIDSRC_ME_BASE_URL}/{movie_id}"
    elif provider == 'movies123':
        embed_url = f"{settings.MOVIES123_BASE_URL}/{movie_id}"
    elif provider == 'putlocker':
        embed_url = f"{settings.PUTLOCKER_BASE_URL}/{movie_id}"
    elif provider == 'solarmovie':
        embed_url = f"{settings.SOLARMOVIE_BASE_URL}/{movie_id}"
    elif provider == 'fmovies':
        embed_url = f"{settings.FMOVIES_BASE_URL}/{movie_id}"
    else:
        embed_url = f"{settings.VIDSRC_BASE_URL}/{movie_id}"
    
    return Response({
        'embed_url': embed_url,
        'provider': provider,
        'movie_id': movie_id
    })


@api_view(['GET'])
def tv_episodes(request, tv_id):
    """Get episode list for a TV show season."""
    season = request.GET.get('season', '1')
    data, error = tmdb_get(f'/tv/{tv_id}/season/{season}')
    if error:
        return Response({'error': error}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    return Response(data)


@api_view(['GET'])
def tv_stream(request, tv_id):
    """Get streaming embed URL for a TV show."""
    provider = request.GET.get('provider', 'vidsrc')
    season = request.GET.get('season', '1')
    episode = request.GET.get('episode', '1')
    
    if provider == 'vidsrc':
        embed_url = f"{settings.VIDSRC_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    elif provider == 'vidsrc_to':
        embed_url = f"{settings.VIDSRC_TO_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    elif provider == 'embed2':
        embed_url = f"{settings.EMBED2_BASE_URL}/{tv_id}/{season}/{episode}"
    elif provider == 'vidsrc_me':
        embed_url = f"{settings.VIDSRC_ME_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    elif provider == 'movies123':
        embed_url = f"{settings.MOVIES123_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    elif provider == 'putlocker':
        embed_url = f"{settings.PUTLOCKER_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    elif provider == 'solarmovie':
        embed_url = f"{settings.SOLARMOVIE_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    elif provider == 'fmovies':
        embed_url = f"{settings.FMOVIES_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    else:
        embed_url = f"{settings.VIDSRC_BASE_URL.replace('/movie', '/tv')}/{tv_id}/{season}/{episode}"
    
    return Response({
        'embed_url': embed_url,
        'provider': provider,
        'tv_id': tv_id,
        'season': season,
        'episode': episode
    })
