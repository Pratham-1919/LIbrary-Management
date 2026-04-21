from database.database import cursor,psycopg2,conn
from logger import logger




def create_table():
    commands = [
    """
        CREATE TABLE IF NOT EXISTS author (
            author_id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL
        );
    """
        
    ,
    """
        CREATE TABLE IF NOT EXISTS member(
            member_id SERIAL PRIMARY KEY,
            name VARCHAR(265) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            phone VARCHAR(20) NOT NULL,
            valid_date TIMESTAMP,
            status BOOLEAN DEFAULT TRUE
        );
     """
     ,
    """
        CREATE TABLE IF NOT EXISTS books(
            book_id SERIAL PRIMARY KEY,
            author_id INT NOT NULL,
            title VARCHAR(265) NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            quantity INT NOT NULL,
            status BOOLEAN DEFAULT TRUE,
            FOREIGN KEY (author_id) REFERENCES author (author_id)
        );

    """
    ,
    """
        CREATE TABLE IF NOT EXISTS book_copies(
            copy_id SERIAL PRIMARY KEY,
            book_id INT NOT NULL,
            status BOOLEAN NOT NULL DEFAULT TRUE,
            FOREIGN KEY (book_id) REFERENCES books (book_id) ON DELETE CASCADE
        );

    """
    ,
    """
        CREATE TABLE IF NOT EXISTS transaction(
            transaction_id SERIAL PRIMARY KEY,
            copy_id INT NOT NULL,
            member_id INT NOT NULL,
            issue_date TIMESTAMP,
            due_date TIMESTAMP,
            return_date TIMESTAMP,
            FOREIGN KEY (copy_id) REFERENCES book_copies (copy_id),
            FOREIGN KEY (member_id) REFERENCES member (member_id)
        );

    """
    ]

    try: 
        for command in commands:
            cursor.execute(command)

        logger.info("Connection successful: ")
        conn.commit()
        

    except(Exception, psycopg2.DatabaseError) as error:
        if conn:
            conn.rollback()
        logger.error(f"Error occured: {error}")

    finally:
        cursor.close()


var = create_table()
