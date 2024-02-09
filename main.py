import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import random

class Gamescreen(App):
    def build(self):
        self.layout = self.createtable()
        Clock.schedule_interval(self.random_letter,0.1)  # Schedule random_letter function to run every 3 seconds
        return self.layout

    def createtable(self):
        Screen = GridLayout(cols=1, rows=2)
        playzone = GridLayout(cols=6, rows=6)
        Screen.add_widget(playzone)
        # Initialize grid with labels
        self.labels = []
        for i in range(36):
            label = Label(text='', font_size=50)
            self.labels.append(label)
            playzone.add_widget(label)
        
        input_box = BoxLayout(size_hint_y=None, height=0.1*Window.height)
        Screen.add_widget(input_box)
        # Add a row for text input
        self.text_input = TextInput(text='Enter text here')
        input_box.add_widget(self.text_input)
        
        return Screen

    def random_letter(self, dt):
        # Function to place a random letter on the grid
        char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Randomly choose a letter
        label = random.choice(self.labels)  # Randomly select a label from the grid
        label.text = char  # Set the text of the label to the random letter

if __name__ == "__main__":
    Gamescreen().run()

