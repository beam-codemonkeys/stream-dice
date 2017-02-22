from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.stacklayout import StackLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle
from random import randint

DICE_TYPES = {
    'd20': {
        'sides': 20,
        'button_label': 'D20'
    },
    'd10': {
        'sides': 10,
        'button_label': 'D10'
    },
    'd6': {
        'sides': 6,
        'button_label': 'D6'
    },
    'd4': {
        'sides': 4,
        'button_label': 'D4'
    },
    'coin': {
        'sides': 2,
        'button_label': 'Coin'
    },
    'd100': {
        'sides': 100,
        'button_label': 'D100'
    }
}

DICE = []


class Die(Button):

    label_string = "{}: {}"

    def __init__(self, **kwargs):
        super(Die, self).__init__(**kwargs)
        die_type = kwargs['die_type']

        self._type = die_type
        self._sides = DICE_TYPES[self._type]['sides']
        self._current_roll = 1
        if self._sides == 2:
            self.text = self.label_string.format(DICE_TYPES[self._type]['button_label'], "Flip")
        else:
            self.text = self.label_string.format(DICE_TYPES[self._type]['button_label'], "Roll")

    def on_press(self):
        self._current_roll = randint(1, self._sides)
        print "Rolling D{}: {}".format(self._sides, self._current_roll)
        if self._sides == 2:
            coin_text = "Tails"
            if self._current_roll == 1:
                coin_text = "Heads"
            self.text = self.label_string.format(DICE_TYPES[self._type]['button_label'], coin_text)
        else:
            self.text = self.label_string.format(DICE_TYPES[self._type]['button_label'], self._current_roll)




class DiceOverlay(GridLayout):

    # Borrowed from
    # https://kivy.org/docs/guide/widgets.html#add-a-color-to-the-background-of-a-custom-layouts-rule-class
    def __init__(self, **kwargs):
        # make sure we aren't overriding any important functionality
        super(DiceOverlay, self).__init__(**kwargs)

        with self.canvas.before:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


class DiceApp(App):

    overlay = DiceOverlay(cols=5)

    def build(self):
        s = StackLayout()
        d = DropDown()
        for die in DICE_TYPES:
            btn = Button(text=DICE_TYPES[die]['button_label'], size_hint_y=None, height=35)
            btn.value = die
            btn.bind(on_release=lambda instance: d.select(instance.value))
            d.add_widget(btn)

        add_button = Button(text="Add Die", width=100, height=40, size_hint=(None, None))
        add_button.bind(on_release=d.open)
        d.bind(on_select=self.add_die)
        s.add_widget(add_button)
        s.add_widget(self.overlay)
        return s

    def add_die(self, instance, value):
        print "Adding Die: {}".format(value)
        d = Die(
            die_type=value,
            )

        print "Created Die"
        self.overlay.add_widget(d)
        print "Added Die to Overlay"

    def test_press(self):
        print "Test Press"

def main():

    try:
        menu = DiceApp()
        menu.run()

    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()
