import psycopg2


def create_db(conn):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
    client_id SERIAL PRIMARY KEY,
    first_name VARCHAR(40) NOT NULL,
    last_name VARCHAR(40) NOT NULL,
    email VARCHAR(40) NOT NULL
    );
        """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS phone_book(
    client_id INTEGER REFERENCES client(client_id),
    phone CHAR(12)
    );
        """)
    conn.commit()  # фиксируем в БД
    pass


# 2 Функция, позволяющая добавить нового клиента.
def add(conn, first_name, last_name, email, phones=None):
    cur.execute("""
    INSERT INTO client(first_name, last_name, email) values (%s, %s, %s);
    """, (first_name, last_name, email))
    conn.commit()
    pass


# 3 Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(conn, client_id, phone):
    cur.execute("""
    INSERT INTO phone_book(client_id, phone) VALUES(%s,%s)
    """, (client_id,phone))
    conn.commit()
    pass


# 4 Функция, позволяющая изменить данные о клиенте.

def change_client(conn, client_id, name=None, surname=None, email=None, phones=None):
    cur.execute("""
    UPDATE client
    SET email = %s
    WHERE client_id = %s
    """,(client_id, email))
    conn.commit()
    pass


# 5 Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(conn, client_id, phone):
    cur.execute("""
    DELETE FROM phone_book
    WHERE phone = %s, client_id = %s;
    """,(phone, client_id))
    conn.commit()
    pass


# 6 Функция, позволяющая удалить существующего клиента.

def delete_client(conn, client_id):
    cur.execute("""
    DELETE FROM phone_book
    WHERE client_id = %s;
    """,(client_id))
    cur.execute("""
    DELETE FROM client
    WHERE client_id = %s;
    """,(client_id))
    conn.commit()
    pass


# 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(conn, first_name=None, last_name=None, email=None, phones=None):
    cur.execute("""
    SELECT *
    FROM client
    WHERE first_name = %s OR last_name = %s OR email=%s;
    """, (first_name, last_name, email))
    print(cur.fetchone())

    pass


with psycopg2.connect(database="clients_db", user="postgres", password="8812") as conn:
    with conn.cursor() as cur:
        create_db(conn)
        add(conn, 'name', 'last_name', 'asdf@gmail.com', phones=None)
        #add_phone(conn,'1', 99999999999)
        #change_client(conn,'1', name=None, surname=None, email=None, phones=None)
        find_client(conn,'name')
        delete_client(conn, '1')
    pass  # вызывайте функции здесь

conn.close()