import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scatter import Scatter
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import pandas as pd
from kivy.properties import ListProperty
from kivy.graphics.vertex_instructions import (Rectangle,
                                               Ellipse,
                                               Line)
from kivy.graphics.context_instructions import Color
import random

def getRandomWord():
    """ Return a random word """
    data = pd.read_csv("words.txt")
    random_word = data.sample(n=1)
    random_word = (random_word.iloc[0]['words'])

    return random_word

class HangMan(App):
    def build(self):
        self.random_word = getRandomWord()
        self.count_attempts = 0
        self.count_corrects = 0
        self.max_attempts = 6

        b = BoxLayout(orientation='vertical')
        t = TextInput(text='',
                      font_size=150,
                      size_hint_y=None,
                      height=200,
                      multiline=False)
        f = FloatLayout()
        s = Scatter()
        l = Label(text='',
                  font_size=70)
        l.color = (1,0,0,1)

        b.add_widget(t)
        b.add_widget(l)

        b2 = BoxLayout(orientation='vertical')
        l2 = Label(text='What word?', font_size=100)
        b2.add_widget(l2)

        b.add_widget(b2)

        self.found_letters = []
        for i in range(0,len(self.random_word)):
            self.found_letters.append('_')

        self.found_str = "".join(self.found_letters)

        l.text = self.found_str
        
        def callback(instance, value):
            self.random_word = getRandomWord()
            self.count_attempts = 0
            self.count_corrects = 0
            self.found_letters = []
            for i in range(0,len(self.random_word)):
                self.found_letters.append('_')

            self.found_str = "".join(self.found_letters)
            l.text = self.found_str
            t.text = ''

        restart_button = Button(text='Restart?')
        restart_button.bind(state=callback)
        b.add_widget(restart_button)

        def on_text(instance, value):
            if(len(t.text)>0):
                letter = t.text[-1]
                if letter not in self.random_word:
                    self.count_attempts += 1
                    l2.text = str(self.count_attempts)

                else:
                    for i in range(0,len(self.random_word)):
                        if self.random_word[i] == letter:
                            self.found_letters[i] = letter
                            self.count_corrects += 1

                    self.found_str = "".join(self.found_letters)
                    l.text = self.found_str
                    

                if (self.count_corrects == len(self.random_word)):
                    l.font_size = 20
                    l.text = f"Congratulation you won! The word is {self.random_word}"

                if(self.count_attempts == self.max_attempts):
                    l2.font_size = 20
                    l2.text = f"Game Over the correct answer was {self.random_word}"

        t.bind(text=on_text)
        return b

if __name__ == "__main__":
    HangMan().run()