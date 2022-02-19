#!/usr/bin/python3

class Cycle978:
    '''
    class represents Siemens CYCLE978 - probing surface
    '''

    def __ask(self, variants, text):
        while True:
            print('\n'+text)
            for n in range(len(variants)):
                print('{0}: {1}'.format(n+1, variants[n]))
            try:
                x = int(input())
                return variants[x-1]
            except ValueError:
                print('Set number.')
            except IndexError:
                print('Out of range.')

    def __enter_float(self, text):
        while 1:
            try:
                return float(input('\n'+text))
            except ValueError:
                print('Enter float value.')

    def __enter_int(self, text):
        while 1:
            try:
                return int(input('\n'+text))
            except ValueError:
                print('Enter int value.')



    def __init__(self):
        self.body = [100,0,'',1,0,0,0,0,0,'1','\"\"','','0','1.01','1.01','-1.01','0.34','1','0','','1','1']

        # set probing variant _MVAR
        vars = ['just measure','set zero point']
        a = self.__ask(vars,'Just measure value or set zero point?:')
        if a == vars[0]: self.body[0] = 0
        else: self.body[0] = 100

        # set offset
        vars = ['G54','G55','G56','G57','G505','G506','G507','G508']
        a = self.__ask(vars, 'Set offset:')
        for n in vars:
            if n == a: self.body[1] = vars.index(n) + 1

        # raw or soft result values
        vars = ['raw', 'soft']
        a = self.__ask(vars, 'Say if result values put into \'raw\' or \'soft\' offset table cell:')
        if a == vars[0]: self.body[1] += 10000

        # measured value
        self.body[4] = self.__enter_float('Enter measured value [+-mm]:')

        # safe distance
        self.body[5] = self.__enter_float('Enter safe distance DFA [mm]')

        # contingence interval
        self.body[6] = self.__enter_int('Enter contingence interval [s]')

        # measuring axis
        vars = ['X', 'Y', 'Z']
        a = self.__ask(vars, 'Set measured axis:')
        for n in vars:
            if n == a: self.body[7] = vars.index(n) + 1

        # measuring direction
        vars = ['+', '-']
        a = self.__ask(vars, 'Enter measuring direction:')
        for n in vars:
            if n == a: self.body[8] = vars.index(n) + 1


    def __str__(self) -> str:
        x = ''
        for n in self.body:
            x += str(n)+','
        return 'CYCLE978({})'.format(x[:(len(x)-1)])


print('''\nSiemens probing CYCLE978
Probe surface, single axis
by jakvok 2022
--------------------------''')

while 1:
    x = Cycle978()
    print('\n{}\n'.format(x))
    a = input('Continue? Y/N:')
    if a in 'Nn': break