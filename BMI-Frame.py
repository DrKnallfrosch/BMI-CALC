import wx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from BmiCalc import BmiCalc


class BMICalculatorApp(wx.App):
    """
    Main application class for the BMI calculator.

    This class initializes the BMI calculator frame and runs the application.

    Methods
    -------
    OnInit() -> bool
        Initializes the application and shows the main frame.
    """
    def OnInit(self):
        """
        Initializes the main frame of the application.

        :return: True if initialization is successful, False otherwise.
        :rtype: bool
        """
        self.frame = BMIFrame(None, title="Calculator")
        self.frame.Show()
        return True


class BMIFrame(wx.Frame):
    """
    Main frame of the BMI calculator application.

    This class creates and manages the GUI components for the BMI calculator,
    including input fields for size, weight, age, sex, and options for unit system.
    It connects to the backend for BMI calculation and updates the displayed results.

    Attributes
    ----------
    backend: BmiCalc
        The backend object used for BMI calculations and category retrieval.
    unit: str
        The unit system being used for input ('m' for metric, 'i' for imperial).

    Methods
    -------
    __init__(self, *args, **kwargs)
        Initializes the BMI frame and sets up all necessary controls.
    on_unit_change(self, event)
        Updates the unit system (metric/imperial) and adjusts the input fields accordingly.
    on_size_change(self, event)
        Handles the change in size input and updates the backend.
    on_weight_change(self, event)
        Handles the change in weight input and updates the backend.
    on_sex_change(self, event)
        Handles the change in sex selection and updates the backend.
    on_age_checkbox(self, event)
        Toggles the age input fields (spin control and slider) and updates the backend accordingly.
    on_age_spin_change(self, event)
        Handles the change in the age spin control and updates the backend.
    on_age_slider_change(self, event)
        Handles the change in the age slider and updates the backend.
    on_enter(self, event)
        Updates the BMI results when the user presses the Enter key.
    update_results(self)
        Updates the displayed BMI results and categories based on the current input.
    paint_scale(self)
        Draws the BMI category scale on the result panel.
    """
    def __init__(self, *args, **kwargs):
        """
        Initializes the BMI frame and sets up all necessary controls.

        :param args: Additional positional arguments passed to the frame initialization.
        :param kwargs: Additional keyword arguments passed to the frame initialization.
        """
        super().__init__(*args, **kwargs, size=(756, 319))
        self.SetSizeHints(self.GetSize(), self.GetSize())
        self._backend = BmiCalc(1.80, 70) # Connection to backend
        self._unit = "m"

        # Constants to assign flags and styles to multiple similar widgets
        standard_flags = wx.EXPAND | wx.ALIGN_CENTRE | wx.ALL
        unit_flags = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_LEFT
        label_flags = wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT | wx.LEFT
        spin_styles = wx.ALIGN_RIGHT | wx.TE_PROCESS_ENTER | wx.SP_ARROW_KEYS

        self.panel = wx.Panel(self)
        main_box_sizer = wx.BoxSizer(wx.HORIZONTAL)


        ### Control Panel ###
        self.control_panel = wx.Panel(self.panel)
        grid_sizer = wx.GridBagSizer()

        # Labels; Don't need to be referenced
        grid_sizer.Add(wx.StaticText(self.control_panel, label="Größe:"), pos=(1, 0), flag=label_flags, border=10)
        grid_sizer.Add(wx.StaticText(self.control_panel, label="Gewicht:"), pos=(2, 0), flag=label_flags, border=10)
        grid_sizer.Add(wx.StaticText(self.control_panel, label="Geschlecht:"), pos=(3, 0), flag=label_flags, border=10)
        grid_sizer.Add(wx.StaticText(self.control_panel, label="Alter:"), pos=(4, 0), flag=label_flags, border=10)

        # Unit Texts; Need to be referenced
        self.size_unit_label = wx.StaticText(self.control_panel, label="cm")
        self.weight_unit_label = wx.StaticText(self.control_panel, label="kg")
        grid_sizer.Add(self.size_unit_label, pos=(1, 2), flag=unit_flags)
        grid_sizer.Add(self.weight_unit_label, pos=(2, 2), flag=unit_flags)

        # RadioBox to change the currently used unit system
        self.unit_radiobox = wx.RadioBox(self.control_panel, label="Einheit", choices=("Metrisch", "Imperial"))
        self.unit_radiobox.SetMinSize((250, 50))
        self.unit_radiobox.Bind(wx.EVT_RADIOBOX, self.on_unit_change)
        grid_sizer.Add(self.unit_radiobox, pos=(0, 0), span=(1, 3), flag=standard_flags, border=10)

        # Input Boxes for required values
        self.size_spin = wx.SpinCtrlDouble(self.control_panel, min=1, max=999, initial=180, style=spin_styles)
        self.weight_spin = wx.SpinCtrlDouble(self.control_panel, min=30, max=999, initial=70, style=spin_styles)
        self.size_spin.SetDigits(1)
        self.weight_spin.SetDigits(1)
        self.size_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_size_change)
        self.weight_spin.Bind(wx.EVT_SPINCTRLDOUBLE, self.on_weight_change)
        grid_sizer.Add(self.size_spin, pos=(1, 1), flag=wx.EXPAND | wx.ALL, border=5)
        grid_sizer.Add(self.weight_spin, pos=(2, 1), flag=wx.EXPAND | wx.ALL, border=5)

        # Optional Dropdown for specifying sex
        self.sex_combobox = wx.ComboBox(self.control_panel, size=(110, 24), value="Keine Angabe",
                                        choices=("Keine Angabe", "Männlich", "Weiblich"), style=wx.CB_READONLY)
        self.sex_combobox.Bind(wx.EVT_COMBOBOX, self.on_sex_change)
        grid_sizer.Add(self.sex_combobox, pos=(3, 1), flag=standard_flags, border=5)

        # Input Box and Slider for changing age value; CheckBox to enable / disable calculation with age
        self.age_spin = wx.SpinCtrl(self.control_panel, min=19, max=99, style=spin_styles)
        self.age_spin.Bind(wx.EVT_SPINCTRL, self.on_age_spin_change)
        grid_sizer.Add(self.age_spin, pos=(4, 1), flag=wx.EXPAND | wx.ALL, border=5)
        self.age_spin.Disable()

        self.age_checkbox = wx.CheckBox(self.control_panel)
        self.age_checkbox.Bind(wx.EVT_CHECKBOX, self.on_age_checkbox)
        grid_sizer.Add(self.age_checkbox, pos=(4, 2), flag=wx.EXPAND | wx.ALL, border=5)

        self.age_slider = wx.Slider(self.control_panel, minValue=19, maxValue=99, style=wx.SL_HORIZONTAL)
        self.age_slider.Bind(wx.EVT_SLIDER, self.on_age_slider_change)
        grid_sizer.Add(self.age_slider, pos=(5, 0), span=(1, 3), flag=wx.LEFT | wx.RIGHT | wx.EXPAND, border=10)
        self.age_slider.Disable()

        # Texts to allow Strings to be used in slider labels
        labels_sizer = wx.BoxSizer(wx.HORIZONTAL)
        labels_sizer.Add(wx.StaticText(self.control_panel, label="19", style=wx.ALIGN_CENTER), flag=wx.LEFT, border=5)
        labels_sizer.AddStretchSpacer(1)
        labels_sizer.Add(wx.StaticText(self.control_panel, label="99+", style=wx.ALIGN_CENTRE), flag=wx.RIGHT, border=10)
        grid_sizer.Add(labels_sizer, pos=(6, 0), span=(1, 3), flag=wx.EXPAND)


        self.control_panel.SetSizer(grid_sizer)
        main_box_sizer.Add(self.control_panel, flag=wx.EXPAND | wx.ALL, border=5)


        # Static Line Divider
        main_box_sizer.Add(wx.StaticLine(self.panel, style=wx.LI_VERTICAL), flag=wx.EXPAND | wx.ALL, border=25)


        ### Result Panel ###
        self.result_panel = wx.Panel(self.panel)
        result_box_sizer = wx.BoxSizer(wx.VERTICAL)

        result_box_sizer.Add(wx.StaticText(self.result_panel), flag=wx.EXPAND) # Spacer

        # Title text
        headline_text = wx.StaticText(self.result_panel, label="Ihr BMI Ergebnis")
        headline_text.SetForegroundColour(wx.Colour(10, 110, 210))
        headline_text.SetFont(wx.Font(18, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_box_sizer.Add(headline_text, flag=wx.ALIGN_CENTRE | wx.ALL, border=5)

        # Label for BMI-Value
        result_header = wx.StaticText(self.result_panel, label="Body-Mass-Index:")
        result_header.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_box_sizer.Add(result_header, flag=wx.ALIGN_CENTRE | wx.ALL, border=5)

        # Displays BMI-Value
        self.result_value = wx.StaticText(self.result_panel, label=f"{self._backend.get_bmi():.1f}")
        self.result_value.SetFont(wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_box_sizer.Add(self.result_value, flag=wx.ALIGN_CENTRE)

        self.figure, self.ax = plt.subplots(figsize=(4, 1))
        self.figure.set_facecolor("#f0f0f0")
        self.canvas = FigureCanvas(self.result_panel, -1, self.figure)
        self.paint_scale()
        result_box_sizer.Add(self.canvas)

        # Label and Display for Category
        self.category_label = wx.StaticText(self.result_panel, label=f"Kategorie: {self._backend.get_category()}")
        self.category_label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_box_sizer.Add(self.category_label, flag=wx.ALIGN_CENTRE | wx.ALL, border=5)

        # Label and Display for Ideal Weight
        self.ideal_weight_label = wx.StaticText(self.result_panel, label=f"Ideales Gewicht: {self._backend.get_ideal_weight():.1f} kg")
        self.ideal_weight_label.SetFont(wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        result_box_sizer.Add(self.ideal_weight_label, flag=wx.ALIGN_CENTRE | wx.ALL, border=5)

        self.result_panel.SetSizer(result_box_sizer)
        main_box_sizer.Add(self.result_panel, flag=wx.EXPAND | wx.ALL, border=5)


        self.panel.SetSizer(main_box_sizer)
        self.Layout()
        self.Centre(wx.BOTH)

        self.update_results()
        self.Refresh()

    def on_unit_change(self, event):
        """
        Handles the change of unit selection in the radiobox.

        :param event: The event triggered by the unit selection change.
        :type event: wx.Event
        """
        if self.unit_radiobox.GetSelection() == 0:
            self.size_unit_label.SetLabel("cm")
            self.weight_unit_label.SetLabel("kg")
            self.size_spin.SetDigits(1)
            self.size_spin.SetValue(self._backend.get_size() * 100)
            self.weight_spin.SetValue(self._backend.get_weight())
            self._unit = "m"
        elif self.unit_radiobox.GetSelection() == 1:
            self.size_unit_label.SetLabel("ft")
            self.weight_unit_label.SetLabel("lb")
            self.size_spin.SetDigits(3)
            self.size_spin.SetValue(self._backend.get_size() * 3.280)
            self.weight_spin.SetValue(self._backend.get_weight() * 2.205)
            self._unit = "i"
        self.update_results()

    def on_size_change(self, event):
        """
        Handles the change of size input (either in cm or ft) and updates the backend.

        :param event: The event triggered by the size input change.
        :type event: wx.Event
        """
        if self._unit == "m":
            self._backend.set_size(self.size_spin.GetValue() / 100)
        elif self._unit == "i":
            self._backend.set_size(self.size_spin.GetValue() * 0.3048)
        self.update_results()

    def on_weight_change(self, event):
        """
        Handles the change of weight input (either in kg or lb) and updates the backend.

        :param event: The event triggered by the weight input change.
        :type event: wx.Event
        """
        if self._unit == "m":
            self._backend.set_weight(self.weight_spin.GetValue())
        elif self._unit == "i":
            self._backend.set_weight(self.weight_spin.GetValue() / 2.205)
        self.update_results()

    def on_sex_change(self, event):
        """
        Handles the change of sex selection in the combobox.

        :param event: The event triggered by the sex selection change.
        :type event: wx.Event
        """
        if self.sex_combobox.GetValue() == "Männlich":
            self._backend.set_sex("m")
        elif self.sex_combobox.GetValue() == "Weiblich":
            self._backend.set_sex("f")
        elif self.sex_combobox.GetValue() == "Keine Angabe":
            self._backend.set_sex(None)
        self.update_results()

    def on_age_checkbox(self, event):
        """
        Handles the toggling of the age checkbox. Enables or disables age inputs accordingly.
        Modifies the states of both age_spin and age_slider.

        :param event: The event triggered by the checkbox state change.
        :type event: wx.Event
        """
        if self.age_checkbox.IsChecked():
            self.age_spin.Enable()
            self.age_slider.Enable()
            self._backend.set_age(self.age_spin.GetValue())
        else:
            self.age_spin.Disable()
            self.age_slider.Disable()
            self._backend.set_age(None)
        self.update_results()

    def on_age_spin_change(self, event):
        """
        Handles the change of the age spin input and updates the backend.
        Synced with the age_slider Slider-Object

        :param event: The event triggered by the age spin input change.
        :type event: wx.Event
        """
        self.age_slider.SetValue(self.age_spin.GetValue())
        self._backend.set_age(self.age_spin.GetValue())
        self.update_results()

    def on_age_slider_change(self, event):
        """
        Handles the change of the age slider input and updates the backend.
        Synced with the age_spin SpinCtrl-Object.

        :param event: The event triggered by the age slider input change.
        :type event: wx.Event
        """
        self.age_spin.SetValue(self.age_slider.GetValue())
        self._backend.set_age(self.age_slider.GetValue())
        self.update_results()


    def update_results(self):
        """
        Updates the results displayed based on the current input values.
        Gets called on every change.

        :return: None
        """
        self.result_value.SetLabel(str(f"{self._backend.get_bmi():.1f}"))
        self.category_label.SetLabel(f"Katgorie: {self._backend.get_category()}")
        if self._unit == "m":
            self.ideal_weight_label.SetLabel(f"Ideales Gewicht: {self._backend.get_ideal_weight():.1f} kg")
        elif self._unit == "i":
            self.ideal_weight_label.SetLabel(f"Ideales Gewicht: {(self._backend.get_ideal_weight() * 2.205):.1f} lb")

        self.paint_scale()

    def paint_scale(self):
        """
        Uses matplotlib objects in order to draw a BMI scale on the canvas.
        Assigns each weight category to a color:

        1st orange: Underweight
        green : Normal weight
        2nd orange: Overweight
        red: Obesity (all types)

        Also creates a black bar that indicates the currently calculated BMI-Value.

        :return: None
        """
        self.figure.set_facecolor("#f0f0f0")
        self.ax.cla()
        self.ax.set_xlim(15, 35)
        self.ax.set_ylim(0, 1)
        self.ax.set_xticks(range(15, 36, 5))
        self.ax.set_yticks([])
        categories = self._backend.category.get(self._backend.get_sex(), self._backend.category[None])
        for (lower, upper), category in categories.items():
            match category:
                case "Untergewicht":
                    color = (1.0, 0.6, 0.15)
                case "Normalgewicht":
                    color = (0.08, 0.8, 0.5)
                case "Übergewicht":
                    color = (1.0, 0.6, 0.15)
                case "Adipositas Grad I" | "Adipositas Grad II" | "Adipositas Grad III":
                    color = (0.98, 0.22, 0.15)
            try:
                self.ax.barh(0.5, upper - lower, left=lower, color=color, height=0.8)
            except NameError:
                pass

        self.ax.set_ylim(0, 1)
        self.ax.set_aspect(1.0)
        self.ax.vlines(self._backend.get_bmi(), 0.1, 0.9, color='black', linewidth=3)
        self.canvas.draw()


if __name__ == "__main__":
    app = BMICalculatorApp()
    app.MainLoop()