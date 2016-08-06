from peachpy.x86_64 import *
from peachpy import *
from multiply_common import *
from common.YepStatus import *
from common.pipeline import software_pipelined_loop

def multiply_VV_V_generic(arg_x, arg_y, arg_z, arg_n, isa_ext):
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_TYPE = arg_z.c_type.base
    INPUT_TYPE_SIZE = INPUT_TYPE.size
    OUTPUT_TYPE_SIZE = OUTPUT_TYPE.size
