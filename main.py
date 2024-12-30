import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.core.window import Window  # Import the Window class

class MyApp(App):

    def build(self):
        Window.set_title("My Kivy App")  # Set the window title
        return Label(text='Hello world')


if __name__ == '__main__':
    MyApp().run()

