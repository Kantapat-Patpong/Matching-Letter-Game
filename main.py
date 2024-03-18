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
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
import random

# คลาสสำหรับหน้า Home Screen ที่สามารถกดปุ่ม Start Game เพื่อเข้าเกม
# กดปุ่ม How to play เพื่อแสดงวิธีการเล่นเกม
# กดปุ่ม Setting sound เพื่อตั้งค่าระดับเสียงภายในเกม
class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        self.start_button = Button(text="Start Game" , font_size=50 , background_normal = 'Home_screen/00.png' , border = (0,0,0,0) ,outline_width=3 , outline_color=(0,0,0,1))
        self.start_button.bind(on_press=self.start_game)
        self.how_to_play_button = Button(text="How to play" , font_size=50 , background_normal = 'Home_screen/01.png', border = (0,0,0,0) , outline_width=3 , outline_color=(0,0,0,1))
        self.how_to_play_button.bind(on_press=self.show_how_to_play)
        self.setting_sound_button = Button(text="Setting Sound" , font_size=50 , background_normal = 'Home_screen/02.png', border = (0,0,0,0), outline_width=3 , outline_color=(0,0,0,1))
        self.setting_sound_button.bind(on_press=self.set_sound)
        layout.add_widget(self.start_button)
        layout.add_widget(self.how_to_play_button)
        layout.add_widget(self.setting_sound_button)
        self.add_widget(layout)

    # เมธอดสำหรับเปลี่ยน screen ปัจจุบันให้เป็น game screen 
    def start_game(self, instance):
        game_screen = GameScreen(name='game')
        self.manager.add_widget(game_screen)
        self.manager.current = 'game'

    # เมธอดสำหรับเปลี่ยน screen ปัจจุบันให้เป็น setting sound screen
    def set_sound(self, instance):
        self.manager.current = 'setting_sound'

    # เมธอดสำหรับเปลี่ยน screen ปัจจุบันให้เป็น how to play screen
    def show_how_to_play(self, instance):
        self.manager.current = 'how_to_play'

# คลาสสำหรับหน้า How to play screen ที่แสดงรายละเอียดวิธีการเล่นเกม
# โดยจะแสดงวิธีการเล่นเกมเป็นรูปภาพในสไลด์ผ่านการทำงานของ widget carousal
# มีปุ่ม back สำหรับย้อนกลับไปหน้า Home screen
class HowToPlayScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.back_button = Button(text="Back", size_hint_y=0.1 ,font_size=50)
        self.back_button.bind(on_press=self.back_to_home)
        self.layout.add_widget(self.back_button)
        self.carousel = Carousel(direction='right')
        self.add_slides_to_carousel()
        self.layout.add_widget(self.carousel)
        self.add_widget(self.layout)

    # เมธอดสำหรับเพิ่มรูปภาพวิธีการเล่นลงในสไลด์ผ่าน widget carousal
    def add_slides_to_carousel(self):
        slide1 = Image(source='./introduction/1.png')
        slide2 = Image(source='./introduction/2.png')
        slide3 = Image(source='./introduction/3.png')
        slide4 = Image(source='./introduction/4.png')
        slide5 = Image(source='./introduction/5.png')
        self.carousel.add_widget(slide1)
        self.carousel.add_widget(slide2)
        self.carousel.add_widget(slide3)
        self.carousel.add_widget(slide4)
        self.carousel.add_widget(slide5)

    # เมธอดสำหรับเปลี่ยน screen ปัจจุบันให้เป็น home screen
    def back_to_home(self, instance):
        self.manager.current = 'home'

# คลาสสำหรับตั้งค่าระดับเสียงภายในเกม และสร้าง object music ต่าง ๆ สำหรับใช้ภายในเกม
# สามารถปรับระดับเสียงของ background sound และสามารถปรับระดับเสียงของ effect sound
# ( effect sound ประกอบด้วยเสียงเมื่อกดถูก, เสียงเมื่อกดผิด, เสียงเมื่อเปลี่ยนด่านเพิ่มความเร็ว  และเสียงเมื่อเกมจบลง)
# โดยการกดปุ่มเครื่องหมายบวก (+) หรือ ลบ(-) เพื่อเปลี่ยนระดับเสียงทีละ 5 หน่วย (ระดับเสียงจะแสดงอยู่ในรูปร้อยละ)
# มีปุ่ม mute all สำหรับเปลี่ยนระดับเสียงของ background sound และ effect sound ให้กลายเป็น 0
# มีปุ่ม back เพื่อย้อนกลับไปยังหน้า home screen
class SettingSoundScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_music_volume = 0.5
        self.effect_volume = 0.5
        self.background_music = Music('./sound/Background.mp3')
        self.background_music.loop(True)
        self.background_music.volume(self.background_music_volume)
        self.gameover_sound = Music('./sound/gameover.mp3')
        self.gameover_sound.volume(self.effect_volume)
        self.correct_sound = Music('./sound/correct_sound.mp3')
        self.correct_sound.volume(self.effect_volume)
        self.incorrect_sound = Music('./sound/oof_soundeffect.mp3')
        self.incorrect_sound.volume(self.effect_volume)
        self.speed_increase_sound = Music('./sound/speed_increase.mp3')
        self.speed_increase_sound.volume(self.effect_volume)
        self.layout = BoxLayout(orientation='vertical')
        self.background_layout = BoxLayout(orientation='horizontal')
        self.effect_layout = BoxLayout(orientation='horizontal')
        self.background = Label(text=f'Background Sound: {self.background_music_volume*100:.0f}', font_size=25)
        self.effect = Label(text=f'Effect Sound: {self.effect_volume*100:.0f}', font_size=25)
        self.background_increase_button = Button(text="+", font_size=50)
        self.background_increase_button.bind(on_press=self.increase_background_volume)
        self.background_decrease_button = Button(text="-", font_size=50)
        self.background_decrease_button.bind(on_press=self.decrease_background_volume)
        self.effect_increase_button = Button(text="+", font_size=50)
        self.effect_increase_button.bind(on_press=self.increase_effect_volume)
        self.effect_decrease_button = Button(text="-", font_size=50)
        self.effect_decrease_button.bind(on_press=self.decrease_effect_volume)
        self.mute_button = Button(text="Mute All" , font_size=50)
        self.mute_button.bind(on_press=self.mute_all)
        self.back_button = Button(text="Back" , font_size=50)
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
        self.background_music.play()

    # เมธอดสำหรับเรียก object music ทั้งหมด
    def get_sound_objects(self):
        return self.background_music, self.correct_sound, self.incorrect_sound, self.speed_increase_sound, self.gameover_sound

    # เมธอดสำหรับเปลี่ยน screen ให้เป็น home screen
    def back_to_home(self, instance):
        self.manager.current = 'home'

    # เมธอดสำหรับเพิ่มระดับเสียงให้กับ background sound ขึ้นทีละ 0.05 หน่วย
    # ซึ่งระดับเสียงของ background sound ก่อนหน้านั้น จะต้องมีค่าไม่ถึง 1
    # และเมื่อเรียกใช้จะเล่นเสียง correct sound ขึ้นมา
    def increase_background_volume(self, instance):
        if self.background_music_volume < 1:
            self.background_music_volume += 0.05
            self.background.text = f"Background Sound: {self.background_music_volume*100:.0f}"
            self.background_music.volume(self.background_music_volume)
            self.correct_sound.play()

    # เมธอดสำหรับลดระดับเสียงให้กับ background sound ลงทีละ 0.05 หน่วย
    # ซึ่งระดับเสียงของ background sound ก่อนหน้านั้น จะต้องมีค่าประมาณทศนิยมหนึ่งตำแหน่งไม่เท่ากับ 0
    # และเมื่อเรียกใช้จะเล่นเสียง correct sound ขึ้นมา
    def decrease_background_volume(self, instance):
        if round(self.background_music_volume, 1) != 0:
            self.background_music_volume -= 0.05
            self.background.text = f"Background Sound: {self.background_music_volume*100:.0f}"
            self.background_music.volume(self.background_music_volume)
            self.correct_sound.play()
    
    # เมธอดสำหรับเพิ่มระดับเสียงให้กับ effect sound ขึ้นทีละ 0.05 หน่วย
    # ซึ่งระดับเสียงของ effect sound ก่อนหน้านั้น จะต้องมีค่าไม่ถึง 1
    # และเมื่อเรียกใช้จะเล่นเสียง correct sound ขึ้นมา
    def increase_effect_volume(self, instance):
        if self.effect_volume < 1:
            self.effect_volume += 0.05
            self.effect.text = f"Effect Sound: {self.effect_volume*100:.0f}"
            self.correct_sound.volume(self.effect_volume)
            self.incorrect_sound.volume(self.effect_volume)
            self.speed_increase_sound.volume(self.effect_volume)
            self.gameover_sound.volume(self.effect_volume)
            self.correct_sound.play()

    # เมธอดสำหรับลดระดับเสียงให้กับ effect sound ลงทีละ 0.05 หน่วย
    # ซึ่งระดับเสียงของ effect sound ก่อนหน้านั้น จะต้องมีค่าประมาณทศนิยมหนึ่งตำแหน่งไม่เท่ากับ 0
    # และเมื่อเรียกใช้จะเล่นเสียง correct sound ขึ้นมา
    def decrease_effect_volume(self, instance):
        if round(self.effect_volume, 1) != 0:
            self.effect_volume -= 0.05
            self.effect.text = f"Effect Sound: {self.effect_volume*100:.0f}"
            self.correct_sound.volume(self.effect_volume)
            self.incorrect_sound.volume(self.effect_volume)
            self.speed_increase_sound.volume(self.effect_volume)
            self.gameover_sound.volume(self.effect_volume)
            self.correct_sound.play()

    # เมธอดสำหรับตั้งค่าระดับเสียงทั้ง background sound และ effect sound ให้กลายเป็น 0
    # เมื่อระดับเสียงของตัวใดตัวหนึ่งมากกว่า 0
    def mute_all(self, instance):
        if self.background_music_volume > 0 or self.effect_volume > 0 :
            self.background_music_volume = 0
            self.effect_volume = 0
            self.background.text = f"Background Sound: {self.background_music_volume*100:.0f}"
            self.effect.text = f"Effect Sound: {self.effect_volume*100:.0f}"
            self.background_music.volume(self.background_music_volume)
            self.correct_sound.volume(self.effect_volume)
            self.incorrect_sound.volume(self.effect_volume)
            self.speed_increase_sound.volume(self.effect_volume)
            self.gameover_sound.volume(self.effect_volume)

# คลาสสำหรับหน้า game screen ที่เรียกใช้เสียง background sound และ effect sound 
# ผ่าน App ที่เรียก object music มาจาก setting sound screen
# ภายในหน้า screen มี layout หลักเป็น GridLayout 1 คอลัมน์ 2 แถว
# แถวแรกจะประกอบด้วยส่วน header ที่เป็น GridLayout มี 3 ส่วนคือ ส่วนแสดงเลขด่าน
# ส่วนแสดงคะแนน และส่วนแสดงแถบหลอดเลือด แถวที่สองจะเป็น play zone พื้นที่ GridLayout
# 7 คอลัมน์ 6 แถว ที่มีการสุ่มตัวอักษรลงในแต่ละช่อง (ความเร็วเริ่มต้นอยู่ที่ 2 วินาที)ซึ่งความเร็วที่สุ่ม
# จะเปลี่ยนไปตามเงื่อนไขของจำนวนการกดถูกตัวอักษร เมื่อกดถูกก็จะได้รับคะแนนครั้งละ 100 คะแนน
# คะแนนที่ได้รับนั้นจะคูณเพิ่มขึ้นด้วยตัวคูณที่เพิ่มมาจากการเปลี่ยนด่า (ตัวคูณเริ่มต้นเท่ากับ 1)
# แต่ถ้าหากผู้เล่นกดผิดตัวอักกษรจะลดระดับเลือดลง 1 หน่วย ซึ่งผู้เล่นจะมีระดับเลือดทั้งหมด 5 หน่วย
# object self.health เลือดของผู้เล่นนั้นจะถูกสร้างมาจากคลาส HealthBar ที่รับค่า max_health = 5
# รูปแถบเลือดปัจจุบันจะถูกดึงมาจาก attributes source ของ object self.health มนเรียกใช้ใน widget Image
# เมื่อผู้เล่นกดผิดครบ 5 ครั้ง เกมก็จะจบลงพร้อม pop up สรุปผลจำนวนครั้งที่กดถูก และจำนวนคะแนนที่ได้
# ผูกการกดคีย์บนแป้นพิมพ์กับ EventLoop.window
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_music = App.get_running_app().background_music
        self.correct_sound = App.get_running_app().correct_sound
        self.incorrect_sound = App.get_running_app().incorrect_sound
        self.speed_increase_sound = App.get_running_app().speed_increase_sound
        self.gameover_sound = App.get_running_app().gameover_sound
        self.background_music.play()
        self.layout = GridLayout(cols=1, rows=2)
        self.play_zone = self.play_table()
        self.header = GridLayout(cols=3, rows=1, size_hint_y=None)
        self.layout.add_widget(self.header)
        self.level_number = 1
        self.level_text = Label(text=f'Level {self.level_number}', font_size=50)
        self.header.add_widget(self.level_text)
        self.layout.add_widget(self.play_zone)
        self.correct_input_count = 0
        self.score = 0
        self.score_text = Label(text=f'Score : {self.score:,.0f}', font_size=50)
        self.header.add_widget(self.score_text)
        self.score_multiplier = 1
        self.game_speed = 2
        self.current_time = Clock.get_time()
        self.health = HealthBar(max_health=5)
        self.image = Image(source=self.health.source)
        self.header.add_widget(self.image)
        EventLoop.window.bind(on_key_down=self.on_key_down)
        Clock.schedule_interval(self.random_letter, self.game_speed)
        self.add_widget(self.layout)

    # เมธอดสำหรับสร้างกระดานตาราง 7 x 6 จาก Gridlayout โดยในแต่ละช่องจะใส่ widget
    # เป็น Label เพื่อรองรับการสุ่มตัวอักษรลงในช่อง (รวมทั้งหมด 42 ช่อง) และมีการใส่สีให้กับ
    # ช่อง Label จาก widget Rectangle (สร้างพื้นที่สี่เหลี่ยมมุมฉากลงใน canvas ของ Label
    # จากขนาดและตำแหน่งของ Label) และ Color (เก็บค่าสี rgba เพื่อใส่สีลงใน canvas ของ Lbael)
    # สีสำหรับใส่ให้กับช่องจะมี 2 ชุด การใส่สีแต่ละช่องนั้นจะมีการเปลี่ยนชุดสี ไม่ให้เป็นสีเดียวกับช่องที่อยู่ติดกัน
    # จะได้ผลลัพธ์การใส่สีเป็นลายตารางหมากรุก การเปลี่ยนชุดสีปัจจุบันจะทำผ่านเมธอด next_color
    # ที่เช็คค่า red ของ current_color
    def play_table(self):
        play_zone = GridLayout(cols=7, rows=6)
        self.labels = []    #List สำหรับเก็บตัวอักษรที่อยู่บนกระดานทั้งหมด ณ ปัจจุบัน
        current_color = Color(0.1, 0.1, 0.1, 1)     #สีพื้นหลังช่องแรก
        for i in range(42):
            label = Label(text='', font_size=50)    #สร้าง label โดยกำหนดเป็น string ว่างตอนเริ่มต้น
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
    
    #กำหนดตำแหน่งของ label ให้คืนค่าเดิมเมื่ออักษรนั้นถูกลบไปแล้ว
    def update_rect_pos(self, instance, value):
        for instruction in instance.canvas.before.children:
            if isinstance(instruction, Rectangle):
                instruction.pos = instance.pos
                
    #กำหนดขนาดของ label ให้คืนค่าเดิมเมื่ออักษรนั้นถูกลบไปแล้ว
    def update_rect_size(self, instance, value):
        for instruction in instance.canvas.before.children:
            if isinstance(instruction, Rectangle):
                instruction.size = instance.size

    # เมธอดสำหรับเปลี่ยนชุดสีภายในเมธอด play_table จะรับค่าเป็น curren_color ค่าชุดสีปัจจุบัน
    # จะเปลี่ยนค่าสีจากการเช็คค่า red ของ current_color ถ้ามีค่าเท่ากับ 0.1 จะใช้ชุดสีสีเทา
    # แต่ถ้าไม่จะใช้ชุดสีเทาเข้ม
    def next_color(self, current_color):
        if current_color.r == 0.1:
            return Color(0.05, 0.05, 0.05, 1)
        else:
            return Color(0.1, 0.1, 0.1, 1)

    # เมธอดสำหรับเช็คค่าตัวอักษรที่ผู้เล่นกดลงมีค่าตรงกับ text ใน Label ช่องใดหรือไม่
    # จะเก็บค่าที่ผู้เล่นกดคีย์มาเปลี่ยนไปเป็นตัวอักษรที่เป็นพิมพ์ใหญ่ และกำหนดค่า char_matched เป็น False สำหรับการเรียกใช้เมธอดทุกครั้ง
    # เพื่อใช้ในการเข้าเงื่อนไขการลดระดับเลือดของผู้เล่น ถ้า char_matched ที่ค่าเป็น False หมายถึง คีย์ที่ผู้เล่น
    # กดลงมานั้น ไม่ตรงกับ text ใน Label ใดเลย จึงจะเข้าเงื่อนไขลดเลือดได้ ภายในเงื่อนไขลดเลือด
    # จะเรียกใช้เมธอด lose_health กับ object self.health จากคลาส HealthBar ลดเลือดของผู้เล่น
    # ลง 1 หน่วย พร้อมเรียก source ของรูปแถบเลือดใหม่มาจาก self.health หลังผ่านการใช้เมธอด lose_health
    # และยังเรียกใช้เสียง effect incorrect_sound แต่ถ้าหากระดับเลือดปัจจุบันของผู้เล่นเท่า 0 จะเรียกใช้เมธอด 
    # game_over ของคลาส GameScreen การเช็คตัวอักษรจะทำผ่านลูป for เพื่อเช็คกับ text ของ Label
    # โดยจะเช็คกับ text ของ Label ที่ไม่เท่ากับสตริงเปล่า ถ้า text ของ Label ตรงกับตัวอักษรของคีย์ที่ผู้เล่นกด
    # จะทำการ set ค่า char_matched เป็น True เรียกเล่นเสียง effect correct_sound พร้อมกับเรียกใช้เมธอด
    # animate_disappear เพื่อทำให้ตัวอักษรใน Label หายไป แล้วเพิ่มจำวนครั้งการกดถูก เพิ่มจำนวนคะแนนที่ผ่านการคำนวณจากตัวคูณ
    # พร้อมเซ็ตค่า text ของ score_text ใน header ให้เป็นค่าคะแนนปัจจุบัน และเรียกใช้เมธอด change_level เพื่อเช็คเงื่อนไขการเปลี่ยนด่าน
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
                self.score_text.text = f"Score : {self.score:,.0f}"
                self.change_level_section()

        if not char_matched:
            self.health.lose_health()
            print("Health:", self.health)
            self.incorrect_sound.play()
            self.image.source = self.health.source
            if self.health.current_health == 0:
                self.game_over()

    # เมธอดสำหรับเปลี่ยนความเร็วของการสุ่มตัวอักษรที่ตัวแปร self.game_speed ที่จะเพิ่มขึ้นทีละ 0.9 เท่า
    # พร้อมเซ็ตค่าความเร็วใหม่ลงใน Clock เพื่อเรียกใช้เมธอด random_letter และเพิ่มตัวคูณคะแนนขึ้นทีละ 0.1
    # เพิ่มเลขด่านขึ้นทีละ 1 พร้อมเซ็ตค่า text ของ level_text ให้กลายเป็นเลขด่านปัจจุบัน
    def increase_speed(self):
        Clock.unschedule(self.random_letter)
        self.game_speed *= 0.9
        self.score_multiplier += 0.1
        Clock.schedule_interval(self.random_letter, self.game_speed)
        self.level_number += 1
        self.level_text.text = f"Level {self.level_number}"
        print("*******Speed increased*******")

    # เมธอดสำหรับเช็คเงื่อนไขในการเปลี่ยนด่านเพื่อเรียกใช้เมธอด increase_speed เพิ่มความเร็วของการสุ่ม
    # และเรียกใช้เสียง effect speed_increase_sound โดยที่เงื่อนไขจะแบ่งการเพิ่มความเร็วเป็น 3 ช่วง
    # ช่วงที่ 1 จะเป็นช่วงที่ level ไม่ถึง 10 และมีจำนวนการกดถูกทุก ๆ 10 ครั้ง จะเปลี่ยนด่าน
    # ช่วงที่ 2 จะเป็นช่วงที่ level เริ่มที่ 10 แต่ไม่ถึง 30 และมีจำนวนการกดถูกทุก ๆ 25 ครั้ง จะเปลี่ยนด่าน
    # ช่วงที่ 3 จะเป็นช่วงที่ level เริ่มที่ 30 ขึ้นไป และมีจำนวนการกดถูกทุก ๆ 50 ครั้ง จะเปลี่ยนด่าน
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

    # เมธอดสำหรับสุ่มตัวอักษรภาษาอังกฤษพิมพ์ใหญ่ลงใน text ของ Label โดยจะเรียกลิสต์ของ Label จาก self.labels
    # แค่ Label ที่มี text เป็นสตริงเปล่า พร้อมสุ่มตัวอักษรจาก choice ที่สร้างไว้ แล้วเรียกใช้เมธอด animate_appear
    # ถ้าหากช่อง Label ที่ว่างนั้นเหลือแค่ 1 ช่อง จะเรียกใช้เมธอด game_over
    def random_letter(self, dt):
        char = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        empty_labels = [label for label in self.labels if label.text == '']
        label = random.choice(empty_labels)
        if len(empty_labels) == 1:
            self.game_over()
        self.animate_appear(label, char)

    # เมธอดสำหรับเปลี่ยน text ของ Label ให้เป็นสตริงเปล่า
    def set_label_to_empty(self, label):
        label.text = ''

    # เมธอดสำหรับจบเกม เมื่อเเรียกใช้จะหยุดเล่น background_music ของเกม แล้วเรียกใช้เสียง effect gameover_sound
    #  เลิกผูกการกดคีย์บนแป้นพิมพ์กับ EventLoop.window ทำให้ผู้เล่นไม่สามารถเล่นเกมต่อได้ และสร้าง object Popup
    # สำหรับแสดงผลสรุปคะแนน และจำนวนครั้งที่กดถูก
    def game_over(self):
        Clock.unschedule(self.random_letter)
        background_music = self.background_music
        background_music.stop()
        self.gameover_sound.play()
        EventLoop.window.unbind(on_key_down=self.on_key_down)
        print("*******Game Over!*******")
        popup = Popup(title='Matching Letter Game', content=Label(text=f'Game Over! \nyour perfect count: {self.correct_input_count} \nyour score: {self.score:,.0f}'),
                      auto_dismiss=True, size_hint=(0.4, 0.4))
        popup.open()

    # เมธอดสำหรับสร้าง object animation เพื่อใช้ในเมธอด on_key_down ซึ่ง object นี้จะผูกกับเมธอด set_label_to_empty
    # โดยที่ animation จะเป็นการเซ็ตขนาดของ text ใน Label ให้ใหญ่ขึ้นแบบค่อย ๆ จางลง แล้วค่อย ๆ ตัวเล็กลงจนเป็น 0 และ text จะกลายเป็นสตริงเปล่า
    def animate_disappear(self, label):
        anim = Animation(font_size=label.font_size, opacity=100, duration=0)
        anim += Animation(font_size=label.font_size * 2, opacity=0, duration=0.15)
        anim += Animation(font_size=0, opacity=100, duration=0.15)
        anim.bind(on_complete=lambda *args: self.set_label_to_empty(label))
        anim.start(label)

    # เมธอดสำหรับสร้าง object animation เพื่อใช้ในเมธอด random_letter โดยที่ animation จะเป็นการเช็ตขนาดเริ่มต้นของ text ใน Label
    # ให้มีขนาด 100 แบบมองไม่เห็น แล้วค่อย ๆ ลดขนาดลงและสีทึบขึ้นเรื่อย ๆ
    def animate_appear(self, label, char):
        label.text = char
        anim = Animation(font_size=100, opacity=0, duration=0)
        anim += Animation(font_size=50, opacity=100, duration=0.25)
        anim.start(label)

# คลาสสำหรับสร้าง object music ที่มี parent เป็น SoundLoader โดยจะรับค่าเป็น path ของ sound ที่ต้องการ
class Music(SoundLoader) :
    def __init__(self,music_path):      #สร้าง object เพลง
        super().__init__()
        self.music = SoundLoader.load(music_path)
    
    # เมธอดสำหรับเล่นเสียง object music
    def play(self) :
        self.music.play()
    
    # เมธอดสำหรับหยุดเล่นเสียง object music
    def stop(self) :
        self.music.stop()
    
    # เมธอดสำหรับเปลี่ยนระดับเสียง object music โดยรับค่าระดับเสียงมาเป็นตัวเลข
    def volume(self ,loud) :
        self.music.volume = loud
    
    # เมธอดสำหรับเซ็ตให้ object music วนลูป โดยรับค่าเป็น boolean
    def loop(self,bool) :
        self.music.loop = bool

# คลาสสำหรับสร้าง object HealthBar จะรับค่า max_health เป็นตัวเลข มีการเก็บค่าเลือดปัจจุบัน 
# และเก็บ source เป็น path สำหรับการเข้าถึงรูปแถบเลือดตามระดับเลือดปัจจุบัน
class HealthBar:
    def __init__(self, max_health):
        self.max_health = max_health
        self.current_health = max_health
        self.source = './image/health_bar_5.png'

    # เมธอดสำหรับแสดงระดับเลือดปัจจุบันเป็นสตริง
    def __str__(self) -> str:
        return f"health: {self.current_health}"

    # เมธอดสำหรับลดระดับเลือดปัจจุบันลง 1 หน่วยเมื่อเลือดปัจจุบันไม่เท่ากับ 0 หน่วย 
    # และเรียกใช้เมธอด change_source เพื่อเปลี่ยนรูปแถบเลือดให้เป็นปัจจุบัน
    def lose_health(self):
        if self.current_health != 0:
            self.current_health -= 1
            self.change_source()

    # เมธอดสำหรับเปลี่ยน path รูปของแถบเลือดตามเงื่อนไขระดับเลือดปัจจุบันที่เหลืออยู่
    def change_source(self):
        if self.current_health == 4:
            self.source = './image/health_bar_4.png'
        elif self.current_health == 3:
            self.source = './image/health_bar_3.png'
        elif self.current_health == 2:
            self.source = './image/health_bar_2.png'
        elif self.current_health == 1:
            self.source = './image/health_bar_1.png'

# คลาสสำหรับจัดการเชื่อมไปยังหน้า screen ต่าง ๆ ซึ่งคลาสสร้างจาก parent App 
# และคลาสนี้จะรับ object music ที่ผ่านการตั้งค่าจาก setting sound screen
class MatchingLetterGameApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_music = None
        self.correct_sound = None
        self.incorrect_sound = None
        self.speed_increase_sound = None

    # เมธอดสำหรับสร้างตัวจัดการ screen หน้าต่าง ๆ โดยจะเพิ่ม object screen 
    # จากคลาส HomeScreen, SettingSoundScreen, HowToPlayScreen ลงในตัวจัดการ screen
    def build(self):
        screen_manager = ScreenManager()
        screen_manager.add_widget(HomeScreen(name='home'))
        self.setting_sound_screen = SettingSoundScreen(name='setting_sound')
        screen_manager.add_widget(self.setting_sound_screen)
        how_to_play_screen = HowToPlayScreen(name='how_to_play')
        screen_manager.add_widget(how_to_play_screen)
        return screen_manager
    
    # เมธอดสำหรับเรียก object music มาจาก setting sound screen
    def on_start(self):
        self.background_music, self.correct_sound, self.incorrect_sound, self.speed_increase_sound, self.gameover_sound = self.setting_sound_screen.get_sound_objects()
    
if __name__ == "__main__":
    MatchingLetterGameApp().run()