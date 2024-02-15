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
        self.correct_input_count = 0
        Clock.schedule_interval(self.random_letter,3)  # Schedule random_letter function to run every 3 seconds
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
        if len(empty_labels) == 1:
            self.game_over()
        label.text = char

    def check_char(self,instance,value) :
        
        char_for_check = value.upper()
        for label in self.labels:
            if label.text == char_for_check:
                label.text = ''
                print(self.correct_input_count)
                self.correct_input_count += 1
                if self.correct_input_count == 10:
                    self.increase_speed()
        instance.text = ''
        Clock.schedule_once(lambda dt: self.focus_input(instance))

    def focus_input(self, instance):
        instance.focus = True  # Set focus back to the input box

    def increase_speed(self):
        Clock.unschedule(self.random_letter)
        Clock.schedule_interval(self.random_letter, 1)
        print("Speed increased")

    def game_over(self):
        self.input.disabled = True
        Clock.unschedule(self.random_letter)
        print("Game Over!")

if __name__ == "__main__":
    GameScreen().run()

