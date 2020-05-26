import os
import sys
import unittest

from calculator import Calculator, Store

sys.path.append(os.getcwd())

_SYNTAXERROR = "SyntaxError. The identifier or value does not meet the requirements. \n" \
               "To get more information use the <_/info> command."


class TestCalculator(unittest.TestCase):
    calc = Calculator()
    st = Store()
    st.assign('a = 6')
    st.assign('b = 7')

    def test_main(self, calc=calc):
        self.assertEqual(calc.perform_action('1+1'), 2)
        self.assertEqual(calc.perform_action('a+b'), 13)
        self.assertEqual(calc.perform_action('a - 2'), 4)
        self.assertEqual(calc.perform_action('(13*1+1)/14'), 1)
        self.assertEqual(calc.perform_action('0/0'), "ZeroDivisionError. Please review your expression.")
        self.assertEqual(calc.perform_action('(13*1+46343434358**-*+541)/14'),
                         "SyntaxError. Please review your expression. \n"
                         "To get more information use the <_/info> command.")
        self.assertEqual(calc.perform_action('_/help'), "Available commands:\n"
                                                        "_/exit: use to exit the program\n"
                                                        "_/help: shows all available commands\n"
                                                        "_/del <variable_name>: use to remove a variable\n"
                                                        "_/info: use to get more information about mathematical expression requirements")
        self.assertEqual(calc.perform_action('_/info'), "You have the opportunity to use variables:\n "
                                                        "create [a = 12 or num = 55],\n "
                                                        "the name of the variable should consist of only LATIN letters,\n "
                                                        "and the value of the variable should consist of only numbers.\n "
                                                        "reassign existing variables [a = 77]\n "
                                                        "delete variables [/del a].\n "
                                                        "The mathematical expression should consist of numbers in the decimal number system,\n"
                                                        "characters [-, +, *, /, ^] and variable names created in advance.\n"
                                                        "Repeating the characters [*, /, ^] two or more times is prohibited.")


class TestStore(unittest.TestCase):
    st = Store()

    def test_assign(self, st=st):
        self.assertEqual(st.assign('a = 6'), 'Variable: a created successfully.')
        self.assertEqual(st.assign('b = 6'), 'Variable: b created successfully.')
        self.assertEqual(st.assign('c = 7'), 'Variable: c created successfully.')
        self.assertEqual(st.assign('zero = 0'), 'Variable: zero created successfully.')
        self.assertEqual(st.assign('a = 9'), 'Variable: a created successfully.')
        self.assertEqual(st.assign('ficus = 700050505'), 'Variable: ficus created successfully.')
        self.assertEqual(st.assign('9 = f'), _SYNTAXERROR)
        self.assertEqual(st.assign('9 = 7'), _SYNTAXERROR)
        self.assertEqual(st.assign('f = g'), _SYNTAXERROR)
        self.assertEqual(st.assign('* = 66'), _SYNTAXERROR)
        self.assertEqual(st.assign('= = ='), _SYNTAXERROR)
        self.assertEqual(st.assign('99 = *'), _SYNTAXERROR)
        self.assertEqual(st.assign('= = *'), _SYNTAXERROR)
        self.assertEqual(st.assign('jjjj = ='), _SYNTAXERROR)
        self.assertEqual(st.assign('f = print'), _SYNTAXERROR)

    def test_get_var(self, st=st):
        self.assertEqual(st.get_var('a'), '9')
        self.assertEqual(st.get_var('zero'), '0')
        self.assertEqual(st.get_var('aa'), 'This: aa identifier does not exist.')

    def test_qdel_var(self, st=st):
        self.assertEqual(st.del_var('a'), 'Variable: a deleted successfully.')
        self.assertEqual(st.del_var('a'), 'This: a identifier does not exist.')
        self.assertEqual(st.del_var('zero'), 'Variable: zero deleted successfully.')


if __name__ == '__main__':
    unittest.main()
