from sqlalchemy import create_engine, update
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from threading import Thread, Event
from random import randrange

Base = declarative_base()
class go_time_trivia(Base):
   __tablename__ = 'go_time_trivia'
   rowid = Column(Integer, primary_key=True)
   question = Column(String)
   yellow = Column(String)
   green = Column(String)
   red = Column(String)
   blue = Column(String)
   correct_answer = Column(String)
   has_been_used = Column(Integer)

# Event object used to send signals from one thread to another
stopGameEvent = Event()

# Ask Questions
def Question(rowid=-1):
    None

def AskQuestions(TeamMemberCount=5):
    score = 0
    dbConnect = create_engine('sqlite:///quizShow.db')
    dbConnection = dbConnect.connect()

    # create a configured "Session" class
    Session = sessionmaker(bind=dbConnect)

    # create a Session
    session = Session()

    while (1):
        # Ask a question and verify answer
        questionList = dbConnection.execute('''SELECT
                        g.rowid,
                        g.QUESTION,
                        g.yellow,
                        g.green,
                        g.red,
                        g.blue,
                        g.correct_answer,
                        g.has_been_used
                    FROM
                        go_time_trivia AS g
                    WHERE
                        g.has_been_used = 0
                    ORDER BY
                        RANDOM() ASC
                ''')

        #result = {'trivia_question': [dict(zip(tuple(questionList.keys()), i))
        #                              for i in questionList.cursor]}

        for question in questionList:
            # Ask a not previously asked question and verify answer
            print('\n')
            print("rowid: ", question['rowid'])
            print("question: ", question['question'])
            print("yellow: ", question['yellow'])
            print("green: ", question['green'])
            print("red: ", question['red'])
            print("blue: ", question['blue'])
            print("correct_answer: ", question['correct_answer'])

            session.query(go_time_trivia).filter(go_time_trivia.rowid == question['rowid']). \
                update({go_time_trivia.has_been_used: 1}, synchronize_session=False)

            questioningMember = randrange(1, TeamMemberCount-1)

            # Send question to the board and wait for answer
            ans = input('Member ' + str(questioningMember) + ' what your answer? ')
            if ans != question['correct_answer']:
                print("Wrong")
                score = score - 1
            else:
                print("Correct Answer")
                score = score + 1

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
GameTimeLength = 330

# Start Game loop
# Create Question thread
questionThread = Thread(target=AskQuestions, args=(3,))

# Here we start the thread and we wait 330 seconds before the code continues to execute.
questionThread.start()
score = questionThread.join(timeout=GameTimeLength)
if (isinstance(score, int) == False):
    score = 0

# We send a signal that the other thread should stop.
stopGameEvent.set()

print("Hey there! You timed out! The Game is over!")
print("The final score was: %5d" % (score))
