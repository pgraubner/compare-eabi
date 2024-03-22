# compare-eabi
compare-eabi helps interpreting ARM Attributes in objects file for the ARM32 ABI

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