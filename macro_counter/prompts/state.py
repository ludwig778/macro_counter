from macro_counter.models import Component


class State:
    def __init__(self):
        self.load_components()

    def load_components(self):
        self.components = {
            i.name: i
            for i in Component.list()
        }


state = State()
