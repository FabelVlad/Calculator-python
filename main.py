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

    @staticmethod
    def display(text: str):
        print(text)

    @staticmethod
    def get_expt() -> str:
        return input('-> ')


class Store:
    var_dict = {'h': 3, 'k': 6}


class Command(metaclass=Singleton):
    def __init__(self, store_obj: Store):
        self.store_obj = store_obj
        self.command_dict = {'/exit': lambda kwargs: exit(),
                             '/help': lambda kwargs: self.__help(),
                             '/del': lambda kwargs: self.__del_var(kwargs['var']),
                             '/info': lambda kwargs: self.__info(kwargs)}

    def __del_var(self, var: str) -> str:
        try:
            self.store_obj.var_dict.pop(var)
            return 'text..'  # todo add text
        except KeyError:
            return 'error'  # todo add text

    def __help(self):
        return 'text'  # todo add text

    def __info(self, kwargs):
        return 'info'  # todo action

    def process(self, command: str, **kwargs):
        if command in self.command_dict:
            return self.command_dict[command](kwargs)
        else:
            return 'text error'  # todo add text


class Calculator:
    pass
