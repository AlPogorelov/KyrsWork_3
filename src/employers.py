class Employers:
    __slots__ = ('employer_id', 'employer_name')

    def __init__(self, employer_id, employer_name):
        self.employer_id = employer_id
        self.employer_name = employer_name


    @classmethod
    def csd(cls):
        pass