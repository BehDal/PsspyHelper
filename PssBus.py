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

# Bus
class Bus:
    def __init__(self, id):
        if id is int:
            if busexs(ibus) <> 0:
                raise PssError('Bus number {} not found'.format(id))
            self.__bus_num = id
        elif id is str:
            ierr, ibus = natono(id)
            if ierr <> 0:
                raise PssError('Bus name {} not found'.format(id))
            self.__bus_num = ibus
        else:
            raise ValueError('Bad bus name/number.')

    @property
    def Number(self):
        return self.__bus_num

    @property
    def ExName(self):
        _, name = notona(self.__bus_num)
        return name

    @property
    def Name(self):
        return self.ExName[:12]

    def GetProp(self, prop):
        prop = prop.upper()
        if prop in ('BASE', 'PU', 'KV', 'ANGLE', 'ANGLED', 'NVLMHI', 'NVLMLO', 'EVLMHI', 'EVLMLO'):
            ierr, value = busdat(self.__bus_num, prop)
        elif prop in ('TYPE', 'AREA', 'ZONE', 'OWNER', 'DUMMY'):
            ierr, value = busint(self.__bus_num, prop)
        else:
            raise PssError('Property invalid.')
        if ierr <> 0:
            raise PssError('Some error occurred.')
        return value

    def SetProps(self, **props):
        with mute:
            ierr = bus_chng_3(self.__bus_num,
                              intgar1=props.get('type'),
                              intgar2=props.get('area'),
                              intgar3=props.get('zone'),
                              intgar4=props.get('owner'),
                              realar1=props.get('basekv'),
                              realar2=props.get('vm'),
                              realar3=props.get('va'),
                              realar4=props.get('nmaxv'),
                              realar5=props.get('nminv'),
                              realar6=props.get('emaxv'),
                              realar7=props.get('eminv'))
            if ierr <> 0:
                raise PssError('Some error occurred.')

    def Disconnect(self):
        ierr = dscn(bus)
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def Reconnect(self):
        ierr = recn(bus)
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def RenumberTo(self, new_num):
        with mute:
            ierr = bsnm(all=1, opt=0)
            ierr = bsnm(all=1, opt=2, busrng1=self.__bus_num, busrng2=new_num, out=2)
            if ierr <> 0:
                raise PssError('Some error occurred.')
            ierr = bsnm(all=1, opt=7)
            self.__bus_num = new_num

    def Close(self):
        ierr = close_powerflow()
        if ierr <> 0:
            raise PssError('Some error occurred.')
