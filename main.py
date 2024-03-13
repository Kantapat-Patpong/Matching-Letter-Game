import kivy
import time
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.core.audio import SoundLoader
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color,Rectangle
from kivy.uix.image import Image
import random

class GameScreen(App):
    def build(self):
        self.layout = GridLayout(cols=1, rows=4) 
        self.play_zone = self.play_table()
        self.level_zone = BoxLayout(size_hint_y=None, height=50)
        self.layout.add_widget(self.level_zone)
        self.level_number = 1
        self.level_text = Label(text=f'Level {self.level_number}', font_size=50)
        self.level_zone.add_widget(self.level_text)
        self.layout.add_widget(self.play_zone)
        self.input = self.input_box()
        self.layout.add_widget(self.input)
        self.correct_input_count = 0
        self.score = 0
        self.score_multiplier = 1
        self.game_speed = 2
        self.current_time = Clock.get_time()
        
        self.background_music = Music('./sound/Background.mp3')
        self.background_music.volume(0.5)
        self.background_music.play()
        self.correct_sound = Music('./sound/correct_sound.mp3')
        self.correct_sound.volume(0.2)
        self.speed_increase_sound = Music('./sound/speed_increase.mp3')
        self.health = HealthBar(max_health=5)
        Clock.schedule_interval(self.random_letter,self.game_speed)
        return self.layout

    def play_table(self):
        play_zone = GridLayout(cols=7, rows=6)
        self.labels = []
        current_color = Color(0.1, 0.1, 0.1, 1)
        for i in range(42):
            label = Label(text='', font_size=50) #pls add some background color here
            self.labels.append(label)
            rect = Rectangle(pos=label.pos, size=label.size)
            rect_color = Color(current_color.r, current_color.g, current_color.b, 1)
            label.canvas.before.add(rect_color)  # Set the background color (RGBA values)
            label.canvas.before.add(rect)
            label.bind(pos=self.update_rect_pos)  # Bind the label's position update to update the rectangle's position
            label.bind(size=self.update_rect_size)  # Bind the label's size update to update the rectangle's size
            play_zone.add_widget(label)
            current_color = self.next_color(current_color)
        return play_zone
    
    def update_rect_pos(self, instance, value):
        for instruction in instance.canvas.before.children:
            if isinstance(instruction, Rectangle):
                instruction.pos = instance.pos  # Update the position of the rectangle when the label's position changes

    def update_rect_size(self, instance, value):
        for instruction in instance.canvas.before.children:
            if isinstance(instruction, Rectangle):
                instruction.size = instance.size  # Update the size of the rectangle when the label's size changes
    
    def next_color(self, current_color):
        # Function to switch between two colors
        if current_color.r == 0.1:  # If current color is the initial color
            return Color(0.05, 0.05, 0.05, 1)  # Switch to the alternate color
        else:
            return Color(0.1, 0.1, 0.1, 1)  # Switch back to the initial color
        
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
        self.animate_appear(label,char)

    def check_char(self,instance,value) :
        if value != '' :
            dt = Clock.get_time() - self.current_time
            print("dt =" , dt)
            self.current_time = Clock.get_time()
            print("current time = ",self.current_time)
            if dt < 0.25 :
                print("disable")
                self.input.disabled = True
                Clock.schedule_once(self.enable_input,2)
            char_for_check = value.upper()
            char_matched = False
            for label in self.labels:
                if label.text == char_for_check and label.text != '':
                    self.correct_sound.play()
                    self.animate_disappear(label)
                    self.correct_input_count += 1
                    self.score += (100 * self.score_multiplier)
                    char_matched = True
                    if self.correct_input_count % 10 == 0 and self.correct_input_count != 0:
                        self.speed_increase_sound.play()
                        self.increase_speed()
                        
            instance.text = ''
            Clock.schedule_once(lambda dt: self.focus_input(instance))
            
            if not char_matched:
                self.health.lose_health()
                print("Health:", self.health)
                if self.health.current_health == 0:
                    self.game_over()
        else :
            pass

    def enable_input(self,dt) :
        self.input.disabled = False
        self.focus_input(self.input)
    
    def set_label_to_empty(self, label):
        label.text = ''
    
    def focus_input(self, instance):
        instance.focus = True

    def increase_speed(self):
        Clock.unschedule(self.random_letter)
        self.game_speed *= 0.9
        self.score_multiplier += 0.1
        Clock.schedule_interval(self.random_letter, self.game_speed)
        self.level_number += 1
        self.level_text.text = f"Level {self.level_number}"
        print("*******Speed increased*******")

    def game_over(self):
        self.input.disabled = True
        Clock.unschedule(self.random_letter)
        background_music = self.background_music
        background_music.stop()
        print("*******Game Over!*******")
        popup = Popup(title='Matching Letter Game', content=Label(text=f'Game Over! \ncorrect input count: {self.correct_input_count} \nyour score: {self.score}'),
                auto_dismiss=True, size_hint=(0.4, 0.4))
        popup.open()

    def animate_disappear(self, label) :
        anim = Animation(font_size=label.font_size, opacity=100, duration=0)
        anim += Animation(font_size=label.font_size*2, opacity=0, duration=0.15)

        anim.bind(on_complete=lambda *args: self.set_label_to_empty(label))
        anim.start(label)

    def animate_appear(self, label ,char) :
        label.text = char
        anim = Animation(font_size=100, opacity=0,duration=0) 
        anim += Animation(font_size=50, opacity=100, duration=0.25)
        anim.start(label)

class Music(SoundLoader) :
    def __init__(self,music_path):
        super().__init__()
        self.music = SoundLoader.load(music_path)
        
    def play(self) :
        self.music.play()
        
    def stop(self) :
        self.music.stop()
        
    def volume(self ,loud) :
        self.music.volume = loud

class HealthBar:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health

    def __str__(self) -> str:
        return f"health: {self.current_health}"

    def lose_health(self):
        if self.current_health != 0:
            self.current_health -= 1


if __name__ == "__main__":
    GameScreen().run()

