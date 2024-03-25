# compare-eabi
compare-eabi helps comparing and interpreting ARM32 ABI Attributes from objects files.


## Usage Example

```bash
# show usage
> python3 compare-eabi.py --help

# run an example with previously generated text files from the examples/ folder.
> python3 compare-eabi.py --textfiles examples/cortex-m/* --diff

Tags with non-identical values (possibly conflicting)
------------------------------------------------------
...
procedure-call attribute types
------------------------------
Tag_ABI_PCS_GOT_use
| direct                         |   0x1 | uleb128 | librust_app.a.txt          |
| None (Default)                 |   0x0 | uleb128 | log_output.c.              |
...

# explain attribute with arm_eabi_diagnostics
> python3 compare-eabi.py --explain Tag_ABI_PCS_GOT_use

 Tag_ABI_PCS_GOT_use

Procedure call-related attribute describing compatibility with the ABI. Summarizes how the user intended the attributed entity to address static data.
       0  The user did not permit this entity to import static data
       1  The user permitted this entity to address imported data directly
       2  The user permitted this entity to address imported data indirectly (e.g. via a GOT)
```

## License

This project is licenced under MIT license, see [here](LICENSE). The only execption is the python module ``arm_eabi_diagnostics``, which contains text taken from the ["Addenda to the ABI for ARM" documentation](https://github.com/ARM-software/abi-aa/blob/fe46d4335d87e792991ceab9c8fd7b79f927a918/addenda32/addenda32.rst). This particular module is licensed under CC-BY-SA-4.0, see [here](arm_eabi_diagnostics/LICENSE).
