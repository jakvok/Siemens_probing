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
                    print('Set number.')
            else:
                try:
                    return int(nr)
                except ValueError:
                    print('Set number.')

    def __enter_positive_nr(self, text):
        while 1:
            nr = self.__enter_nr(text)
            if nr > 0: return nr
            print('Must be positive value!')

    def __init__(self):

        # set offset?
        vars = ['Just measure', 'Set offset']
        a = self.__ask(vars, 'Just measure or set offset?')
        if a == vars[0]: self.__set_offset = False
        else: self.__set_offset = True

        # probing variant
        vars = ['surface', 'hole', 'shaft', 'groove', 'web']
        a = self.__ask(vars, 'Enter probing variant:')
        for n in vars:
            if a == n: self.__probing_var = a

        # cycle name
        if self.__probing_var == 'surface': self.__cycle_name = 'CYCLE978'
        else: self.__cycle_name = 'CYCLE977'

        # offset
        if self.__set_offset:
            while 1:
                self.__offset = self.__enter_nr('Enter offset [G54-57, G505-G599]: G')
                if self.__offset in range(54,58) or self.__offset in range(505, 600): break
            if self.__offset < 500: self.__offset -= 53
            else: self.__offset -= 500

        # raw / soft
        vars = ['raw', 'soft']
        a = self.__ask(vars, 'Say if result values put into \'raw\' or \'soft\' offset table cell:')
        if a == vars[0]: self.__raw = True
        else: self.__raw = False

        # set of calibration data
        while 1:
            self.__calib_data = (self.__enter_nr('Enter set of calibration data [1-10]:'))
            if int(self.__calib_data) in range(1,11): break
            print('Out of range.')

        # contingence interval
        self.__contingence_interval = (self.__enter_positive_nr('Enter contingence interval [s]:'))
        
        # set of all cycle parameters
        self.__body = []

        # static parameters when cycle sets offset
        self.__static_params_offset = [1, '\"\"', '', 0, 1.01, 1.01, -1.01, 0.34, 1, 0, '', 1]

        # static parameters when cycle just measures
        self.__static_params_measure = [1, '\"\"', '', 0, 1.01, 1.01, -1.01, '', '', '', '', 1]



        #----------------  CYCLE978  ------------------------------------

        if self.__cycle_name == 'CYCLE978':
            
            # measured value
            self.__value = self.__enter_nr('Enter measured value [mm]:')

            # travel distance
            self.__travel_dist = self.__enter_positive_nr('Enter travel distance [mm]:')

            # probing axis
            vars = ['X', 'Y', 'Z']
            a = self.__ask(vars, 'Set probing axe:')
            for n in vars:
                if n == a: self.__axe = (vars.index(n) + 1)

            # probing direction
            vars = ['+', '-']
            a = self.__ask(vars, 'Enter probing direction:')
            for n in vars:
                if n == a: self.__direction = (vars.index(n) + 1)

            # fill parameters
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

        if self.__cycle_name == 'CYCLE977':

            # measured value
            if self.__probing_var == 'hole': text = 'hole diameter'
            elif self.__probing_var == 'shaft': text = 'shaft diameter'
            elif self.__probing_var == 'groove': text = 'groove width'
            elif self.__probing_var == 'width': text = 'web width'
            else: pass
            self.__value = self.__enter_nr('Enter {} [mm]:'.format(text))

            # safety distance DFA
            self.__safety_dist = self.__enter_positive_nr('Set safety distance [mm]:')

            # probing angle
            while 1:
                self.__probing_angle = self.__enter_nr('Enter probing angle between probing direction and axe [deg]:')
                if int(self.__probing_angle) in range(0, 360): break
                print('Probing angle must be in range 0-360 deg!')

            # protection zone
            vars = ['YES', 'NO']
            a = self.__ask(vars, 'Protection zone?:')
            if a == vars[0]:
                self.__protection_zone = True
                self.__prot_zone_dimm = self.__enter_positive_nr('Enter width/diameter of protection zone [mm]:')
            else: self.__protection_zone = False

            # dive distance
            if self.__probing_var in ['hole', 'groove'] and self.__protection_zone:
                self.__dive_dist = self.__enter_positive_nr('Set dive distance DZ [mm]:')

            # probing axe
            if self.__probing_var in ['groove', 'web']:
                vars = ['X', 'Y']
                a = self.__ask(vars, 'Set probing axe:')
                for n in vars:
                    if n == a: self.__axe = vars.index(n) + 1
                # center position
                self.__center = [self.__enter_nr('Set groove/web center position in axe {} [mm]:'.format(chr(87+self.__axe)))]            
            else:
                self.__center = [self.__enter_nr('Set hole/shaft position in axe X [mm]:')]
                self.__center += [self.__enter_nr('Set hole/shaft position in axe Y [mm]:')]



            # fill parameters
            #-----------------

            # param 1
            if self.__probing_var == 'hole': variant = 1
            elif self.__probing_var == 'shaft': variant = 2
            elif self.__probing_var == 'groove': variant = 3
            elif self.__probing_var == 'web': variant = 4
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
            if self.__probing_var in ['hole', 'groove'] and not self.__protection_zone:
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
        x = ''
        for n in self.__body:
            x += str(n)+','
        return '{0}({1})'.format(self.__cycle_name, x[:(len(x)-1)])


print('''\n
+-------------------------------------+
| Siemens probing cycles for Grob 350 |
|              v1.0.0                 |
|          by jakvok 2022             |
+-------------------------------------+''')

while 1:
    x = Cycle()
    print('\n{}\n'.format(x))
    a = input('Continue? Y/N:')
    if a in 'Nn': break