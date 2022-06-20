import psycopg2
import os

DATABASE_URL = ""
try:
    DATABASE_URL = os.environ["DATABASE_URL"]
except KeyError:
    print("Sem variáveis de ambiente DATABASE_URL!")

def get_registered_user(user_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except:
        print("Error connecting to data bank!")
    query = f"""SELECT group_id FROM registered_anon 
    WHERE
        user_id = {user_id};"""
    cur = conn.cursor()
    cur.execute(query)
    group_id = cur.fetchone()
    conn.commit()
    conn.close()
    cur.close()
    return(group_id) 

def set_user_group(user_id, group_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except:
        print("Error connecting to data bank!")
    query = f"""INSERT INTO registered_anon(user_id, group_id)
    VALUES({user_id}, {group_id})
    ON CONFLICT(user_id)
    DO
        UPDATE SET group_id = EXCLUDED.group_id;"""
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    conn.close()
    cur.close()

#Placeholder language getter. Someday it will allow for groups to select what language they would like the bot to use
def get_group_language(group_id):
    return "pt-br"
     