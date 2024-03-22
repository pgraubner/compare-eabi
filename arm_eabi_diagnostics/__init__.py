#!/usr/bin/python3

# The following information was taken and modified from https://github.com/ARM-software/abi-aa/blob/fe46d4335d87e792991ceab9c8fd7b79f927a918/addenda32/addenda32.rst#L1006
# licensed under CC-BY-SA-4.0 along with an additional patent license.
# Release: https://github.com/ARM-software/abi-aa/releases/tag/2023Q3
# For ARM ABI releases, see https://github.com/ARM-software/abi-aa/releases
#
# License: https://github.com/ARM-software/abi-aa/addenda32/LICENSE

Diagnostics = {
"Tag_CPU_raw_name": """

Target-related attribute.
The raw name is the name a user gave to a tool or selected from a menu. It can
be:

*  The name of a specific manufacturer’s part (such as ML692000).

*  The name of a generic part (such as Arm946E-S) or architecture (such as
   v5TE).

*  Any other name acceptable to the toolchain.

The value "" denotes that the raw name is identical to the CPU name
(described immediately below) and records that the user built for a generic
implementation (such as Arm946E-S) rather than any manufacturer-specific
part (such as ML692000) based on it.

It is always safe to use "" as a dummy value for this tag, or to omit this
tag.
""",
   "Tag_CPU_name": """
A CPU name is defined by Arm or the architecture licensee responsible for
designing the part. It is the official product name, with no extension and
no abbreviation.

An Arm-defined architecture name may be used instead of a CPU name, and
denotes that the user had more generic intentions. Arm-defined names of CPUs
and architectures recognized by Arm Compiler 5.01 are listed in
`Arm CPU names recognized by Arm Compiler 5.01 (armcc)`_.

The following tags describe the processor architecture version and
architecture profile for which the user intended the producer to produce
code.

""",
   "Tag_CPU_arch": """
Target-related attribute.
       0  Pre-v4
       1  Arm v4     // e.g. SA110
       2  Arm v4T    // e.g. Arm7TDMI
       3  Arm v5T    // e.g. Arm9TDMI
       4  Arm v5TE   // e.g. Arm946E-S
       5  Arm v5TEJ  // e.g. Arm926EJ-S
       6  Arm v6     // e.g. Arm1136J-S
       7  Arm v6KZ   // e.g. Arm1176JZ-S
       8  Arm v6T2   // e.g. Arm1156T2F-S
       9  Arm v6K    // e.g. Arm1136J-S
      10  Arm v7     // e.g. Cortex-A8, Cortex-M3
      11  Arm v6-M   // e.g. Cortex-M1
      12  Arm v6S-M  // v6-M with the System extensions
      13  Arm v7E-M  // v7-M with DSP extensions
      14  Arm v8-A
      15  Arm v8-R
      16  Arm v8-M.baseline
      17  Arm v8-M.mainline
      18  Arm v8.1-A
      19  Arm v8.2-A
      20  Arm v8.3-A
      21  Arm v8.1-M.mainline
      22  Arm v9-A
""",
   "Tag_CPU_arch_profile": """
Target-related attribute.
       0  Architecture profile is not applicable (e.g. pre v7, or cross-profile code),
          or is indicated by Tag_CPU_arch
      'A' (0x41) The application profile (e.g. for Cortex-A8)
      'R' (0x52) The real-time profile (e.g. for Cortex-R4)
      'M' (0x4D) The microcontroller profile (e.g. for Cortex-M3)
      ’S’ (0x53) Application or real-time profile (i.e. the ‘classic’ programmer’s model)

``Tag_CPU_arch_profile`` states that the attributed entity requires the noted
architecture profile.

The value 0 states that there is no requirement for any specific
architecture profile. The value ‘S’ denotes that the attributed entity
requires the classic programmer’s model rather than the microcontroller
programmer’s model.

Starting with architecture versions v8-A, v8-R and v8-M, the profile is
represented by Tag_CPU_arch. For these architecture versions and any later
versions, a value of 0 should be used for ``Tag_CPU_arch_profile``.

The following tags track the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
""",
   "Tag_ARM_ISA_use": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user did not permit this entity to use Arm instructions
      1  The user intended that this entity could use Arm instructions
""",
   "Tag_THUMB_ISA_use": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user did not permit this entity to use Thumb instructions
      1  (deprecated) The user permitted this entity to use 16-bit Thumb instructions (including BL)
      2  (deprecated) 32-bit Thumb instructions were permitted (implies 16-bit instructions permitted)
      3  The user permitted this entity to use Thumb code. The set of permitted instructions can be
         determined by the setting of Tag_CPU_arch and Tag_CPU_arch_profile

      Note: The historical use of values 1 and 2 date to a time when there was
      a clear separation between implementations using 16-bit only Thumb
      instructions and those using the extended set of instructions. The
      introduction of Armv8-M.baseline has blurred this distinction to the
      point where it is no-longer useful. Arm recommends that in future all
      toolchains emit a value of 3 when use of Thumb was intended by the user
      and 0 (or omitting the tag entirely) when use of Thumb was not intended.
""",
   "Tag_FP_arch": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user did not permit this entity to use instructions requiring FP hardware
      1  The user permitted use of instructions from v1 of the floating point (FP) ISA
      2  Use of the v2 FP ISA was permitted (implies use of the v1 FP ISA)
      3  Use of the v3 FP ISA was permitted (implies use of the v2 FP ISA)
      4  Use of the v3 FP ISA was permitted, but only citing registers D0-D15, S0-S31
      5  Use of the v4 FP ISA was permitted (implies use of the non-vector v3 FP ISA)
      6  Use of the v4 FP ISA was permitted, but only citing registers D0-D15, S0-S31
      7  Use of the Arm v8-A FP ISA was permitted
      8  Use of the Arm v8-A FP ISA was permitted, but only citing registers D0-D15, S0-S31
""",
   "Tag_WMMX_arch": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user did not permit this entity to use WMMX
      1  The user permitted this entity to use WMMX v1
      2  The user permitted this entity to use WMMX v2
""",
   "Tag_Advanced_SIMD_arch": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user did not permit this entity to use the Advanced SIMD Architecture (Neon)
      1  Use of the Advanced SIMDv1 Architecture (Neon) was permitted
      2  Use of Advanced SIMDv2 Architecture (Neon) (with half-precision floating-point and
         fused MAC operations) was permitted
      3  Use of the Arm v8-A Advanced SIMD Architecture (Neon) was permitted
      4  Use of the Arm v8.1-A Advanced SIMD Architecture (Neon) was permitted
""",
   "Tag_MVE_arch": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user did not permit this entity to use the M-profile Vector Extension
      1  Use of the Integer M-profile Vector Extension was permitted
      2  Use of the Integer and Floating Point M-profile Vector Extension was
      permitted
""",
   "Tag_FP_HP_extension": """
Target-related attribute.  Tracks the permitted use of instruction sets. The
architecture revision (``Tag_CPU_arch``) implies the permitted subset of
instructions from the permitted ISA.
      0  The user intended half-precision floating point instructions may be used if they
         exist in the available FP and ASIMD instruction sets as indicated by Tag_FP_arch
         and Tag_ASIMD_arch
      1  Use of the half-precision instructions first added as an optional extension to
         VFPv3/Advanced SIMDv1 was permitted, in addition to those indicated by Tag_FP_arch
         and Tag_ASIMD_arch
      2  Use of the half-precision instructions first added as an optional extension to
         Armv8.2-A Floating-Point and Advanced SIMD was permitted, in addition to those
         indicated by Tag_FP_arch and Tag_ASIMD_arch

""",
   "Tag_CPU_unaligned_access": """
Target-related attribute. Describes the unaligned data accesses the user permitted the producer to make.
      0  The user did not intend this entity to make unaligned data accesses
      1  The user intended that this entity might make v6-style unaligned data accesses

""",
   "Tag_T2EE_use": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  No use of T2EE extension was permitted, or no information is available
       1  Use of the T2EE extension was permitted

In effect, ``Tag_T2EE_use`` describes the intended use of ENTERX and LEAVEX
instructions. ``Tag_T2EE_use`` is deprecated from r2.09.
""",
   "Tag_Virtualization_use": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  No use of any virtualization extension was permitted, or no information available
       1  Use of the TrustZone extension was permitted
       2  Use of the virtualization extensions (HVC, ERET) were permitted
       3  Use of TrustZone and virtualization extensions were permitted

In effect, ``Tag_Virtualization_use`` describes the intended use of the SMC
instruction in bit 0 of the tag value and the intended use of HVC and ERET
instructions in bit 1.
""",
   "Tag_MPextension_use": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  No use of Arm v7 MP extension was permitted, or no information available.
       1  Use of the Arm v7 MP extension was permitted.

In effect, ``Tag_MPextension_use`` describes the intended use of the PLDW
(preload write hint) instruction.
""",
   "Tag_DIV_use": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  The user intended divide instructions may be used if they exist, or no explicit
          information recorded. This code was permitted to use SDIV and UDIV if the
          instructions are guaranteed present in the architecture,
          as indicated by Tag_CPU_arch and Tag_CPU_arch_profile.
       1  This code was explicitly not permitted to use SDIV or UDIV.
       2  This code was permitted to use SDIV and UDIV in the Arm and Thumb ISAs; the
          instructions are present as an optional architectural extension above the base
          architecture implied by Tag_CPU_arch and Tag_CPU_arch_profile.

   Value 1 records an explicit intention to not use divide instructions in
   this code, on targets where they would otherwise be permitted. This
   intention could be conveyed to the object producer by citing a "no
   divide" command-line option, or by other means. How a linker interprets
   this intention is QoI.

   Producers must emit value 2 if and only if the permission to use SDIV and
   UDIV cannot be conveyed using values 0 and 1.
""",
   "Tag_DSP_extension": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  The user intended DSP instructions may be used if they exist. This
          entity is permitted to use DSP instructions if they are guaranteed
          present in the architecuture as indicated by Tag_CPU_arch.
       1  This code was permitted to use Thumb DSP functions as an optional
          architecture extension above the base architecture as indicated by
          Tag_CPU_arch.
""",
    "Tag_PAC_extension": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  The user did not permit this entity to use PAC/AUT instructions
       1  The user permitted this entity to use PAC/AUT instructions in the NOP
          space
       2  The user permitted this entity to use PAC/AUT instructions in the NOP
          and in the non-NOP space

""",
   "Tag_BTI_extension": """
Target-related attribute. Describes the intended use of optional an architectural extension.
       0  The user did not permit this entity to use BTI instructions
       1  The user permitted this entity to use BTI instructions in the NOP space
       2  The user permitted this entity to use BTI instructions in the NOP and
          in the non-NOP space
""",
   "Tag_PCS_config": """
Procedure call-related attribute describing compatibility with the ABI.
       0  No standard configuration used, or no information recorded
       1  Bare platform configuration
       2  Linux application configuration
       3  Linux DSO configuration
       4  Palm OS 2004 configuration
       5  Reserved to future Palm OS configuration
       6  Symbian OS 2004 configuration
       7  Reserved to future Symbian OS configuration

``Tag_PCS_config`` summarizes the user intention behind the procedure-call
standard configuration used. Its value must be consistent with the values
given to the tags below, and must not be used as a macro in place of them.
""",
   "Tag_ABI_PCS_R9_use": """
Procedure call-related attribute describing compatibility with the ABI. Summarizes how the user intended the attributed
entity to address static data.

       0  R9 used as V6 (just another callee-saved register, implied by omitting the tag)
       1  R9 used as SB, a global Static Base register
       2  R9 used as a Thread Local Storage (TLS) pointer
       3  R9 not used at all by code associated with the attributed entity

R9 has a role in some variants of the PCS. ``Tag_ABI_PCS_R9_use`` describes the
user’s chosen PCS variant.

When R9 is used as a Thread Local Storage (TLS) pointer (``Tag_ABI_PCS_R9_use``
= 2), R9 plays the role that would otherwise be played by one of the three
Software Thread ID Registers ``TPIDRURW``, ``TPIDRURO``, ``TPIDRPRW`` defined in section
B3.12.46, CP15 c13 Software Thread ID registers, of the Arm Architecture
Reference Manual Arm v7-A and Arm v7-R edition [Arm DDI 0406].

The role played by that ``TPID*`` register is defined by the software platform’s
ABI.
""",
   "Tag_ABI_PCS_RW_data": """
Procedure call-related attribute describing compatibility with the ABI. Summarizes how the user intended the attributed
entity to address static data.

       0  RW static data was permitted to be addressed absolutely
       1  RW static data was only permitted to be addressed PC-relative
       2  RW static data was only permitted to be addressed SB-relative
       3  The user did not permit this entity to use RW static data
""",
   "Tag_ABI_PCS_RO_data": """
Procedure call-related attribute describing compatibility with the ABI. Summarizes how the user intended the attributed
entity to address static data.
       0  RO static data was permitted to be addressed absolutely
       1  RO static data was only permitted to be addressed PC-relative
       2  The user did not permit this entity to use RO static data
""",
   "Tag_ABI_PCS_GOT_use": """
Procedure call-related attribute describing compatibility with the ABI. Summarizes how the user intended the attributed
entity to address static data.
       0  The user did not permit this entity to import static data
       1  The user permitted this entity to address imported data directly
       2  The user permitted this entity to address imported data indirectly (e.g. via a GOT)
""",
   "Tag_ABI_PCS_wchar_t": """
Describes the permitted sizes of a wide character.
       0  The user prohibited the use of wchar_t when building this entity
       2  The user intended the size of wchar_t to be 2
       4  The user intended the size of wchar_t to be 4
""",
   "Tag_ABI_enum_size": """
Describes the permitted sizes of an enumerated data item.
       0  The user prohibited the use of enums when building this entity
       1  Enum values occupy the smallest container big enough to hold all their values
       2  The user intended Enum containers to be 32-bit
       3  The user intended that every enumeration visible across an ABI-complying interface
          contains a value needing 32 bits to encode it; other enums can be containerized
""",
   "Tag_ABI_align_needed": """
Summarizes the alignment contract across an interface.
       0  The user did not permit code to depend the alignment of 8-byte data or data with
          extended (> 8-byte) alignment
       1  Code was permitted to depend on the 8-byte alignment of 8-byte data items
       2  Code was permitted to depend on the 4-byte alignment of 8-byte data items
       3  Reserved
       n  (in 4..12) Code was permitted to depend on the 8-byte alignment of 8-byte data items
          and the alignment of data items having up to 2n-byte extended alignment
""",
   "Tag_ABI_align_preserved": """
Summarizes the alignment contract across an interface.
       0  The user did not require code to preserve 8-byte alignment of 8-byte data objects
       1  Code was required to preserve 8-byte alignment of 8-byte data objects
       2  Code was required to preserve 8-byte alignment of 8-byte data objects and to
          ensure (SP MOD 8) = 0 at all instruction boundaries (not just at function calls)
       3  Reserved
       n (in 4..12) Code was required to preserve the alignments of case 2 and the alignment
         of data items having up to 2n-byte extended alignment.
""",
   "Tag_ABI_FP_rounding": """
Summarizes the requirements code associated with this attributed entity was permitted to place on floating-point arithmetic.
       0  The user intended this code to use the IEEE 754 round to nearest rounding mode
       1  The user permitted this code to choose the IEEE 754 rounding mode at run time
""",
   "Tag_ABI_FP_denormal": """
Summarizes the requirements code associated with this attributed entity was permitted to place on floating-point arithmetic.
       0  The user built this code knowing that denormal numbers might be flushed to (+) zero
       1  The user permitted this code to depend on IEEE 754 denormal numbers
       2  The user permitted this code to depend on the sign of a flushed-to-zero number being
          preserved in the sign of 0
""",
   "Tag_ABI_FP_exceptions": """
Summarizes the requirements code associated with this attributed entity was permitted to place on floating-point arithmetic.
       0  The user intended that this code should not check for inexact results
       1  The user permitted this code to check the IEEE 754 inexact exception
""",
   "Tag_ABI_FP_user_exceptions": """
Summarizes the requirements code associated with this attributed entity was permitted to place on floating-point arithmetic.
       0  The user intended that this code should not enable or use IEEE user exceptions
       1  The user permitted this code to enables and use IEEE 754 user exceptions
""",
   "Tag_ABI_FP_number_model": """
Summarizes the requirements code associated with this attributed entity was permitted to place on floating-point arithmetic.
       0  The user intended that this code should not use floating point numbers
       1  The user permitted this code to use IEEE 754 format normal numbers only
       2  The user permitted numbers, infinities, and one quiet NaN (see [RTABI32_])
       3  The user permitted this code to use all the IEEE 754-defined FP encodings

FP model hierarchies are difficult to specify. In practice, there is a large
lattice of potentially useful models, depending on whether FP arithmetic is
done by software or by hardware, and on the properties of that hardware. The
tags above allow requirements to be specified using independent features.
For example, code following the Java numerical model should record
``Tag_ABI_FP_denormal = 1`` and ``Tag_ABI_FP_number_model = 2``, while graphics
code concerned with speed above all other considerations might record
``Tag_ABI_FP_number_model = 1`` and ``Tag_ABI_FP_optimization_goals = 2`` (see
below).

""",
   "Tag_ABI_FP_16bit_format": """
Summarizes use of 16-bit floating point numbers by the attributed entities.
       0  The user intended that this entity should not use 16-bit floating point numbers
       1  Use of IEEE 754 (draft, November 2006) format 16-bit FP numbers was permitted
       2  Use of VFPv3/Advanced SIMD “alternative format” 16-bit FP numbers was permitted

Options 1 and 2 are mutually incompatible.
""",
   "Tag_ABI_HardFP_use": """
Records th epermitted use of the VFP extension and WMMX co-processor.
Note that:

*  Under the base variant of the procedure call standard [AAPCS32_], FP
   parameters and results are passed the soft FP way, in core registers or on
   the stack. WMMX parameters and results are passed the same way.

*  The VFP variant of [AAPCS32_] uses VFP registers D0-D7
   (s0-s15) to pass parameters and results.

*  The Intel WMMX convention is to use wR0-wR9 to pass parameters and
   results.
       0  The user intended that FP use should be implied by Tag_FP_arch
       1  The user intended this code to execute on the single-precision variant
          derived from Tag_FP_arch
       2  Reserved
       3  The user intended that FP use should be implied by Tag_FP_arch
          (Note: This is a deprecated duplicate of the default encoded by 0)
""",
   "Tag_ABI_VFP_args": """
Records th epermitted use of the VFP extension.
Note that:

*  Under the base variant of the procedure call standard [AAPCS32_], FP
   parameters and results are passed the soft FP way, in core registers or on
   the stack. WMMX parameters and results are passed the same way.

*  The VFP variant of [AAPCS32_] uses VFP registers D0-D7
   (s0-s15) to pass parameters and results.

*  The Intel WMMX convention is to use wR0-wR9 to pass parameters and
   results.

       0  The user intended FP parameter/result passing to conform to AAPCS, base variant
       1  The user intended FP parameter/result passing to conform to AAPCS, VFP variant
       2  The user intended FP parameter/result passing to conform to toolchain-specific
          conventions
       3  Code is compatible with both the base and VFP variants; the user did not permit
          non-variadic functions to pass FP parameters/results
""",
   "Tag_ABI_WMMX_args": """
Records th epermitted use of WMMX co-processor.
Note that:

*  Under the base variant of the procedure call standard [AAPCS32_], FP
   parameters and results are passed the soft FP way, in core registers or on
   the stack. WMMX parameters and results are passed the same way.

*  The VFP variant of [AAPCS32_] uses VFP registers D0-D7
   (s0-s15) to pass parameters and results.

*  The Intel WMMX convention is to use wR0-wR9 to pass parameters and
   results.
       0  The user intended WMMX parameter/result passing conform to the AAPCS, base variant
       1  The user intended WMMX parameter/result passing conform to Intel’s WMMX conventions
       2  The user intended WMMX parameter/result passing conforms to toolchain-specific
          conventions
""",
   "Tag_FramePointer_use": """
Summarizes the level of conformance to the rules for creating and maintaining a chain of frame records on the stack.
       0  This code makes no claims to conformance with the rules for use of a frame pointer
       1  This code creates a frame record for all functions that may modify the value stored
          in the link register (LR)
       2  This code does not create frame records, but preserves the value stored in the
          frame pointer register (FP)

It is recommended that code that uses a private convention for
maintaining a frame chain should leave this tag unset (=0) and then
use a vendor-specific attribute to record this property.

Generally this tag can be ignored for the purposes of diagnosing
object file compatibility, unless a program explictly needs to depend
on being able to walk the frame chain.

""",
   "Tag_BTI_use": """
Describes a producer use of branch target identification instructions.
       0  This code is compiled without branch target enforcement
       1  This code is compiled with branch target enforcement
""",
   "Tag_PACRET_use": """
Describes a producer use of pointer authentication instructions.
       0  This code is compiled without return address signing and authentication
       1  This code is compiled with return address signing and authentication
""",
   "Tag_ABI_optimization_goals": """
ABI-related tag recording optimization goals. It is not required for reasoning about incompatibility,
but assist with selecting appropriate variants of library members.
       0  No particular optimization goals, or no information recorded
       1  Optimized for speed, but small size and good debug illusion preserved
       2  Optimized aggressively for speed, small size and debug illusion sacrificed
       3  Optimized for small size, but speed and debugging illusion preserved
       4  Optimized aggressively for small size, speed and debug illusion sacrificed
       5  Optimized for good debugging, but speed and small size preserved
       6  Optimized for best debugging illusion, speed and small size sacrificed

With ``Tag_ABI_optimization_goals`` we capture one of three potentially
conflicting intentions – high performance, small size, and easy debugging –
at one of two levels.

At the first level the goal is unambiguous, but pursuit of it is
constrained. The conflicting goals still matter, but less than the primary
goal.

At the second level, the conflicting goals are insignificant in comparison
to the primary goal. It is difficult to capture optimization intentions
precisely, but to a significant degree what matters to a toolchain is the
user’s goal (speed, small size, or debug-ability), and whether or not the
user is willing to sacrifice all other considerations to achieving that
goal.
""",
   "Tag_ABI_FP_optimization_goals": """
ABI-related tag recording optimization goals. It is not required for reasoning about incompatibility, but assist with selecting appropriate variants of library members.
       0  No particular FP optimization goals, or no information recorded
       1  Optimized for speed, but small size and good accuracy preserved
       2  Optimized aggressively for speed, small size and accuracy sacrificed
       3  Optimized for small size, but speed and accuracy preserved
       4  Optimized aggressively for small size, speed and accuracy sacrificed
       5  Optimized for accuracy, but speed and small size preserved
       6  Optimized for best accuracy, speed and small size sacrificed

With ``Tag_ABI_FP_optimization_goals`` we also capture one of three potentially
conflicting goals at one of the same two levels as
``Tag_ABI_optimization_goals`` captures.

Some accuracy sacrificed is intended to allow, for example, re-association
of expressions in generated code. In library code it is intended to permit
the assumption that value ranges will be reasonable. In particular, binary
to decimal and decimal to binary conversion may meet only the minimum
standards specified by IEEE 754, and range reduction for trigonometric
functions should be assumed to be naive.
""",
   "Tag_compatibility": """

An omitted tag implies flag = 0, vendor-name = “”. An explicit flag value is
not 0 and can be considered to be the first byte(s) of the vendor name for
the purpose of skipping the entry. The default value of 0 describes the
implicit claim made by files generated prior to v1.06 of this specification.

The defined flag values and their meanings are as follows.
   0   The tagged entity has no toolchain-specific requirements
       (and no vendor tag hides an ABI incompatibility)
   1   This entity can conform to the ABI if processed by the named toolchain.
       The ABI variant to which it conforms is described solely by public “aeabi” tags
   >1  The tagged entity does not conform to the ABI but it can be processed by other
       tools under a private arrangement described by flag and vendor-name

A flag value >1 identifies an arrangement, beyond the scope of the ABI,
defined by the named vendor. A toolchain that recognizes the arrangement
might successfully process this file. Note that a producer must use the name
of the vendor defining the arrangement, not the name of the producing
toolchain.

(Versions of this specification through v1.05 stated:
   >1  The tagged entity is compatible only with identically tagged entities,
       *and entities not tagged by this toolchain*

The underlined part of that definition was a mistake that makes the
definition useless. With the underlined part removed, the old definition is
effectively compatible with, but more restrictive than, the new one).

""",
   "Tag_also_compatible_with": """

The data string must be further interpreted as a ULEB128-encoded tag
followed by a value of that tag. If that value is numerical (i.e. ULEB128),
there is an additional NUL byte following it. Thus, the data string value of
the ``Tag_also_compatible_with`` tag must be in one of the following two
formats:

*  ULEB128: tag, ULEB128: value, 0.
*  ULEB128: tag, NTBS: data.

""",
   "Tag_also_compatible_with": """

At this release of the ABI (|release|) there are only two defined uses of
``Tag_also_compatible_with``:

* To express v4T also compatible with v6-M and v6-M also compatible with v4T.

* To express v8-A also compatible with v8-R and v8-R also compatible with v8-A.

All other uses are RESERVED to the ABI.  Future releases of the ABI may relax
this constraint.
""",
   "Tag_conformance": """
Describes the version of the ABI to which conformity is claimed by an entity.
This version of the ABI is “\ |release|\ ”. The minor version (dot-xy) is
for information and does not affect the claim. Version “0” denotes no claim
to conform and is the default if the tag is omitted.

To simplify recognition by consumers in the common case of claiming
conformity for the whole file, this tag should be emitted first in a
file-scope sub-subsection of the first public subsection of the attributes
section.

In this case, the dot-ARM-dot-attributes section would begin
“A~~~~aeabi\0\1~~~~C\ |release|\ ”, where ‘~’ denotes an unknown byte value.

History of attributes in ABI revisions and ABI-Addenda document versions:
   +--------------+---------+--------------------+
   | ABI Revision | Doc vsn | Date               |
   +==============+=========+====================+
   | r2.0         | v1.0    | March 2005         |
   +--------------+---------+--------------------+
   | r2.01        | v1.01   | 5th July 2005      |
   +--------------+---------+--------------------+
   | r2.02        | v1.03   | 13th October 2005  |
   +--------------+---------+--------------------+
   | r2.03        | v1.04   | 6th January 2006   |
   +--------------+---------+--------------------+
   | r2.04        | v1.05   | 8th May 2006       |
   +--------------+---------+--------------------+
   | r2.05        | v1.06   | 25th January 2007  |
   +--------------+---------+--------------------+
   | r2.06        | A       | October 2007       |
   +--------------+---------+--------------------+
   | r2.07        | B       | October 2008       |
   +--------------+---------+--------------------+
   | r2.08        | C       | October 2009       |
   +--------------+---------+--------------------+
   | r2.09        | D       | November 2012      |
   +--------------+---------+--------------------+
"""
,
   "Tag_nodefaults": """

A consuming tool may take IMPLEMENTATION DEFINED action if any tag has an
UNDEFINED value after a dot-ARM-dot-attributes section has been fully
processed.

Consumers that do not recognize this tag will default UNDEFINED values to 0.

To make processing easy for consumers, this tag should be emitted before any
other tag in an attributes sub-subsection other than the conformance tag
(`Conformance tag`_).

We expect the no defaults tag to be used only by linkers that merge
attributed and un-attributed (legacy) relocatable files.

   From the 2.09 release, section and symbol attributes are deprecated and
   optional. Primary object producers are discouraged from generating them
   and consumers are permitted to ignore them. Hence from the 2.09 release
   use of this tag is deprecated.
"""
}

"""
 According to the ARM ABI documentation, the ABI requires the following of files
 that claim to conform (`Build attributes and conformance to the ABI`_) to the ABI.

 *  Attributes that record data about the compatibility of this file with
    other files must be recorded in a public "aeabi" subsection.

"""

