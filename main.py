import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
import random

class Gamescreen(App):
    def build(self):
        self.layout = self.createtable()
        Clock.schedule_interval(self.random_letter,)  # Schedule random_letter function to run every 3 seconds
        return self.layout

    def createtable(self):
        layout = GridLayout(cols=6, rows=7)
        # Initialize grid with buttons
        for i in range(36):
            label = Label(text='', font_size=20)
            layout.add_widget(label)
        # Add a row for text input
        text_input = TextInput(text='Enter text here')
        layout.add_widget(text_input)
        return layout

    def random_letter(self, dt):
        # Function to place a random letter on the grid
        char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Randomly choose a letter
        label = random.choice(self.layout.children)  # Randomly select a button from the grid
        label.text = char  # Set the text of the button to the random letter

if __name__ == "__main__":
    Gamescreen().run()

