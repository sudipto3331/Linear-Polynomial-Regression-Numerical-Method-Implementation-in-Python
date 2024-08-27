# Linear Polynomial Regression Numerical Method Implementation in Python

This repository contains a Python implementation of Linear Polynomial Regression for fitting a polynomial to a set of data points using the Gauss-Seidel method for solving the system of linear equations. The code reads data from an Excel file (`Regression.xls`), performs polynomial regression, and plots the original data points along with the fitted polynomial curve.

## Table of Contents
- [Linear Polynomial Regression Theory](#linear-polynomial-regression-theory)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)
- [Code Explanation](#code-explanation)
- [Example](#example)
- [Files in the Repository](#files-in-the-repository)
- [Input Parameters](#input-parameters)
- [Troubleshooting](#troubleshooting)
- [Author](#author)

## Linear Polynomial Regression Theory
Linear Polynomial Regression is a form of regression analysis where the relationship between the independent variable \( x \) and the dependent variable \( y \) is modeled as an \( m \)-degree polynomial. The Gauss-Seidel method is an iterative technique used to solve the system of equations derived from the normal equations of the regression problem.

**Steps:**
1. Formulate the normal equations from the polynomial regression problem.
2. Use the Gauss-Seidel method to iteratively solve the system of linear equations.
3. Obtain the polynomial coefficients and plot the regression curve.

## Dependencies
To run this code, you need the following libraries:
- `numpy`
- `xlrd`
- `matplotlib`

## Installation
To install the required libraries, you can use `pip`:
```sh
pip install numpy xlrd matplotlib
```

## Usage
1. Clone the repository.
2. Ensure the script and the Excel file (`Regression.xls`) are in the same directory.
3. Run the script using Python:
    ```sh
    python polynomial_regression.py
    ```
4. Provide the required input when prompted:
    - Enter the order of the regression polynomial.

## Code Explanation
The code begins by importing the necessary libraries and defining the Gauss-Seidel function for solving systems of linear equations. It reads the data points from the Excel file and constructs the normal equations for the polynomial regression problem. The Gauss-Seidel method is used to solve for the polynomial coefficients, which are then used to compute the fitted values. The original data points and the fitted polynomial curve are plotted.

Below is a snippet from the code illustrating the main logic:

```python
import numpy as np
import xlrd
from matplotlib import pyplot as plt

def brcond_Seidel(E, err, n):
    a = 0
    for i in range(n):
        if E[i] < err:
            a += 1
    return a / n

def Gauss_Seidel(a):
    err = 10**-15         # Assumed percentage relative error
    ite = 10**4          # Assumed number of iterations
    
    n = np.shape(a)[0]
    E = np.zeros([n])
    rel_err = np.zeros([ite, n])
    X = np.zeros([n])
    x = np.zeros([ite, n])
    itern = np.zeros([ite])
    p = np.zeros([n])
    
    for j in range(ite):
        itern[j] = j + 1
        for i in range(n):
            summation = 0
            for k in range(n):
                if k != i:
                    summation += a[i, k] * x[j, k]
            x[j, i] = (a[i, n] - summation) / a[i, i]
            if j > 0:
                rel_err[j, i] = abs((x[j, i] - x[j-1, i]) / x[j, i]) * 100
                E[i] = rel_err[j, i]
        if j > 0 and brcond_Seidel(E, err, n) == 1:
            break
        if j == ite - 1:
            break
        x[j+1, :] = x[j, :]
    
    X = x[j, :]
    
    # Result Verification    
    for i in range(n):
        summation = 0
        for j in range(n):
            summation += a[i, j] * X[j]
        p[i] = summation - a[i, j+1]
    
    return X, p

m = int(input('Enter the order of the regression polynomial: '))

# Reading data from excel file
loc = ('Regression.xls')
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(3)

N = sheet.ncols - 1
x = np.zeros([N])
y = np.zeros([N])
Y = np.zeros([N])
a = np.zeros([m+1, m+2])

# Creating matrix from the data 
for i in range(1, sheet.ncols):
    x[i-1] = sheet.cell_value(0, i)
    y[i-1] = sheet.cell_value(1, i)

for p in range(m+1):
    for q in range(m+2):
        if p == 0 and q == 0:
            a[p, q] = N
        elif p == 0:
            a[p, q] = sum(x**q)
        elif q < m+1:
            a[p, q] = sum(x**(q+p))
        else:
            a[p, q] = sum((x**p) * y)

X, p = Gauss_Seidel(a)

for Z in range(N):
    addition = 0
    for v in range(m+1):
        addition += X[v] * x[Z]**v
    Y[Z] = addition

plt.figure(1)
plt.plot(x, y, 'o')
plt.plot(x, Y)
plt.xlabel('Values of x')
plt.ylabel('Values of y')
plt.title('Curve fitting using polynomial regression')
plt.legend(['Measured', 'Estimated'], loc='upper left')
plt.show()
```

The code completes by plotting the original data points and the fitted polynomial curve using `matplotlib`.

## Example
Below is an example of how to use the script:

1. Prepare the `Regression.xls` file with the data points in two rows: the first row for \( x \)-values and the second row for \( y \)-values.
2. **Run the script**:
    ```sh
    python polynomial_regression.py
    ```

3. **Enter the input value**:
    ```
    Enter the order of the regression polynomial: 2
    ```

4. **Output**:
    - The script will compute the polynomial regression and plot the original data points along with the fitted polynomial curve.

## Files in the Repository
- `polynomial_regression.py`: The main script for performing polynomial regression.
- `Regression.xls`: Excel file from which the data points are read.

## Input Parameters
The initial input data is expected to be in the form of two rows within the `Regression.xls` file:
- First row: \( x \)-values
- Second row: \( y \)-values

## Troubleshooting
1. **Excel File**: Ensure that the input data is correctly formatted and placed in the `Regression.xls` file.
2. **Order of Polynomial**: The order of the polynomial should be a non-negative integer and less than the number of data points.
3. **Python Version**: This script is compatible with Python 3. Ensure you have Python 3 installed.

## Author
Script created by Sudipto.

---

This documentation should guide you through understanding, installing, and using the polynomial regression script. For further issues or feature requests, please open an issue in the repository on GitHub. Feel free to contribute by creating issues and submitting pull requests. Happy coding!
