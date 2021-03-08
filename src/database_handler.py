import psycopg2


def get_registered_user(user_id):
    try:
        conn = psycopg2.connect("postgres://fkvxayzijvnjgu:451a996eb499da4342fbf3504caf3dfe9e52a67f3bbf0474b30cb899bc2dd172@ec2-3-208-224-152.compute-1.amazonaws.com:5432/dcj1dv4k3ghlig")
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
        conn = psycopg2.connect("postgres://fkvxayzijvnjgu:451a996eb499da4342fbf3504caf3dfe9e52a67f3bbf0474b30cb899bc2dd172@ec2-3-208-224-152.compute-1.amazonaws.com:5432/dcj1dv4k3ghlig")
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
     