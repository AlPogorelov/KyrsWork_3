import psycopg2


class DBManager:

    def __init__(self):
        conn = psycopg2.connect(host="localhost",
                                user="postgres",
                                password=5288,
                                port=5432
                                )
        conn.autocommit = True
        cur = conn.cursor()

        cur.execute(f"DROP DATABASE {'homework3'}")
        cur.execute(f"CREATE DATABASE {'homework3'}")

        conn.close()

        conn = psycopg2.connect(dbname="homework3",
                                host="localhost",
                                user="postgres",
                                password=5288,
                                port=5432
                                )

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE employers (
                            employer_id SERIAL PRIMARY KEY,
                            employer_name VARCHAR(255) NOT NULL,
                            vacancies_url TEXT
                        )
                    """)

        with conn.cursor() as cur:
            cur.execute("""
                        CREATE TABLE vacancies (
                            id SERIAL PRIMARY KEY,
                            name varchar(255) not null,    
                            salary int,
                            city varchar(55) not null,
                            requirement varchar(255),
                            responsibility varchar(255),
                            employer_id INT REFERENCES Employers(employer_id),
                            url TEXT
                        )
                    """)

        conn.commit()
        conn.close()

    @staticmethod
    def connect_db():
        '''Подключение к БД'''
        conn = psycopg2.connect(dbname="homework3",
                                host="localhost",
                                user="postgres",
                                password=5288,
                                port=5432
                                )
        return conn

    @staticmethod
    def save_date_to_database(employers_list, vacancies_list):
        '''Метод заполнения таблиц БД полученные из API запроса'''

        conn = DBManager.connect_db()

        conn.autocommit = True

        cur = conn.cursor()

        with conn.cursor() as cur:
            for employer in employers_list:
                cur.execute('''
                    INSERT INTO employers (employer_id, employer_name, vacancies_url)
                    VALUES
                     (%s, %s, %s)
                    ''', (employer['employer_id'], employer['employer_name'], employer['vacancies_url'])
                )


        with conn.cursor() as cur:
            for vacancies in vacancies_list:
                cur.execute('''
                    INSERT INTO vacancies (name, salary, city, requirement, responsibility, url, employer_id)
                    VALUES
                    (%s, %s, %s, %s, %s, %s, %s)
                    ''', (vacancies['vacancies_name'],
                          vacancies['salary'],
                          vacancies['city'],
                          vacancies['requirement'],
                          vacancies['responsibility'],
                          vacancies['url'],
                          vacancies['employer_id']
                          )
                )

        conn.commit()
        cur.close()
        conn.close()

    def get_companies_and_vacancies_count(self):
        '''Формирует и выводит результат sql запроса. Выводит список компаний и количество вакансий этой компании'''
        conn = DBManager.connect_db()
        conn.cursor()
        with conn.cursor() as cur:
            cur.execute('''
            SELECT e.employer_name, COUNT(v.employer_id) AS vacancy_count
            FROM employers e
            JOIN vacancies v ON v.employer_id = e.employer_id
            GROUP BY e.employer_name
            ORDER BY vacancy_count DESC;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print(row)
        cur.close()
        conn.close()

    @staticmethod
    def get_all_vacancies():
        '''Формирует и выводит результат sql запроса. Выводит список всех вакансий с названием компании,
         названием вакансии, зарпалтой и ссылкой на вакансию'''
        conn = DBManager.connect_db()
        conn.cursor()
        with conn.cursor() as cur:
            cur.execute('''
            SELECT 
            e.employer_name, v.name, v.salary, v.url                    
            FROM employers e
            JOIN vacancies v ON e.employer_id = v.employer_id;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print(row)
        cur.close()
        conn.close()

    @staticmethod
    def get_avg_salary():
        '''Формирует и выводит результат sql запроса. выводит среднюю зарпалту
         по всем вакансиям округляя её для удобства'''
        conn = DBManager.connect_db()
        conn.cursor()
        with conn.cursor() as cur:
            cur.execute(''' 
            SELECT ROUND(AVG(salary)) from vacancies;
            ''')
            rows = cur.fetchall()
            for row in rows:
                print(row)
        cur.close()
        conn.close()

    @staticmethod
    def get_vacancies_with_higher_salary():
        '''Формирует и выводит результат sql запроса. Список вакансий в которых зарпалата
         выше средней зарплаты относительно все вакансий'''
        conn = DBManager.connect_db()
        conn.cursor()

        with conn.cursor() as cur:
            cur.execute('''
            SELECT * FROM vacancies WHERE salary > (SELECT AVG(salary) FROM vacancies);
            ''')
            rows = cur.fetchall()

            for row in rows:
                print(row)

        cur.close()
        conn.close()

    @staticmethod
    def get_vacancies_with_keyword(key_word):
        '''Формирует и выводит результат список вакансий sql запроса по ключевому слову в назваинии вакансии'''
        conn = DBManager.connect_db()
        conn.cursor()

        with conn.cursor() as cur:
            keyword = key_word.replace("'", "''")
            cur.execute(f"SELECT * FROM vacancies WHERE name LIKE '%{keyword}%'")
            rows = cur.fetchall()

            for row in rows:
                print(row)

        cur.close()
        conn.close()
