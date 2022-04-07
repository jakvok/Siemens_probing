#!/usr/bin/python3

import sys
class Cycle:
    '''
    Class represents Siemens probing cycles.
    Probing cycles are used for drive CNC machines measuring probe.
    The object get all cycle parameters from text input, store them and is able to generate cycle representation in right syntax.
    The cycles involved in class are CYCLE977 (hole, shaft, groove, web probing) and CYCLE978 (surface probing).
    '''

    def __ask(self, variants, text):
        '''
        Method ask to choose input from several posibilities.
        parameters: list of posibilities, explain text
        return: one of the possibilities choosen
        '''
        while True:
            print('\n'+text)
            for n in range(len(variants)):
                print('{0}: {1}'.format(n+1, variants[n]))
            try:
                x = int(input())
                return variants[x-1]
            except ValueError:
                print(self.__langs[5][lang])
            except IndexError:
                print(self.__langs[6][lang])

    def __enter_nr(self, text):
        '''
        Method for input positive/negative/float/integer number.
        parameter: explain text
        return: the number
        '''
        while 1:
            nr = input('\n'+text)
            if '.' in nr:
                try:
                    return float(nr)
                except ValueError:
                    print(self.__langs[5][lang])
            else:
                try:
                    return int(nr)
                except ValueError:
                    print(self.__langs[5][lang])

    def __enter_positive_nr(self, text):
        '''
        Method for input positive/float/integer number.
        parameter: explain text
        return: the positive value number
        '''
        while 1:
            nr = self.__enter_nr(text)
            if nr > 0: return nr
            print(self.__langs[7][lang])

    def __init__(self, lang):
        '''
        Method ask for all cycle parameters and initialize cycle object
        parameter: int number for choose language variant
        '''

        # language dictionary, involves different languages variant of text used for user communication
        # 0 = english
        # 1 = czech
        self.__langs = [
            ['surface', 'povrch'], # 0
            ['hole', 'dira'],
            ['shaft', 'cep'],
            ['groove', 'drazka'],
            ['web', 'zebro'],
            ['Set number.', 'Zadej cislo.'],
            ['Out of range.', 'Mimo rozsah.'],
            ['Must be positive value!', 'Hodnota musi byt vetsi nez 0!'],
            ['Just measure', 'Pouze mereni'],
            ['Set offset', 'Posunuti nuloveho bodu'],
            ['Just measure or set offset?', 'Jen merit nebo zadat nulovy bod?'], # 10
            ['Enter probing variant', 'Zadej zpusob mereni'],
            ['Enter offset [G54-57, G505-G599]: G', 'Zadej nulovy bod [G54-57, G505-G599]: G'],
            ['raw', 'hruby'],
            ['soft', 'jemny'],
            ['Say if result values put into \'raw\' or \'soft\' offset table cell:', 'Zvol jestli hodnoty zapisovat do \'hrube\' nebo \'jemne\' tabulky posunuti.'],
            ['Enter set of calibration data [1-10]:', 'Zadej sadu kalibracnich dat [1-10]:'],
            ['Enter contingence interval [s]:', 'Zadej kontingencni interval [s]:'],
            ['Enter measured value [mm]:','Zadej merenou hodnotu [mm]:'],
            ['Enter travel distance [mm]:','Zadej drahu pohybu mereni [mm]:'],
            ['Set probing axe:','Zadej osu mereni:'], # 20
            ['Enter probing direction:','Zadej smer mereni:'],
            ['hole diameter','prumer diry'],
            ['shaft diameter','prumer cepu'],
            ['groove width','sirku drazky'],
            ['web width','sirku zebra'],
            ['Enter ','Zadej '],
            ['Set safety distance [mm]:','Zadej bezpecnostni vzdalenost [mm]:'],
            ['Enter probing angle between probing direction and axe [deg]:','Zadej uhel mereni mezi smerem mereni a osou [st]:'],
            ['Probing angle must be in range -359 to 359 deg!','Uhel mereni musi byt v rozmezi +-359 stupnu!'],
            ['YES','ANO'], #30
            ['NO','NE'],
            ['Protection zone?:','Ochranna zona?:'],
            ['Enter width/diameter of protection zone [mm]:','Zadej sirku/prumer ochranne zony [mm]:'],
            ['Set dive distance DZ [mm]:','Zadej ponoreni DZ v ose Z [mm]:'],
            ['Set groove/web center position in axe','Zadej pozici stredu drazky/zebra v ose'],
            ['Set hole/shaft position in axe X [mm]:','Zadej pozici stredu diry/cepu v ose X [mm]:'],
            ['Set hole/shaft position in axe Y [mm]:','Zadej pozici stredu diry/cepu v ose Y [mm]:'],
            ['',''],
            ['',''],
        ]

        # Followed cycle parameters are united for both 977 and 978 cycles

        # set offset or just measure value?
        vars = [self.__langs[8][lang], self.__langs[9][lang]]
        a = self.__ask(vars, self.__langs[10][lang])
        if a == vars[0]: self.__set_offset = False
        else: self.__set_offset = True

        # probing variant (surface, hole, shaft, groove, web)
        vars = [self.__langs[0][lang], self.__langs[1][lang], self.__langs[2][lang], self.__langs[3][lang], self.__langs[4][lang]]
        a = self.__ask(vars, self.__langs[11][lang])
        for n in vars:
            if a == n: self.__probing_var = a

        # cycle name comming from probing variant
        if self.__probing_var == self.__langs[0][lang]: self.__cycle_name = 'CYCLE978'
        else: self.__cycle_name = 'CYCLE977'

        # number of coordinate system offset to where write the measured value G54-G57 and G505-G599 
        if self.__set_offset:
            while 1:
                self.__offset = self.__enter_nr(self.__langs[12][lang])
                if self.__offset in range(54,58) or self.__offset in range(505, 600): break
                print(self.__langs[6][lang])
            if self.__offset < 500: self.__offset -= 53
            else: self.__offset -= 500

        # write offset to raw/soft values
        if self.__set_offset:
            vars = [self.__langs[13][lang], self.__langs[14][lang]]
            a = self.__ask(vars, self.__langs[15][lang])
            if a == vars[0]: self.__raw = True
            else: self.__raw = False

        # set of the probe calibration data
        while 1:
            self.__calib_data = (self.__enter_nr(self.__langs[16][lang]))
            if int(self.__calib_data) in range(1,11): break
            print(self.__langs[6][lang])

        # contingence interval
        self.__contingence_interval = (self.__enter_positive_nr(self.__langs[17][lang]))
        
        # list of all cycle parameters where the parameters will be stored
        self.__body = []

        # static parameters when cycle sets offset
        self.__static_params_offset = [1, '\"\"', '', 0, 1.01, 1.01, -1.01, 0.34, 1, 0, '', 1]

        # static parameters when cycle just measures
        self.__static_params_measure = [1, '\"\"', '', 0, 1.01, 1.01, -1.01, '', '', '', '', 1]



        #----------------  CYCLE978  ------------------------------------
        # parameters used just in cycle 978

        if self.__cycle_name == 'CYCLE978':
            
            # measured value
            self.__value = self.__enter_nr(self.__langs[18][lang])

            # travel distance
            self.__travel_dist = self.__enter_positive_nr(self.__langs[19][lang])

            # probing axis
            vars = ['X', 'Y', 'Z']
            a = self.__ask(vars, self.__langs[20][lang])
            for n in vars:
                if n == a: self.__axe = (vars.index(n) + 1)

            # probing direction
            vars = ['+', '-']
            a = self.__ask(vars, self.__langs[21][lang])
            for n in vars:
                if n == a: self.__direction = (vars.index(n) + 1)

            # fill parameters into cycle body
            #-----------------

            # param 1
            if self.__set_offset: self.__body.append(100)
            else: self.__body.append(0)

            # param 2
            if self.__set_offset:
                if self.__raw: self.__offset += 10000
                self.__body.append(self.__offset)
            else: self.__body.append('')

            # param 3
            self.__body.append('')
            
            # param 4
            self.__body.append(self.__calib_data)

            # param 5
            self.__body.append(self.__value)

            # param 6
            self.__body.append(self.__travel_dist)

            # param 7
            self.__body.append(self.__contingence_interval)

            # param 8
            self.__body.append(self.__axe)

            # param 9
            self.__body.append(self.__direction)

            # params 10 to 21
            if self.__set_offset:
                self.__body += self.__static_params_offset
            else:
                self.__body += self.__static_params_measure

            # param 22
            self.__body.append(1)



        #----------------  CYCLE977  ------------------------------------
        # parameters used just in cycle 977

        if self.__cycle_name == 'CYCLE977':

            # measured value
            if self.__probing_var == self.__langs[1][lang]: text = self.__langs[22][lang]
            elif self.__probing_var == self.__langs[2][lang]: text = self.__langs[23][lang]
            elif self.__probing_var == self.__langs[3][lang]: text = self.__langs[24][lang]
            elif self.__probing_var == self.__langs[4][lang]: text = self.__langs[25][lang]
            else: pass
            self.__value = self.__enter_positive_nr(self.__langs[26][lang]+'{} [mm]:'.format(text))

            # safety distance DFA
            self.__safety_dist = self.__enter_positive_nr(self.__langs[27][lang])

            # probing angle
            while 1:
                self.__probing_angle = self.__enter_nr(self.__langs[28][lang])
                if int(self.__probing_angle) in range(-359, 360): break
                print(self.__langs[29][lang])

            # protection zone
            vars = [self.__langs[30][lang], self.__langs[31][lang]]
            a = self.__ask(vars, self.__langs[32][lang])
            if a == vars[0]:
                self.__protection_zone = True
                self.__prot_zone_dimm = self.__enter_positive_nr(self.__langs[33][lang])
            else: self.__protection_zone = False

            # dive distance
            if self.__probing_var in [self.__langs[1][lang], self.__langs[3][lang]] and not self.__protection_zone:
                self.__dive_dist = 1
            else:
                self.__dive_dist = self.__enter_positive_nr(self.__langs[34][lang])

            # probing axe
            if self.__probing_var in [self.__langs[3][lang], self.__langs[4][lang]]:
                vars = ['X', 'Y']
                a = self.__ask(vars, self.__langs[20][lang])
                for n in vars:
                    if n == a: self.__axe = vars.index(n) + 1

            # center position
            if self.__set_offset and self.__probing_var in [self.__langs[3][lang], self.__langs[4][lang]]:
                self.__center = [self.__enter_nr(self.__langs[35][lang]+' {} [mm]:'.format(chr(87+self.__axe)))]            
            elif self.__set_offset and self.__probing_var in [self.__langs[1][lang], self.__langs[2][lang]]:
                self.__center = [self.__enter_nr(self.__langs[36][lang])]
                self.__center += [self.__enter_nr(self.__langs[37][lang])]
            else: self.__center = [0, 0]


            # fill parameters into cycle body
            #-----------------

            # param 1
            if self.__probing_var == self.__langs[1][lang]: variant = 1
            elif self.__probing_var == self.__langs[2][lang]: variant = 2
            elif self.__probing_var == self.__langs[3][lang]: variant = 3
            elif self.__probing_var == self.__langs[4][lang]: variant = 4
            else: pass
            if self.__set_offset: variant += 100
            if self.__protection_zone: variant += 1000
            self.__body.append(variant)

            # param 2
            if self.__set_offset:
                if self.__raw: self.__offset += 10000
                self.__body.append(self.__offset)
            else: self.__body.append('')

            # param 3
            self.__body.append('')
            
            # param 4
            self.__body.append(self.__calib_data)

            # param 5
            self.__body.append(self.__value)

            # params 6, 7
            self.__body += ['', '']

            # param 8
            self.__body.append(self.__safety_dist)

            # param 9
            self.__body.append(self.__contingence_interval)

            # param 10
            self.__body.append(self.__probing_angle)

            # param 11
            if self.__probing_var in [self.__langs[1][lang], self.__langs[3][lang]] and not self.__protection_zone:
                self.__body.append(1)
            else: self.__body.append(self.__dive_dist)

            # param 12
            if self.__protection_zone: self.__body.append(self.__prot_zone_dimm)
            else: self.__body.append(1)

            # param 13
            self.__body.append('')

            # param 14
            try:
                self.__body.append(self.__axe)
            except:
                self.__body.append('')

            # params 15 to 26
            if self.__set_offset:
                self.__body += self.__static_params_offset
            else:
                self.__body += self.__static_params_measure

            # param 27
            if self.__center[0] == 0 and sum(self.__center) == 0:
                self.__body.append(1)
            else:
                self.__body.append(11)
                # param 28, ~29
                self.__body += self.__center
 

    def __str__(self) -> str:
        '''
        Method for text representation of probing cycle in right syntax
        '''
        x = ''
        for n in self.__body:
            x += str(n)+','
        return '{0}({1})'.format(self.__cycle_name, x[:(len(x)-1)])


langs = [
    ['| Siemens probing cycles for Grob 350 |','|  Siemens merici cykly pro Grob 350  |'],
    ['Continue? Y/N:','Pokracovat? A/N:'],
]

# choose language
lang = 0 # default = english
if len(sys.argv) > 1:
    if sys.argv[1] == 'cz': lang = 1

print('''\n
+-------------------------------------+
{}
|              v1.1.0                 |
|          by jakvok 2022             |
+-------------------------------------+'''.format(langs[0][lang]))

# main loop
while 1:
    x = Cycle(lang)
    print('\n{}\n'.format(x))
    a = input(langs[1][lang])
    if a in 'Nn': break