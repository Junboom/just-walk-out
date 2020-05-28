#내부 디비에 저장되느지 확인

import MySQLdb

def save_record(title, article, date, writer, cnt):
    #Open database connection
    db = MySQLdb.connect(host="localhost", user="newuser",passwd="rkd123",db="newworld")
    db.set_character_set('utf-8')

    # Prepare a cursorr object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database
    sql = "INSERT INTO documnet (title, article, wdate, writer , vcnt) " \
          "VALUES (%s, %s, %s, %s, %s)" ("'"+title+"'","'"+article+"'","'"+date+"'","'"+writer+"'","'"+cnt+"'")

    try:
        # Execute ths SQL command
        cursor.execute(sql)
        #Commit changes in the database
        db.commit()

    except Exception as e:
        print(str(e))
        # Rollback in case there is any error
        db.rollback()
    # Disconnect from database
    db.close()