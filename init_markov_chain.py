"""This script for initialization of Markov chain"""

from sqlalchemy import and_, desc
from sqlalchemy.sql.expression import func
from upload_jokes_to_DB import connect_to_db


def add_correct_words_and_jokes(min_rating_=10, min_length_=50, max_length_=500):
    connection, meta_data = connect_to_db('postgres', 'postgres', 'postgres')
    jokes = meta_data.tables['jokes']
    words = meta_data.tables['words']
    select_correct_jokes = connection.execute(jokes.select().
                                              where(and_(jokes.c.rating >= min_rating_,
                                                         func.length(jokes.c.joke_text) >= min_length_,
                                                         func.length(jokes.c.joke_text) <= max_length_)
                                                    ).order_by(desc(jokes.c.id)))
    words_dict = {}
    k = 0
    words_set = set()
    for row in select_correct_jokes:
        for word in row.joke_text.split(' '):
            if word not in words_set:
                words_set.add(word)
                result = connection.execute(words.insert().values(word=word))
                print('#{} word was added to db :)'.format(result.inserted_primary_key))
                words_dict[word] = result.inserted_primary_key[0]
            k += 1
    print('\nk =', k)

    correct_jokes = meta_data.tables['correct_jokes']
    select_correct_jokes = connection.execute(jokes.select().
                                              where(and_(jokes.c.rating >= min_rating_,
                                                         func.length(jokes.c.joke_text) >= min_length_,
                                                         func.length(jokes.c.joke_text) <= max_length_)
                                                    ).order_by(desc(jokes.c.id)))
    for row in select_correct_jokes:
        joke_text = []
        for word in row.joke_text.split(' '):
            joke_text.append(words_dict[word])
        print('joke_text =', joke_text)
        result = connection.execute(correct_jokes.insert().values(joke_text=joke_text))
        print('#{} joke was added to db :)'.format(result.inserted_primary_key))


def add_chains(power_=4):
    connection, meta_data = connect_to_db('postgres', 'postgres', 'postgres')
    correct_jokes = meta_data.tables['correct_jokes']
    markov_chains = meta_data.tables['markov_chains']

    for row in connection.execute(correct_jokes.select().order_by(desc(correct_jokes.c.id))):
        # 0 is beginning empty word, 1 is ending empty word
        current_joke_text = [0 for _ in range(power_ - 1)] + row.joke_text + [-1 for _ in range(power_ - 1)]
        for i in range(len(current_joke_text) - (power_ - 1)):
            result = connection.execute(markov_chains.insert().values(chain=current_joke_text[i:i+power_]))
            print('#{} chain was added to db :)'.format(result.inserted_primary_key))


'''
add_correct_words_and_jokes()
add_chains()
'''
