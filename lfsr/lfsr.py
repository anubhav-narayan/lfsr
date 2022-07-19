class LFSR():
    '''
    Linear Feedback Shift Register Model

        +-------+...+-------+     +-------+
    +---|       |   |       |--+--|       |--+--
    |   |  FFn  |   |  FF1  |  |  |  FF0  |  ^
    |   |       |   |       |  |  |       |  |
    |   +-------+...+-------+  |  +-------+  |
    |             |            |             |
    |             v            v             |
    |   +---------+------------+----------+  |
    |   |                                 |  |
    +-->|             f(x)                |--+
        |                                 |
        +---------------------------------+

    Where f(x) is determined by the polynomial
    provided to the LFSR.

    Args:
        poly:int - Polynomial for the LFSR as int
        state:int - Initial state of the LFSR

    '''

    def __init__(self, poly: int, state: int):
        self.poly = poly
        self.state = state
        self.__state_init = state
        self.build_poly()

    def build_poly(self):
        '''
        Build the polynomial LFSR.
        Calculates field order, round function
        '''
        from cmath import log
        from math import ceil
        self.field_order = ceil(log(self.poly, 2).real)
        poly_str = f'{self.poly:0{self.field_order}b}'

        def fround():
            self.state_elab = [
                int(x, 2)
                for x in f'{self.state:0{self.field_order}b}'
            ]
            self.__feedback = []
            for x in range(0, self.field_order):
                if poly_str[x] == '1':
                    self.__feedback.append(self.state_elab[x])

            self.state_elab[0:self.field_order-1] =\
                self.state_elab[1:self.field_order]

            from functools import reduce

            self.state_elab[self.field_order-1] = reduce(
                lambda x, y: x ^ y, self.__feedback
            )
            self.state = int(''.join([str(x) for x in self.state_elab]), 2)

        self.__round = fround

    @property
    def polynomial_algebric(self):
        '''
        Gives the algebric form of the polynomial
        '''
        poly_math = []
        poly_str = f'{self.poly:0{self.field_order}b}'
        for x in range(0, self.field_order-2):
            if poly_str[x] == '1':
                poly_math.append(f'x ^ {self.field_order-x-1}')
        if poly_str[self.field_order-2] == '1':
            poly_math.append('x')
        if poly_str[self.field_order-1] == '1':
            poly_math.append('1')
        return ' + '.join(poly_math)

    @property
    def state_table(self):
        '''
        State table generation
        '''
        state_table = {'Cycle': [], 'State': [], 'Register State': []}
        for x in range(0, 2 ** self.field_order):
            state_table['Cycle'].append(x)
            state_table['State'].append(self.state)
            state_table['Register State'].append(
                f'{self.state:0{self.field_order}b}'
            )
            self.__round()
        self.reset()
        return state_table

    def next(self):
        '''
        Get the next state
        '''
        self.__round()
        return self.state

    def cycle(self, rounds: int):
        '''
        Cycle the LFSR for `rounds`
        '''
        for x in range(0, rounds):
            self.__round()
        return self.state

    def full_cycle(self):
        '''
        Complete a full cycle or (2 ^ M) cycles,
        where M is the field order of the LFSR
        '''
        for x in range(0, 2 ** self.field_order):
            self.__round()
        return self.state

    def reset(self):
        '''
        Reset to initial state
        '''
        self.__init__(self.poly, self.__state_init)

    def load(self, state: int):
        '''
        Load a state
        '''
        self.__init__(self.poly, state)