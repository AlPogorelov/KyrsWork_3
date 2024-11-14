import psycopg2

from src.DBManager import DBManager
from src.api_employers import HeadHunterAPIEmployers




def start_test_program():

    hh_api = HeadHunterAPIEmployers()

    employers = {"1C-Рарус", "Почта банк", 'DNS Технологии', 'В2В-Персонал', '1C-Рарус',
                 'Газпром нефть', 'ПАО «Россети Сибирь»'}

    employers_id = hh_api.get_employer_id(employers)



    vac_list_by_empl = hh_api.get_vac_by_employer(employers_id)






    db = DBManager()

    db.save_date_to_database(employers_id, vac_list_by_empl)

    count = db.get_companies_and_vacancies_count()

    all_vac = db.get_all_vacancies()

    avg = db.get_avg_salary()

    hi_sal = db.get_vacancies_with_higher_salary

    keyword ='зам'

    key_vac = db.get_vacancies_with_keyword(keyword)





if __name__ == '__main__':
    start_test_program()
