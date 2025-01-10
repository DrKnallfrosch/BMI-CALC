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
    pip install wxPython matplotlib
    ```

3. Run the application:
    ```bash
    python app.py
    ```

## Usage

### Main Interface

1. **Unit Selection**:
   - Choose between Metric (cm, kg) or Imperial (ft, lb) units using the radio box.

2. **Input Fields**:
   - Enter your size, weight, and optionally your age and sex.

3. **Results**:
   - BMI value, category, and ideal weight range are dynamically displayed.
   - A graphical scale highlights your BMI in the category chart.

### Additional Features

- Enable or disable age input using the checkbox.
- Adjust age using the spin box or slider.

## Code Overview

### Main Components

1. **`BMICalculatorApp`**:
   - The main application class that initializes the GUI.

2. **`BMIFrame`**:
   - Manages the GUI, including input fields, results, and event handling.

3. **`BmiCalc`**:
   - Backend class for BMI calculations and category determination.

### Key Methods

- `on_unit_change`: Handles unit conversions between Metric and Imperial systems.
- `update_results`: Updates the displayed BMI results, category, and ideal weight.
- `paint_scale`: Draws the BMI category scale using `matplotlib`.

## BMI Categories

The application uses the following BMI categories based on sex:

| Category              | Male BMI Range | Female BMI Range | Default BMI Range |
|-----------------------|----------------|------------------|-------------------|
| Underweight           | 0–20          | 0–19            | 0–18.5           |
| Normal weight         | 20–25         | 19–24           | 18.5–25          |
| Overweight            | 25–30         | 24–30           | 25–30            |
| Obesity I             | 30–35         | 30–35           | 30–35            |
| Obesity II            | 35–40         | 35–40           | 35–40            |
| Obesity III           | >40           | >40             | >40              |

## Contributing

1. Fork the repository.
2. Create a new branch:
    ```bash
    git checkout -b feature-name
    ```
3. Commit your changes:
    ```bash
    git commit -m "Description of changes"
    ```
4. Push to the branch:
    ```bash
    git push origin feature-name
    ```
5. Open a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

Feel free to contribute or report issues!
