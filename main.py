from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Rectangle, Color
from kivy.uix.checkbox import CheckBox

Builder.load_string("""
<StartScreen>:
    name: 'start'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation:'horizontal'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'Развернуть Dallas Lock сейчас'
            on_press: root.manager.current = 'deploy'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'Настроить ожидание сборки'
            on_press: root.manager.current = 'waitsettings'

<DeployScreen>:
    name: 'deploy'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation:'horizontal'
        Button:
            text: 'Выбрать список ОС для установки'
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'setos'
        Button:
            text: 'Вернуться начальному экрану'
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'start'
            
<WaitSettingsScreen>:
    name: 'waitsettings'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'setwait'
            text: 'Настроить параметры ожидания'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'Назад в главное меню'
            on_press: root.manager.current = 'start'
<SetOsScreen>
    name: 'setos'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'start'
            text: 'Запустить установку Dallas Locks'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'В главное меню'
            on_press: root.manager.current = 'start'
<SetWaitScreen>
    name: 'sewait'
    canvas:
        Color:
            rgba: 1, 1, 1, 1   
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            on_press: root.manager.current = 'start'
            text: 'Запустить ожидание Dallas Lock'
        Button:
            size_hint: 0.3, 0.3
            pos_hint: {"x":0.25, "top":0.6}
            text: 'В главное меню'
            on_press: root.manager.current = 'start'
""")

class Display(BoxLayout):
    pass

class StartScreen(Screen):
    pass

class DeployScreen(Screen):
    pass

class WaitSettingsScreen(Screen):
    pass

class SetOsScreen(Screen):
    pass

class SetWaitScreen(Screen):
    pass


class DallasLockConfiguratorApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(DeployScreen(name='deploy'))
        sm.add_widget(WaitSettingsScreen(name='waitsettings'))
        sm.add_widget(SetOsScreen(name='setos'))
        sm.add_widget(SetWaitScreen(name='setwait'))
        return sm


if __name__ == '__main__':
    DallasLockConfiguratorApp().run()