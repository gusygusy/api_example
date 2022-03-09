import re


class Validator:
    def __init__(self, num_range: tuple = None, alfa_range: tuple = None):
        self.num_range = num_range  # for refactoring purposes
        self.alfa_range = tuple(c for c in self._char_range(alfa_range))

    def _char_range(self, alfa_range):
        for c in range(ord(alfa_range[0]), ord(alfa_range[1]) + 1):
            yield chr(c)

    @staticmethod
    def _name_valid(name_allowed_sym: tuple,  name: str):
        name = name.lower()
        for i in range(len(name) - 1):  # digit checker
            if name[i].isdigit():
                if name[i + 1].isdigit():
                    return False
        name_len_validation = all([len(name) > 54])  # len checker
        if not name_len_validation:
            #  alfa range checker
            name_validation = all([not x for x in name if x not in name_allowed_sym and x.isalpha()])
            if name_validation:
                return True
            return False

    @staticmethod
    def _mail_valid(email: str ):
        try:
            email_valid = re.search(r'\w+\.*\w+@\w+\.\w+', email).group()
            if email_valid:
                return True
        except Exception as e:
            print(f'Exception ocurred during this email validation {email} >>> {e}  ')

    def validate(self, name, email):
        name_validation = self._name_valid(self.alfa_range, name)
        email_validation = self._mail_valid(email)
        if name_validation:
            if email_validation:
                return True
            else:
                raise NameEmailException("Can't pass email validation")
        else:
            raise NameEmailException("Can't pass name validation")

    def db_exist_check(self, name, email, player):
        p = []
        z = [p for p in player.objects.all().values_list('name', flat=True)]
        for i in z:
            for i_ in player.objects.filter(name=i):

                p.append(i_.email)

        name = [str(name)]
        email = [str(email)]

        name_checker = [n for n in name if n in z]
        email_checker = [e for e in email if e in p]

        if email[0] in email_checker:
            raise EntryAlreadyExists('Email doubling is not allowed')
        if name[0] in name_checker:
            raise EntryAlreadyExists('Name doubling is not allowed')
        else:
            return True


class NameEmailException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return 'NameEmailException has been raised'.format(self.message)
        else:
            return 'NameEmailException has been raised'


class EntryAlreadyExists(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):

        if self.message:
            return 'EntryAlreadyExists has been raised'.format(self.message)
        else:
            return 'EntryAlreadyExists has been raised'


