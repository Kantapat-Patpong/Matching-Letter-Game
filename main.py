import kivy
import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
import random

class GameScreen(App):
    def build(self):
        self.layout = GridLayout(cols=1, rows=2) 
        self.playzone = self.play_table()
        self.layout.add_widget(self.playzone)
        self.input = self.input_box()
        self.layout.add_widget(self.input)
        Clock.schedule_interval(self.random_letter,1)  # Schedule random_letter function to run every 3 seconds
        return self.layout

    def play_table(self):
        playzone = GridLayout(cols=6, rows=6)
        # Initialize grid with labels
        self.labels = []
        for i in range(36):
            label = Label(text='', font_size=50)
            self.labels.append(label)
            playzone.add_widget(label)
        
        return playzone
    
    def input_box(self):
        input_box = BoxLayout(size_hint_y=None, height=0.1*Window.height)
        input = TextInput(text='',multiline=True)
        input.focus=True
        input.bind(text=self.check_char)
        input_box.add_widget(input)
        return input_box

    def random_letter(self, dt):
        char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        empty_labels = [label for label in self.labels if label.text == '']
        label = random.choice(empty_labels)
        label.text = char

    def check_char(self,instance,value) :
        char_for_check = value.upper()  # Get input text and convert to uppercase for case insensitivity
        for label in self.labels:
            if label.text == char_for_check:
                label.text = ''  # Clear the label text if it matches the input text
        instance.text = ''  # Clear the input box after checking
        Clock.schedule_once(lambda dt: self.focus_input(instance))

    def focus_input(self, instance):
        instance.focus = True  # Set focus back to the input box

if __name__ == "__main__":
    GameScreen().run()

