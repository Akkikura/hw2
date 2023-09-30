import psycopg2


def create_db(conn):
    with conn.cursor() as cur:
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
            """)  # фиксируем в БД
        pass


# 2 Функция, позволяющая добавить нового клиента.
def add(conn, first_name, last_name, email, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO client(first_name, last_name, email) values (%s, %s, %s);
        """, (first_name, last_name, email))
        pass


# 3 Функция, позволяющая добавить телефон для существующего клиента.

def add_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO phone_book(client_id, phone) VALUES(%s,%s)
        """, (client_id,phone))
        pass


# 4 Функция, позволяющая изменить данные о клиенте.

def change_client(conn, client_id, name=None, last_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE client
        SET email = %s name = %s last_name = %s
        WHERE client_id = %s
        """,(client_id, email, name, lastname))
        pass


# 5 Функция, позволяющая удалить телефон для существующего клиента.

def delete_phone(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_book
        WHERE phone = %s, client_id = %s;
        """,(phone, client_id))
        pass


# 6 Функция, позволяющая удалить существующего клиента.

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM phone_book
        WHERE client_id = %s;
        """,(client_id))
        cur.execute("""
        DELETE FROM client
        WHERE client_id = %s;
        """,(client_id))
        pass


# 7 Функция, позволяющая найти клиента по его данным: имени, фамилии, email или телефону.

def find_client(conn, first_name, last_name, email, phones=None):
    if first_name == '':
        first_name = '%'
    if last_name == '':
        last_name = '%'
    if email == '':
        email = '%'
    with conn.cursor() as cur:
        cur.execute("""
        SELECT *
        FROM client
        WHERE first_name LIKE %s AND last_name LIKE %s AND email LIKE %s;
        """, (first_name, last_name, email))
        print(cur.fetchall())
        pass



if __name__ == '__main__':
    with psycopg2.connect(database="clients_db", user="postgres", password="8812") as conn:
        create_db(conn)
        add(conn, 'name123', 'last_name111', 'asdf@gmail.com111', phones=None)
        # add_phone(conn,'1', 99999999999)
        # change_client(conn,'1', name=None, surname=None, email=None, phones=None)
        first_name = input('Введите имя человека: ')
        last_name = input('Введите фамилию человека: ')
        email = input('Введите email человека: ')
        find_client(conn,first_name,last_name, email)
        delete_client(conn, '1')
        pass  # вызывайте функции здесь
