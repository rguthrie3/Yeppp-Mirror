from peachpy.x86_64 import *
from peachpy import *
from peachpy.c.types import *

packed_low_mult_map = {
    Yep16s      : VPMULLW,
    Yep16u      : VPMULLW,
    Yep32s      : VPMULLD,
    Yep32u      : VPMULLD
}

packed_high_mult_map = {
    Yep16s      : VPMULHW,
    Yep16u      : VPMULHUW
}

packed_mult_map = {
    Yep32f      : VMULPS,
    Yep64f      : VMULPD
}

high_unpack_map = {
    (Yep16s, Yep32s)    : VPUNPCKHWD,
    (Yep16u, Yep32u)    : VPUNPCKHWD,
    (Yep32s, Yep64s)    : VPUNPCKHDQ
}

low_unpack_map = {
    (Yep16s, Yep32s)    : VPUNPCKLWD,
    (Yep32s, Yep64s)    : VPUNPCKLDQ
}

packed_aligned_move_map = {
    Yep8s       : VMOVDQA,
    Yep8u       : VMOVDQA,
    Yep16s      : VMOVDQA,
    Yep16u      : VMOVDQA,
    Yep32s      : VMOVDQA,
    Yep32u      : VMOVDQA,
    Yep64s      : VMOVDQA,
    Yep64u      : VMOVDQA,
    Yep32f      : VMOVAPS,
    Yep64f      : VMOVAPD,
}

packed_unaligned_move_map = {
    Yep8s : VMOVDQU,
    Yep8u : VMOVDQU,
    Yep16s: VMOVDQU,
    Yep16u: VMOVDQU,
    Yep32s: VMOVDQU,
    Yep64s: VMOVDQU,
    Yep32f: VMOVUPS,
    Yep64f: VMOVUPD
}

scalar_move_map = {
    Yep8s       : MOV,
    Yep8u       : MOV,
    Yep16s      : MOV,
    Yep16u      : MOV,
    Yep32s      : MOV,
    Yep32u      : MOV,
    Yep64s      : MOV,
    Yep64u      : MOV,
    Yep32f      : VMOVSS,
    Yep64f      : VMOVSD
}

scalar_mult_map = {
    Yep8s       : IMUL,
    Yep8u       : IMUL,
    Yep16s      : IMUL,
    Yep16u      : IMUL,
    Yep32s      : IMUL,
    Yep32u      : IMUL,
    Yep64s      : IMUL,
    Yep64u      : IMUL,
    Yep32f      : VMULSS,
    Yep64f      : VMULSD
}

scalar_register_map = {
    Yep8s       : GeneralPurposeRegister8,
    Yep8u       : GeneralPurposeRegister8,
    Yep16s      : GeneralPurposeRegister16,
    Yep16u      : GeneralPurposeRegister16,
    Yep32s      : GeneralPurposeRegister32,
    Yep32u      : GeneralPurposeRegister32,
    Yep64s      : GeneralPurposeRegister64,
    Yep64u      : GeneralPurposeRegister64,
    Yep32f      : XMMRegister,
    Yep64f      : XMMRegister
}
