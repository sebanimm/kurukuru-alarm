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
        super().__init__(root)

        self.main_frame = self
        self.main_frame.pack(fill=BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.rowconfigure(1, weight=1)

        self.create_widgets()

    def create_widgets(self):
        self.gif_label = Label(
            self.main_frame, bg="BLACK", border=0, highlightthickness=0
        )

        self.gif_label.grid(column=0, row=0)

        self.gif_frames = self._get_frames(self.gif_path)

        root.after(0, self._play_gif, self.gif_label, self.gif_frames)

        self.config_frame = Frame(self.main_frame)

        self.entry_frame = LabelFrame(self.config_frame, text="타이머 주기 설정")

        self.minutes = IntVar(value=10)

        self.minutes_entry = Entry(self.entry_frame, width=4, textvariable=self.minutes)
        self.minutes_entry.pack(side=LEFT)

        self.minutes_label = Label(self.entry_frame, text="분", width=3)
        self.minutes_label.pack(side=LEFT)

        self.seconds = IntVar()

        self.seconds_entry = Entry(self.entry_frame, width=4, textvariable=self.seconds)
        self.seconds_entry.pack(side=LEFT)

        self.seconds_label = Label(self.entry_frame, text="초", width=3)
        self.seconds_label.pack(side=LEFT)

        self.entry_frame.pack(side=LEFT)

        self.start_button = Button(
            self.config_frame,
            text="시작",
            width=10,
            height=2,
            command=self._repeat_mp3,
        )
        self.start_button.pack(side=RIGHT)

        self.config_frame.grid(column=0, row=1, sticky=W + E, padx=50)

        root.protocol("WM_DELETE_WINDOW", self._stop_program)

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

    def _repeat_mp3(self):
        timer_minutes_cycle = self.minutes.get()
        timer_seconds_cycle = self.seconds.get()
        timer_cycle_into_seconds = timer_minutes_cycle * 60 + timer_seconds_cycle

        playsound(self.mp3_path, block=False)

        schedule.every(timer_cycle_into_seconds).seconds.do(
            playsound, self.mp3_path, block=False
        )

        def start_schedule():
            while True:
                schedule.run_pending()
                time.sleep(1)

        schedule_thread = threading.Thread(target=start_schedule)
        schedule_thread.start()

    def _stop_program(self):
        root.destroy()


root = Tk()
root.title("Kurukuru Alarm")
root.geometry("600x600")
root.resizable(width=False, height=False)

app_instance = App(root)

root.mainloop()
