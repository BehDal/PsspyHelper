# add PSS/E path to python
import pssepath
pssepath.add_pssepath()

# import all psspy functions
from psspy import *

# redirect PSS/E alerts/messages to python command line
import redirect
redirect.psse2py()

# declare 'with mute:' block to silent PSS/E alerts
import os
from contextlib2 import redirect_stdout
mute = redirect_stdout(open(os.devnull, 'w'))

class PssError(BaseException):
    pass

#############################################################################

# Line
class Line:
    def __init__(self, ibus, jbus, ckt):
        if (ibus is int and jbus is int) or (ibus is str and jbus is str):
            self.__fromBus = Bus(ibus)
            self.__toBus = Bus(jbus)
        elif ibus is Bus and jbus is Bus:
            self.__fromBus = ibus
            self.__toBus = jbus
        else:
            raise ValueError('ibus and jbus must be of the same type, either string or integer or Bus.')
        if ckt is str:
            self.__ckt = ckt
        else:
            raise ValueError('ckt must be string')
        ierr, _ = brnint(self.__fromBus.BusNum, self.__toBus.BusNum, self.__ckt, 'STATUS')
        if ierr == 2:
            raise PssError('Line not found.')

    @property
    def FromBus(self):
        return self.__fromBus

    @property
    def ToBus(self):
        return self.__toBus

    @property
    def Ckt(self):
        return self.__ckt

    def GetProp(self, prop):
        prop = prop.upper()
        if prop in ('RATEA', 'RATEB', 'RATEC', 'RATE', 'LENGTH', 'CHARG', 'CHARGZ',
                    'FRACT1', 'FRACT2', 'FRACT3', 'FRACT4'):
            ierr, value = brndat(self.__fromBus.BusNum, self.__toBus.BusNum, self.__ckt, prop)
        elif prop in ('RX', 'ISHNT', 'JSHNT', 'RXZ', 'ISHNTZ', 'JSHNTZ', 'LOSSES'):
            ierr, value = brndt2(self.__fromBus.BusNum, self.__toBus.BusNum, self.__ckt, prop)
        elif prop in ('STATUS', 'METER', 'NMETR', 'OWNERS', 'OWN1', 'OWN2', 'OWN3', 'OWN4'):
            ierr, value = brnint(self.__fromBus.BusNum, self.__toBus.BusNum, self.__ckt, prop)
        elif prop == 'FLO':
            ierr, value = brnflo(self.__fromBus.BusNum, self.__toBus.BusNum, self.__ckt)
        else:
            raise PssError('Property invalid.')
        if ierr <> 0:
            raise PssError('Some error occurred.')
        return value

    def SetProps(self, **props):
        with mute:
            ierr = branch_chng(self.__fromBus.BusNum, self.__toBus.BusNum, self.__ckt,
                               intgar1=props.get('status'),
                               intgar2=props.get('metbus'),
                               intgar3=props.get('owner1'),
                               intgar4=props.get('owner2'),
                               intgar5=props.get('owner3'),
                               intgar6=props.get('owner4'),
                               realar1=props.get('r'),
                               realar2=props.get('x'),
                               realar3=props.get('b'),
                               realar4=props.get('rate_a'),
                               realar5=props.get('rate_b'),
                               realar6=props.get('rate_c'),
                               realar7=props.get('gi'),
                               realar8=props.get('bi'),
                               realar9=props.get('gj'),
                               realar10=props.get('bj'),
                               realar11=props.get('len'),
                               realar12=props.get('F1'),
                               realar13=props.get('F2'),
                               realar14=props.get('F3'),
                               realar15=props.get('F4'))
            if ierr <> 0:
                raise PssError('Some error occurred.')


















