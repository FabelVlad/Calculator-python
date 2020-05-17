from time import ctime


class Singleton(type):
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance


class Display(metaclass=Singleton):
    __template = f"Hi, I'm Vladyslav <daprostovseeto@gmail.com> {ctime()}\n" \
                 "This calculator helps you calculate the value of an expression.\n" \
                 "To get more information, use the </help> or </info> command"

    def __init__(self):
        self.display(self.__template)

    def __del__(self):
        self.display('Bye!')

    @staticmethod
    def display(text: str):
        print(text)

    @staticmethod
    def get_expr() -> str:
        return input('-> ')


class Store(metaclass=Singleton):
    def __init__(self):
        self.__var_dict = {}

    def assign(self, expr: str):
        identifier, value = expr.replace(' ', '').split('=')
        if identifier.isalpha():
            if value.isalpha():
                value = self.get_var(value)
            if value.isnumeric():
                return self.__set_var(identifier, value)
        return "SyntaxError. The identifier or value does not meet the requirements. \n" \
               "To get more information use the <_/info> command."

    def __set_var(self, key: str, value):
        self.__var_dict[key] = value
        return f'Variable: {key} created successfully.'

    def get_var(self, key: str):
        try:
            return self.__var_dict[key]
        except KeyError:
            return f'This: {key} identifier does not exist.'

    def del_var(self, key):
        try:
            self.__var_dict.pop(str(key))
            return f'Variable: {key} deleted successfully.'
        except KeyError:
            return f'This: {key} identifier does not exist.'
        except TypeError:
            return "SyntaxError. Please review your command. \n" \
                   "To get more information use the <_/info> command."

    # def get_vars(self):
    #     return self.__var_dict


class Command(metaclass=Singleton):
    def __init__(self, store_obj: Store):
        self.__store_obj = store_obj
        self.__command_dict = {'_/exit': lambda kwargs: exit(),
                               '_/help': lambda kwargs: self.__help(),
                               '_/del': lambda kwargs: self.__del_var(*kwargs['var']),
                               '_/info': lambda kwargs: self.__info(kwargs)}

    def __del_var(self, var: str) -> str:
        return self.__store_obj.del_var(var)

    def __help(self, kwargs):
        return 'text'  # todo add text

    def __info(self, kwargs):
        return 'info'  # todo action

    def process(self, command: str, **kwargs):
        if command in self.__command_dict:
            return self.__command_dict[command](kwargs)
        else:
            return 'Unknown command.'


class Calculator(Store, Command):
    def __init__(self):
        super().__init__()
        self.store = Store()
        self.command = Command(self.store)

    def _calculate(self, expr):
        try:
            expr = self.__check_expr(expr)
            return eval(expr)  # todo check/contro eval
        except SyntaxError:
            return "SyntaxError. Please review your expression. \n" \
                   "To get more information use the <_/info> command."

    def __get_var_names(self, expr: str) -> list:
        var_names = [char if char.isalpha() else ' ' for char in expr]
        return ''.join(var_names).split()

    def __replace_var(self, expr: str, variables: list):
        for var in variables:
            expr = expr.replace(var, self.store.get_var(var))
        if variables[0] in expr:
            raise SyntaxError
        return expr

    def __check_expr(self, expr):
        variables = self.__get_var_names(expr)
        if variables:
            expr = self.__replace_var(expr, variables)
        return expr

    def perform_action(self, expr: str):
        if expr.count('=') == 1 and len(expr.split()) == 3:
            return self.store.assign(expr)
        elif len(expr.split()) == 1 and expr.isalpha():
            return self.store.get_var(expr)
        elif '_/' in expr:
            return self.command.process(expr.split()[0], var=expr.split()[1:])
        else:
            return self._calculate(expr)


if __name__ == '__main__':
    dis = Display()
    calculator = Calculator()
    while True:
        data = dis.get_expr()
        dis.display(calculator.perform_action(data))
