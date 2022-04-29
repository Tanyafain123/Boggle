import tkinter
import datetime

class Timer():
    """"""

    def __init__(self, time):
        self.__seconds_left = time

    def init_timer(self, frame):
        """"""
        self.__time_lable = tkinter.Label(frame,width=20,height=2, text="00:00:00",borderwidth=3, relief="ridge")
        self.__time_lable.grid(row=2, column=0)

        
    def countdown(self):
        """"""
        self.__time_lable["text"] = self.__convert_seconds_left_to_time()
        if self.__seconds_left:
            self.__seconds_left -= 1
            self.root.after(1000, self.countdown)

    def set_root(self, root):
        self.root = root

    def __convert_seconds_left_to_time(self):
        """"""
        return datetime.timedelta(seconds=self.__seconds_left)

    def set_time(self,time):
        """"""
        self.__seconds_left = time

    def get_time(self):
        return self.__seconds_left


