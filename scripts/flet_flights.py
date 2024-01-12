"""
Makes a web page showing operated flights, departures or arrivals, separated by Terminal.

*Created on 12 Jan 2024.*
"""

from enum import Enum
from random import choice
from typing import Optional, NoReturn

import flet
from flet_core import TextAlign

from assets import *
from assets.models import CycleEnum


class Category(Enum):
    DEPARTURE, ARRIVAL = "Departure", "Arrival"


Terminal = CycleEnum("Terminal", [(terminal, terminal) for terminal in database.terminals()])


class FlightCategories(dict):

    def __init__(self) -> NoReturn:
        super().__init__()
        _list = [(category, terminal) for category in Category.__members__ for terminal in Terminal.__members__]
        for category, terminal in _list:
            category = category.capitalize()
            _key = category + terminal
            _airport_column = "destination" if category == Category.DEPARTURE.value else "starting_point"
            _date_column = "departure" if category == Category.DEPARTURE.value else "arrival"
            self[_key] = database(f"select code, airline, ?, ?, state, check_in, gate from {category} "
                                  f"where terminal = ? order by ? limit 100",
                                  (_airport_column, _date_column, terminal, category.lower())).fetchall()
            if not hasattr(self, category):
                self.__setattr__(category, ["code", "airline", _airport_column, _date_column,
                                            "state", "check_in", "gate"])
        return


data = FlightCategories()


class State:
    CATEGORY, TERMINAL = choice(list(Category)), choice(list(Terminal))
    COLUMNS, DATA = list(), list()


def departures(page: flet.Page):
    top: Optional[flet.Row] = flet.Row()
    table: Optional[flet.DataTable] = flet.DataTable()

    def set_state():
        title = flet.Text(value=f"TERMINAL {State.TERMINAL.value} {(State.CATEGORY.value + 's').upper()}",
                          color="yellow", size=40, width=1550, text_align=TextAlign.CENTER)
        category = flet.ElevatedButton(text=State.CATEGORY.value, on_click=change_category, width=150, color="yellow")
        terminal = flet.ElevatedButton(text=State.TERMINAL.value, on_click=change_terminal, width=150, color="yellow")

        top = flet.Row(controls=[title, category, terminal])

        State.COLUMNS = getattr(data, State.CATEGORY.value)
        State.DATA = data[State.CATEGORY.value + State.TERMINAL.value]

        table_columns = [flet.DataColumn(flet.Text(value=column.upper(), size=20)) for column in State.COLUMNS]
        table_rows = list()
        for row in State.DATA:
            table_rows.append(flet.DataRow(cells=[flet.DataCell(flet.Text(value=str(column))) for column in row]))
            for index, color in enumerate(["blue", "yellow", "orange", "blue", "white", "yellow", "yellow"]):
                table_rows[-1].cells[index].content.color = color

        table = flet.DataTable(columns=table_columns, rows=table_rows, width=1900,
                               horizontal_lines=flet.border.BorderSide(1.5, "yellow"))
        page.clean()
        page.add(top, table)
        page.update()

    def keyboard(e: flet.KeyboardEvent):
        if e.key == "Escape":
            page.clean()
        elif e.key == "R":
            set_state()
        elif e.key == "C":
            change_category(e)
        elif e.key == "T":
            change_terminal(e)

    def change_category(e):
        State.CATEGORY = Category.ARRIVAL if State.CATEGORY == Category.DEPARTURE else Category.DEPARTURE
        set_state()

    def change_terminal(e):
        State.TERMINAL = State.TERMINAL.next()
        set_state()

    set_state()
    page.on_keyboard_event = keyboard
    page.scroll = flet.ScrollMode.ALWAYS
    page.update()
    return


flet.app(target=departures, view=flet.AppView.WEB_BROWSER, port=9000)
