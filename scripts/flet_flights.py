import sys
sys.path.append("./")
from enum import Enum
from threading import Lock
from typing import Optional

import flet
from flet_core import TextAlign


from assets import *


class Category(Enum):
    DEPARTURE, ARRIVAL = "Departure", "Arrival"


class Terminal(Enum):
    A, B, C = database.terminals()  # bad


class State:
    CATEGORY: Category = Category.DEPARTURE
    TERMINAL: Terminal = Terminal.A
    COLUMNS: list[str] = list()
    DATA: list = list()


# top: Optional[flet.Row] = None
# table: Optional[flet.DataTable] = None

lock = Lock()


def departures(page: flet.Page):
    top: Optional[flet.Row] = flet.Row()
    table: Optional[flet.DataTable] = flet.DataTable()
    # global top, table

    def set_state():
        # global top, table
        title = flet.Text(value=f"TERMINAL {State.TERMINAL.value} {(State.CATEGORY.value + 's').upper()}",
                          color="yellow", size=40, width=1600, text_align=TextAlign.CENTER)
        category = flet.ElevatedButton(text=State.CATEGORY.value, on_click=change_category, width=150, color="yellow")
        # category = flet.IconButton(flet.icons.CHANGE_CIRCLE, on_click=change_category, width=150)
        terminal = flet.ElevatedButton(text=State.TERMINAL.value, on_click=change_terminal, width=150, color="yellow")
        # terminal = flet.IconButton(flet.icons.TV, on_click=change_terminal, width=150)

        top = flet.Row(controls=[title, category, terminal])

        try:
            lock.acquire(True)
            State.COLUMNS = database.table_columns(State.CATEGORY.value)
            '''State.DATA = database("select * from ? where terminal = ? limit 100",
                                  (State.CATEGORY.value, State.TERMINAL.value)).fetchall()'''
            State.DATA = database(f"select * from {State.CATEGORY.value} "
                                  f"where terminal = '{State.TERMINAL.value}' limit 100").fetchall()
        except Exception as e:
            print(e)
        finally:
            lock.release()

        table_columns, table_rows = [flet.DataColumn(flet.Text(value=column[0])) for column in State.COLUMNS], list()
        for row in State.DATA:
            table_rows.append(flet.DataRow(cells=[flet.DataCell(flet.Text(str(column))) for column in row]))
        table = flet.DataTable(columns=table_columns, rows=table_rows, width=1900,
                               horizontal_lines=flet.border.BorderSide(1, "yellow"))
        page.clean()
        page.add(top, table)
        page.update()

    def keyboard(e: flet.KeyboardEvent):
        if e.key == "C":
            change_category(e)
        elif e.key == "T":
            change_terminal(e)

    def change_category(e):
        State.CATEGORY = Category.ARRIVAL if State.CATEGORY == Category.DEPARTURE else Category.DEPARTURE
        set_state()

    def change_terminal(e):
        if State.TERMINAL == Terminal.A:
            State.TERMINAL = Terminal.B
        elif State.TERMINAL == Terminal.B:
            State.TERMINAL = Terminal.C
        elif State.TERMINAL == Terminal.C:
            State.TERMINAL = Terminal.A
        set_state()

    set_state()
    page.on_keyboard_event = keyboard
    page.scroll = flet.ScrollMode.ALWAYS
    page.update()
    return


flet.app(target=departures, view=flet.AppView.WEB_BROWSER, port=9000)
