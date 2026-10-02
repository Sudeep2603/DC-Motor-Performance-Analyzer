# Usage Guide

## 1. Start the Application

Run:

```bash
python src/motor_performance_analyzer.py
```

The **Motor Performance Analyzer** main window opens.

## 2. Select an Experiment

The program provides:

- Swinburne's Test
- Load Test on DC Series Motor
- Load Test on DC Shunt Motor

## 3. Swinburne's Test

Choose either:

- Motor Operation
- Generator Operation

Enter:

- Supply Voltage
- Field Current
- No-Load Line Current
- Armature Resistance
- Rated Line Current
- Rated Speed

The program calculates the required performance values and displays a graph.

## 4. Load Test

Select either DC Series or DC Shunt motor.

Enter the number of readings, then provide:

- Brake Drum Radius
- Rated Current
- Voltage
- Current
- Spring-balance reading S1
- Spring-balance reading S2
- Speed

The program calculates torque, input/output power, efficiency, and related performance characteristics.

## 5. Save Results

After calculation, the application asks whether the result should be saved.

Choose **Yes** and select a location. The result is stored as a CSV file.

## 6. Load Previous Results

Use:

**File → Load Saved Data**

Select a previously generated CSV file. The program reads the data and plots it.

## 7. Adding GitHub Screenshots

Take screenshots of:

- Main application window
- Input window
- Performance graph
- Machine-life inference
- Saved CSV output

Store them inside:

```text
images/output/
```

Recommended filenames:

```text
main_window.png
input_window.png
performance_graph.png
machine_life_inference.png
saved_csv.png
```
