import time
import schedule
import threading
from tkinter import *
from playsound import playsound
from PIL import Image, ImageTk


class App(Frame):
    gif_path = "assets/kuru_kuru_herta.gif"
    mp3_path = "assets/kuru_kuru_herta.mp3"

    def __init__(self, root):
        super().__init__(root, bg="WHITE")

        self.main_frame = self
        self.main_frame.pack(fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.label_gif1 = Label(
            self.main_frame, bg="BLACK", border=0, highlightthickness=0
        )

        self.label_gif1.grid(column=0, row=0)

        self.gif1_frames = self._get_frames(self.gif_path)

        root.after(0, self._play_gif, self.label_gif1, self.gif1_frames)

        self.button = Button(
            self.main_frame,
            text="시작",
            width=10,
            height=2,
            command=self._repeat_play_mp3,
        )

        self.button.grid(column=0, row=1)

        root.protocol("WM_DELETE_WINDOW", self._stop_program)

    def _stop_program():
        root.destroy()

    def _get_frames(self, img):
        with Image.open(img) as gif:
            index = 0
            frames = []
            while True:
                try:
                    gif.seek(index)
                    frame = ImageTk.PhotoImage(gif)
                    frames.append(frame)
                except EOFError:
                    break

                index += 1

            return frames

    def _play_gif(self, label, frames):
        total_delay = 0
        delay_frames = 50

        for frame in frames:
            root.after(total_delay, self._next_frame, frame, label, frames)
            total_delay += delay_frames

        root.after(total_delay, self._next_frame, frame, label, frames, True)

    def _next_frame(self, frame, label, frames, restart=False):
        if restart:
            root.after(0, self._play_gif, label, frames)
            return

        label.config(image=frame)

    def _repeat_play_mp3(self):
        playsound(self.mp3_path, block=False)

        schedule.every(10).minutes.do(playsound, self.mp3_path)

        def start_schedule():
            while True:
                schedule.run_pending()
                time.sleep(1)

        schedule_thread = threading.Thread(target=start_schedule)
        schedule_thread.start()


root = Tk()
root.title("Kurukuru Alarm")
root.geometry("600x600")
root.resizable(width=False, height=False)

app_instance = App(root)

root.mainloop()
