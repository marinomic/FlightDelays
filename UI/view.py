import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "Flight Delays Manager"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.DARK
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self.__theme_switch = None
        self._title = None
        self._x_comp = None
        self._btn_CercaItinerario = None
        self._numeroTratteMax = None
        self._ddAeroportoA = None
        self._btn_AeroportiConnessi = None
        self._ddAeroportoP = None
        self._btn_AnalizzaAreoporti = None
        self._txt_result = None

    def load_interface(self):
        # title
        self.__theme_switch = ft.Switch(label="Dark Mode", on_change=self._theme_changed)
        self._title = ft.Text("Flight Delays", color="blue", size=24)
        self._page.controls.append(self.__theme_switch)
        self._page.controls.append(self._title)

        # ROW 0
        self._x_comp = ft.TextField(
                label="compagnie minimo",
                width=250,
        )
        self._btn_AnalizzaAreoporti = ft.ElevatedButton(
                text="Analizza aeroporti",
                on_click=self._controller.handle_analizza_aeroporti,
                width=300,
                height=50,
        )
        row0 = ft.Row([self._x_comp, self._btn_AnalizzaAreoporti], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row0)

        # ROW 1
        self._ddAeroportoP = ft.Dropdown(
                label="Aeroporto di partenza",
                width=250,
                disabled=True,
        )
        self._btn_AeroportiConnessi = ft.ElevatedButton(
                text="Aeroporti connessi",
                on_click=self._controller.handle_aeroporti_connessi,
                width=300,
                height=50,
                disabled=True,
        )
        row1 = ft.Row([self._ddAeroportoP, self._btn_AeroportiConnessi], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # ROW 2
        self._ddAeroportoA = ft.Dropdown(
                label="Aeroporto di destinazione",
                width=250,
                disabled=True,
        )
        row2 = ft.Row([self._ddAeroportoA, ft.Container(width=300)], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        # ROW 3
        self._numeroTratteMax = ft.TextField(
                label="Numero tratte massimo",
                width=250,
                disabled=True,
        )

        self._btn_CercaItinerario = ft.ElevatedButton(
                text="Cerca itinerario",
                on_click=self._controller.handle_cerca_itinerario,
                width=300,
                height=50,
                disabled=True,
        )
        row3 = ft.Row([self._numeroTratteMax, self._btn_CercaItinerario], alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row3)

        # List View where the reply is printed
        self._txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self._txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def _theme_changed(self, event):
        """Function that changes the color theme of the app, when the corresponding
                switch is triggered"""
        self._page.theme_mode = (
            ft.ThemeMode.LIGHT
            if self._page.theme_mode == ft.ThemeMode.DARK
            else ft.ThemeMode.DARK
        )
        self.__theme_switch.label = (
            "Light theme" if self._page.theme_mode == ft.ThemeMode.LIGHT else "Dark theme"
        )
        self.update_page()

    def update_page(self):
        self._page.update()
