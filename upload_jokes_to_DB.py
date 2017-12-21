"""This script for uploading jokes to exists table JOKES"""

import sqlalchemy as sql


def connect_to_db(user, password, db, host='localhost', port=5432):
    """ Returns a connection and a metadata object

    # Connect with the help of the PostgreSQL URL
    # postgresql://postgres:postgres@localhost:5432/postgres

    """
    url = 'postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db)

    connection_ = sql.create_engine(url, client_encoding='utf8')

    # We then bind the connection to MetaData()
    meta_data_ = sql.MetaData(bind=connection_, reflect=True)

    return connection_, meta_data_


def upload_jokes_to_db(connection_, meta_data_):
    jokes = meta_data_.tables['jokes']
    file_names = ['jokes(910к-800к).txt', 'jokes(800к-700к).txt',
                  'jokes(700к-500к).txt', 'jokes(500к-400к).txt',
                  'jokes(400к-300к).txt', 'jokes(300к-100к).txt',
                  'jokes(100к-0).txt']

    for file_name in file_names:
        with open('jokes/' + file_name, 'r', encoding='utf-8') as input_file:
            file_iter = iter(input_file.readlines())
            while True:
                current_line = next(file_iter, '$END$')
                while current_line != '$END$' and current_line[:7] != 'number=':
                    current_line = next(file_iter, '$END$')
                if current_line == '$END$':
                    break
                number_of_joke = int(current_line[7:])
                print('joke #{}'.format(number_of_joke))

                current_line = next(file_iter, '$END$').strip()
                joke_text = ''
                while current_line != '$END$' and current_line[:7] != 'rating=':
                    # not add strings like '\n', '\t', '', etc.
                    if current_line == '':
                        current_line = next(file_iter, '$END$').strip()
                        continue
                    joke_text += current_line
                    if joke_text[len(joke_text) - 1] != ' ':
                        joke_text += ' '
                    joke_text += '\n'
                    current_line = next(file_iter, '$END$').strip()
                # remove last two symbols ' \n'
                joke_text = joke_text[:len(joke_text) - 2]
                if current_line == '$END$':
                    print('Adding of joke, without rating:')
                    print('joke_text: {}'.format(joke_text))
                    result = connection_.execute(jokes.insert().values(joke_text=joke_text))
                else:
                    rating = int(current_line[7:])
                    print('Adding of joke:')
                    print('joke_text: {}'.format(joke_text))
                    print('rating: {}'.format(rating))
                    result = connection_.execute(jokes.insert().values(joke_text=joke_text, rating=rating))
                print('#{} joke was added to db :)'.format(result.inserted_primary_key))
                print()


'''
connection, meta_data = connect_to_db('postgres', 'postgres', 'postgres')
print(connection)
print(meta_data)

# here will be 'jokes' table
print('All tables:')
for table in meta_data.tables:
    print(table)
print()

upload_jokes_to_db(connection, meta_data)
'''
