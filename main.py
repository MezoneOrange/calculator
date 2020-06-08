from kivymd.app import MDApp
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window


Window.size = Window.size = (360, 640)


class Container(GridLayout):
    """Creates the app's container and contains methods for work with calculator functions.

    Variables:
        'result' - result of every operation. (int or float or str ("ERROR" or "FAIL"))
            default value: 0.
        'number' - numeric representation of final input data. (int or float)
            default value: 0.
        'data' - input data, which user dials on calculator. (str)
            default value: '0'.
        'operation_flag' - type of operation, which choose user on the calculator. (str)
            (+, -, *, /) default value: ''.
        'is_new_data' - Flag for reset 'data's value to default value. (bool)
            default value: True.
        'is_float' - Flag for convert 'data's value to float type. (bool)
            default value: False.
        'is_cycle_operation' - Flag for pushing '=' several times in a row
        and to repeat previous state of 'operation_flag's value. (bool)
            default value: False.
    """
    result = 0
    number = 0
    data = '0'
    operation_flag = ''
    is_new_data = True
    is_float = False
    is_cycle_operation = False

    def add_number(self, x):
        """Creates number and shows it on the display.

        Max value of digits is 9.
        Checks to exist of sign and point.
        Checks to state of number. Create the new number if set of number is after equal's operation.
        Shows a value of number into display.
        """
        if self.is_new_data:
            self.data = '0'
            self.is_float = False
        self.is_new_data = False
        if len(self.data) < 9 and not self.is_float and self.data[0] != '-':
            if self.data == '0':
                self.data = '0' if x == '0' else x
            else:
                self.data += x
        elif (self.is_float or self.data[0] == '-') and len(self.data) < 10:
            if self.data == '0':
                self.data = '0' if x == '0' else x
            elif self.data == '-0':
                self.data = '-0' if x == '-0' else '-' + x
            else:
                self.data += x
        elif self.is_float and self.data[0] == '-' and len(self.data) < 11:
            if self.data == '0':
                self.data = '0' if x == '0' else x
            elif self.data == '-0':
                self.data = '-0' if x == '-0' else '-' + x
            else:
                self.data += x

        self.output_field.text = self.data

    def change_to_float(self):
        """Changes integer number to float number.

        Checks number to exist of point.
        If is not point - adds the point to the end of number and change variable 'is_new_data' to True.
        Shows a value of number into display.
        """
        if self.is_new_data:
            self.data = '0'
            self.is_float = False
        self.is_new_data = False
        if not self.is_float:
            self.data += '.'
            self.is_float = True
        self.output_field.text = self.data

    def change_sign(self):
        """Changes sign of number.

        Checks number to exist of sign and point.
        If number is positive that adds sign to the start of number.
        If number is negative that removes sign from the number.
        Checks to state of number. Create the new number if set of number is after equal's operation.
        Shows a value of number into display.
        """
        if self.is_new_data:
            self.data = '0'
            self.is_float = False
        self.is_new_data = False
        if self.data[0] != '-':
            self.data = '-' + self.data
        else:
            self.data = self.data[1:]
        self.output_field.text = self.data

    def clear(self):
        """Clears number and result.

        Resets all variables to default values.
        Shows a default value of number into display.
        """
        self.data = '0'
        self.number = 0
        self.result = 0
        self.operation_flag = ''
        self.is_new_data = True
        self.is_float = False
        self.is_cycle_operation = False
        self.output_field.text = self.data

    def addition(self):
        """Changes operation flag to addition.

        Shows result of previous operation. If it was.
        If it was a serial of repeat pushing to '=' before,
        that only changes operation flag to addition.
        """
        if not self.is_cycle_operation:
            self.calc_operation()
            self.is_cycle_operation = False
        self.operation_flag = '+'
        self.is_new_data = True
        self.is_float = False

    def subtraction(self):
        """Changes operation flag to subtraction.

        Shows result of previous operation. If it was.
        If it was a serial of repeat pushing to '=' before,
        that only changes operation flag to subtraction.
        """
        if not self.is_cycle_operation:
            self.calc_operation()
            self.is_cycle_operation = False
        self.operation_flag = '-'
        self.is_new_data = True
        self.is_float = False

    def multiplication(self):
        """Changes operation flag to multiplication.

        Shows result of previous operation. If it was.
        If it was a serial of repeat pushing to '=' before,
        that only changes operation flag to multiplication.
        """
        if not self.is_cycle_operation:
            self.calc_operation()
            self.is_cycle_operation = False
        self.operation_flag = '*'
        self.is_new_data = True
        self.is_float = False

    def division(self):
        """Changes operation flag to division.

        Shows result of previous operation. If it was.
        If it was a serial of repeat pushing to '=' before,
        that only changes operation flag to division.
        """
        if not self.is_cycle_operation:
            self.calc_operation()
            self.is_cycle_operation = False
        self.operation_flag = '/'
        self.is_new_data = True
        self.is_float = False

    def result_of_operation(self):
        """Shows result of previous operation.

        If you push to '=' several times in a row that will be repeat
        previous state of 'operation_flag's value.
        """
        x = self.operation_flag
        self.calc_operation()
        self.operation_flag = x
        self.is_cycle_operation = True
        self.is_new_data = True
        self.is_float = True

    def calc_operation(self):
        """Produces calc operations and shows the result.

        Converts 'data' to float or integer type:
        if flag 'is_float' is True that converts to float. Otherwise converts to integer.

        Calculates numbers based to value of variable 'operation_flag':
        - if '+' - makes the addition.
        - if '-' - makes the subtraction.
        - if '*' - makes the multiplication.
        - if '/' - makes the division. If 'number' == 0 that shows 'ERROR',
        and resets all variables to default values.
        - if '' - makes nothing, shows value of 'data' if result is 0, otherwise shows a result.
        - if another value - makes nothing, shows 'FAIL',
        and resets all variables to default values.
        """
        self.number = float(self.data) if self.is_float else int(self.data)
        if self.operation_flag == '+':
            self.result = self.result + self.number
            self.operation_flag = ''
            self.output_field.text = (str(self.result) if len(str(self.result)) < 11
                                      else '{:.4e}'.format(self.result))
        elif self.operation_flag == '-':
            self.result = self.result - self.number
            self.operation_flag = ''
            self.output_field.text = (str(self.result) if len(str(self.result)) < 11
                                      else '{:.4e}'.format(self.result))
        elif self.operation_flag == '*':
            self.result = self.result * self.number
            self.operation_flag = ''
            self.output_field.text = (str(self.result) if len(str(self.result)) < 11
                                      else '{:.4e}'.format(self.result))
        elif self.operation_flag == '/':
            if self.number == 0:
                self.output_field.text = 'ERROR'
                self.number = 0
                self.result = 0
                self.operation_flag = ''
                self.is_cycle_operation = False
            else:
                self.result = self.result / self.number
                self.operation_flag = ''
                self.is_float = True
                self.output_field.text = (str(self.result) if len(str(self.result)) < 11
                                          else '{:.4e}'.format(self.result))
        elif self.operation_flag == '':
            self.result = self.result if self.result else self.number
            self.operation_flag = ''
            self.output_field.text = (str(self.result) if len(str(self.result)) < 11
                                      else '{:.4e}'.format(self.result))
        else:
            self.output_field.text = 'FAIL'
            self.number = 0
            self.result = 0
            self.operation_flag = ''
            self.is_cycle_operation = False


class CalcApp(MDApp):
    def __init__(self, **kwargs):
        self.theme_cls.theme_style = "Light"
        self.title = 'My calculator'
        super().__init__(**kwargs)

    def build(self):
        return Container()


if __name__ == "__main__":
    CalcApp().run()
