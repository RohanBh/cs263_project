## CS263 Project

### Setup
```bash
$ git clone https://github.com/RohanBh/cs263_project.git
$ cd cs263_project
$ conda env create -f conda_cs263.yml
$ conda activate conda_cs263
```
 
### Building and Running the benchmarks
We demonstrate the steps used for running the benchmarks `ml-mnist`. Other programs require similar steps. In the directory, `cs263_project/programs/ml-mnist`, we see the following files:
* `Profiling.md`: Contains information from Profiling the program and comparing performance of different variants and understanding it.
* Run `python <setup-script> build_ext --inplace` to compile Cython (using `setup_cython.py`) and Cython Typed (using `setup_cython_typed.py`) programs and create `.so` files.
* `profile_train.py`: Use this program to profile/time the training of a neural network with Numpy.
* Similarly, use `profile_train_cython.py` and `profile_train_cython_typed.py` for profiling Cython and Cython-Typed respectively.

The programs `profile_*.py` run the corresponding benchmark variant for 5 times and prints the execution time and the median time (in seconds).
