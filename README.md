# DC Motor Performance Analyzer

A Python-based GUI application for analyzing the performance of DC machines using **Swinburne's Test** and **load tests on DC Series and DC Shunt motors**.

This project was developed as an **Object-Oriented Programming (OOP)** application and demonstrates inheritance, encapsulation, abstraction, code reusability, GUI programming, numerical computation, plotting, and file handling.

---

## Features

- Graphical user interface using Tkinter
- Swinburne's Test
  - Motor operation
  - Generator operation
- Load test on DC Series Motor
- Load test on DC Shunt Motor
- Calculates:
  - Efficiency
  - Output Power
  - Speed
  - Torque
  - Line / Load Current
- Generates performance-characteristic graphs
- Provides qualitative machine-life insights
- Detects operation above rated current
- Saves calculated results as CSV files
- Loads previously saved CSV files
- Re-plots stored test results

---

## OOP Concepts Used

### 1. Classes and Objects

The application is organized using multiple classes:

- `BaseMotorTest`
- `SwinburnesTest`
- `LoadTest`
- `SeriesMotorLoadTest`
- `ShuntMotorLoadTest`
- `MotorTestApp`

Objects of these classes are created to perform the required motor tests and manage the GUI application.

---

### 2. Inheritance

Inheritance is used extensively to avoid code duplication.

`SwinburnesTest` and `LoadTest` inherit common functionality from:

```python
BaseMotorTest
