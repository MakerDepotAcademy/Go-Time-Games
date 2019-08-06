import datetime
from sqlalchemy import create_engine
import time
from threading import Thread, Event

# Event object used to send signals from one thread to another
stop_event = Event()

# Ask Questions
def AskQuestions():
    score = 0
    db_connect = create_engine('sqlite:///quizShow.db')

    conn = db_connect.connect()
    while (1):
        # Ask question and verify answer
        query = conn.execute('''SELECT
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
                    LIMIT 1
                ''')
        #result = {'trivia_question': [dict(zip(tuple(query.keys()), i))
        #                              for i in query.cursor]}    
        for row in query:
            print("rowid: ", row['rowid'])
            print("question: ", row['question'])
            print("yellow: ", row['yellow'])
            print("green: ", row['green'])
            print("red: ", row['red'])
            print("blue: ", row['blue'])
            print("correct_answer: ", row['correct_answer'])

        # Send question to the board and wait for answer
        ans = input(row['question'])
        if ans != row['correct_answer']:
            print("Wrong")
            score = score - 1
        else:
            print("CORRECT")
            score = score + 1

        if stop_event.is_set():
            AskQuestions = score
            print("The final score was: %5d" % (score))
            return score
            break

    conn.close()
    return score

score = 0

# Start Game loop
question_thread = Thread(target=AskQuestions)

# Here we start the thread and we wait 6 seconds before the code continues to execute.
question_thread.start()
score = question_thread.join(timeout=6)

# We send a signal that the other thread should stop.
stop_event.set()

print("Hey there! I timed out! The Game is over!")
print("The final score was: %5d" % (score))
