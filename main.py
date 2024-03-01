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
import random

class GameScreen(App):
    def build(self):
        self.layout = GridLayout(cols=1, rows=3) 
        self.play_zone = self.play_table()
        self.layout.add_widget(self.play_zone)
        self.input = self.input_box()
        self.layout.add_widget(self.input)
        self.correct_input_count = 0
        self.score = 0
        self.score_multiplier = 1
        self.game_speed = 2
        self.level_zone = BoxLayout(size=(300, 300))
        self.input.add_widget(self.level_zone)
        self.level_number = 1
        self.level_text = Label(text=f'Level {self.level_number}', font_size=50)
        self.level_zone.add_widget(self.level_text)
        self.background_music = music('./sound/Background.mp3')
        self.background_music.volume(0.5)
        self.background_music.play()
        self.correct_sound = music('./sound/correct_sound.mp3')
        self.correct_sound.volume(0.2)
        self.speed_increase_sound = music('./sound/speed_increase.mp3')
        Clock.schedule_interval(self.random_letter,self.game_speed)
        return self.layout

    def play_table(self):
        play_zone = GridLayout(cols=6, rows=6)
        self.labels = []
        for i in range(36):
            label = Label(text='', font_size=50)
            self.labels.append(label)
            play_zone.add_widget(label)
        return play_zone
    
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
        char_for_check = value.upper()
        for label in self.labels:
            if label.text == char_for_check and label.text != '':
                self.correct_sound.play()
                self.animate_disappear(label)
                self.correct_input_count += 1
                self.score += (100 * self.score_multiplier)
                if self.correct_input_count % 10 == 0 and self.correct_input_count != 0:
                    self.speed_increase_sound.play()
                    self.increase_speed()

        instance.text = ''
        Clock.schedule_once(lambda dt: self.focus_input(instance))
    
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

class music(SoundLoader) :
    def __init__(self,music_path):
        super().__init__()
        self.music = SoundLoader.load(music_path)
        
    def play(self) :
        self.music.play()
        
    def stop(self) :
        self.music.stop()
        
    def volume(self ,loud) :
        self.music.volume = loud

if __name__ == "__main__":
    GameScreen().run()

