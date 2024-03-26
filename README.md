# compare-eabi
compare-eabi helps comparing and interpreting ARM32 ABI Attributes from objects files.


## Usage Example

```bash
# show usage
> python3 compare-eabi.py --help

# run an example with previously generated text files from the examples/ folder.
> python3 compare-eabi.py --textfiles examples/cortex-*/* --diff

Tags with non-identical values (possibly conflicting)
------------------------------------------------------
...
target-related attribute types
------------------------------
Tag_ARM_ISA_use
| Yes                            |   0x1 | uleb128 | cortex-a8-simple.o.txt     |
| No (Default)                   |   0x0 | uleb128 | cortex-m-simple.o.         |
...

# explain attribute with arm_eabi_diagnostics
> python3 compare-eabi.py --explain Tag_ARM_ISA_use
```

## License

This project is licenced under MIT license, see [here](LICENSE). The only execption is the python module ``arm_eabi_diagnostics``, which contains text taken from the ["Addenda to the ABI for ARM" documentation](https://github.com/ARM-software/abi-aa/blob/fe46d4335d87e792991ceab9c8fd7b79f927a918/addenda32/addenda32.rst). This particular module is licensed under CC-BY-SA-4.0, see [here](arm_eabi_diagnostics/LICENSE).
