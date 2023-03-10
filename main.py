import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.image import AsyncImage
from PIL import Image, ImageDraw as PILImage


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        self.Ascent_image_background = AsyncImage(source="Crosshair backgrounds/Ascent.PNG")


        # Add the canvas.before instruction to set the background color
        with self.canvas.before:
            Color(0.89, 0.85, 0.79, 1)  # Set the color to bone white
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Three main buttons
        Crosshair_color_button = Button(text='Crosshair colors', size_hint=(0.15, .2))
        Crosshair_color_button.bind(on_press=self.show_crosshair_colors_screen)
        Line_ups_button = Button(text='Line ups', size_hint=(0.15, .2))
        View_lobby_button = Button(text='View lobby', size_hint=(0.15, .2))

        # Add the buttons to the layout
        self.add_widget(Crosshair_color_button)
        self.add_widget(Line_ups_button)
        self.add_widget(View_lobby_button)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def show_crosshair_colors_screen(self, *args):
        # Create a new screen to show the crosshair colors
        crosshair_colors_screen = Screen(name='crosshair_colors')

        # Back button
        Back_button = Button(text='Back', size_hint=(0.2, .15), on_press=self.go_back)
        crosshair_colors_screen.add_widget(Back_button)

        # Add an Image widget
        self.Ascent_image_background.pos = (75, 400)
        self.Ascent_image_background.size_hint = (.3, .3)
        crosshair_colors_screen.add_widget(self.Ascent_image_background)

        # Generate new crosshair color
        generate_New_Crosshair_color_button = Button(text='Generate', size_hint=(0.2, .15), pos=(300, 0))
        crosshair_colors_screen.add_widget(generate_New_Crosshair_color_button)
        generate_New_Crosshair_color_button.bind(on_press=self.on_button_press)

        # Switch to the new screen using the ScreenManager
        sm = App.get_running_app().root
        sm.add_widget(crosshair_colors_screen)
        sm.current = 'crosshair_colors'

    # generate button functionality
    def on_button_press(self, button):
        self.generate_new_crosshair_color()
        self.Ascent_image_background.reload()

    # back button functionality
    def go_back(self, *args):
        # Switch back to the main screen using the ScreenManager
        sm = App.get_running_app().root
        sm.current = 'main'


    def generate_new_crosshair_color(self, *args):
        # Open the image file
        image = Image.open("Ascent.PNG")

        # Get the size of the image
        width = image.width
        height = image.height

        # Create a new image with the same size as the original
        new_image = Image.new("RGB", (width, height), (255, 255, 255))

        # Paste the original image onto the new image
        new_image.paste(image, (0, 0))

        # Draw a circle in the center of the image
        maxRed = random.randint(0, 255)
        maxGreen = random.randint(0, 255)
        maxBlue = random.randint(0, 255)
        draw = PILImage.Draw(new_image)
        center_x = width // 2
        center_y = height // 2
        radius = 5
        color = (maxRed, maxGreen, maxBlue)  # Change the color to the desired color
        draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=color)

        # Set the image source of the Image widget
        new_image.save("Crosshair backgrounds/Ascent.PNG")

        rgb = (maxRed, maxGreen, maxBlue)
        hex_value = '#{:02x}{:02x}{:02x}'.format(*rgb)
        print(hex_value)
        # Display the image

        #new_image.show()


class MyApp(App):
    def build(self):
        # Create a ScreenManager to manage the screens
        sm = ScreenManager()
        main_screen = Screen(name='main')
        main_screen.add_widget(MyBoxLayout())
        sm.add_widget(main_screen)
        return sm


if __name__ == '__main__':
    MyApp().run()
