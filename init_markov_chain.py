"""This script for initialization of Markov chain"""

from upload_jokes_to_DB import connect_to_db

power = 4


def add_words(min_rating_=10, min_length_=50, max_length_=500):
    connection, meta_data = connect_to_db('postgres', 'postgres', 'postgres')
    jokes = meta_data.tables['jokes']
    words = meta_data.tables['words']
    words_set = set()

    for row in connection.execute(jokes.select()):
        if row.rating >= min_rating_ and min_length_ <= len(row.joke_text) <= max_length_:
            for word in row.joke_text.split(' '):
                print('Add word {}'.format([word]))
                words_set.add(word)
    for word in words_set:
        result = connection.execute(words.insert().values(word=word))
        print('#{} word was added to db :)'.format(result.inserted_primary_key))


add_words()
