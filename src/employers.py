class Employers:
    __slots__ = ('employer_id', 'employer_name', 'vacancies_url')

    def __init__(self, employer_id, employer_name, vacancies_url):
        self.employer_id = employer_id
        self.employer_name = employer_name
        self.vacancies_url = vacancies_url


    @classmethod
    def get_employers_list(cls, employers):
        '''Создаем объекты компаний'''

        employers_list = []

        for employer in employers:
            employers_list.append(Employers(**employer))

        return employers_list

