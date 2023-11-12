from threading import Thread

import kivy
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label


class FileDownloaderApp(App):
    def build(self):
        self.layout = BoxLayout(orientation="vertical")

        self.label = Label(text="Click the button to download a file.")
        self.layout.add_widget(self.label)

        self.button = Button(text="Download File", on_press=self.download_file)
        self.layout.add_widget(self.button)

        return self.layout

    def download_file(self, instance):
        # Replace the URL with the actual URL of the file you want to download
        file_url = "https://example.com/sample_file.txt"

        # Create a separate thread to avoid blocking the UI
        download_thread = Thread(target=self._download_file, args=(file_url,))
        download_thread.start()

    def _download_file(self, file_url):
        try:
            response = requests.get(file_url, stream=True)

            # Replace "sample_file.txt" with the desired file name
            with open("sample_file.txt", "wb") as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)

            self.label.text = "File downloaded successfully!"
        except Exception as e:
            self.label.text = f"Error downloading file: {str(e)}"


if __name__ == "__main__":
    FileDownloaderApp().run()
