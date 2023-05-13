from multiprocessing import connection
import psycopg2
from config import host, user, password, db_name


#configuring the connection using
#data from config.py file
def config():
    connection = psycopg2.connect(
            host = host,
            user = user,    
            password = password,
            database = db_name
        )
    #connection.autocommit = True
    return connection

#creating table, if it exists, then it ignores
def create_table():

    table = """CREATE TABLE if not exists users(
                name_ varchar(50) PRIMARY KEY,
                score integer
            )"""
    connection = config()
    cursor = connection.cursor()
    cursor.execute(table)
    cursor.close()
    connection.commit()
    connection.close()

#condition to check whether 
#the user is in the table or not
def check_row(name):
    check = "SELECT * FROM users WHERE name_=%s"
    connection = config()
    cursor = connection.cursor()
    cursor.execute(check, (name,))
    return cursor.fetchone() is not None

#returns current user's result to show on screen
def get_current_result(name):
    current_score = "SELECT score FROM users WHERE name_=%s"
    connection = config()
    cursor = connection.cursor()
    cursor.execute(current_score, (name,))
    res = cursor.fetchone()[0]
    return res

#returns the best score to show on screen
def get_best_score():
    best_score = "SELECT MAX(score) as max FROM users"
    connection = config()
    cursor = connection.cursor()
    cursor.execute(best_score)
    res = cursor.fetchone()[0]
    return res

def top_five():
    top5 = "SELECT name_, score FROM users ORDER BY score DESC LIMIT 5"
    connection = config()
    cursor = connection.cursor()
    cursor.execute(top5)
    top_list = list(cursor.fetchall())
    print(top_list)
    return top_list


#inserts the new user's name and score
def new_row(name, score):
    insert = 'INSERT INTO users(name_, score) VALUES(%s, %s)'
    
    connection = config()
    cursor = connection.cursor()
    cursor.execute(insert, (name, score))
    connection.commit()
    cursor.close()
    connection.close()

#updates existing user's score, if it's bigger than the previous result
def save_results(name, score):
   #insert = 'INSERT INTO flappybird(name_, points) VALUES(%s, %s)'
    update = 'UPDATE users SET score = %s WHERE name_ = %s'
    connection = config()
    cursor = connection.cursor()
    #cursor.execute(select, (score, name))
    cursor.execute(update,(score, name))
    connection.commit()
    cursor.close()
    connection.close()
    
