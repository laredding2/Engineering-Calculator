"""
Engineering Calculator
A professional-grade engineering calculator with PyQt6 GUI.
Supports standard arithmetic, scientific functions, unit conversions,
and common engineering calculations.
"""

import sys
import math
import cmath
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QPushButton, QLineEdit, QLabel, QTabWidget,
    QComboBox, QDoubleSpinBox, QFrame, QSizePolicy, QScrollArea
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette, QFontDatabase, QIcon

# ─────────────────────────────────────────────
#  Colour palette
# ─────────────────────────────────────────────
BG          = "#0d1117"
PANEL       = "#161b22"
SURFACE     = "#21262d"
BORDER      = "#30363d"
ACCENT      = "#58a6ff"
ACCENT2     = "#3fb950"
ACCENT3     = "#f78166"
ACCENT4     = "#d2a8ff"
TEXT        = "#e6edf3"
TEXT_DIM    = "#8b949e"
BTN_NUM     = "#21262d"
BTN_OP      = "#1f3a5f"
BTN_FN      = "#1a2e1a"
BTN_SPEC    = "#3a1f1f"
BTN_HOVER   = "#30363d"

STYLESHEET = f"""
QMainWindow, QWidget {{
    background-color: {BG};
    color: {TEXT};
    font-family: 'Consolas', 'Courier New', monospace;
}}

QTabWidget::pane {{
    border: 1px solid {BORDER};
    border-radius: 6px;
    background: {PANEL};
}}

QTabBar::tab {{
    background: {SURFACE};
    color: {TEXT_DIM};
    padding: 8px 20px;
    border: 1px solid {BORDER};
    border-bottom: none;
    border-radius: 4px 4px 0 0;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 0.5px;
}}

QTabBar::tab:selected {{
    background: {PANEL};
    color: {ACCENT};
    border-bottom: 2px solid {ACCENT};
}}

QTabBar::tab:hover:!selected {{
    color: {TEXT};
    background: {BTN_HOVER};
}}

QLineEdit {{
    background: {BG};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 10px 14px;
    color: {TEXT};
    font-size: 26px;
    font-family: 'Consolas', 'Courier New', monospace;
    selection-background-color: {ACCENT};
}}

QLineEdit:focus {{
    border-color: {ACCENT};
}}

QLabel {{
    color: {TEXT_DIM};
    font-size: 11px;
    letter-spacing: 0.5px;
}}

QLabel#result_label {{
    color: {ACCENT2};
    font-size: 13px;
    font-family: 'Consolas', 'Courier New', monospace;
}}

QLabel#section_label {{
    color: {ACCENT};
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}}

QLabel#title_label {{
    color: {TEXT};
    font-size: 22px;
    font-weight: bold;
    letter-spacing: 2px;
}}

QLabel#subtitle_label {{
    color: {TEXT_DIM};
    font-size: 11px;
    letter-spacing: 3px;
}}

QPushButton {{
    background: {BTN_NUM};
    color: {TEXT};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 0;
    font-size: 14px;
    font-family: 'Consolas', 'Courier New', monospace;
}}

QPushButton:hover {{
    background: {BTN_HOVER};
    border-color: {ACCENT};
    color: {ACCENT};
}}

QPushButton:pressed {{
    background: {ACCENT};
    color: {BG};
    border-color: {ACCENT};
}}

QPushButton.op_btn {{
    background: {BTN_OP};
    color: {ACCENT};
    border-color: {ACCENT};
    font-weight: bold;
}}

QPushButton.fn_btn {{
    background: {BTN_FN};
    color: {ACCENT2};
    border-color: {ACCENT2};
    font-size: 12px;
    font-weight: bold;
}}

QPushButton.spec_btn {{
    background: {BTN_SPEC};
    color: {ACCENT3};
    border-color: {ACCENT3};
    font-weight: bold;
}}

QPushButton.eq_btn {{
    background: {ACCENT};
    color: {BG};
    font-size: 20px;
    font-weight: bold;
    border-color: {ACCENT};
}}

QPushButton.eq_btn:hover {{
    background: #79b8ff;
    color: {BG};
}}

QComboBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    color: {TEXT};
    font-size: 13px;
    font-family: 'Consolas', 'Courier New', monospace;
    min-width: 120px;
}}

QComboBox:hover {{
    border-color: {ACCENT};
}}

QComboBox::drop-down {{
    border: none;
    width: 24px;
}}

QComboBox QAbstractItemView {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    color: {TEXT};
    selection-background-color: {ACCENT};
    selection-color: {BG};
    padding: 4px;
}}

QDoubleSpinBox {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 4px;
    padding: 6px 10px;
    color: {TEXT};
    font-size: 14px;
    font-family: 'Consolas', 'Courier New', monospace;
}}

QDoubleSpinBox:focus {{
    border-color: {ACCENT};
}}

QScrollArea {{
    border: none;
    background: transparent;
}}

QFrame#separator {{
    background: {BORDER};
    max-height: 1px;
    min-height: 1px;
}}
"""


# ─────────────────────────────────────────────
#  Helper: custom button
# ─────────────────────────────────────────────
class CalcButton(QPushButton):
    def __init__(self, text, btn_class="", size=(60, 52)):
        super().__init__(text)
        self.setFixedSize(*size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        if btn_class:
            self.setProperty("class", btn_class)
            # Manually apply styling via object name for class simulation
            self.setObjectName(btn_class)


def make_btn(text, btn_class="", w=60, h=52):
    b = QPushButton(text)
    b.setFixedSize(w, h)
    b.setCursor(Qt.CursorShape.PointingHandCursor)
    # Apply colour via stylesheet based on class name
    extra = ""
    if btn_class == "op_btn":
        extra = f"background:{BTN_OP}; color:{ACCENT}; border-color:{ACCENT}; font-weight:bold;"
    elif btn_class == "fn_btn":
        extra = f"background:{BTN_FN}; color:{ACCENT2}; border-color:{ACCENT2}; font-size:12px; font-weight:bold;"
    elif btn_class == "spec_btn":
        extra = f"background:{BTN_SPEC}; color:{ACCENT3}; border-color:{ACCENT3}; font-weight:bold;"
    elif btn_class == "eq_btn":
        extra = f"background:{ACCENT}; color:{BG}; font-size:20px; font-weight:bold; border-color:{ACCENT};"
    if extra:
        b.setStyleSheet(f"QPushButton {{ {extra} }} QPushButton:hover {{ background:{BTN_HOVER}; }}")
    return b


# ─────────────────────────────────────────────
#  Tab 1: Scientific Calculator
# ─────────────────────────────────────────────
class ScientificTab(QWidget):
    def __init__(self):
        super().__init__()
        self.expression = ""
        self.just_evaluated = False
        self.deg_mode = True  # True = degrees, False = radians
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(14, 14, 14, 14)

        # Display area
        display_frame = QFrame()
        display_frame.setStyleSheet(f"background:{PANEL}; border:1px solid {BORDER}; border-radius:8px;")
        disp_layout = QVBoxLayout(display_frame)
        disp_layout.setContentsMargins(12, 8, 12, 8)
        disp_layout.setSpacing(2)

        self.history_label = QLabel("")
        self.history_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.history_label.setStyleSheet(f"color:{TEXT_DIM}; font-size:12px; font-family:Consolas,monospace;")
        disp_layout.addWidget(self.history_label)

        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        disp_layout.addWidget(self.display)

        self.mode_label = QLabel("DEG  |  REAL")
        self.mode_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.mode_label.setStyleSheet(f"color:{ACCENT4}; font-size:10px; letter-spacing:1px;")
        disp_layout.addWidget(self.mode_label)

        layout.addWidget(display_frame)

        # Button grid
        grid = QGridLayout()
        grid.setSpacing(6)

        # Row 0 – mode / memory / special
        row0 = [
            ("DEG", "spec_btn"), ("(", "op_btn"), (")", "op_btn"), ("MC", "spec_btn"),
            ("MR", "spec_btn"), ("M+", "spec_btn"), ("M-", "spec_btn"),
        ]
        for c, (lbl, cls) in enumerate(row0):
            b = make_btn(lbl, cls, 60, 40)
            b.clicked.connect(lambda _, t=lbl: self._special(t))
            grid.addWidget(b, 0, c)

        # Row 1 – scientific functions
        row1 = [
            ("sin", "fn_btn"), ("cos", "fn_btn"), ("tan", "fn_btn"), ("log", "fn_btn"),
            ("ln", "fn_btn"), ("√", "fn_btn"), ("x²", "fn_btn"),
        ]
        for c, (lbl, cls) in enumerate(row1):
            b = make_btn(lbl, cls, 60, 44)
            b.clicked.connect(lambda _, t=lbl: self._fn(t))
            grid.addWidget(b, 1, c)

        # Row 2 – more functions
        row2 = [
            ("asin", "fn_btn"), ("acos", "fn_btn"), ("atan", "fn_btn"), ("10ˣ", "fn_btn"),
            ("eˣ", "fn_btn"), ("∛", "fn_btn"), ("xʸ", "fn_btn"),
        ]
        for c, (lbl, cls) in enumerate(row2):
            b = make_btn(lbl, cls, 60, 44)
            b.clicked.connect(lambda _, t=lbl: self._fn(t))
            grid.addWidget(b, 2, c)

        # Row 3-6 – numpad + ops (5 wide, cols 0-4; ops in col 5-6)
        numpad = [
            [("7", ""), ("8", ""), ("9", ""), ("÷", "op_btn"), ("CE", "spec_btn")],
            [("4", ""), ("5", ""), ("6", ""), ("×", "op_btn"), ("C", "spec_btn")],
            [("1", ""), ("2", ""), ("3", ""), ("−", "op_btn"), ("⌫", "spec_btn")],
            [("0", ""), (".", ""), ("π", "op_btn"), ("+", "op_btn"), ("=", "eq_btn")],
        ]
        for r, row in enumerate(numpad):
            for c, (lbl, cls) in enumerate(row):
                w, h = (60, 56) if lbl != "=" else (60, 56)
                if lbl == "0":
                    b = make_btn(lbl, cls, 60, 56)
                else:
                    b = make_btn(lbl, cls, w, h)
                b.clicked.connect(lambda _, t=lbl: self._press(t))
                grid.addWidget(b, r + 3, c)

        # ±  and 1/x in remaining cols
        extras = [("±", "op_btn"), ("1/x", "fn_btn"), ("e", "op_btn"), ("%", "op_btn")]
        for r, (lbl, cls) in enumerate(extras):
            b = make_btn(lbl, cls, 60, 56)
            b.clicked.connect(lambda _, t=lbl: self._press(t))
            grid.addWidget(b, r + 3, 5)

        layout.addLayout(grid)
        self.memory = 0.0

    # ── event handlers ──────────────────────────────────
    def _press(self, key):
        ops = {"÷": "/", "×": "*", "−": "-"}

        if key == "=":
            self._evaluate()
            return
        if key == "C":
            self.expression = ""
            self.display.setText("0")
            self.history_label.setText("")
            self.just_evaluated = False
            return
        if key == "CE":
            self.display.setText("0")
            self.expression = ""
            self.just_evaluated = False
            return
        if key == "⌫":
            if self.just_evaluated:
                return
            self.expression = self.expression[:-1]
            self.display.setText(self.expression or "0")
            return
        if key == "π":
            self._insert(str(math.pi))
            return
        if key == "e":
            self._insert(str(math.e))
            return
        if key == "±":
            try:
                val = float(self.expression or "0") * -1
                self.expression = str(val)
                self.display.setText(self.expression)
            except Exception:
                pass
            return
        if key == "1/x":
            try:
                val = 1 / float(self.expression or "1")
                self._show_result(val)
            except ZeroDivisionError:
                self.display.setText("Error: 1/0")
            return
        if key == "%":
            try:
                val = float(self.expression or "0") / 100
                self._show_result(val)
            except Exception:
                pass
            return

        if self.just_evaluated and key not in "+-*/÷×−(":
            self.expression = ""
            self.just_evaluated = False

        char = ops.get(key, key)
        self.expression += char
        self.display.setText(self.expression)

    def _insert(self, val):
        if self.just_evaluated:
            self.expression = ""
            self.just_evaluated = False
        self.expression += val
        self.display.setText(self.expression)

    def _fn(self, name):
        try:
            val = float(self.expression or "0")
        except Exception:
            val = 0.0

        angle = math.radians(val) if self.deg_mode else val

        result = None
        try:
            if name == "sin":   result = math.sin(angle)
            elif name == "cos": result = math.cos(angle)
            elif name == "tan":
                # tan is undefined at 90 + 180n degrees (π/2 + nπ radians)
                # Check if angle is a half-integer multiple of π
                if self.deg_mode:
                    # Undefined when val % 180 == 90
                    if abs((val % 180) - 90) < 1e-9:
                        self.display.setText("Undefined")
                        self.expression = ""
                        self.just_evaluated = True
                        return
                else:
                    # Undefined when angle / (π/2) is an odd integer
                    ratio = angle / (math.pi / 2)
                    if abs(ratio - round(ratio)) < 1e-9 and int(round(ratio)) % 2 != 0:
                        self.display.setText("Undefined")
                        self.expression = ""
                        self.just_evaluated = True
                        return
                result = math.tan(angle)
            elif name == "asin":
                r = math.asin(val)
                result = math.degrees(r) if self.deg_mode else r
            elif name == "acos":
                r = math.acos(val)
                result = math.degrees(r) if self.deg_mode else r
            elif name == "atan":
                r = math.atan(val)
                result = math.degrees(r) if self.deg_mode else r
            elif name == "log":  result = math.log10(val)
            elif name == "ln":   result = math.log(val)
            elif name == "√":    result = math.sqrt(val)
            elif name == "∛":    result = val ** (1/3)
            elif name == "x²":   result = val ** 2
            elif name == "xʸ":
                self.expression += "**"
                self.display.setText(self.expression)
                return
            elif name == "10ˣ":  result = 10 ** val
            elif name == "eˣ":   result = math.e ** val
        except Exception as ex:
            self.display.setText(f"Error")
            return

        if result is not None:
            self._show_result(result)

    def _special(self, key):
        if key == "DEG":
            self.deg_mode = not self.deg_mode
            mode = "DEG" if self.deg_mode else "RAD"
            self.mode_label.setText(f"{mode}  |  REAL")
        elif key == "MC":
            self.memory = 0.0
        elif key == "MR":
            self._insert(self._fmt(self.memory))
        elif key == "M+":
            try:
                self.memory += float(self.expression or "0")
            except Exception:
                pass
        elif key == "M-":
            try:
                self.memory -= float(self.expression or "0")
            except Exception:
                pass
        elif key in ("(", ")"):
            self._insert(key)

    def _evaluate(self):
        expr = self.expression.replace("^", "**")
        try:
            result = eval(expr, {"__builtins__": {}}, {
                "sin": math.sin, "cos": math.cos, "tan": math.tan,
                "sqrt": math.sqrt, "log": math.log10, "ln": math.log,
                "pi": math.pi, "e": math.e, "abs": abs, "pow": pow,
            })
            self.history_label.setText(self.expression + " =")
            self._show_result(result)
        except ZeroDivisionError:
            self.display.setText("Error: Division by 0")
        except Exception:
            self.display.setText("Syntax Error")
        self.just_evaluated = True

    def _show_result(self, val):
        self.expression = self._fmt(val)
        self.display.setText(self.expression)
        self.just_evaluated = True

    @staticmethod
    def _fmt(val):
        if isinstance(val, float) and val == int(val) and abs(val) < 1e15:
            return str(int(val))
        return f"{val:.10g}"


# ─────────────────────────────────────────────
#  Tab 2: Unit Converter
# ─────────────────────────────────────────────
UNIT_CATEGORIES = {
    "Length": {
        "Meter":        1.0,
        "Kilometer":    1e3,
        "Centimeter":   1e-2,
        "Millimeter":   1e-3,
        "Micrometer":   1e-6,
        "Mile":         1609.344,
        "Yard":         0.9144,
        "Foot":         0.3048,
        "Inch":         0.0254,
        "Nautical Mile":1852.0,
    },
    "Mass": {
        "Kilogram":     1.0,
        "Gram":         1e-3,
        "Milligram":    1e-6,
        "Metric Ton":   1e3,
        "Pound":        0.45359237,
        "Ounce":        0.028349523,
        "Slug":         14.5939029,
    },
    "Force": {
        "Newton":       1.0,
        "Kilonewton":   1e3,
        "Pound-force":  4.4482216,
        "Kip":          4448.2216,
        "Dyne":         1e-5,
        "Kilogram-force":9.80665,
    },
    "Pressure": {
        "Pascal":       1.0,
        "Kilopascal":   1e3,
        "Megapascal":   1e6,
        "Bar":          1e5,
        "Millibar":     100.0,
        "PSI":          6894.757,
        "Atmosphere":   101325.0,
        "mmHg":         133.322,
        "inHg":         3386.389,
    },
    "Energy": {
        "Joule":        1.0,
        "Kilojoule":    1e3,
        "Megajoule":    1e6,
        "Calorie":      4.184,
        "Kilocalorie":  4184.0,
        "BTU":          1055.056,
        "kWh":          3.6e6,
        "eV":           1.60218e-19,
        "ft·lbf":       1.3558179,
    },
    "Power": {
        "Watt":         1.0,
        "Kilowatt":     1e3,
        "Megawatt":     1e6,
        "Horsepower":   745.69987,
        "BTU/hr":       0.29307107,
        "ft·lbf/s":     1.3558179,
    },
    "Temperature": {  # handled specially
        "Celsius": None,
        "Fahrenheit": None,
        "Kelvin": None,
        "Rankine": None,
    },
    "Velocity": {
        "m/s":          1.0,
        "km/h":         1/3.6,
        "mph":          0.44704,
        "ft/s":         0.3048,
        "knot":         0.5144444,
        "Mach":         340.29,
    },
    "Angle": {
        "Degree":       1.0,
        "Radian":       180/math.pi,
        "Gradian":      0.9,
        "Arcminute":    1/60,
        "Arcsecond":    1/3600,
    },
    "Area": {
        "m²":           1.0,
        "km²":          1e6,
        "cm²":          1e-4,
        "mm²":          1e-6,
        "ft²":          0.09290304,
        "in²":          6.4516e-4,
        "acre":         4046.8564,
        "hectare":      1e4,
    },
    "Volume": {
        "m³":           1.0,
        "Liter":        1e-3,
        "Milliliter":   1e-6,
        "Gallon (US)":  3.785412e-3,
        "Quart (US)":   9.463529e-4,
        "Pint (US)":    4.731765e-4,
        "Cup (US)":     2.365882e-4,
        "fl oz (US)":   2.957353e-5,
        "ft³":          0.0283168,
        "in³":          1.638706e-5,
    },
}

def convert_temperature(val, from_u, to_u):
    # Convert to Celsius first
    if from_u == "Celsius":       c = val
    elif from_u == "Fahrenheit":  c = (val - 32) * 5/9
    elif from_u == "Kelvin":      c = val - 273.15
    elif from_u == "Rankine":     c = (val - 491.67) * 5/9
    else: return val

    if to_u == "Celsius":         return c
    elif to_u == "Fahrenheit":    return c * 9/5 + 32
    elif to_u == "Kelvin":        return c + 273.15
    elif to_u == "Rankine":       return (c + 273.15) * 9/5
    return c


class UnitConverterTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(14, 14, 14, 14)

        # Category selector
        cat_row = QHBoxLayout()
        cat_lbl = QLabel("CATEGORY")
        cat_lbl.setObjectName("section_label")
        cat_lbl.setStyleSheet(f"color:{ACCENT}; font-size:11px; font-weight:bold; letter-spacing:1.5px;")
        cat_row.addWidget(cat_lbl)
        cat_row.addStretch()
        self.cat_combo = QComboBox()
        self.cat_combo.addItems(list(UNIT_CATEGORIES.keys()))
        self.cat_combo.currentTextChanged.connect(self._on_category)
        cat_row.addWidget(self.cat_combo)
        layout.addLayout(cat_row)

        # Separator
        sep = QFrame(); sep.setObjectName("separator")
        layout.addWidget(sep)

        # From row
        from_row = QHBoxLayout()
        from_row.setSpacing(10)
        self.from_spin = QDoubleSpinBox()
        self.from_spin.setDecimals(8)
        self.from_spin.setRange(-1e15, 1e15)
        self.from_spin.setValue(1.0)
        self.from_spin.setFixedWidth(200)
        self.from_spin.valueChanged.connect(self._convert)
        from_row.addWidget(self.from_spin)
        self.from_unit = QComboBox()
        self.from_unit.setMinimumWidth(160)
        self.from_unit.currentTextChanged.connect(self._convert)
        from_row.addWidget(self.from_unit)
        from_row.addStretch()
        layout.addLayout(from_row)

        # Arrow
        arr = QLabel("↓")
        arr.setAlignment(Qt.AlignmentFlag.AlignCenter)
        arr.setStyleSheet(f"color:{ACCENT}; font-size:22px;")
        layout.addWidget(arr)

        # To row
        to_row = QHBoxLayout()
        to_row.setSpacing(10)
        self.to_display = QLineEdit()
        self.to_display.setReadOnly(True)
        self.to_display.setFixedWidth(200)
        self.to_display.setStyleSheet(f"font-size:18px; color:{ACCENT2};")
        to_row.addWidget(self.to_display)
        self.to_unit = QComboBox()
        self.to_unit.setMinimumWidth(160)
        self.to_unit.currentTextChanged.connect(self._convert)
        to_row.addWidget(self.to_unit)
        to_row.addStretch()
        layout.addLayout(to_row)

        # Formula hint
        self.formula_label = QLabel("")
        self.formula_label.setStyleSheet(f"color:{TEXT_DIM}; font-size:11px; font-style:italic;")
        layout.addWidget(self.formula_label)

        layout.addStretch()

        # Populate first category
        self._on_category(self.cat_combo.currentText())

    def _on_category(self, cat):
        units = list(UNIT_CATEGORIES[cat].keys())
        for cb in (self.from_unit, self.to_unit):
            cb.blockSignals(True)
            cb.clear()
            cb.addItems(units)
            cb.blockSignals(False)
        if len(units) >= 2:
            self.to_unit.setCurrentIndex(1)
        self._convert()

    def _convert(self):
        cat = self.cat_combo.currentText()
        from_u = self.from_unit.currentText()
        to_u = self.to_unit.currentText()
        val = self.from_spin.value()

        try:
            if cat == "Temperature":
                result = convert_temperature(val, from_u, to_u)
            else:
                factors = UNIT_CATEGORIES[cat]
                base = val * factors[from_u]
                result = base / factors[to_u]
            self.to_display.setText(f"{result:.10g}")
            self.formula_label.setText(f"1 {from_u}  =  {UNIT_CATEGORIES[cat].get(from_u, '–')} base units")
        except Exception:
            self.to_display.setText("Error")


# ─────────────────────────────────────────────
#  Tab 3: Engineering Formulas
# ─────────────────────────────────────────────
class FormulaWidget(QFrame):
    """One collapsible formula card."""

    def __init__(self, title, fields, formula_fn, result_unit=""):
        super().__init__()
        self.setStyleSheet(f"QFrame {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:8px; }}")
        self.formula_fn = formula_fn
        self.result_unit = result_unit
        self.inputs = {}

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 12)
        layout.setSpacing(8)

        # Title
        t = QLabel(title)
        t.setStyleSheet(f"color:{ACCENT4}; font-size:13px; font-weight:bold; background:transparent; border:none;")
        layout.addWidget(t)

        sep = QFrame(); sep.setObjectName("separator")
        layout.addWidget(sep)

        # Input fields
        for label, default in fields:
            row = QHBoxLayout()
            lbl = QLabel(label)
            lbl.setFixedWidth(160)
            lbl.setStyleSheet(f"color:{TEXT_DIM}; font-size:12px; background:transparent; border:none;")
            row.addWidget(lbl)
            spin = QDoubleSpinBox()
            spin.setDecimals(6)
            spin.setRange(-1e12, 1e12)
            spin.setValue(default)
            spin.setFixedWidth(160)
            spin.valueChanged.connect(self._calc)
            row.addWidget(spin)
            row.addStretch()
            self.inputs[label] = spin
            layout.addLayout(row)

        # Result
        res_row = QHBoxLayout()
        res_lbl = QLabel("Result:")
        res_lbl.setFixedWidth(160)
        res_lbl.setStyleSheet(f"color:{TEXT_DIM}; font-size:12px; background:transparent; border:none;")
        res_row.addWidget(res_lbl)
        self.result_edit = QLineEdit()
        self.result_edit.setReadOnly(True)
        self.result_edit.setFixedWidth(200)
        self.result_edit.setStyleSheet(f"font-size:15px; color:{ACCENT2}; background:{BG}; border:1px solid {BORDER}; border-radius:4px; padding:4px 8px;")
        res_row.addWidget(self.result_edit)
        if result_unit:
            u = QLabel(result_unit)
            u.setStyleSheet(f"color:{ACCENT}; font-size:12px; background:transparent; border:none;")
            res_row.addWidget(u)
        res_row.addStretch()
        layout.addLayout(res_row)

        self._calc()

    def _calc(self):
        vals = {k: w.value() for k, w in self.inputs.items()}
        try:
            r = self.formula_fn(vals)
            self.result_edit.setText(f"{r:.8g}")
        except Exception:
            self.result_edit.setText("Error")


class FormulasTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setSpacing(12)
        layout.setContentsMargins(14, 14, 14, 14)

        def sec(title):
            lbl = QLabel(f"── {title} ──────────────")
            lbl.setStyleSheet(f"color:{ACCENT}; font-size:11px; font-weight:bold; letter-spacing:1.5px;")
            layout.addWidget(lbl)

        # ── Mechanics ──
        sec("MECHANICS")
        layout.addWidget(FormulaWidget(
            "Force  (F = m·a)",
            [("Mass (kg)", 10.0), ("Acceleration (m/s²)", 9.81)],
            lambda v: v["Mass (kg)"] * v["Acceleration (m/s²)"],
            "N"
        ))
        layout.addWidget(FormulaWidget(
            "Kinetic Energy  (KE = ½mv²)",
            [("Mass (kg)", 1.0), ("Velocity (m/s)", 10.0)],
            lambda v: 0.5 * v["Mass (kg)"] * v["Velocity (m/s)"] ** 2,
            "J"
        ))
        layout.addWidget(FormulaWidget(
            "Potential Energy  (PE = mgh)",
            [("Mass (kg)", 1.0), ("Height (m)", 10.0), ("g (m/s²)", 9.80665)],
            lambda v: v["Mass (kg)"] * v["g (m/s²)"] * v["Height (m)"],
            "J"
        ))
        layout.addWidget(FormulaWidget(
            "Torque  (τ = F·r)",
            [("Force (N)", 100.0), ("Moment Arm (m)", 0.5)],
            lambda v: v["Force (N)"] * v["Moment Arm (m)"],
            "N·m"
        ))
        layout.addWidget(FormulaWidget(
            "Power  (P = F·v)",
            [("Force (N)", 100.0), ("Velocity (m/s)", 10.0)],
            lambda v: v["Force (N)"] * v["Velocity (m/s)"],
            "W"
        ))

        # ── Structural / Stress ──
        sec("STRUCTURAL / STRESS")
        layout.addWidget(FormulaWidget(
            "Normal Stress  (σ = F/A)",
            [("Force (N)", 10000.0), ("Area (m²)", 0.01)],
            lambda v: v["Force (N)"] / v["Area (m²)"],
            "Pa"
        ))
        layout.addWidget(FormulaWidget(
            "Shear Stress  (τ = V/A)",
            [("Shear Force (N)", 5000.0), ("Area (m²)", 0.005)],
            lambda v: v["Shear Force (N)"] / v["Area (m²)"],
            "Pa"
        ))
        layout.addWidget(FormulaWidget(
            "Bending Stress  (σ = M·c/I)",
            [("Moment (N·m)", 1000.0), ("Distance c (m)", 0.05), ("Moment of Inertia I (m⁴)", 4.167e-6)],
            lambda v: v["Moment (N·m)"] * v["Distance c (m)"] / v["Moment of Inertia I (m⁴)"],
            "Pa"
        ))
        layout.addWidget(FormulaWidget(
            "Strain  (ε = σ/E)",
            [("Stress σ (Pa)", 1e6), ("Young's Modulus E (Pa)", 200e9)],
            lambda v: v["Stress σ (Pa)"] / v["Young's Modulus E (Pa)"],
            "m/m"
        ))
        layout.addWidget(FormulaWidget(
            "Deflection — Simply Supported  (δ = 5wL⁴/384EI)",
            [("Load w (N/m)", 1000.0), ("Span L (m)", 5.0),
             ("E (Pa)", 200e9), ("I (m⁴)", 8.333e-6)],
            lambda v: 5*v["Load w (N/m)"]*v["Span L (m)"]**4 / (384*v["E (Pa)"]*v["I (m⁴)"]),
            "m"
        ))

        # ── Fluid Mechanics ──
        sec("FLUID MECHANICS")
        layout.addWidget(FormulaWidget(
            "Reynolds Number  (Re = ρvD/μ)",
            [("Density ρ (kg/m³)", 1000.0), ("Velocity v (m/s)", 1.0),
             ("Diameter D (m)", 0.05), ("Dynamic Viscosity μ (Pa·s)", 0.001)],
            lambda v: v["Density ρ (kg/m³)"]*v["Velocity v (m/s)"]*v["Diameter D (m)"] / v["Dynamic Viscosity μ (Pa·s)"],
            ""
        ))
        layout.addWidget(FormulaWidget(
            "Bernoulli Pressure  (P₁ + ½ρv²)",
            [("Static Pressure (Pa)", 101325.0), ("Density ρ (kg/m³)", 1.225), ("Velocity v (m/s)", 50.0)],
            lambda v: v["Static Pressure (Pa)"] + 0.5*v["Density ρ (kg/m³)"]*v["Velocity v (m/s)"]**2,
            "Pa"
        ))
        layout.addWidget(FormulaWidget(
            "Pipe Head Loss  (hL = f·L/D·v²/2g)",
            [("Friction Factor f", 0.02), ("Length L (m)", 100.0),
             ("Diameter D (m)", 0.1), ("Velocity v (m/s)", 2.0), ("g (m/s²)", 9.81)],
            lambda v: v["Friction Factor f"]*v["Length L (m)"]/v["Diameter D (m)"]*v["Velocity v (m/s)"]**2/(2*v["g (m/s²)"]),
            "m"
        ))

        # ── Electrical ──
        sec("ELECTRICAL")
        layout.addWidget(FormulaWidget(
            "Ohm's Law  (V = I·R)",
            [("Current (A)", 2.0), ("Resistance (Ω)", 50.0)],
            lambda v: v["Current (A)"] * v["Resistance (Ω)"],
            "V"
        ))
        layout.addWidget(FormulaWidget(
            "Electrical Power  (P = V·I)",
            [("Voltage (V)", 120.0), ("Current (A)", 10.0)],
            lambda v: v["Voltage (V)"] * v["Current (A)"],
            "W"
        ))
        layout.addWidget(FormulaWidget(
            "Capacitive Reactance  (Xc = 1/2πfC)",
            [("Frequency f (Hz)", 60.0), ("Capacitance C (F)", 100e-6)],
            lambda v: 1 / (2*math.pi*v["Frequency f (Hz)"]*v["Capacitance C (F)"]),
            "Ω"
        ))
        layout.addWidget(FormulaWidget(
            "Inductive Reactance  (XL = 2πfL)",
            [("Frequency f (Hz)", 60.0), ("Inductance L (H)", 0.1)],
            lambda v: 2*math.pi*v["Frequency f (Hz)"]*v["Inductance L (H)"],
            "Ω"
        ))

        # ── Thermodynamics ──
        sec("THERMODYNAMICS")
        layout.addWidget(FormulaWidget(
            "Ideal Gas Law  (P = nRT/V)",
            [("n (mol)", 1.0), ("T (K)", 298.15), ("V (m³)", 0.0224)],
            lambda v: v["n (mol)"]*8.314*v["T (K)"]/v["V (m³)"],
            "Pa"
        ))
        layout.addWidget(FormulaWidget(
            "Heat Transfer Conduction  (Q = kA·ΔT/d)",
            [("Conductivity k (W/m·K)", 1.0), ("Area A (m²)", 1.0),
             ("ΔT (K)", 20.0), ("Thickness d (m)", 0.1)],
            lambda v: v["Conductivity k (W/m·K)"]*v["Area A (m²)"]*v["ΔT (K)"]/v["Thickness d (m)"],
            "W"
        ))
        layout.addWidget(FormulaWidget(
            "Thermal Efficiency  (η = 1 - Tc/Th)",
            [("Cold Temp Tc (K)", 300.0), ("Hot Temp Th (K)", 600.0)],
            lambda v: (1 - v["Cold Temp Tc (K)"]/v["Hot Temp Th (K)"])*100,
            "%"
        ))

        layout.addStretch()
        scroll.setWidget(inner)
        outer.addWidget(scroll)


# ─────────────────────────────────────────────
#  Tab 4: Reference Constants
# ─────────────────────────────────────────────
CONSTANTS = [
    ("FUNDAMENTAL", [
        ("Speed of Light",          "c",        "2.99792458 × 10⁸ m/s"),
        ("Gravitational Constant",  "G",        "6.674 × 10⁻¹¹ m³·kg⁻¹·s⁻²"),
        ("Planck's Constant",       "h",        "6.62607 × 10⁻³⁴ J·s"),
        ("Boltzmann Constant",      "k_B",      "1.38065 × 10⁻²³ J/K"),
        ("Avogadro's Number",       "N_A",      "6.02214 × 10²³ mol⁻¹"),
        ("Elementary Charge",       "e",        "1.60218 × 10⁻¹⁹ C"),
        ("Electron Mass",           "m_e",      "9.10938 × 10⁻³¹ kg"),
        ("Proton Mass",             "m_p",      "1.67262 × 10⁻²⁷ kg"),
    ]),
    ("MECHANICS & GRAVITY", [
        ("Standard Gravity",        "g",        "9.80665 m/s²"),
        ("Atmospheric Pressure",    "P_atm",    "101 325 Pa"),
        ("Speed of Sound (air)",    "v_s",      "343 m/s at 20 °C"),
        ("Water Density (4 °C)",    "ρ_w",      "999.97 kg/m³"),
        ("Air Density (STP)",       "ρ_air",    "1.225 kg/m³"),
    ]),
    ("THERMODYNAMICS", [
        ("Universal Gas Constant",  "R",        "8.31446 J·mol⁻¹·K⁻¹"),
        ("Stefan-Boltzmann",        "σ",        "5.6704 × 10⁻⁸ W·m⁻²·K⁻⁴"),
        ("Absolute Zero",           "0 K",      "−273.15 °C"),
    ]),
    ("ELECTRICAL", [
        ("Vacuum Permittivity",     "ε_0",      "8.85419 × 10⁻¹² F/m"),
        ("Vacuum Permeability",     "μ_0",      "1.25664 × 10⁻⁶ H/m"),
        ("Impedance of Free Space", "Z_0",      "376.73 Ω"),
        ("Electron Volt",           "eV",       "1.60218 × 10⁻¹⁹ J"),
    ]),
    ("MATERIAL PROPERTIES (typical)", [
        ("Steel – Young's Modulus", "E",        "200 GPa"),
        ("Aluminum – E",            "E",        "69 GPa"),
        ("Concrete – E",            "E",        "30 GPa"),
        ("Steel – Yield Strength",  "σ_y",      "250 MPa"),
        ("Steel – Density",         "ρ",        "7 850 kg/m³"),
        ("Copper – Conductivity",   "k",        "401 W·m⁻¹·K⁻¹"),
    ]),
]


class ConstantsTab(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        inner = QWidget()
        layout = QVBoxLayout(inner)
        layout.setSpacing(14)
        layout.setContentsMargins(14, 14, 14, 14)

        for section, items in CONSTANTS:
            lbl = QLabel(f"── {section} ──────────────")
            lbl.setStyleSheet(f"color:{ACCENT}; font-size:11px; font-weight:bold; letter-spacing:1.5px;")
            layout.addWidget(lbl)

            card = QFrame()
            card.setStyleSheet(f"QFrame {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:8px; }}")
            card_layout = QVBoxLayout(card)
            card_layout.setContentsMargins(14, 10, 14, 10)
            card_layout.setSpacing(6)

            for name, symbol, value in items:
                row = QHBoxLayout()
                n = QLabel(name)
                n.setFixedWidth(210)
                n.setStyleSheet(f"color:{TEXT}; font-size:12px; background:transparent; border:none;")
                s = QLabel(symbol)
                s.setFixedWidth(70)
                s.setStyleSheet(f"color:{ACCENT4}; font-size:12px; font-style:italic; background:transparent; border:none;")
                v = QLabel(value)
                v.setStyleSheet(f"color:{ACCENT2}; font-size:12px; font-family:Consolas,monospace; background:transparent; border:none;")
                row.addWidget(n)
                row.addWidget(s)
                row.addWidget(v)
                row.addStretch()
                card_layout.addLayout(row)

            layout.addWidget(card)

        layout.addStretch()
        scroll.setWidget(inner)
        outer.addWidget(scroll)


# ─────────────────────────────────────────────
#  Main Window
# ─────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Engineering Calculator")
        self.setMinimumSize(560, 760)
        self.resize(600, 820)
        self.setStyleSheet(STYLESHEET)
        self._build_ui()

    def _build_ui(self):
        root = QWidget()
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        # Header
        header = QFrame()
        header.setFixedHeight(62)
        header.setStyleSheet(f"background:{PANEL}; border-bottom:1px solid {BORDER};")
        h_layout = QHBoxLayout(header)
        h_layout.setContentsMargins(18, 0, 18, 0)

        # Icon placeholder (a unicode character)
        ico = QLabel("⚙")
        ico.setStyleSheet(f"color:{ACCENT}; font-size:26px; background:transparent;")
        h_layout.addWidget(ico)

        title_block = QVBoxLayout()
        title_block.setSpacing(0)
        t1 = QLabel("ENGINEERING CALCULATOR")
        t1.setObjectName("title_label")
        t1.setStyleSheet(f"color:{TEXT}; font-size:16px; font-weight:bold; letter-spacing:2px; background:transparent;")
        t2 = QLabel("PRECISION  ·  SCIENCE  ·  ENGINEERING")
        t2.setObjectName("subtitle_label")
        t2.setStyleSheet(f"color:{TEXT_DIM}; font-size:9px; letter-spacing:3px; background:transparent;")
        title_block.addWidget(t1)
        title_block.addWidget(t2)
        h_layout.addLayout(title_block)
        h_layout.addStretch()
        root_layout.addWidget(header)

        # Tabs
        tabs = QTabWidget()
        tabs.setDocumentMode(True)
        tabs.addTab(ScientificTab(),   "  CALCULATOR  ")
        tabs.addTab(UnitConverterTab(),"  UNIT CONVERT  ")
        tabs.addTab(FormulasTab(),     "  FORMULAS  ")
        tabs.addTab(ConstantsTab(),    "  CONSTANTS  ")
        root_layout.addWidget(tabs)

        self.setCentralWidget(root)


# ─────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Engineering Calculator")
    app.setOrganizationName("EngCalc")
    win = MainWindow()
    win.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
