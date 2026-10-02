# OOP Concepts Used in the Project

## Class and Object

The application is divided into classes, each representing a logical part of the program.

- `BaseMotorTest` provides common motor-test functionality.
- `SwinburnesTest` handles Swinburne's Test.
- `LoadTest` implements common load-test logic.
- `SeriesMotorLoadTest` and `ShuntMotorLoadTest` specialize the load test.
- `MotorTestApp` controls the main graphical interface.

## Inheritance

Inheritance is used to reuse common functionality.

```python
class SwinburnesTest(BaseMotorTest):
    ...
```

```python
class LoadTest(BaseMotorTest):
    ...
```

```python
class SeriesMotorLoadTest(LoadTest):
    ...
```

```python
class ShuntMotorLoadTest(LoadTest):
    ...
```

The child classes automatically obtain useful methods from their parent classes.

## Encapsulation

The program groups related data and operations inside classes.

For example, the `LoadTest` class stores the entered values and provides methods to collect the input and calculate performance.

## Abstraction

The user only needs to interact with GUI controls such as buttons, text fields, and dialogs. Internal calculations for efficiency, torque, speed, output power, and losses are hidden behind class methods.

## Polymorphism / Specialization

`SeriesMotorLoadTest` and `ShuntMotorLoadTest` use the same load-test logic inherited from `LoadTest`, while each object represents a different motor type.

The application can therefore work with related objects through a common design while producing motor-specific labels and outputs.

## Constructor Use

Constructors initialize objects when they are created.

Example:

```python
def __init__(self, root, motor_type):
    super().__init__(root)
    self.motor_type = motor_type
    self.entries = []
```

`super().__init__(root)` calls the constructor of the parent class.

## Reusability

The base class contains methods that are useful to several motor tests:

- `get_motor_life_inference()`
- `plot_graph()`
- `save_results_to_file()`
- `load_results_from_file()`

This reduces duplicated code and makes the program easier to maintain.
