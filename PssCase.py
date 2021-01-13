from PssConst import *

# add PSS/E path to python
import pssepath
pssepath.add_pssepath()

# import all psspy functions
from psspy import *

# redirect PSS/E alerts\messages to python command line
import redirect
redirect.psse2py()

# declare 'with mute:' block to silent PSS/E alerts
import os
from contextlib2 import redirect_stdout
mute = redirect_stdout(open(os.devnull, 'w'))

class PssError(BaseException):
    pass

#############################################################################

# Case
class PssCase:
    def __init__(self, num_of_buses=None):
        with mute:
            if num_of_buses is None:
                psseinit()
            elif num_of_buses is int:
                psseinit(num_of_buses)
            else:
                raise ValueError("'num_of_buses' must be an interger.")

    def ReadRaw(self, filename, use_bus_nums=True):
        self.__filename = filename
        if use_bus_nums:
            numnam = 0
        else:
            numnam = 1
        with mute:
            _, major, _, _, _, _ = psseversion()
            versions = [str(n) for n in range(major, 14, -1)]
            for ver in versions:
                readrawversion(numnam=numnam, vernum=ver, ifile=filename)
                if check_powerflow_data(0, 1, 0) == 0:
                    return
        raise PssError("Can't open file.")

    def ReadSavedCase(self, fileName):
        self.__filename = fileName
        ierr = case(fileName)
        if ierr <> 0:
            raise PssError("Can't open file.")

    @property
    def FileName(self):
        return self.__filename

    def RunPowerFlow(self, method=0, **opts):
        pf_functions = (fdns, fnsl, nsol, solv, mslv)
        run_pf = pf_functions[method]
        with mute:
            ierr = run_pf(options1=opts.get('tap_adj', 0),
                          options2=opts.get('ar_intr_adj', 0),
                          options3=opts.get('phase_adj', 0),
                          options4=opts.get('dc_tap_adj', 0),
                          options5=opts.get('sw_shant_adj', 0),
                          options6=opts.get('flat_start', 0),
                          options7=opts.get('var_limit', 0),
                          options8=opts.get('non_div_sol', 0)
                          )
        if ierr <> 0:
            raise PssError('Some error occurred.')

    @property
    def BaseFrequency(self):
        ierr, value = base_frequency()
        if ierr <> 0:
            raise PssError('Some error occurred.')
        return value

    @BaseFrequency.setter
    def BaseFrequency(self, value):
        ierr = base_frequency(value)
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def Close(self):
        ierr = close_powerflow()
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def IncreaseBusSizeTo(self, buses):
        ierr = new_dimension(buses)
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def SaveAs(self, filename):
        ierr = save(filename)
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def Scale(self, act_method, react_method, machine_limits, bus_type, **scales):
        with mute:
            ierr, _, _ = scal(all=1, apiopt=0,
                              status1=act_method,
                              status2=machine_limits,
                              status3=react_method,
                              status4=bus_type,
                              scalval1=scales.get('load_mw'),
                              scalval2=scales.get('gen_mw'),
                              scalval3=scales.get('shunt_mw'),
                              scalval4=scales.get('react_mvar'),
                              scalval5=scales.get('cap_mvar'),
                              scalval6=scales.get('mot_mw'),
                              scalval7=scales.get('reac_load_val')
                              )
        if ierr <> 0:
            raise PssError('Some error occurred.')

    @property
    def TapAdjustment(self):
        ierr, value = tap_adjustment()
        if ierr <> 0:
            raise PssError('Some error occurred.')
        return TAPS[value]

    @TapAdjustment.setter
    def TapAdjustment(self, value):
        ierr = tap_adjustment(TAP[value])
        if ierr <> 0:
            raise PssError('Some error occurred.')

    def WriteToRaw(self, filename, version=None):
        if version is None:
            _, version, _, _, _, _ = psseversion()
        ierr = writerawversion(vernum=version, out=0, ofile=filename)
        if ierr == 1:
            raise PssError('Invalid version number.')
        elif ierr > 1:
            raise PssError('Some error occurred.')

    @property
    def AreaInterchange(self):
        pass
