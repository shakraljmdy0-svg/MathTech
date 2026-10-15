# ============================================================
# MathTech Pro v1.0
# تطبيق رياضيات وتكنولوجيا متكامل
# ============================================================

from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.storage.jsonstore import JsonStore
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel

import os
import math
import re
from collections import Counter

APP_NAME = "MathTech"
APP_VERSION = "1.0.0"


# ============================================================
#                          KV String
# ============================================================
KV = """
#:import get_color_from_hex kivy.utils.get_color_from_hex

<MenuItem@MDCard>:
    orientation: "vertical"
    size_hint: None, None
    size: dp(100), dp(110)
    radius: [dp(20)]
    elevation: 3
    md_bg_color: get_color_from_hex("#161B22")
    ripple_behavior: True
    MDIcon:
        icon: root.icon_name if hasattr(root, 'icon_name') else "calculator"
        halign: "center"
        theme_icon_color: "Custom"
        icon_color: get_color_from_hex("#58A6FF")
        font_size: "38sp"
        pos_hint: {"center_x": .5, "center_y": .62}
    MDLabel:
        text: root.item_text if hasattr(root, 'item_text') else ""
        halign: "center"
        theme_text_color: "Custom"
        text_color: get_color_from_hex("#C9D1D9")
        font_size: "12sp"
        pos_hint: {"center_x": .5, "center_y": .15}


# ============================================================
#                        Home Screen
# ============================================================
<HomeScreen>:
    name: "home"
    FloatLayout:

        Image:
            source: "assets/splash.png"
            allow_stretch: True
            keep_ratio: False
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}
            opacity: 0.10

        canvas.before:
            Color:
                rgba: 0.05, 0.07, 0.09, 0.80
            Rectangle:
                pos: self.pos
                size: self.size

        MDBoxLayout:
            orientation: "vertical"

            MDTopAppBar:
                title: "MathTech Pro"
                elevation: 4
                md_bg_color: get_color_from_hex("#1F6FEB")
                left_action_items: [["theme-light-dark", lambda x: app.toggle_theme()]]
                right_action_items: [["history", lambda x: app.open_history()]]

            MDBoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: dp(110)
                padding: dp(10)
                MDLabel:
                    text: "MathTech"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#58A6FF")
                    font_style: "H4"
                    bold: True
                MDLabel:
                    text: "الرياضيات + التكنولوجيا = مستقبل أفضل"
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#C9D1D9")
                    font_style: "Caption"

            ScrollView:
                MDGridLayout:
                    cols: 3
                    spacing: dp(8)
                    padding: dp(10)
                    adaptive_height: True
                    size_hint_y: None

                    MenuItem:
                        item_text: "الحاسبة"
                        icon_name: "calculator"
                        on_release: app.go_to("calculator")
                    MenuItem:
                        item_text: "الإحصاء"
                        icon_name: "chart-bar"
                        on_release: app.go_to("stats")
                    MenuItem:
                        item_text: "الرسوم"
                        icon_name: "chart-line"
                        on_release: app.go_to("charts")
                    MenuItem:
                        item_text: "المصفوفات"
                        icon_name: "grid"
                        on_release: app.go_to("matrix")
                    MenuItem:
                        item_text: "الوحدات"
                        icon_name: "ruler"
                        on_release: app.go_to("units")
                    MenuItem:
                        item_text: "الاحتمالات"
                        icon_name: "dice-5"
                        on_release: app.go_to("probability")
                    MenuItem:
                        item_text: "الدوال"
                        icon_name: "function-variant"
                        on_release: app.go_to("grapher")
                    MenuItem:
                        item_text: "السجل"
                        icon_name: "history"
                        on_release: app.open_history()
                    MenuItem:
                        item_text: "حول"
                        icon_name: "information"
                        on_release: app.open_about()


# ============================================================
#                       Calculator
# ============================================================
<CalculatorScreen>:
    name: "calculator"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "الحاسبة"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        MDCard:
            orientation: "vertical"
            size_hint_y: None
            height: dp(130)
            padding: dp(12)
            spacing: dp(4)
            md_bg_color: get_color_from_hex("#161B22")
            radius: [dp(12)]
            MDLabel:
                id: expr_label
                text: ""
                halign: "right"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#8B949E")
                font_size: "16sp"
            MDLabel:
                id: result_label
                text: "0"
                halign: "right"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#3FB950")
                font_size: "32sp"
                bold: True

        MDGridLayout:
            cols: 5
            size_hint_y: None
            height: dp(50)
            spacing: dp(2)
            padding: dp(4)
            MDFlatButton:
                text: "sin"
                on_release: app.calc_insert("sin(")
            MDFlatButton:
                text: "cos"
                on_release: app.calc_insert("cos(")
            MDFlatButton:
                text: "tan"
                on_release: app.calc_insert("tan(")
            MDFlatButton:
                text: "log"
                on_release: app.calc_insert("log(")
            MDFlatButton:
                text: "sqrt"
                on_release: app.calc_insert("sqrt(")

        MDGridLayout:
            cols: 4
            spacing: dp(4)
            padding: dp(4)
            size_hint_y: None
            height: self.minimum_height
            row_default_height: dp(58)
            row_force_default: True

            MDRaisedButton:
                text: "C"
                md_bg_color: get_color_from_hex("#F85149")
                on_release: app.calc_clear()
            MDRaisedButton:
                text: "DEL"
                md_bg_color: get_color_from_hex("#1F6FEB")
                on_release: app.calc_back()
            MDRaisedButton:
                text: "("
                on_release: app.calc_insert("(")
            MDRaisedButton:
                text: ")"
                on_release: app.calc_insert(")")

            MDRaisedButton:
                text: "7"
                on_release: app.calc_insert("7")
            MDRaisedButton:
                text: "8"
                on_release: app.calc_insert("8")
            MDRaisedButton:
                text: "9"
                on_release: app.calc_insert("9")
            MDRaisedButton:
                text: "/"
                md_bg_color: get_color_from_hex("#1F6FEB")
                on_release: app.calc_insert("/")

            MDRaisedButton:
                text: "4"
                on_release: app.calc_insert("4")
            MDRaisedButton:
                text: "5"
                on_release: app.calc_insert("5")
            MDRaisedButton:
                text: "6"
                on_release: app.calc_insert("6")
            MDRaisedButton:
                text: "*"
                md_bg_color: get_color_from_hex("#1F6FEB")
                on_release: app.calc_insert("*")

            MDRaisedButton:
                text: "1"
                on_release: app.calc_insert("1")
            MDRaisedButton:
                text: "2"
                on_release: app.calc_insert("2")
            MDRaisedButton:
                text: "3"
                on_release: app.calc_insert("3")
            MDRaisedButton:
                text: "-"
                md_bg_color: get_color_from_hex("#1F6FEB")
                on_release: app.calc_insert("-")

            MDRaisedButton:
                text: "0"
                on_release: app.calc_insert("0")
            MDRaisedButton:
                text: "."
                on_release: app.calc_insert(".")
            MDRaisedButton:
                text: "%"
                on_release: app.calc_insert("%")
            MDRaisedButton:
                text: "+"
                md_bg_color: get_color_from_hex("#1F6FEB")
                on_release: app.calc_insert("+")

        MDRaisedButton:
            text: "="
            size_hint_y: None
            height: dp(58)
            md_bg_color: get_color_from_hex("#3FB950")
            on_release: app.calc_calculate()


# ============================================================
#                          Stats
# ============================================================
<StatsScreen>:
    name: "stats"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "الإحصاء الوصفي"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        MDBoxLayout:
            orientation: "vertical"
            padding: dp(10)
            spacing: dp(8)

            MDTextField:
                id: input_field
                hint_text: "أدخل الأرقام مفصولة بفواصل"
                text: "10,20,30,40,50"
                mode: "rectangle"

            MDBoxLayout:
                size_hint_y: None
                height: dp(45)
                spacing: dp(6)
                MDRaisedButton:
                    text: "بيانات خام"
                    on_release: app.compute_stats("raw")
                MDRaisedButton:
                    text: "جدول تكراري"
                    md_bg_color: get_color_from_hex("#58A6FF")
                    on_release: app.compute_stats("table")

            ScrollView:
                MDLabel:
                    id: stats_output
                    text: "النتائج ستظهر هنا..."
                    halign: "right"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#3FB950")
                    size_hint_y: None
                    text_size: self.width - dp(20), None
                    height: self.texture_size[1]


# ============================================================
#                         Charts
# ============================================================
<ChartsScreen>:
    name: "charts"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "الرسوم البيانية"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        MDBoxLayout:
            padding: dp(8)
            spacing: dp(6)
            size_hint_y: None
            height: dp(50)
            MDTextField:
                id: chart_input
                hint_text: "60-62:5, 63-65:15 ..."
                text: "60-62:5, 63-65:15, 66-68:45, 69-71:27, 72-74:8"
                mode: "rectangle"

        MDBoxLayout:
            size_hint_y: None
            height: dp(45)
            spacing: dp(4)
            padding: dp(4)
            MDRaisedButton:
                text: "مدرج"
                on_release: app.draw_chart("hist")
            MDRaisedButton:
                text: "مضلع"
                md_bg_color: get_color_from_hex("#E3B341")
                on_release: app.draw_chart("poly")
            MDRaisedButton:
                text: "دائرة"
                md_bg_color: get_color_from_hex("#56D364")
                on_release: app.draw_chart("pie")
            MDRaisedButton:
                text: "تراكمي"
                md_bg_color: get_color_from_hex("#FF7B72")
                on_release: app.draw_chart("ogive")

        Widget:
            id: chart_container


# ============================================================
#                         Matrix
# ============================================================
<MatrixScreen>:
    name: "matrix"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "المصفوفات"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        MDBoxLayout:
            size_hint_y: None
            height: dp(45)
            padding: dp(6)
            spacing: dp(4)
            MDLabel:
                text: "الحجم:"
                size_hint_x: None
                width: dp(60)
                halign: "center"
            MDRaisedButton:
                text: "2x2"
                on_release: app.set_matrix_size(2)
            MDRaisedButton:
                text: "3x3"
                on_release: app.set_matrix_size(3)
            MDRaisedButton:
                text: "4x4"
                on_release: app.set_matrix_size(4)

        ScrollView:
            MDGridLayout:
                id: matrix_grid
                cols: 2
                spacing: dp(10)
                padding: dp(8)
                size_hint_y: None
                adaptive_height: True

        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(3)
            padding: dp(4)
            MDRaisedButton:
                text: "+"
                on_release: app.matrix_op("add")
            MDRaisedButton:
                text: "-"
                on_release: app.matrix_op("sub")
            MDRaisedButton:
                text: "x"
                on_release: app.matrix_op("mul")
            MDRaisedButton:
                text: "detA"
                md_bg_color: get_color_from_hex("#3FB950")
                on_release: app.matrix_op("det")
            MDRaisedButton:
                text: "AT"
                md_bg_color: get_color_from_hex("#8250DF")
                on_release: app.matrix_op("trans")
            MDRaisedButton:
                text: "A-1"
                md_bg_color: get_color_from_hex("#56D364")
                on_release: app.matrix_op("inv")

        ScrollView:
            size_hint_y: None
            height: dp(100)
            MDLabel:
                id: matrix_output
                text: "النتيجة ستظهر هنا..."
                halign: "center"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#3FB950")
                size_hint_y: None
                text_size: self.width - dp(20), None
                height: self.texture_size[1]


# ============================================================
#                          Units
# ============================================================
<UnitsScreen>:
    name: "units"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "محول الوحدات"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        ScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(10)
                size_hint_y: None
                adaptive_height: True

                MDLabel:
                    text: "الفئة"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#58A6FF")
                    size_hint_y: None
                    height: dp(25)
                MDDropDownItem:
                    id: category_item
                    text: "الطول"
                    on_release: app.open_category_menu()

                MDLabel:
                    text: "القيمة"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#58A6FF")
                    size_hint_y: None
                    height: dp(25)
                MDTextField:
                    id: unit_value
                    text: "1"
                    input_filter: "float"
                    mode: "rectangle"

                MDLabel:
                    text: "من"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#58A6FF")
                    size_hint_y: None
                    height: dp(25)
                MDDropDownItem:
                    id: from_item
                    text: "متر (m)"
                    on_release: app.open_from_menu()

                MDLabel:
                    text: "إلى"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#58A6FF")
                    size_hint_y: None
                    height: dp(25)
                MDDropDownItem:
                    id: to_item
                    text: "كيلومتر (km)"
                    on_release: app.open_to_menu()

                MDRaisedButton:
                    text: "Convert"
                    size_hint_y: None
                    height: dp(50)
                    md_bg_color: get_color_from_hex("#3FB950")
                    on_release: app.convert_unit()

                MDLabel:
                    id: unit_result
                    text: ""
                    halign: "center"
                    theme_text_color: "Custom"
                    text_color: get_color_from_hex("#3FB950")
                    font_size: "22sp"
                    bold: True
                    size_hint_y: None
                    height: dp(80)


# ============================================================
#                       Probability
# ============================================================
<ProbabilityScreen>:
    name: "probability"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "الاحتمالات"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        MDTabs:
            id: prob_tabs

            Tab:
                text: "بسيط"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(14)
                    spacing: dp(10)
                    MDTextField:
                        id: p_fav
                        hint_text: "العدد المؤيد"
                        text: "1"
                        input_filter: "float"
                        mode: "rectangle"
                    MDTextField:
                        id: p_tot
                        hint_text: "العدد الكلي"
                        text: "6"
                        input_filter: "float"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "احسب"
                        md_bg_color: get_color_from_hex("#3FB950")
                        on_release: app.prob_simple()

            Tab:
                text: "توافيق"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(14)
                    spacing: dp(10)
                    MDTextField:
                        id: cp_n
                        hint_text: "n"
                        text: "5"
                        input_filter: "int"
                        mode: "rectangle"
                    MDTextField:
                        id: cp_r
                        hint_text: "r"
                        text: "2"
                        input_filter: "int"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "احسب"
                        md_bg_color: get_color_from_hex("#3FB950")
                        on_release: app.prob_comb()

            Tab:
                text: "طبيعي"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(14)
                    spacing: dp(10)
                    MDTextField:
                        id: nd_mu
                        hint_text: "mu"
                        text: "0"
                        input_filter: "float"
                        mode: "rectangle"
                    MDTextField:
                        id: nd_sigma
                        hint_text: "sigma"
                        text: "1"
                        input_filter: "float"
                        mode: "rectangle"
                    MDTextField:
                        id: nd_x
                        hint_text: "x"
                        text: "0"
                        input_filter: "float"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "احسب"
                        md_bg_color: get_color_from_hex("#3FB950")
                        on_release: app.prob_normal()

            Tab:
                text: "ذو حدين"
                MDBoxLayout:
                    orientation: "vertical"
                    padding: dp(14)
                    spacing: dp(10)
                    MDTextField:
                        id: bn_n
                        hint_text: "n"
                        text: "10"
                        input_filter: "int"
                        mode: "rectangle"
                    MDTextField:
                        id: bn_p
                        hint_text: "p"
                        text: "0.5"
                        input_filter: "float"
                        mode: "rectangle"
                    MDTextField:
                        id: bn_k
                        hint_text: "k"
                        text: "5"
                        input_filter: "int"
                        mode: "rectangle"
                    MDRaisedButton:
                        text: "احسب"
                        md_bg_color: get_color_from_hex("#3FB950")
                        on_release: app.prob_binom()

        ScrollView:
            size_hint_y: None
            height: dp(180)
            MDLabel:
                id: prob_output
                text: ""
                halign: "center"
                theme_text_color: "Custom"
                text_color: get_color_from_hex("#3FB950")
                size_hint_y: None
                text_size: self.width - dp(20), None
                height: self.texture_size[1]


# ============================================================
#                        Grapher
# ============================================================
<GrapherScreen>:
    name: "grapher"
    MDBoxLayout:
        orientation: "vertical"
        md_bg_color: get_color_from_hex("#0D1117")

        MDTopAppBar:
            title: "راسم الدوال"
            left_action_items: [["arrow-right", lambda x: app.go_back()]]
            md_bg_color: get_color_from_hex("#1F6FEB")

        MDBoxLayout:
            size_hint_y: None
            height: dp(55)
            padding: dp(8)
            spacing: dp(6)
            MDTextField:
                id: graph_expr
                hint_text: "sin(x)"
                text: "sin(x)"
                mode: "rectangle"

        MDBoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(4)
            padding: dp(6)
            MDTextField:
                id: gxmin
                hint_text: "x min"
                text: "-10"
                mode: "rectangle"
            MDTextField:
                id: gxmax
                hint_text: "x max"
                text: "10"
                mode: "rectangle"
            MDRaisedButton:
                text: "Draw"
                md_bg_color: get_color_from_hex("#3FB950")
                on_release: app.draw_function()

        Widget:
            id: graph_container
"""


# ============================================================
#                          Screens
# ============================================================
class HomeScreen(Screen): pass
class CalculatorScreen(Screen): pass
class StatsScreen(Screen): pass
class ChartsScreen(Screen): pass
class MatrixScreen(Screen): pass
class UnitsScreen(Screen): pass
class ProbabilityScreen(Screen): pass
class GrapherScreen(Screen): pass


# ============================================================
#                           App
# ============================================================
class MathTechApp(MDApp):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.expression = ""
        self.history = []
        self.store = None
        self.sm = None
        self.matrix_size = 2
        self.matrix_entries_a = []
        self.matrix_entries_b = []
        self.units_data = self._unit_categories()
        self.current_category = "الطول"

    # ---------- Build ----------
    def build(self):
        self.title = APP_NAME
        try:
            self.store = JsonStore("mathtech_data.json")
            if self.store.exists("history"):
                self.history = self.store.get("history")["items"]
        except Exception:
            pass

        Builder.load_string(KV)
        self.sm = ScreenManager(transition=SlideTransition())
        for s in [HomeScreen(), CalculatorScreen(), StatsScreen(),
                  ChartsScreen(), MatrixScreen(), UnitsScreen(),
                  ProbabilityScreen(), GrapherScreen()]:
            self.sm.add_widget(s)
        return self.sm

    def on_start(self):
        self.show_splash()

    # ---------- Splash ----------
    def show_splash(self):
        splash = FloatLayout()
        with splash.canvas:
            Color(0.05, 0.07, 0.09, 1)
            Rectangle(pos=splash.pos, size=Window.size)
        try:
            img = Image(source="assets/splash.png",
                        allow_stretch=True, keep_ratio=True,
                        size_hint=(1, 1),
                        pos_hint={"center_x": .5, "center_y": .5})
            splash.add_widget(img)
        except Exception:
            pass
        Window.add_widget(splash)
        Clock.schedule_once(lambda dt: Window.remove_widget(splash), 3)

    # ---------- Navigation ----------
    def go_to(self, name):
        self.sm.transition.direction = "left"
        self.sm.current = name

    def go_back(self):
        self.sm.transition.direction = "right"
        self.sm.current = "home"

    def toggle_theme(self):
        if self.theme_cls.theme_style == "Dark":
            self.theme_cls.theme_style = "Light"
        else:
            self.theme_cls.theme_style = "Dark"

    # ---------- Calculator ----------
    def calc_insert(self, v):
        self.expression += v
        self.update_calc()

    def calc_back(self):
        self.expression = self.expression[:-1]
        self.update_calc()

    def calc_clear(self):
        self.expression = ""
        self.update_calc()
        try:
            self.sm.get_screen("calculator").ids.result_label.text = "0"
        except Exception:
            pass

    def update_calc(self):
        try:
            scr = self.sm.get_screen("calculator")
            scr.ids.expr_label.text = self.expression
            if self.expression.strip():
                scr.ids.result_label.text = self.format_res(self.evaluate(self.expression))
        except Exception:
            pass

    def calc_calculate(self):
        try:
            scr = self.sm.get_screen("calculator")
            res = self.format_res(self.evaluate(self.expression))
            scr.ids.result_label.text = res
            self.history.append(f"{self.expression} = {res}")
            self.save_store()
            self.expression = res
            scr.ids.expr_label.text = res
        except Exception:
            try:
                self.sm.get_screen("calculator").ids.result_label.text = "Error"
            except Exception:
                pass

    def format_res(self, v):
        if isinstance(v, float):
            if v.is_integer():
                return str(int(v))
            return f"{v:.10g}"
        return str(v)

    def evaluate(self, expr):
        expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        expr = expr.replace("^", "**").replace("π", "pi")
        expr = re.sub(r"(\d+(?:\.\d+)?)%", r"(\1/100)", expr)
        env = {
            "sin": math.sin, "cos": math.cos, "tan": math.tan,
            "log": math.log10, "ln": math.log, "sqrt": math.sqrt,
            "abs": abs, "exp": math.exp, "pi": math.pi, "e": math.e,
            "__builtins__": {},
        }
        while "!" in expr:
            m = re.search(r"(\d+)!", expr)
            if not m:
                break
            expr = expr[:m.start()] + str(math.factorial(int(m.group(1)))) + expr[m.end():]
        return eval(expr, env, {})

    def save_store(self):
        if self.store:
            try:
                self.store.put("history", items=self.history[-200:])
            except Exception:
                pass

    # ---------- Stats ----------
    def compute_stats(self, mode):
        try:
            scr = self.sm.get_screen("stats")
            text = scr.ids.input_field.text
            if mode == "raw":
                data = [float(x) for x in text.replace(" ", "").split(",") if x]
                out = self._stats_raw(data)
            else:
                bins, counts = self._parse_table(text)
                out = self._stats_table(bins, counts)
            scr.ids.stats_output.text = out
        except Exception as e:
            self.sm.get_screen("stats").ids.stats_output.text = f"Error: {e}"

    def _stats_raw(self, data):
        n = len(data)
        mean = sum(data) / n
        s = sorted(data)
        med = (s[n // 2 - 1] + s[n // 2]) / 2 if n % 2 == 0 else s[n // 2]
        c = Counter(data)
        mf = max(c.values())
        mode = ", ".join(str(k) for k, v in c.items() if v == mf) if mf > 1 else "None"
        var_s = sum((x - mean) ** 2 for x in data) / (n - 1) if n > 1 else 0
        std_s = math.sqrt(var_s)
        var_p = sum((x - mean) ** 2 for x in data) / n
        std_p = math.sqrt(var_p)
        return (f"n         = {n}\n"
                f"Mean      = {mean:.6g}\n"
                f"Median    = {med:.6g}\n"
                f"Mode      = {mode}\n"
                f"Variance  = {var_s:.6g}\n"
                f"Std Dev   = {std_s:.6g}\n"
                f"Std Pop   = {std_p:.6g}\n"
                f"Min       = {min(data)}\n"
                f"Max       = {max(data)}\n"
                f"Range     = {max(data) - min(data)}")

    def _stats_table(self, bins, counts):
        mid = [(lo + hi) / 2 for lo, hi in bins]
        n = sum(counts)
        mean = sum(m * c for m, c in zip(mid, counts)) / n
        var_p = sum(c * (m - mean) ** 2 for m, c in zip(mid, counts)) / n
        std_p = math.sqrt(var_p)
        return (f"n         = {n}\n"
                f"Mean      = {mean:.6g}\n"
                f"Variance  = {var_p:.6g}\n"
                f"Std Dev   = {std_p:.6g}")

    def _parse_table(self, text):
        text = text.replace(" ", "")
        parts = [p for p in text.split(",") if p]
        bins, counts = [], []
        for p in parts:
            rng, cnt = p.split(":")
            lo, hi = rng.split("-")
            bins.append((float(lo), float(hi)))
            counts.append(int(float(cnt)))
        return bins, counts

    # ---------- Charts ----------
    def draw_chart(self, mode):
        from kivy.graphics import Color, Rectangle, Line, Ellipse
        scr = self.sm.get_screen("charts")
        try:
            bins, counts = self._parse_table(scr.ids.chart_input.text)
        except Exception:
            return

        c = scr.ids.chart_container
        c.canvas.clear()

        with c.canvas:
            Color(0.086, 0.106, 0.13, 1)
            Rectangle(pos=c.pos, size=c.size)

            w, h = c.width, c.height
            ml, mr, mt, mb = 50, 20, 30, 60
            pw, ph = w - ml - mr, h - mt - mb
            ox, oy = c.x + ml, c.y + mb
            y_max = max(counts) * 1.15 if counts else 1
            x_min, x_max = bins[0][0], bins[-1][1]

            def tx(x):
                return ox + (x - x_min) / (x_max - x_min) * pw

            def ty(y):
                return oy + y / y_max * ph

            if mode != "pie":
                Color(0.78, 0.82, 0.85, 1)
                Line(points=[ox, oy, ox + pw, oy], width=1.5)
                Line(points=[ox, oy, ox, oy + ph], width=1.5)

            if mode == "hist":
                Color(1.0, 0.65, 0.34, 1)
                for i, cc in enumerate(counts):
                    x1, x2 = tx(bins[i][0]), tx(bins[i][1])
                    y1, y2 = ty(cc), ty(0)
                    Rectangle(pos=(x1, y1), size=(x2 - x1, y2 - y1))

            elif mode == "poly":
                mid = [(lo + hi) / 2 for lo, hi in bins]
                bw = bins[0][1] - bins[0][0]
                pts = [tx(mid[0] - bw), ty(0)]
                for i, cc in enumerate(counts):
                    pts.extend([tx(mid[i]), ty(cc)])
                pts.extend([tx(mid[-1] + bw), ty(0)])
                Color(0.89, 0.70, 0.25, 1)
                Line(points=pts, width=2.5)
                Color(0.25, 0.89, 0.31, 1)
                for i, cc in enumerate(counts):
                    Ellipse(pos=(tx(mid[i]) - 5, ty(cc) - 5), size=(10, 10))

            elif mode == "pie":
                total = sum(counts)
                cx, cy = c.center_x, c.center_y
                r = min(w, h) / 2 - 40
                palette = [(0.35, 0.65, 1, 1), (0.73, 0.55, 1, 1),
                           (0.25, 0.89, 0.31, 1), (0.97, 0.32, 0.29, 1),
                           (0.89, 0.70, 0.25, 1), (0.22, 0.89, 0.84, 1)]
                start = 90
                for i, cc in enumerate(counts):
                    if cc == 0:
                        continue
                    ext = -360 * cc / total
                    Color(*palette[i % len(palette)])
                    steps = max(3, int(abs(ext) / 3))
                    pts = [cx, cy]
                    for s in range(steps + 1):
                        a = math.radians(start + ext * s / steps)
                        pts.extend([cx + r * math.cos(a), cy + r * math.sin(a)])
                    pts.extend([cx, cy])
                    Line(points=pts, width=1)
                    start += ext

            elif mode == "ogive":
                cum = []
                s = 0
                for cc in counts:
                    s += cc
                    cum.append(s)
                Color(1.0, 0.42, 0.42, 1)
                pts = [tx(bins[0][0]), ty(0)]
                for i, cf in enumerate(cum):
                    pts.extend([tx(bins[i][1]), ty(cf)])
                Line(points=pts, width=2.5)

    # ---------- Matrix ----------
    def set_matrix_size(self, n):
        self.matrix_size = n
        self.matrix_entries_a = []
        self.matrix_entries_b = []
        grid = self.sm.get_screen("matrix").ids.matrix_grid
        grid.clear_widgets()

        for label_text, entries in [("A", self.matrix_entries_a),
                                     ("B", self.matrix_entries_b)]:
            box = MDBoxLayout(orientation="vertical",
                              spacing=dp(4),
                              size_hint_y=None,
                              height=dp(40 + n * 45))
            box.add_widget(MDLabel(text=f"Matrix {label_text}",
                                    halign="center", bold=True))
            for i in range(n):
                row = MDBoxLayout(spacing=dp(4),
                                   size_hint_y=None,
                                   height=dp(40))
                row_entries = []
                for j in range(n):
                    tf = MDTextField(text="0",
                                      input_filter="float",
                                      mode="rectangle",
                                      size_hint_x=1)
                    row.add_widget(tf)
                    row_entries.append(tf)
                entries.append(row_entries)
                box.add_widget(row)
            grid.add_widget(box)

    def _get_matrix(self, entries):
        n = self.matrix_size
        return [[float(entries[i][j].text or "0") for j in range(n)]
                for i in range(n)]

    def matrix_op(self, op):
        try:
            A = self._get_matrix(self.matrix_entries_a)
            B = self._get_matrix(self.matrix_entries_b)
            out = self.sm.get_screen("matrix").ids.matrix_output
            n = self.matrix_size

            if op == "add":
                C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
                out.text = self._mat_str(C, "A + B =")
            elif op == "sub":
                C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
                out.text = self._mat_str(C, "A - B =")
            elif op == "mul":
                C = [[sum(A[i][k] * B[k][j] for k in range(n))
                      for j in range(n)] for i in range(n)]
                out.text = self._mat_str(C, "A x B =")
            elif op == "det":
                out.text = f"det(A) = {self._det(A):.6g}"
            elif op == "trans":
                T = [[A[j][i] for j in range(n)] for i in range(n)]
                out.text = self._mat_str(T, "A transposed =")
            elif op == "inv":
                inv = self._inverse(A)
                if inv is None:
                    out.text = "No inverse (det ~ 0)"
                else:
                    out.text = self._mat_str(inv, "A inverse =")
        except Exception as e:
            self.sm.get_screen("matrix").ids.matrix_output.text = f"Error: {e}"

    def _mat_str(self, M, title):
        s = title + "\n"
        for r in M:
            s += "  ".join(f"{v:9.3f}" for v in r) + "\n"
        return s

    def _det(self, m):
        if len(m) == 1:
            return m[0][0]
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]
        s = 0
        for c in range(len(m)):
            sub = [r[:c] + r[c + 1:] for r in m[1:]]
            s += ((-1) ** c) * m[0][c] * self._det(sub)
        return s

    def _inverse(self, A):
        n = len(A)
        M = [row[:] + [1 if i == j else 0 for j in range(n)]
             for i, row in enumerate(A)]
        for col in range(n):
            piv = max(range(col, n), key=lambda r: abs(M[r][col]))
            if abs(M[piv][col]) < 1e-12:
                return None
            M[col], M[piv] = M[piv], M[col]
            pv = M[col][col]
            M[col] = [x / pv for x in M[col]]
            for r in range(n):
                if r != col:
                    f = M[r][col]
                    M[r] = [M[r][k] - f * M[col][k] for k in range(2 * n)]
        return [row[n:] for row in M]

    # ---------- Units ----------
    def _unit_categories(self):
        return {
            "الطول": {"متر (m)": 1.0, "كيلومتر (km)": 1000.0,
                      "سنتيمتر (cm)": 0.01, "مليمتر (mm)": 0.001,
                      "ميل (mi)": 1609.344, "قدم (ft)": 0.3048,
                      "بوصة (in)": 0.0254},
            "الوزن": {"كيلوغرام (kg)": 1.0, "غرام (g)": 0.001,
                      "طن (t)": 1000.0, "باوند (lb)": 0.45359237,
                      "أونصة (oz)": 0.028349523125},
            "الحرارة": {"مئوية (C)": "C", "فهرنهايت (F)": "F",
                        "كلفن (K)": "K"},
            "المساحة": {"متر مربع (m2)": 1.0, "كيلومتر مربع (km2)": 1e6,
                        "هكتار (ha)": 10000.0, "فدان (acre)": 4046.8564224},
            "الحجم": {"لتر (L)": 1.0, "مليلتر (mL)": 0.001,
                      "متر مكعب (m3)": 1000.0, "غالون (gal)": 3.785411784},
            "السرعة": {"متر/ث (m/s)": 1.0, "كم/س (km/h)": 0.277777778,
                       "ميل/س (mph)": 0.44704},
            "الزمن": {"ثانية (s)": 1.0, "دقيقة (min)": 60.0,
                      "ساعة (h)": 3600.0, "يوم (d)": 86400.0},
            "التخزين": {"بايت (B)": 1.0, "كيلوبايت (KB)": 1024.0,
                        "ميغابايت (MB)": 1024.0 ** 2,
                        "غيغابايت (GB)": 1024.0 ** 3},
        }

    def open_category_menu(self):
        from kivymd.uix.menu import MDDropdownMenu
        items = [{"text": k, "viewclass": "OneLineListItem",
                  "on_release": lambda x=k: self._set_category(x)}
                 for k in self.units_data.keys()]
        self._cat_menu = MDDropdownMenu(
            caller=self.sm.get_screen("units").ids.category_item,
            items=items, width_mult=4)
        self._cat_menu.open()

    def _set_category(self, name):
        self.current_category = name
        self.sm.get_screen("units").ids.category_item.text = name
        self._cat_menu.dismiss()
        units = list(self.units_data[name].keys())
        self.sm.get_screen("units").ids.from_item.text = units[0]
        self.sm.get_screen("units").ids.to_item.text = (
            units[1] if len(units) > 1 else units[0])

    def open_from_menu(self):
        from kivymd.uix.menu import MDDropdownMenu
        units = list(self.units_data[self.current_category].keys())
        items = [{"text": u, "viewclass": "OneLineListItem",
                  "on_release": lambda x=u: self._set_from(x)} for u in units]
        self._from_menu = MDDropdownMenu(
            caller=self.sm.get_screen("units").ids.from_item,
            items=items, width_mult=4)
        self._from_menu.open()

    def _set_from(self, name):
        self.sm.get_screen("units").ids.from_item.text = name
        self._from_menu.dismiss()

    def open_to_menu(self):
        from kivymd.uix.menu import MDDropdownMenu
        units = list(self.units_data[self.current_category].keys())
        items = [{"text": u, "viewclass": "OneLineListItem",
                  "on_release": lambda x=u: self._set_to(x)} for u in units]
        self._to_menu = MDDropdownMenu(
            caller=self.sm.get_screen("units").ids.to_item,
            items=items, width_mult=4)
        self._to_menu.open()

    def _set_to(self, name):
        self.sm.get_screen("units").ids.to_item.text = name
        self._to_menu.dismiss()

    def convert_unit(self):
        try:
            scr = self.sm.get_screen("units")
            v = float(scr.ids.unit_value.text)
            cat = self.current_category
            f = scr.ids.from_item.text
            t = scr.ids.to_item.text
            if cat == "الحرارة":
                if f.startswith("مئوية"):
                    cc = v
                elif f.startswith("فهرنهايت"):
                    cc = (v - 32) * 5 / 9
                else:
                    cc = v - 273.15
                if t.startswith("مئوية"):
                    o = cc
                elif t.startswith("فهرنهايت"):
                    o = cc * 9 / 5 + 32
                else:
                    o = cc + 273.15
            else:
                o = v * self.units_data[cat][f] / self.units_data[cat][t]
            scr.ids.unit_result.text = f"{v} {f}\n->\n{o:.10g} {t}"
        except Exception as e:
            self.sm.get_screen("units").ids.unit_result.text = f"Error: {e}"

    # ---------- Probability ----------
    def _prob_out(self):
        return self.sm.get_screen("probability").ids.prob_output

    def prob_simple(self):
        try:
            scr = self.sm.get_screen("probability")
            fav = float(scr.ids.p_fav.text or "0")
            tot = float(scr.ids.p_tot.text or "1")
            if tot == 0:
                raise ZeroDivisionError
            p = fav / tot
            self._prob_out().text = (f"P(A)     = {p:.6g}\n"
                                      f"P(A')    = {1 - p:.6g}\n"
                                      f"Percent  = {p * 100:.2f}%\n"
                                      f"Odds     = {fav:.0f}:{tot - fav:.0f}")
        except Exception as e:
            self._prob_out().text = f"Error: {e}"

    def prob_comb(self):
        try:
            scr = self.sm.get_screen("probability")
            n = int(scr.ids.cp_n.text or "0")
            r = int(scr.ids.cp_r.text or "0")
            c = math.comb(n, r)
            p = math.perm(n, r)
            self._prob_out().text = (f"C({n},{r}) = {c}\n"
                                      f"P({n},{r}) = {p}\n"
                                      f"n! = {math.factorial(n)}\n"
                                      f"r! = {math.factorial(r)}")
        except Exception as e:
            self._prob_out().text = f"Error: {e}"

    def prob_normal(self):
        try:
            scr = self.sm.get_screen("probability")
            mu = float(scr.ids.nd_mu.text or "0")
            sg = float(scr.ids.nd_sigma.text or "1")
            x = float(scr.ids.nd_x.text or "0")
            if sg <= 0:
                raise ValueError("sigma > 0")
            z = (x - mu) / sg
            cdf = 0.5 * (1 + math.erf(z / math.sqrt(2)))
            pdf = (1 / (sg * math.sqrt(2 * math.pi))) * \
                  math.exp(-0.5 * ((x - mu) / sg) ** 2)
            self._prob_out().text = (f"z = {z:.6g}\n"
                                      f"P(X <= x) = {cdf:.6g}\n"
                                      f"P(X > x)  = {1 - cdf:.6g}\n"
                                      f"f(x) PDF  = {pdf:.6g}")
        except Exception as e:
            self._prob_out().text = f"Error: {e}"

    def prob_binom(self):
        try:
            scr = self.sm.get_screen("probability")
            n = int(scr.ids.bn_n.text or "10")
            p = float(scr.ids.bn_p.text or "0.5")
            k = int(scr.ids.bn_k.text or "5")
            if not (0 <= p <= 1):
                raise ValueError("0 <= p <= 1")
            c = math.comb(n, k)
            pk = c * (p ** k) * ((1 - p) ** (n - k))
            cdf = sum(math.comb(n, i) * (p ** i) * ((1 - p) ** (n - i))
                      for i in range(k + 1))
            self._prob_out().text = (f"P(X=k)   = {pk:.6g}\n"
                                      f"P(X<=k)  = {cdf:.6g}\n"
                                      f"P(X>k)   = {1 - cdf:.6g}\n"
                                      f"Mean = {n * p:.6g}\n"
                                      f"Std = {math.sqrt(n * p * (1 - p)):.6g}")
        except Exception as e:
            self._prob_out().text = f"Error: {e}"

    # ---------- Grapher ----------
    def draw_function(self):
        from kivy.graphics import Color, Rectangle, Line
        scr = self.sm.get_screen("grapher")
        expr = scr.ids.graph_expr.text
        try:
            xmin = float(scr.ids.gxmin.text)
            xmax = float(scr.ids.gxmax.text)
        except Exception:
            return

        c = scr.ids.graph_container
        c.canvas.clear()

        N = 500
        ys = []
        for i in range(N):
            x = xmin + (xmax - xmin) * i / (N - 1)
            try:
                y = eval(expr.replace("^", "**").replace("π", "pi"),
                         {"x": x, "sin": math.sin, "cos": math.cos,
                          "tan": math.tan, "log": math.log, "ln": math.log,
                          "sqrt": math.sqrt, "abs": abs, "exp": math.exp,
                          "pi": math.pi, "e": math.e, "__builtins__": {}})
                ys.append(y if math.isfinite(y) else None)
            except Exception:
                ys.append(None)

        valid = [y for y in ys if y is not None]
        if not valid:
            return

        ymin, ymax = min(valid), max(valid)
        if ymax - ymin < 1e-9:
            ymin -= 1
            ymax += 1
        pad = (ymax - ymin) * 0.1
        ymin -= pad
        ymax += pad

        with c.canvas:
            Color(0.086, 0.106, 0.13, 1)
            Rectangle(pos=c.pos, size=c.size)

            W, H = c.width, c.height

            def tx(x):
                return c.x + (x - xmin) / (xmax - xmin) * W

            def ty(y):
                return c.y + H - (y - ymin) / (ymax - ymin) * H

            Color(0.5, 0.55, 0.6, 1)
            if ymin <= 0 <= ymax:
                Line(points=[c.x, ty(0), c.x + W, ty(0)], width=1)
            if xmin <= 0 <= xmax:
                Line(points=[tx(0), c.y, tx(0), c.y + H], width=1)

            Color(1.0, 0.65, 0.34, 1)
            prev = None
            for i, y in enumerate(ys):
                if y is None:
                    prev = None
                    continue
                px = c.x + i * W / (N - 1)
                py = max(c.y - 1000, min(c.y + H + 1000, ty(y)))
                if prev is not None:
                    Line(points=[prev[0], prev[1], px, py], width=2)
                prev = [px, py]

    # ---------- History ----------
    def open_history(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        text = "\n".join(self.history[-30:]) if self.history else "No history"
        if hasattr(self, "_dlg_h") and self._dlg_h:
            self._dlg_h.dismiss()
        self._dlg_h = MDDialog(
            title="History",
            text=text,
            buttons=[MDFlatButton(text="Close",
                                   on_release=lambda x: self._dlg_h.dismiss())])
        self._dlg_h.open()

    # ---------- About ----------
    def open_about(self):
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton
        if hasattr(self, "_dlg_a") and self._dlg_a:
            self._dlg_a.dismiss()
        self._dlg_a = MDDialog(
            title="MathTech Pro",
            text=(f"Version {APP_VERSION}\n\n"
                  "Math + Technology\n"
                  "Idea + Code = Better Future"),
            buttons=[MDFlatButton(text="Close",
                                   on_release=lambda x: self._dlg_a.dismiss())])
        self._dlg_a.open()


# ============================================================
#                         Run
# ============================================================
if __name__ == "__main__":
    MathTechApp().run()