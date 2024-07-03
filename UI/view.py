import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        # page stuff
        self._page = page
        self._page.title = "TdP Exercise on MIA Art database"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        # controller (it is not initialized. Must be initialized in the main, after the controller is created)
        self._controller = None
        # graphical elements
        self._title = None

    def load_interface(self):
        # title
        self._title = ft.Text("The MIA Collection database", color="orange", size=24)
        self._page.controls.append(self._title)

        # controls
        self._btnAnalizzaOggetti = ft.ElevatedButton(text="Analizza oggetti",
                                                     on_click=self._controller.handleAnalizzaOggetti,
                                                     bgcolor="orange",
                                                     color="white",
                                                     width=200)  # button che crea il grafo
        self._txtIdOggetto = ft.TextField(label="Id Oggetto", color="orange", border_color="orange")
        self._btnCompConnessa = ft.ElevatedButton(text="Cerca Connessa", on_click=self._controller.handleCompConnessa,
                                                  bgcolor="orange",
                                                  color="white",
                                                  width=200)  # button che mi farà stampare la componente connessa

        row1 = ft.Row([ft.Container(self._btnAnalizzaOggetti, width=250),
                       ft.Container(self._txtIdOggetto, width=250),
                       ft.Container(self._btnCompConnessa, width=250)],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)

        # row 2
        self._ddLun = ft.Dropdown(label="Lunghezza", border_color="orange", disabled=True)
        self._btnCercaPercorso = ft.ElevatedButton(text="Cerca oggetti",
                                                   on_click=self._controller.handleCercaPercorso,
                                                   bgcolor="orange",
                                                   color="white",
                                                   disabled=True)
        row2 = ft.Row([ft.Container(None, width=250),
                       ft.Container(self._ddLun, width=250),
                       ft.Container(self._btnCercaPercorso, width=250)],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

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

    def update_page(self):
        self._page.update()
