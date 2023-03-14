import os
import shutil
import random
from kivy.config import Config
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.graphics import Color, Rectangle
from kivy.uix.image import AsyncImage
from PIL import Image, ImageDraw as PILImage
from kivy.uix.label import Label


class MyBoxLayout(BoxLayout):
    def __init__(self, **kwargs):
        # disabling some random function that creates an orange dot when you right-click
        Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
        super(MyBoxLayout, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 20
        self.Ascent_image_background = AsyncImage(source="Crosshair backgrounds/Ascent.PNG")
        self.Icebox_image_background = AsyncImage(source="Crosshair backgrounds/Icebox.PNG")
        self.hex_Code_Color = "N/A"
        self.hex_Code_label = Label(text=self.hex_Code_Color, pos=(0, 0))

        # Add the canvas.before instruction to set the background color
        with self.canvas.before:
            Color(0.89, 0.85, 0.79, 1)  # Set the color to bone white
            self.rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect)

        # Buttons on main screen
        Crosshair_color_button = Button(text='Crosshair colors', size_hint=(0.15, .2))
        Crosshair_color_button.bind(on_press=self.show_crosshair_colors_screen)
        show_saved_Crosshair_Colors = Button(text='saved_Crosshair_Colors', size_hint=(0.4, .2))
        show_saved_Crosshair_Colors.bind(on_press=self.show_saved_Crosshair_Colors)
        Line_ups_button = Button(text='Line ups', size_hint=(0.15, .2))
        View_lobby_button = Button(text='View lobby', size_hint=(0.15, .2))

        # Add the buttons to the layout
        self.add_widget(Crosshair_color_button)
        self.add_widget(Line_ups_button)
        self.add_widget(View_lobby_button)
        self.add_widget(show_saved_Crosshair_Colors)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    # Second screen with Crosshair color generator
    def show_crosshair_colors_screen(self, *args):
        # Create a new screen to show the crosshair colors
        crosshair_colors_screen = Screen(name='crosshair_colors')

        # Back button
        Back_button = Button(text='Back', size_hint=(0.2, .15), on_press=self.go_back)
        crosshair_colors_screen.add_widget(Back_button)

        # Add an Ascent Image widget
        self.Ascent_image_background.pos = (75, 400)
        self.Ascent_image_background.size_hint = (.3, .3)
        crosshair_colors_screen.add_widget(self.Ascent_image_background)

        # Add an Icebox Image widget
        self.Icebox_image_background.pos = (500, 400)
        self.Icebox_image_background.size_hint = (.3, .3)
        crosshair_colors_screen.add_widget(self.Icebox_image_background)

        # Generate new crosshair color button
        generate_New_Crosshair_color_button = Button(text='Generate', size_hint=(0.2, .15), pos=(300, 0))
        crosshair_colors_screen.add_widget(generate_New_Crosshair_color_button)
        generate_New_Crosshair_color_button.bind(on_press=self.on_button_press)

        # Save button
        save_Crosshair_color = Button(text='Save', size_hint=(0.15, .15), pos=(600, 0))
        crosshair_colors_screen.add_widget(save_Crosshair_color)
        save_Crosshair_color.bind(on_press=self.saveCrosshair)

        # show hexcode for the color
        self.hex_Code_label.color = [1, 1, 1, 1]
        crosshair_colors_screen.add_widget(self.hex_Code_label)

        # Switch to the new screen using the ScreenManager
        sm = App.get_running_app().root
        sm.add_widget(crosshair_colors_screen)
        sm.current = 'crosshair_colors'

    # generate button functionality
    def on_button_press(self, button):
        self.generate_new_crosshair_color()
        self.Ascent_image_background.reload()
        self.Icebox_image_background.reload()
        self.hex_Code_label.text = self.hex_Code_Color

    # back button functionality
    def go_back(self, *args):
        # Switch back to the main screen using the ScreenManager
        sm = App.get_running_app().root
        sm.current = 'main'

    def generate_new_crosshair_color(self, *args):
        map_Images = ["Ascent.PNG", "Icebox.PNG"]

        # Generates the random color to be applied to photos
        maxRed = random.randint(0, 255)
        maxGreen = random.randint(0, 255)
        maxBlue = random.randint(0, 255)

        for Images in map_Images:
            # Open the image file
            image = Image.open(Images)

            # Get the size of the image
            width = image.width
            height = image.height

            # Create a new image with the same size as the original
            new_image = Image.new("RGB", (width, height), (255, 255, 255))

            # Paste the original image onto the new image
            new_image.paste(image, (0, 0))

            draw = PILImage.Draw(new_image)
            center_x = width // 2
            center_y = height // 2
            radius = 5
            color = (maxRed, maxGreen, maxBlue)  # Change the color to the desired color
            draw.ellipse((center_x - radius, center_y - radius, center_x + radius, center_y + radius), fill=color)

            # Set the image source of the Image widget
            new_image_name = "Crosshair backgrounds/" + Images
            new_image.save(new_image_name)
            rgb = (maxRed, maxGreen, maxBlue)
            hex_value = str('#{:02x}{:02x}{:02x}'.format(*rgb))
            self.hex_Code_Color = hex_value
            image.close()

    def saveCrosshair(self, *args):
        # writing the hex codes to a text file
        color_Code = "\n" + self.hex_Code_Color
        opened_File_Crosshair_codes = open("Saved Crosshair Colors.txt", "a")
        opened_File_Crosshair_codes.write(color_Code)
        opened_File_Crosshair_codes.close()

        # Define the source and destination folders
        source_folder = 'Crosshair backgrounds'
        destination_folder = 'Saved Crosshair Screenshots'

        # Create the destination folder if it does not exist
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        # Loop through all files in the source folder
        for filename in os.listdir(source_folder):
            # Check if the file is a PNG
            if filename.endswith('.PNG'):
                # Construct the full path of the source and destination files
                source_file = os.path.join(source_folder, filename)
                destination_file = os.path.join(destination_folder, filename)
                # Check if the destination file already exists
                if os.path.exists(destination_file):
                    # Append a counter to the filename
                    counter = 0
                    while True:
                        new_destination_file = os.path.join(destination_folder,
                                                            f"{os.path.splitext(filename)[0]}_{counter}.png")
                        if os.path.exists(new_destination_file):
                            counter += 1
                        else:
                            destination_file = new_destination_file
                            break
                # Copy the source file to the destination folder
                shutil.copy(source_file, destination_file)



    # Screen which shows the saved crosshair colors and their respective hex codes
    def show_saved_Crosshair_Colors(self, *args):
        # Create a new screen to show the crosshair colors
        show_saved_Crosshair_Colors = Screen(name='saved_Crosshair_Colors')

        # Switch to the new screen using the ScreenManager
        sm = App.get_running_app().root
        sm.add_widget(show_saved_Crosshair_Colors)
        sm.current = 'saved_Crosshair_Colors'


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
