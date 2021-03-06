__author__ = 'Anti'

from widgets import AbstractWidget
import Tkinter


class OptionMenu(AbstractWidget.WidgetWithCommand):
    def __init__(self, parent, name, row, column, **kwargs):
        AbstractWidget.WidgetWithCommand.__init__(self, name, row, column, **self.setDefaultKwargs(kwargs, {
            "default_value": self.getDefaultValue(kwargs),
            "columnspan": kwargs.get("columnspan", 2)
        }))
        self.values = kwargs.get("values", [])
        self.variable = Tkinter.StringVar()
        self.command = kwargs.get("command", lambda: None)
        label = Tkinter.Label(parent, text=self.name)
        label.grid(row=self.row, column=self.column-1, padx=self.padx, pady=self.pady)
        self.create(Tkinter.OptionMenu(parent, self.variable, *self.values, command=lambda x: self.command()))

    def getValue(self):
        return self.variable.get()

    def setValue(self, value):
        self.variable.set(value)

    def getDefaultValue(self, kwargs):
        return kwargs.get("default_value", kwargs.get("values", [None])[0])
