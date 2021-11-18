* Python 'range' for loops are converted to C loops only when all variables (in the loop) and the sign of the step size is known at compile-time. Unfortunately if using a variable (even though it is typed) as a step-size, the sign can not be determined statically and the loop incurs some type-checking overheads. We can see the difference this overhead makes in `sieve_of_eratosthenes_cython_typed.pyx`:
```
# Unoptimized loop
Times: [0.1946296668611467, 0.16565347998403013, 0.15952699701301754, 0.15945811895653605, 0.15964443096891046]
Median: 0.15964443096891046
# After converting to C-loop
Times: [0.09256194299086928, 0.0762948680203408, 0.0704366760328412, 0.0706046090926975, 0.07054292690008879]
Median: 0.0706046090926975
```
Clearly, a 2x speedup is visible

We could also see that even though the variables `j` and `i` are typed, Cython performs unnecessary conversions:
```
 __pyx_t_2 = __Pyx_PyInt_From_long((2 * __pyx_v_i)); if (unlikely(!__pyx_t_2)) __PYX_ERR(0, 17, __pyx_L1_error)
__Pyx_GOTREF(__pyx_t_2);
__pyx_t_3 = __Pyx_PyInt_From_long((__pyx_v_n + 1)); if (unlikely(!__pyx_t_3)) __PYX_ERR(0, 17, __pyx_L1_error)
__Pyx_GOTREF(__pyx_t_3);
__pyx_t_6 = __Pyx_PyInt_From_int(__pyx_v_i); if (unlikely(!__pyx_t_6)) __PYX_ERR(0, 17, __pyx_L1_error)
__Pyx_GOTREF(__pyx_t_6);
```
TODO: Dig more deep into what the compiled code is doing for 'for loop'