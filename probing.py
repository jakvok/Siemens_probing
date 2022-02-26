#!/usr/bin/python3

class Cycle:
    '''
    Class represents Siemens probing cycles
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

    def __enter_nr(self, text):
        while 1:
            nr = input('\n'+text)
            if '.' in nr:
                try:
                    return float(nr)
                except ValueError:
                    print('Zadej cislo!')
            else:
                try:
                    return int(nr)
                except ValueError:
                    print('Zadej cislo!')

    def __init__(self):
        # [0,0,'',0,0,0,0,0,0,'1','\"\"','','0','1.01','1.01','-1.01','0.34','1','0','','1','1']
        self.body = []

        # set probing variant _MVAR
        vars = ['just measure','set zero point']
        a = self.__ask(vars,'Just measure value or set zero point?:')
        if a == vars[0]: self.body.append(0)
        else: self.body.append(100)

        vars = ['surface', 'hole', 'shaft', 'groove', 'web']
        a = self.__ask(vars, 'Enter probing variant:')
        for n in vars:
            if n == a: self.body[0] += vars.index(n)
        if a == vars[0]:
            self.name = 978
        else:
            self.name = 977

        if self.name == 977:
            vars = ['YES', 'NO']
            a = self.__ask(vars, 'Protection zone?:')
            if a == vars[0]: self.body[0] += 1000

        # set offset
        if self.body[0] not in [1001, 1002, 1003, 1004, 0, 1, 2, 3, 4]:    # if set zero point
            while 1:
                x = self.__enter_nr('Enter offset [G54-57, G508-G599]: G')
                if x in range(54,58) or x in range(508, 600): break
            if x < 500: self.body.append(x-53)
            else: self.body.append(x-500)
        else:   # if just measure
            self.body.append('')

        # raw or soft result values
        if self.body[0] not in [1001, 1002, 1003, 1004, 0, 1, 2, 3, 4]:    # if set zero point
            vars = ['raw', 'soft']
            a = self.__ask(vars, 'Say if result values put into \'raw\' or \'soft\' offset table cell:')
            if a == vars[0]: self.body[1] += 10000

        self.body.append('') # empty value

        # set of calibration data
        self.body.append(self.__enter_nr('Enter set of calibration data [1-10]:'))

        # measured value
        if self.body[0] in [0,100]: text = 'measured value'
        elif self.body[0] in [1, 101, 1001, 1101]: text = 'hole diameter'
        elif self.body[0] in [2, 102, 1002, 1102]: text = 'shaft diameter'
        elif self.body[0] in [3, 103, 1003, 1103]: text = 'groove width'
        elif self.body[0] in [4, 104, 1004, 1104]: text = 'web width'
        else: pass
        self.body.append(self.__enter_nr('Enter {} [mm]:'.format(text)))

        if self.name == 977: self.body += ['', ''] # two empty values        
        
        # safe distance
        if self.body[0] in [0,100]: self.body.append(self.__enter_nr('Enter travel distance [mm]:'))
        else: self.body.append(self.__enter_nr('Enter safety distance DFA [mm]:'))

        # contingence interval
        self.body.append(self.__enter_nr('Enter contingence interval [s]:'))

        # probing angle
        if self.name == 977:
            self.body.append(self.__enter_nr('Enter probing angle along with axe [deg]:'))

            # Z axis move
            if self.body[0] in [1001, 1101, 1003, 1103]: self.body.append(self.__enter_nr('Enter dive dist. into hole/groove in Z-axis [mm]:'))
            elif self.body[0] in [1, 101, 3, 103]: self.body.append(1)
            elif self.body[0] in [2, 102, 1002, 1102, 4, 104, 1004, 1104]: self.body.append(self.__enter_nr('Enter dive dist. in Z-axis [mm]:'))
            else: pass

            # width/diameter of protection zone
            if self.body[0] >= 1000: self.body.append(self.__enter_nr('Enter width/diameter of protection zone [mm]:'))
            else: self.body.append(1)

            # empty value
            self.body.append('')

            # probing axe only in groove/web 
            if self.body[0] in [3, 103, 1003, 1103, 4, 104, 1004, 1104]:
                vars = ['X', 'Y']
                a = self.__ask(vars, 'Set probing axe:')
                for n in vars:
                    if n == a: self.body.append(vars.index(n) + 1)
            else: self.body.append('') #not probing axe when hole/shaft
        if self.name == 978:
            vars = ['X', 'Y', 'Z']
            a = self.__ask(vars, 'Set probing axe:')
            for n in vars:
                if n == a: self.body.append(vars.index(n) + 1)
            # probing direction
            vars = ['+', '-']
            a = self.__ask(vars, 'Enter probing direction:')
            for n in vars:
                if n == a: self.body.append(vars.index(n) + 1)

        # mandatory values
        if self.body[0] not in [1001, 1002, 1003, 1004, 0, 1, 2, 3, 4]:    # if set zero point
            self.body += ['1','\"\"','','0','1.01','1.01','-1.01','0.34','1','0','','1']
        else:   # if just measure
            self.body += ['1','\"\"','','0','1.01','1.01','-1.01','','','','','1']

        # groove/web/hole/shaft center position
        if self.body[0] in [103, 1103, 104, 1104]: # if set Z.P. on groove/web
            x = self.__enter_nr('Enter groove/web center position [mm]:')
            if x == 0: self.body.append(1)
            else: self.body += [11,x]
        elif self.body[0] in [101, 1101, 102, 1102]:
            x = self.__enter_nr('Enter hole/shaft center position in axe X [mm]:')
            y = self.__enter_nr('Enter hole/shaft center position in axe Y [mm]:')
            if x == 0 and y ==0: self.body.append(1)
            else: self.body += [11,x,y]
        else: self.body.append(1)

    def __str__(self) -> str:
        x = ''
        for n in self.body:
            x += str(n)+','
        return 'CYCLE{0}({1})'.format(self.name, x[:(len(x)-1)])

print('''\n
+-------------------------------------+
| Siemens probing cycles for Grob 350 |
|              v0.2.2                 |
|          by jakvok 2022             |
+-------------------------------------+''')

while 1:
    x = Cycle()
    print('\n{}\n'.format(x))
    a = input('Continue? Y/N:')
    if a in 'Nn': break