#!/usr/bin/python3


Tag_CPU_arch=[
  "Pre-v4",
  "v4",
  "v4T",
  "v5T",
  "v5TE",
  "v5TEJ",
  "v6",
  "v6KZ",
  "v6T2",
  "v6K",
  "v7",
  "v6-M",
  "v6S-M",
  "v7E-M",
  "v8",
  "v8-R",
  "v8-M.baseline",
  "v8-M.mainline",
  "v8.1-A",
  "v8.2-A",
  "v8.3-A",
  "v8.1-M.mainline",
  "v9"]

Tag_ARM_ISA_use = [
 "No",
 "Yes"
]
Tag_THUMB_ISA_use = [
  "No",
  "Thumb-1",
  "Thumb-2",
  "Yes"
]
Tag_FP_arch = [
  "No",
  "VFPv1",
  "VFPv2",
  "VFPv3",
  "VFPv3-D16",
  "VFPv4",
  "VFPv4-D16",
  "FP for ARMv8",
  "FPv5/FP-D16 for ARMv8"
]
Tag_WMMX_arch = [
 "No"
 "WMMXv1"
 "WMMXv2"
]
Tag_Advanced_SIMD_arch = [
  "No",
  "NEONv1",
  "NEONv1 with Fused-MAC",
  "NEON for ARMv8",
  "NEON for ARMv8.1"
]
Tag_PCS_config = [
  "None",
  "Bare platform",
  "Linux application",
  "Linux DSO",
  "PalmOS 2004",
  "PalmOS (reserved)",
  "SymbianOS 2004",
  "SymbianOS (reserved)"
]
Tag_ABI_PCS_R9_use = [
  "V6",
  "SB",
  "TLS",
  "Unused"
]
Tag_ABI_PCS_RW_data = [
  "Absolute",
  "PC-relative",
  "SB-relative",
  "None"
]
Tag_ABI_PCS_RO_data = [
  "Absolute",
  "PC-relative",
  "None"
]
Tag_ABI_PCS_GOT_use = [
  "None",
  "direct",
  "GOT-indirect"
]
Tag_ABI_PCS_wchar_t = [
  "None",
  "??? 1",
  "2",
  "??? 3",
  "4"
]
Tag_ABI_FP_rounding = [
 "Unused"
 "Needed"
]
Tag_ABI_FP_denormal = [
  "Unused",
  "Needed",
  "Sign only"
]
Tag_ABI_FP_exceptions = [
 "Unused",
 "Needed"
]
Tag_ABI_FP_user_exceptions = [
 "Unused",
 "Needed"
]
Tag_ABI_FP_number_model = [
  "Unused",
  "Finite",
  "RTABI",
  "IEEE 754"
]
Tag_ABI_IntEnum_size = [
  "Unused",
  "small",
  "int",
  "forced to int"
]
Tag_ABI_HardFP_use = [
  "As Tag_FP_arch",
  "SP only",
  "Reserved",
  "Deprecated"
]
Tag_ABI_VFP_args = [
  "AAPCS",
  "VFP registers",
  "custom",
  "compatible"
]
Tag_ABI_WMMX_args = [
  "AAPCS",
  "WMMX registers",
  "custom"
]
Tag_ABI_optimization_goals = [
  "None",
  "Prefer Speed",
  "Aggressive Speed",
  "Prefer Size",
  "Aggressive Size",
  "Prefer Debug",
  "Aggressive Debug"
]
Tag_ABI_FP_optimization_goals = [
  "None",
  "Prefer Speed",
  "Aggressive Speed",
  "Prefer Size",
  "Aggressive Size",
  "Prefer Accuracy",
  "Aggressive Accuracy"
]
Tag_CPU_unaligned_access = [
 "None",
 "v6"
]
Tag_FP_HP_extension = [
  "Not Allowed",
  "Allowed"
]
Tag_ABI_FP_16bit_format = [
  "None",
  "IEEE 754",
  "Alternative Format"
]
Tag_DSP_extension = [
  "Follow architecture",
  "Allowed"
]
Tag_MPextension_use = [
  "Not Allowed",
  "Allowed"
]
Tag_DIV_use = [
  "Allowed in Thumb-ISA",
  "v7-R or v7-M",
  "Not allowed",
  "Allowed in v7-A with integer division extension"
]
Tag_T2EE_use = [
 "Not Allowed"
 "Allowed"
]
Tag_Virtualization_use = [
  "Not Allowed",
  "TrustZone",
  "Virtualization Extensions",
  "TrustZone and Virtualization Extensions"
]
Tag_MPextension_use_legacy = [
  "Not Allowed",
  "Allowed"
]
Tag_MVE_arch = [
  "No MVE",
  "MVE Integer only",
  "MVE Integer and FP"
]
Tag_PAC_extension = [
  "No PAC/AUT instructions",
  "PAC/AUT instructions permitted in the NOP space",
  "PAC/AUT instructions permitted in the NOP and in the non-NOP space"
]
Tag_BTI_extension = [
  "BTI instructions not permitted",
  "BTI instructions permitted in the NOP space",
  "BTI instructions permitted in the NOP and in the non-NOP space"
]
Tag_BTI_use = [
  "Compiled without branch target enforcement",
  "Compiled with branch target enforcement"
]
Tag_PACRET_use = [
  "Compiled without return address signing and authentication",
  "Compiled with return address signing and authentication"
]
Tag_CPU_arch_profile = {
  "None": 0,
  "Application": 0x41,
  "Realtime": 0x52,
  "Microcontroller": 0x4D,
  "Application or Realtime": 0x53,
}
Tag_align_needed = [
  "None",
  "8-byte",
  "4-byte",
  "8-byte and up to 8-byte extended",
  "8-byte and up to 10-byte extended",
  "8-byte and up to 12-byte extended",
  "8-byte and up to 14-byte extended",
  "8-byte and up to 16-byte extended",
  "8-byte and up to 18-byte extended",
  "8-byte and up to 20-byte extended",
  "8-byte and up to 22-byte extended",
  "8-byte and up to 24-byte extended"
]
Tag_align_preserved = [
  "None",
  "8-byte, except leaf SP",
  "8-byte",
  "8-byte and up to 8-byte extended",
  "8-byte and up to 10-byte extended",
  "8-byte and up to 12-byte extended",
  "8-byte and up to 14-byte extended",
  "8-byte and up to 16-byte extended",
  "8-byte and up to 18-byte extended",
  "8-byte and up to 20-byte extended",
  "8-byte and up to 22-byte extended",
  "8-byte and up to 24-byte extended"
]

Tag_align_needed = [
  "None",
  "8-byte",
  "4-byte",
  "8-byte and up to 8-byte extended",
  "8-byte and up to 10-byte extended",
  "8-byte and up to 12-byte extended",
  "8-byte and up to 14-byte extended",
  "8-byte and up to 16-byte extended",
  "8-byte and up to 18-byte extended",
  "8-byte and up to 20-byte extended",
  "8-byte and up to 22-byte extended",
  "8-byte and up to 24-byte extended",
]
Tag_align_preserved = [
  "None",
  "8-byte, except leaf SP",
  "8-byte",
  "8-byte and up to 8-byte extended",
  "8-byte and up to 10-byte extended",
  "8-byte and up to 12-byte extended",
  "8-byte and up to 14-byte extended",
  "8-byte and up to 16-byte extended",
  "8-byte and up to 18-byte extended",
  "8-byte and up to 20-byte extended",
  "8-byte and up to 22-byte extended",
  "8-byte and up to 24-byte extended",
]
Tag_nodefaults=["<undefined>"]
Tag_FramePointer_use=["<undefined>"]
Tag_BTI_use=["<undefined>"]
Tag_PACRET_use=["<undefined>"]

Tags_Config = {
    "Tag_File": (1, "uint32", None),
    "Tag_Section": (2, "uint32", None),
    "Tag_Symbol": (3, "uint32", None),
    "Tag_CPU_raw_name": (4, "NTBS", None),
    "Tag_CPU_name": (5, "NTBS", None),
    "Tag_CPU_arch": (6, "uleb128", Tag_CPU_arch),
    "Tag_CPU_arch_profile": (7, "uleb128", Tag_CPU_arch_profile),
    "Tag_ARM_ISA_use": (8, "uleb128", Tag_ARM_ISA_use),
    "Tag_THUMB_ISA_use": (9, "uleb128", Tag_THUMB_ISA_use),
    "Tag_FP_arch": (10, "uleb128", Tag_FP_arch),
    "Tag_WMMX_arch": (11, "uleb128", Tag_WMMX_arch),
    "Tag_Advanced_SIMD_arch": (12, "uleb128", Tag_Advanced_SIMD_arch),
    "Tag_PCS_config": (13, "uleb128", Tag_PCS_config),
    "Tag_ABI_PCS_R9_use": (14, "uleb128", Tag_ABI_PCS_R9_use),
    "Tag_ABI_PCS_RW_data": (15, "uleb128", Tag_ABI_PCS_RW_data),
    "Tag_ABI_PCS_RO_data": (16, "uleb128", Tag_ABI_PCS_RO_data),
    "Tag_ABI_PCS_GOT_use": (17, "uleb128", Tag_ABI_PCS_GOT_use),
    "Tag_ABI_PCS_wchar_t": (18, "uleb128", Tag_ABI_PCS_wchar_t),
    "Tag_ABI_FP_rounding": (19, "uleb128", Tag_ABI_FP_rounding),
    "Tag_ABI_FP_denormal": (20, "uleb128", Tag_ABI_FP_denormal),
    "Tag_ABI_FP_exceptions": (21, "uleb128", Tag_ABI_FP_exceptions),
    "Tag_ABI_FP_user_exceptions": (22, "uleb128", Tag_ABI_FP_user_exceptions),
    "Tag_ABI_FP_number_model": (23, "uleb128", Tag_ABI_FP_number_model),
    "Tag_ABI_align_needed": (24, "uleb128", Tag_align_needed),
    "Tag_ABI_align_preserved": (25, "uleb128", Tag_align_preserved),
    "Tag_ABI_enum_size": (26, "uleb128", Tag_ABI_IntEnum_size),
    "Tag_ABI_HardFP_use": (27, "uleb128", Tag_ABI_HardFP_use),
    "Tag_ABI_VFP_args": (28, "uleb128", Tag_ABI_VFP_args),
    "Tag_ABI_WMMX_args": (29, "uleb128", Tag_ABI_WMMX_args),
    "Tag_ABI_optimization_goals": (30, "uleb128", Tag_ABI_optimization_goals),
    "Tag_ABI_FP_optimization_goals": (31, "uleb128", Tag_ABI_FP_optimization_goals),
    "Tag_compatibility": (32, "NTBS", None),
    "Tag_CPU_unaligned_access": (34, "uleb128", Tag_CPU_unaligned_access),
    "Tag_FP_HP_extension": (36, "uleb128", Tag_FP_HP_extension),
    "Tag_ABI_FP_16bit_format": (38, "uleb128", Tag_ABI_FP_16bit_format),
    "Tag_MPextension_use": (42, "uleb128", Tag_MPextension_use),
    "Tag_DIV_use": (44, "uleb128", Tag_DIV_use),
    "Tag_DSP_extension": (46, "uleb128", Tag_DSP_extension),
    "Tag_MVE_arch": (48, "uleb128", Tag_MVE_arch),
    "Tag_PAC_extension": (50, "uleb128", Tag_PAC_extension),
    "Tag_BTI_extension": (52, "uleb128", Tag_BTI_extension),
    "Tag_nodefaults": (64, "uleb128", Tag_nodefaults),
    "Tag_also_compatible_with": (65, "NTBS", None),
    "Tag_conformance": (67, "NTBS", None),
    "Tag_T2EE_use": (66, "uleb128", Tag_T2EE_use),
    "Tag_Virtualization_use": (68, "uleb128", Tag_Virtualization_use),
    "Tag_FramePointer_use": (72, "uleb128", Tag_FramePointer_use),
    "Tag_BTI_use": (74, "uleb128", Tag_BTI_use),
    "Tag_PACRET_use": (76, "uleb128", Tag_PACRET_use),
}

# TODO
# "Tag_FramePointer_use": (72),
# "Tag_BTI_use": (74),
# "Tag_PACRET_use": (76),
