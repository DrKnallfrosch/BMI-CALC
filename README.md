# BMI Calculator Application

A desktop application built using `wxPython` and `matplotlib` for calculating Body Mass Index (BMI). It allows users to input their size, weight, age, and sex to calculate their BMI and display the results in a user-friendly interface.

## Features

- Supports both Metric (cm, kg) and Imperial (ft, lb) units.
- Dynamic BMI result updates on input changes.
- Visual representation of BMI categories with a scale.
- Optional inclusion of age and sex to refine BMI category results.
- Displays ideal weight range based on age and BMI.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/bmi-calculator.git
    cd bmi-calculator
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    - Simply Run the BMI-Frame.py file

## Usage

### Main Interface

1. **Unit Selection**:
   - Choose between Metric (cm, kg) or Imperial (ft, lb) units using the radio box.

2. **Input Fields**:
   - Enter your size, weight, and optionally your age and sex.

3. **Results**:
   - BMI value, category, and ideal weight range are dynamically displayed.
   - A graphical scale highlights your BMI in the category chart.

## Code Overview

### Main Components

1. **`BMICalculatorApp`**:
   - The main application class that initializes the GUI.

2. **`BMIFrame`**:
   - Manages the GUI, including input fields, results, and event handling.

3. **`BmiCalc`**:
   - Backend class for BMI calculations and category determination.


Feel free to contribute or report issues!

© 2025 D0ms-0; DrKnallfrosch
