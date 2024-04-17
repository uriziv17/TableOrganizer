import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView;
from kivy.uix.image import Image
from kivy.uix.popup import Popup
import shutil

class ImageUpload(App):
    ConfirmPopup = Popup(title='Confirmation', content=BoxLayout(orientation='vertical', spacing=10),
                         size_hint=(None, None), size=(400, 300))
    def loadingScreen(self, instance):
        self.ConfirmPopup.dismiss()
        self.layout.clear_widgets()
        self.loadingLabel = Label(text="Thanks, give me a second to think", size_hint=(1, 0.2))
        self.layout.add_widget(self.loadingLabel)

    def uploadImage(self, instance):
        selectedFile = self.fileChooser.selection and self.fileChooser.selection[0] or none
        if selectedFile:
            destination = 'uploaded_image.jpg'
            shutil.copy(selectedFile, destination)
            selectedImage = Image(source=destination, size_hint=(1,1))
            #self.layout.add_widget(selectedImage)

            self.confLabel = Label(text='is this your table?',size_hint = (None, None), size = (300, 150))
            self.ConfirmPopup.content.add_widget(self.confLabel)
            self.ConfirmPopup.content.add_widget(selectedImage)
            self.ConfirmPopup.content.add_widget(Button(text='Yes', size_hint=(1, 0.1), on_press=self.loadingScreen))
            self.ConfirmPopup.open()
        else:
            error_popup = Popup(title='Error', content=Label(text='Please select an image to upload.'),
                                size_hint=(None, None), size=(300, 150))
            error_popup.open()

    def chooseImage(self, instance):
        self.layout.clear_widgets()
        self.fileChooser = FileChooserIconView()
        self.layout.add_widget(self.fileChooser)
        self.uploadButton = Button(text='choose photo', size_hint=(None, None), size=(300, 150))
        self.uploadButton.bind(on_press=self.uploadImage)
        self.layout.add_widget(self.uploadButton)

    def build(self):
        self.layout = BoxLayout(orientation='vertical', spacing=10)
        self.welcomeLabel = Label(text="Hey, I\'m here to help you \n please uplaod your table", size_hint=(1,0.2))
        self.layout.add_widget(self.welcomeLabel)
        self.chooseButton = Button(text="Choose Image", size_hint=(1,0.1))
        self.chooseButton.bind(on_press=self.chooseImage)
        self.layout.add_widget(self.chooseButton)

        return self.layout



if __name__ == "__main__":
    ImageUpload().run()