# Simplex Method Python Implementation

## Overview

This project is a Python implementation of the Interior Point algorithm, a popular algorithm for numerical solution of Linear Programming problems. The Interior Point Algorithm is used for optimizing a linear objective function, subject to linear equality and linear inequality constraints.

## Requirements

- Python 3.x

## Usage

### Define the Linear Programming Problem

The Linear Programming Problem should be of the form:

```
Maximize c.T * x
subject to:
Ax <= b
x >= 0
```

Where:
- `c` is the coefficients of the objective function.
- `A` is the coefficients matrix of the constraints.
- `b` is the right-hand side of the constraints.
- `x` is the vector of variables to be determined.
- `eps` is the approximation accuracy.

### How to Run

1. Define the Linear Programming Problem in the main section of the script, `c`, `A`, `b` and `eps`.
2. Run the `interior_point` function with arguments `c`, `A`, `b` and `eps`.


## Example

Below is a simple example problem:

```python
if __name__ == '__main__':
    c = [1, 2, 0]
    A = [
        [1, 1, 1],
    ]
    b = [8]
    eps = 1e-3
    solution = interior_point(c, A, b, eps)
    print(f"Optimal Solution: {solution}")
```


## Features

- The program finds the initial feasible solution if it is exist.
- Displays the gradiented solution in every iteration.
- Shows the final optimal solution of the objective function.
