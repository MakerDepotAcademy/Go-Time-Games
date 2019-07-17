import sqlite3
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def update_question(conn, question):
    """
    update has_been_used of a trivia question
    :param conn:
    :param rowid:
    :return: project id
    """
    sql = ''' UPDATE go_time_trivia
              SET has_been_used = 1
              WHERE rowid = ?'''
    try:
        cur = conn.cursor()
        cur.execute(sql, question)
        conn.commit()
    except Error as e:
        print(e)

def main():
    database = "/Users/fcorn/tmp/quizShow.db"

    # create a database connection
    conn = create_connection(database)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    questionList =  '''
        SELECT
            g.rowid,
            g.QUESTION,
            g.yellow,
            g.green,
            g.red,
            g.blue,
            g.correct_answer
        FROM
            go_time_trivia AS g
        WHERE
            g.has_been_used = 0
        ORDER BY
            RANDOM() ASC
    '''
    cursor.execute(questionList)

    rows = cursor.fetchall()
    for row in rows:
        # row['name'] returns the name column in the query, row['Question'] returns email column.
        update_question(conn, (row[0],))
        print('{0}: {1}, {2}, {3}, {4}, {5}, {6}'.format(
            row['rowid'], row['question'], row['yellow'], row['green'], row['red'], row['blue'], row['correct_answer']))

    conn.close()

if __name__  == '__main__':
    main()
