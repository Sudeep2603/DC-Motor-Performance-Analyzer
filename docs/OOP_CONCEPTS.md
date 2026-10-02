# OOP Concepts Used in the Project

This project applies Object-Oriented Programming concepts to organize the DC Motor Performance Analyzer into reusable and maintainable components.

The application contains different classes for common motor-test operations, Swinburne's Test, load testing, and the graphical user interface.

---

## 1. Classes and Objects

A class is a blueprint used to define related data and functions, while an object is an instance of a class.

The major classes used in this project are:

- `BaseMotorTest`
- `SwinburnesTest`
- `LoadTest`
- `SeriesMotorLoadTest`
- `ShuntMotorLoadTest`
- `MotorTestApp`

Each class has a specific responsibility.

### `BaseMotorTest`

This is the base class containing common functionality required by different motor tests.

It provides methods for:

- Plotting graphs
- Saving calculated results
- Loading saved results
- Generating machine-life insights

### `SwinburnesTest`

This class handles Swinburne's Test.

It allows the user to select:

- Motor operation
- Generator operation

It then performs the corresponding calculations and plots the results.

### `LoadTest`

This class contains the common logic required for performing load tests.

It handles:

- Input collection
- Torque calculation
- Input power calculation
- Output power calculation
- Efficiency calculation
- Graph plotting

### `SeriesMotorLoadTest`

This class represents the load test for a DC Series Motor.

### `ShuntMotorLoadTest`

This class represents the load test for a DC Shunt Motor.

### `MotorTestApp`

This class controls the main graphical user interface of the application.

It creates the main window and allows the user to select the required experiment.

---

## 2. Inheritance

Inheritance allows one class to reuse the properties and methods of another class.

The project uses the following inheritance structure:

```text
BaseMotorTest
├── SwinburnesTest
└── LoadTest
    ├── SeriesMotorLoadTest
    └── ShuntMotorLoadTest
```

For example:

```python
class SwinburnesTest(BaseMotorTest):
    ...
```

and:

```python
class LoadTest(BaseMotorTest):
    ...
```

Both classes inherit common functions such as graph plotting and file handling from `BaseMotorTest`.

Similarly:

```python
class SeriesMotorLoadTest(LoadTest):
    ...
```

and:

```python
class ShuntMotorLoadTest(LoadTest):
    ...
```

inherit the common load-test functionality from `LoadTest`.

This reduces repeated code.

---

## 3. Encapsulation

Encapsulation means grouping related data and operations inside a class.

For example, the `LoadTest` class contains:

- Input fields
- Motor type
- Input-reading logic
- Calculation methods
- Graph generation

This keeps the variables and functions related to a load test together.

Similarly, `SwinburnesTest` contains the functions specifically required for Swinburne's Test.

This improves code organization and maintainability.

---

## 4. Abstraction

Abstraction hides unnecessary implementation details from the user.

The user does not need to know the mathematical implementation inside the program.

The user simply:

1. Selects an experiment
2. Enters the required values
3. Clicks **Calculate & Plot**
4. Views the results

Internally, the program performs calculations for:

- Input power
- Output power
- Copper loss
- Efficiency
- Speed
- Torque
- Machine-life inference

The calculations are therefore hidden behind the graphical interface and class methods.

---

## 5. Polymorphism and Specialization

The DC Series Motor and DC Shunt Motor load-test classes both use the common functionality of `LoadTest`.

However, each class represents a different motor type.

For example:

```python
class SeriesMotorLoadTest(LoadTest):
    def __init__(self, root):
        super().__init__(root, "DC Series")
```

and:

```python
class ShuntMotorLoadTest(LoadTest):
    def __init__(self, root):
        super().__init__(root, "DC Shunt")
```

Both classes use the same load-test implementation while providing different motor-type information.

This demonstrates specialization through inheritance.

---

## 6. Constructors

Constructors are used to initialize objects when they are created.

For example:

```python
def __init__(self, root, motor_type):
    super().__init__(root)
    self.motor_type = motor_type
    self.entries = []
```

Here:

```python
super().__init__(root)
```

calls the constructor of the parent class.

The constructor also initializes variables required by the object.

---

## 7. Method Reusability

The project uses reusable methods to avoid repeating code.

Important reusable methods include:

```python
plot_graph()
save_results_to_file()
load_results_from_file()
get_motor_life_inference()
```

These functions are defined in `BaseMotorTest` and can be used by the child classes.

For example, both Swinburne's Test and load tests use the same graph plotting method.

---

## 8. Object Creation

Objects are created when the user selects an experiment.

For example:

```python
test = SwinburnesTest(self.root)
```

creates an object for Swinburne's Test.

Similarly:

```python
test = SeriesMotorLoadTest(self.root)
```

creates an object for the DC Series Motor load test.

and:

```python
test = ShuntMotorLoadTest(self.root)
```

creates an object for the DC Shunt Motor load test.

---

## 9. Benefits of Using OOP in This Project

Using Object-Oriented Programming provides several advantages:

- Reduces code duplication
- Improves code organization
- Makes the application easier to modify
- Allows new motor tests to be added more easily
- Improves maintainability
- Encourages reusable functions and classes
- Separates GUI logic from motor-test functionality

---

## Summary

The major OOP concepts demonstrated in this project are:

- Classes
- Objects
- Inheritance
- Encapsulation
- Abstraction
- Specialization
- Constructors
- Method reusability

The use of these concepts allows the DC Motor Performance Analyzer to remain organized, reusable, and easier to extend.
