from peachpy.x86_64 import *
from peachpy import *
from common.YepStatus import *
from common.pipeline import software_pipelined_loop
from add_common import *

def add_IVS_IV_generic(arg_x, arg_y, arg_n, isa_ext):
    """
    Generic add kernel for adding a scalar to an immediate vector.
    """
    INPUT_TYPE = arg_x.c_type.base
    OUTPUT_TYPE = arg_x.c_type.base
    INPUT_TYPE_SIZE = arg_x.c_type.base.size
    OUTPUT_TYPE_SIZE = arg_x.c_type.base.size

    UNROLL_FACTOR = 5

    if isa_ext == "avx":
        SIMD_REGISTER_SIZE = YMMRegister.size
        SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE = avx_scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        SIMD_LOAD, SIMD_ADD, SIMD_STORE = avx_vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        reg_x_scalar = avx_scalar_register_map[OUTPUT_TYPE]()
        reg_y_scalar = avx_scalar_register_map[OUTPUT_TYPE]()
        reg_y_vector = YMMRegister()
        simd_accs = [YMMRegister() for _ in range(UNROLL_FACTOR)]
    elif isa_ext == "sse":
        SIMD_REGISTER_SIZE = XMMRegister.size
        SCALAR_LOAD, SCALAR_ADD, SCALAR_STORE = sse_scalar_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        SIMD_LOAD, SIMD_ADD, SIMD_STORE = sse_vector_instruction_select(INPUT_TYPE, OUTPUT_TYPE)
        reg_x_scalar = sse_scalar_register_map[OUTPUT_TYPE]()
        reg_y_scalar = sse_scalar_register_map[OUTPUT_TYPE]()
        if INPUT_TYPE in [ Yep32f, Yep64f ]:
            reg_y_vector = reg_y_scalar
        else:
            reg_y_vector = XMMRegister()
        simd_accs = [XMMRegister() for _ in range(UNROLL_FACTOR)]


    ret_ok = Label()
    ret_null_pointer = Label()
    ret_misaligned_pointer = Label()


    # Load args and test for null pointers and invalid arguments
    reg_length = GeneralPurposeRegister64() # Keeps track of how many elements are left to process
    LOAD.ARGUMENT(reg_length, arg_n)
    TEST(reg_length, reg_length)
    JZ(ret_ok) # Check there is at least 1 element to process

    reg_x_addr = GeneralPurposeRegister64()
    LOAD.ARGUMENT(reg_x_addr, arg_x)
    TEST(reg_x_addr, reg_x_addr) # Make sure arg_x is not null
    JZ(ret_null_pointer)
    TEST(reg_x_addr, OUTPUT_TYPE_SIZE - 1) # Check that our output arr is aligned
    JNZ(ret_misaligned_pointer)

    if INPUT_TYPE_SIZE < 4:
        LOAD.ARGUMENT(reg_y_scalar.as_dword, arg_y)
    else:
        LOAD.ARGUMENT(reg_y_scalar, arg_y)

    align_loop = Loop() # Loop to align one of the addresses
    scalar_loop = Loop() # Processes remainder elements (if n % 8 != 0)

    # Aligning on X addr
    # Process elements 1 at a time until z is aligned on YMMRegister.size boundary
    TEST(reg_x_addr, SIMD_REGISTER_SIZE - 1) # Check if already aligned
    JZ(align_loop.end) # If so, skip this loop entirely
    with align_loop:
        SCALAR_LOAD(reg_x_scalar, [reg_x_addr])
        SCALAR_ADD(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_x_addr], reg_x_scalar)
        ADD(reg_x_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JZ(ret_ok)
        TEST(reg_x_addr, SIMD_REGISTER_SIZE - 1)
        JNZ(align_loop.begin)

    reg_x_addr_out = GeneralPurposeRegister64()
    MOV(reg_x_addr_out, reg_x_addr)

    if isa_ext == "avx":
        AVX_MOV_GPR_TO_VECTOR(reg_y_vector, reg_y_scalar, INPUT_TYPE, OUTPUT_TYPE)
    elif isa_ext == "sse":
        SSE_MOV_GPR_TO_VECTOR(reg_y_vector, reg_y_scalar, INPUT_TYPE, OUTPUT_TYPE)

    # Batch loop for processing the rest of the array in a pipelined loop
    instruction_columns = [InstructionStream(), InstructionStream(), InstructionStream()]
    instruction_offsets = (0, 1, 2)
    for i in range(UNROLL_FACTOR):
        with instruction_columns[0]:
            SIMD_LOAD(simd_accs[i], [reg_x_addr + i * SIMD_REGISTER_SIZE * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE])
        with instruction_columns[1]:
            SIMD_ADD(simd_accs[i], simd_accs[i], reg_y_vector)
        with instruction_columns[2]:
            SIMD_STORE([reg_x_addr_out + i * SIMD_REGISTER_SIZE], simd_accs[i])
    with instruction_columns[0]:
        ADD(reg_x_addr, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)
    with instruction_columns[2]:
        ADD(reg_x_addr_out, SIMD_REGISTER_SIZE * UNROLL_FACTOR * INPUT_TYPE_SIZE / OUTPUT_TYPE_SIZE)

    software_pipelined_loop(reg_length, UNROLL_FACTOR * SIMD_REGISTER_SIZE / OUTPUT_TYPE_SIZE, instruction_columns, instruction_offsets)

    # Check if there are leftover elements that were not processed in the pipelined loop
    # This loop should iterate at most #(elems processed per iteration in the batch loop) - 1 times
    TEST(reg_length, reg_length)
    JZ(scalar_loop.end)
    with scalar_loop: # Process the remaining elements
        SCALAR_LOAD(reg_x_scalar, [reg_x_addr])
        SCALAR_ADD(reg_x_scalar, reg_x_scalar, reg_y_scalar)
        SCALAR_STORE([reg_x_addr], reg_x_scalar)
        ADD(reg_x_addr, OUTPUT_TYPE_SIZE)
        SUB(reg_length, 1)
        JNZ(scalar_loop.begin)

    with LABEL(ret_ok):
        RETURN(YepStatusOk)

    with LABEL(ret_null_pointer):
        RETURN(YepStatusNullPointer)

    with LABEL(ret_misaligned_pointer):
        RETURN(YepStatusMisalignedPointer)
