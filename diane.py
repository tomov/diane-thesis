# -*- coding: cp1252 -*-

import codecs
import simplejson
import requests

#rotten_tomatoes_key = 'mq7dazg2njhpky3u5g5qqy6x'
# http://developer.rottentomatoes.com/docs

# http://www.omdbapi.com/?i=&t=Nina%27s+Heavenly+Delights
# http://www.imdb.com/xml/find?json=1&nr=1&q=Nina's+Heavenly+Delights


themoviedb_key = '8df14339012799a50c81f9119908160b'
# http://api.themoviedb.org/3/search/movie?api_key=8df14339012799a50c81f9119908160b&query=Nina's+Heavenly+Delights
# http://api.themoviedb.org/3/movie/12808?api_key=8df14339012799a50c81f9119908160b

search_url = "http://api.themoviedb.org/3/search/movie?api_key={0}&query={1}"
get_url = "http://api.themoviedb.org/3/movie/{0}?api_key={1}"

f = codecs.open('Book1.csv', encoding='cp1252')
out = codecs.open('Book1-filled.csv', encoding='utf-8', mode='w+')

line = f.readline();
cols = line.split(',')

print '\n----\n'

out.write('Input Title,Input Year,Country 1,Country 2,Country 3,Country 4,Language 1,Language 2,Language 3,Language 4,Lang 1,Lang 2,Lang 3,Lang 4,Output Title (for verification),Output Release Date (for verification)\n');

cache = dict()

limit = 10000000
line_id = 0
for line in f:
    line_id = line_id + 1
    if line_id > limit:
        break
    vals = line.split(',')
    year = vals[-1].strip('\n\r')
    title = ','.join(vals[:-1])
    title = title.strip('"')

    if line in cache:
        movie_countries = cache[line]['movie_countries']
        movie_languages = cache[line]['movie_languages']
        movie_langs = cache[line]['movie_langs']
        print 'CACHE!'
    else:
        movie_countries = ['', '', '', '']
        movie_languages = ['', '', '', '']
        movie_langs = ['', '', '', '']

        qtitle = title.replace(' ', '+').encode('utf-8')
        query = search_url.format(themoviedb_key, qtitle)
        resp = requests.get(url=query)
        if resp and resp.content:
            data = simplejson.loads(resp.content)
            results = data['results']
            if len(results) == 0:
                print 'NO MOVIE FOUND :((('
            else:
                result = results[0]
                movie_id = result['id']
                query = get_url.format(movie_id, themoviedb_key)
                resp = requests.get(url=query)
                data = simplejson.loads(resp.content)

                original_title = data['original_title']
                release_date = data['release_date']

                countries = data['production_countries']
                if len(countries) > 0:
                    movie_country = ""
                    idx = 0
                    for country in countries:
                        movie_countries[idx] = country['name']
                        idx = idx + 1
                        if idx >= 4:
                            break

                languages = data['spoken_languages']
                if len(languages) > 0:
                    movie_language = ""
                    idx = 0
                    for language in languages:
                        movie_languages[idx] = language['name']
                        movie_langs[idx] = language['iso_639_1']
                        idx = idx + 1
                        if idx >= 4:
                            break

        cache[line] = {
            'movie_countries': movie_countries,
            'movie_languages': movie_languages,
            'movie_langs': movie_langs
        }

    output_line = '"' + title + '",' + year + ',' + ','.join(movie_countries) + ',' + ','.join(movie_languages) + ',' + ','.join(movie_langs) + ',"' + original_title + '",' + release_date + ''
    print output_line
    out.write(output_line + '\n')

