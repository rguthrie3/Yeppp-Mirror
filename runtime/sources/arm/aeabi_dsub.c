//===-- lib/adddf3.c - Double-precision subtraction ---------------*- C -*-===//
//
//                     The LLVM Compiler Infrastructure
//
// This file is dual licensed under the MIT and the University of Illinois Open
// Source Licenses.
//
//==============================================================================
//compiler_rt License
//==============================================================================
//
//The compiler_rt library is dual licensed under both the University of Illinois
//"BSD-Like" license and the MIT license.  As a user of this code you may choose
//to use it under either license.  As a contributor, you agree to allow your code
//to be used under both.
//
//Full text of the relevant licenses is included below.
//
//==============================================================================
//
//University of Illinois/NCSA
//Open Source License
//
//Copyright (c) 2009-2013 by the contributors listed below
//
//All rights reserved.
//
//Developed by:
//
//    LLVM Team
//
//    University of Illinois at Urbana-Champaign
//
//    http://llvm.org
//
//Permission is hereby granted, free of charge, to any person obtaining a copy of
//this software and associated documentation files (the "Software"), to deal with
//the Software without restriction, including without limitation the rights to
//use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
//of the Software, and to permit persons to whom the Software is furnished to do
//so, subject to the following conditions:
//
//    * Redistributions of source code must retain the above copyright notice,
//      this list of conditions and the following disclaimers.
//
//    * Redistributions in binary form must reproduce the above copyright notice,
//      this list of conditions and the following disclaimers in the
//      documentation and/or other materials provided with the distribution.
//
//    * Neither the names of the LLVM Team, University of Illinois at
//      Urbana-Champaign, nor the names of its contributors may be used to
//      endorse or promote products derived from this Software without specific
//      prior written permission.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
//FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
//CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE
//SOFTWARE.
//
//=============================================================================
//
//Copyright (c) 2009-2013 by the contributors listed below
//
//Permission is hereby granted, free of charge, to any person obtaining a copy
//of this software and associated documentation files (the "Software"), to deal
//in the Software without restriction, including without limitation the rights
//to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
//copies of the Software, and to permit persons to whom the Software is
//furnished to do so, subject to the following conditions:
//
//The above copyright notice and this permission notice shall be included in
//all copies or substantial portions of the Software.
//
//THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
//IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
//FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
//AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
//LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
//OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
//THE SOFTWARE.
//
//=============================================================================
//CONTRIBUTORS
//
//Below is a partial list of people who have contributed to the LLVM/CompilerRT
//project.
//
//The list is sorted by surname and formatted to allow easy grepping and
//beautification by scripts.  The fields are: name (N), email (E), web-address
//(W), PGP key ID and fingerprint (P), description (D), and snail-mail address
//(S).
//
//N: Craig van Vliet
//E: cvanvliet@auroraux.org
//W: http://www.auroraux.org
//D: Code style and Readability fixes.
//
//N: Edward O'Callaghan
//E: eocallaghan@auroraux.org
//W: http://www.auroraux.org
//D: CMake'ify Compiler-RT build system
//D: Maintain Solaris & AuroraUX ports of Compiler-RT
//
//N: Howard Hinnant
//E: hhinnant@apple.com
//D: Architect and primary author of compiler-rt
//===----------------------------------------------------------------------===//
//
// This file implements double-precision soft-float subtraction with the
// IEEE-754 default rounding (to nearest, ties to even).
//
//===----------------------------------------------------------------------===//

#define DOUBLE_PRECISION
#include "fp_lib.h"

extern __attribute__((visibility("internal"))) fp_t __aeabi_dadd(fp_t a, fp_t b);

// Subtraction; flip the sign bit of b and add.
extern __attribute__((visibility("internal"))) fp_t __aeabi_dsub(fp_t a, fp_t b) {
    return __aeabi_dadd(a, fromRep(toRep(b) ^ signBit));
}

/* FIXME: rsub for ARM EABI */
