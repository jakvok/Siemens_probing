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
                print('Zadej cislo!')
            except IndexError:
                print('Mimo rozsah!')

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
        vars = ['pouze mereni','posunuti pocatku']
        a = self.__ask(vars,'Pouze mereni nebo posunuti pocatku?:')
        if a == vars[0]: self.body.append(0)
        else: self.body.append(100)

        vars = ['povrch', 'dira', 'cep', 'drazka', 'zebro']
        a = self.__ask(vars, 'Zadej variantu sondovani:')
        for n in vars:
            if n == a: self.body[0] += vars.index(n)
        if a == vars[0]:
            self.name = 978
        else:
            self.name = 977

        if self.name == 977:
            vars = ['ANO', 'NE']
            a = self.__ask(vars, 'Ochranna zona?:')
            if a == vars[0]: self.body[0] += 1000

        # set offset
        if self.body[0] not in [1001, 1002, 1003, 1004, 0, 1, 2, 3, 4]:    # if set zero point
            while 1:
                x = self.__enter_nr('Zadej offset [G54-57, G508-G599]: G')
                if x in range(54,58) or x in range(508, 600): break
            if x < 500: self.body.append(x-53)
            else: self.body.append(x-500)
        else:   # if just measure
            self.body.append('')

        # raw or soft result values
        if self.body[0] not in [1001, 1002, 1003, 1004, 0, 1, 2, 3, 4]:    # if set zero point
            vars = ['hruby', 'jemny']
            a = self.__ask(vars, 'Vysledek do \'hrubeho\' nebo \'jemneho\' posunuti v tabulce?:')
            if a == vars[0]: self.body[1] += 10000

        self.body.append('') # empty value

        # set of calibration data
        self.body.append(self.__enter_nr('Zadej sadu kalibracnich dat sondy (korekce) [1-10]:'))

        # measured value
        if self.body[0] in [0,100]: text = 'merenou hodnotu'
        elif self.body[0] in [1, 101, 1001, 1101]: text = 'prumer diry'
        elif self.body[0] in [2, 102, 1002, 1102]: text = 'prumer cepu'
        elif self.body[0] in [3, 103, 1003, 1103]: text = 'sirku drazky'
        elif self.body[0] in [4, 104, 1004, 1104]: text = 'sirku zebra'
        else: pass
        self.body.append(self.__enter_nr('Zadej {} [mm]:'.format(text)))

        if self.name == 977: self.body += ['', ''] # two empty values        
        
        # safe distance
        if self.body[0] in [0,100]: self.body.append(self.__enter_nr('Zadej drahu mereni [mm]:'))
        else: self.body.append(self.__enter_nr('Zadej bezpecnostni vzdalenost DFA [mm]:'))

        # contingence interval
        self.body.append(self.__enter_nr('Zadej kontingencni interval [s]:'))

        # probing angle
        if self.name == 977:
            self.body.append(self.__enter_nr('Zadej uhel mereni vztazeny k ose [deg]:'))

            # Z axis move
            if self.body[0] in [1001, 1101, 1003, 1103]: self.body.append(self.__enter_nr('Zadej zanoreni do diry/drazky v Z-ose [mm]:'))
            elif self.body[0] in [1, 101, 3, 103]: self.body.append(1)
            elif self.body[0] in [2, 102, 1002, 1102, 4, 104, 1004, 1104]: self.body.append(self.__enter_nr('Zadej zanoreni v Z-ose [mm]:'))
            else: pass

            # width/diameter of protection zone
            if self.body[0] >= 1000: self.body.append(self.__enter_nr('Zadej sirku/prumer ochranne zony [mm]:'))
            else: self.body.append(1)

            # empty value
            self.body.append('')

            # probing axe only in groove/web 
            if self.body[0] in [3, 103, 1003, 1103, 4, 104, 1004, 1104]:
                vars = ['X', 'Y']
                a = self.__ask(vars, 'Zadej osu mereni:')
                for n in vars:
                    if n == a: self.body.append(vars.index(n) + 1)
            else: self.body.append('') #not probing axe when hole/shaft
        if self.name == 978:
            vars = ['X', 'Y', 'Z']
            a = self.__ask(vars, 'Zadej osu mereni:')
            for n in vars:
                if n == a: self.body.append(vars.index(n) + 1)
            # probing direction
            vars = ['+', '-']
            a = self.__ask(vars, 'Zadej smer mereni:')
            for n in vars:
                if n == a: self.body.append(vars.index(n) + 1)

        # mandatory values
        if self.body[0] not in [1001, 1002, 1003, 1004, 0, 1, 2, 3, 4]:    # if set zero point
            self.body += ['1','\"\"','','0','1.01','1.01','-1.01','0.34','1','0','','1']
        else:   # if just measure
            self.body += ['1','\"\"','','0','1.01','1.01','-1.01','','','','','1']

        # groove/web/hole/shaft center position
        if self.body[0] in [103, 1103, 104, 1104]: # if set Z.P. on groove/web
            x = self.__enter_nr('Zadej pozici stredu drazky/zebra na merene ose [mm]:')
            if x == 0: self.body.append(1)
            else: self.body += [11,x]
        elif self.body[0] in [101, 1101, 102, 1102]:
            x = self.__enter_nr('Zadej pozici stredu diry/cepu v ose X [mm]:')
            y = self.__enter_nr('Zadej pozici stredu diry/cepu v ose Y [mm]:')
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
|  Siemens merici cykly pro Grob 350  |
|              v0.2.2                 |
|           jakvok 2022               |
+-------------------------------------+''')

while 1:
    x = Cycle()
    print('\n{}\n'.format(x))
    a = input('Pokracovat? A/N:')
    if a in 'Nn': break