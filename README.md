# compare-eabi
compare-eabi helps comparing and interpreting ARM32 ABI Attributes from objects files.

## Compatibility check between toolchains

Use case: Compatibility check between toolchains
```
                                    Rust modules
                                  +++++++++++++++
 C modules                        +    rustc    +
+++++++++++          BLOBs        +++++++++++++++
+   GCC   +    +++++++++++++++    +    LLVM     +
+++++++++++++++++++++++++++++++++++++++++++++++++
    static libs (.a files = set of .o files)
+++++++++++++++++++++++++++++++++++++++++++++++++
```
## License

This project is licenced under MIT license, see [here](LICENSE). The only execption is the python module ``arm_eabi_diagnostics``, which contains text taken from the ["Addenda to the ABI for ARM" documentation](https://github.com/ARM-software/abi-aa/blob/fe46d4335d87e792991ceab9c8fd7b79f927a918/addenda32/addenda32.rst). This particular module is licensed under CC-BY-SA-4.0, see [here](arm_eabi_diagnostics/LICENSE).
