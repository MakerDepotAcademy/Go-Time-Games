import datetime
from sqlalchemy import create_engine
import time
from threading import Thread, Event
import requests

# Event object used to send signals from one thread to another
stopGameEvent = Event()

class Display():

    def __init__(self, address):
        self._address = address

    def _getEndpoint(self, endpoint):
        return 'http://%s/%s' % (self._address, endpoint)

    def _post(self, endpoint, payload):
        return requests.post(_getEndpoint(endpoint), data=payload)

    def setQuestion(self, question):
        self._post('/question', question)

    def setAnswer(self, label, answer):
        self._post('/answer/%s' % label, answer)

    def setCorrect(self, label):
        self._post('/answer/%s/correct' % label, '')

    def setScore(self, score):
        self._post('/score', score)

    def addScore(self, add):
        self._post('/score/inc', add)

    def subScore(self, sub):
        self._post('/score/dec', sub)

    def getScore(self):
        rsp = requests.get(self._getEndpoint('/score'))
        return int(rsp.content)

    def start(self):
        self._post('/start')

D = Display('localhost:3000')

# Ask Questions
def AskQuestions():
    score = 0
    dbConnect = create_engine('sqlite:///quizShow.db')

    dbConnection = dbConnect.connect()
    while (1):
        # Ask question and verify answer
        query = dbConnection.execute('''SELECT
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

            D.setAnswer('a', row['red'])
            D.setAnswer('b', row['blue'])
            D.setAnswer('c', row['yellow'])
            D.setAnswer('d', row['green'])

            # Send question to the board and wait for answer
            D.setQuestion(row['question'])
            D.start()
            ans = input(row['question'])
            if ans != row['correct_answer']:
                print("Wrong")
                score = score - 1
            else:
                print("Correct Answer")
                D.setCorrect(ans)
                score = score + 1
            D.setScore(score)

            if stopGameEvent.is_set():
                AskQuestions = score
                print("The final score was: %5d" % (score))
                dbConnection.close()
                return score
                break

    dbConnection.close()
    return score

#--------------------------------------------------------------------------------
#- The Quiz Show Game
#--------------------------------------------------------------------------------
score = 0

# Start Game loop
# Create Question thread
questionThread = Thread(target=AskQuestions)

# Here we start the thread and we wait 330 seconds before the code continues to execute.
questionThread.start()
D.start()
score = questionThread.join(timeout=330)
if (isinstance(score, int) == False):
    score = 0

# We send a signal that the other thread should stop.
stopGameEvent.set()

print("Hey there! You timed out! The Game is over!")
print("The final score was: %5d" % (score))
