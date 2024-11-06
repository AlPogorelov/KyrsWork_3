from src.api_employers import HeadHunterAPIEmployers


def start_test_program():

    hh_api = HeadHunterAPIEmployers()

    employers = {"Райффайзенбанк", 'Почта банк'}

    employers_id = hh_api.get_employer_id(employers)


    vac_list = hh_api.get_vac_by_employer(employers_id)

    print(vac_list)

if __name__ == '__main__':
    start_test_program()
