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
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.base import EventLoop
import random

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.start_button = Button(text="Start Game")
        self.start_button.bind(on_press=self.start_game)
        self.setting_sound_button = Button(text="Setting Sound")
        self.setting_sound_button.bind(on_press=self.set_sound)
        layout.add_widget(self.start_button)
        layout.add_widget(self.setting_sound_button)
        self.add_widget(layout)

    def start_game(self, instance):
        game_screen = GameScreen(name='game')
        self.manager.add_widget(game_screen)
        self.manager.current = 'game'

    def set_sound(self, instance):
        self.manager.current = 'setting_sound'

class SettingSoundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_music_volume = 0.5
        self.effect_volume = 0.5
        self.background_music = Music('./sound/Background.mp3')
        self.background_music.volume(self.background_music_volume)
        self.correct_sound = Music('./sound/correct_sound.mp3')
        self.correct_sound.volume(self.effect_volume)
        self.incorrect_sound = Music('./sound/oof_soundeffect.mp3')
        self.incorrect_sound.volume(self.effect_volume)
        self.speed_increase_sound = Music('./sound/speed_increase.mp3')
        self.speed_increase_sound.volume(self.effect_volume)
        self.layout = BoxLayout(orientation='vertical')
        self.background_layout = BoxLayout(orientation='horizontal')
        self.effect_layout = BoxLayout(orientation='horizontal')
        self.background = TextInput()
        self.effect = TextInput()
        self.background_increase_button = Button(text="+")
        self.background_increase_button.bind(on_press=self.back_to_home)
        self.background_decrease_button = Button(text="-")
        self.background_decrease_button.bind(on_press=self.back_to_home)
        self.effect_increase_button = Button(text="+")
        self.effect_increase_button.bind(on_press=self.back_to_home)
        self.effect_decrease_button = Button(text="-")
        self.effect_decrease_button.bind(on_press=self.back_to_home)
        self.mute_button = Button(text="Mute All")
        self.mute_button.bind(on_press=self.back_to_home)
        self.back_button = Button(text="Back")
        self.back_button.bind(on_press=self.back_to_home)
        self.background_layout.add_widget(self.background_decrease_button)
        self.effect_layout.add_widget(self.effect_decrease_button)
        self.background_layout.add_widget(self.background)
        self.effect_layout.add_widget(self.effect)
        self.background_layout.add_widget(self.background_increase_button)
        self.effect_layout.add_widget(self.effect_increase_button)
        self.layout.add_widget(self.background_layout)
        self.layout.add_widget(self.effect_layout)
        self.layout.add_widget(self.mute_button)
        self.layout.add_widget(self.back_button)
        self.add_widget(self.layout)

    def back_to_home(self, instance):
        self.manager.current = 'home'

    def change_volume(self):
        pass

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = GridLayout(cols=1, rows=4)
        self.play_zone = self.play_table()
        self.header = GridLayout(cols=3, rows=1, size_hint_y=None)
        self.layout.add_widget(self.header)
        self.level_number = 1
        self.level_text = Label(text=f'Level {self.level_number}', font_size=50)
        self.header.add_widget(self.level_text)
        self.layout.add_widget(self.play_zone)
        self.correct_input_count = 0
        self.score = 0
        self.score_text = Label(text=f'Score : {self.score}', font_size=50)
        self.header.add_widget(self.score_text)
        self.score_multiplier = 1
        self.game_speed = 2
        self.current_time = Clock.get_time()
        self.background_music = Music('./sound/Background.mp3')
        self.background_music.volume(0.5)
        self.background_music.play()
        self.correct_sound = Music('./sound/correct_sound.mp3')
        self.correct_sound.volume(0.2)
        self.incorrect_sound = Music('./sound/oof_soundeffect.mp3')
        self.incorrect_sound.volume(1)
        self.speed_increase_sound = Music('./sound/speed_increase.mp3')
        self.health = HealthBar(max_health=5)
        self.image = Image(source=self.health.source)
        self.header.add_widget(self.image)
        EventLoop.window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.random_letter, self.game_speed)
        self.add_widget(self.layout)

    def play_table(self):
        play_zone = GridLayout(cols=7, rows=6)
        self.labels = []
        current_color = Color(0.1, 0.1, 0.1, 1)
        for i in range(42):
            label = Label(text='', font_size=50)
            self.labels.append(label)
            rect = Rectangle(pos=label.pos, size=label.size)
            rect_color = Color(current_color.r, current_color.g, current_color.b, 1)
            label.canvas.before.add(rect_color)
            label.canvas.before.add(rect)
            label.bind(pos=self.update_rect_pos)
            label.bind(size=self.update_rect_size)
            play_zone.add_widget(label)
            current_color = self.next_color(current_color)
        return play_zone

    def update_rect_pos(self, instance, value):
        for instruction in instance.canvas.before.children:
            if isinstance(instruction, Rectangle):
                instruction.pos = instance.pos

    def update_rect_size(self, instance, value):
        for instruction in instance.canvas.before.children:
            if isinstance(instruction, Rectangle):
                instruction.size = instance.size

    def next_color(self, current_color):
        if current_color.r == 0.1:
            return Color(0.05, 0.05, 0.05, 1)
        else:
            return Color(0.1, 0.1, 0.1, 1)

    def on_key_down(self, window, key, *args):
        char = chr(key).upper()
        char_matched = False
        for label in self.labels:
            if label.text == char and label.text != '':
                char_matched = True
                self.correct_sound.play()
                self.animate_disappear(label)
                self.correct_input_count += 1
                self.score += (100 * self.score_multiplier)
                self.score_text.text = f"Score : {self.score:.0f}"
                self.change_level()

        if not char_matched:
            self.health.lose_health()
            print("Health:", self.health)
            self.incorrect_sound.play()
            self.image.source = self.health.source
            if self.health.current_health == 0:
                self.game_over()

    def increase_speed(self):
        Clock.unschedule(self.random_letter)
        self.game_speed *= 0.9
        self.score_multiplier += 0.1
        Clock.schedule_interval(self.random_letter, self.game_speed)
        self.level_number += 1
        self.level_text.text = f"Level {self.level_number}"
        print("*******Speed increased*******")

    def change_level(self):
        if self.correct_input_count % 10 == 0 and self.correct_input_count != 0 and self.level_number < 10:
            self.speed_increase_sound.play()
            self.increase_speed()
        elif self.correct_input_count % 25 == 0 and self.correct_input_count != 0 and 10 <= self.level_number < 30:
            self.speed_increase_sound.play()
            self.increase_speed()
        elif self.correct_input_count % 50 == 0 and self.correct_input_count != 0 and 30 <= self.level_number:
            self.speed_increase_sound.play()
            self.increase_speed()

    def random_letter(self, dt):
        char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        empty_labels = [label for label in self.labels if label.text == '']
        label = random.choice(empty_labels)
        if len(empty_labels) == 1:
            self.game_over()
        self.animate_appear(label, char)

    def set_label_to_empty(self, label):
        label.text = ''

    def game_over(self):
        Clock.unschedule(self.random_letter)
        background_music = self.background_music
        background_music.stop()
        EventLoop.window.unbind(on_key_down=self.on_key_down)
        print("*******Game Over!*******")
        popup = Popup(title='Matching Letter Game', content=Label(text=f'Game Over! \ncorrect input count: {self.correct_input_count} \nyour score: {self.score}'),
                      auto_dismiss=True, size_hint=(0.4, 0.4))
        popup.open()

    def animate_disappear(self, label):
        anim = Animation(font_size=label.font_size, opacity=100, duration=0)
        anim += Animation(font_size=label.font_size * 2, opacity=0, duration=0.15)
        anim += Animation(font_size=0, opacity=100, duration=0.15)
        anim.bind(on_complete=lambda *args: self.set_label_to_empty(label))
        anim.start(label)

    def animate_appear(self, label, char):
        label.text = char
        anim = Animation(font_size=100, opacity=0, duration=0)
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
        self.source = './image/health_bar_5.png'

    def __str__(self) -> str:
        return f"health: {self.current_health}"

    def lose_health(self):
        if self.current_health != 0:
            self.current_health -= 1
            self.change_source()

    def change_source(self):
        if self.current_health == 4:
            self.source = './image/health_bar_4.png'
        elif self.current_health == 3:
            self.source = './image/health_bar_3.png'
        elif self.current_health == 2:
            self.source = './image/health_bar_2.png'
        elif self.current_health == 1:
            self.source = './image/health_bar_1.png'

class MatchingLetterGameApp(App):
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name='home'))
        setting_sound_screen = SettingSoundScreen(name='setting_sound')
        screen_manager.add_widget(setting_sound_screen)
        return screen_manager
    
if __name__ == "__main__":
    MatchingLetterGameApp().run()