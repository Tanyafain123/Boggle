from tkinter import *
import tkinter.messagebox


BOARD_COORDINATES = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 2),
                     (1, 3),
                     (2, 0), (2, 1), (2, 2), (2, 3), (3, 0), (3, 1), (3, 2),
                     (3, 3)]

# fonts

BAHNSCHRIFT_CONDENSED_25 = ("bahnschrift condensed", 25)
BAHNSCHRIFT_CONDENSED_14 = ("bahnschrift condensed", 14)
BAHNSCHRIFT_CONDENSED_10 = ("bahnschrift condensed", 10)

START_WINDOW_SIZE = "720x600"
PLAY_WINDOW_SIZE = "800x400"
GAME_TITLE = "BOGGLE YAY"

# Informative messages

ENDGAME_MESSAGE = "Your game came to an end. Let's see what we've got!"
NEW_GAME_QUESTION = "Do you want to play another one?"
WELCOME_MESSAGE = "WELCOME TO THE GAME"
INTRODACTION_MESSAGE = 'The rules are simple. ' \
                       'You have a board, 4x4, and each cell contains a letter.\n' \
                       'By clicking the cells, in a continious order, a word is created.\n' \
                       'If the word is valid, by clicking the “check sequence” button\n' \
                       'You will be awarded for your guess.\n' \
                       'Enjoy!'
BONUS_TEXT = "please give us a 100,\n  we tried so hard!!"

START_GAME_MESSAGE = "PRESS TO START THE GAME"

START_GAME_MESSAGE_STYLE = {"text":BONUS_TEXT,
                            "font":BAHNSCHRIFT_CONDENSED_14}

# Button style

RESET_BUTTON_STYLE = {"text": "RESET", "font": BAHNSCHRIFT_CONDENSED_14,
                      "width": 17, "height": 1}
START_GAME_BUTTON_STYLE = {"text": START_GAME_MESSAGE,
                           "font": BAHNSCHRIFT_CONDENSED_14}
LABEL_WELCOME_STYLE = {"text": WELCOME_MESSAGE,
                       "font": BAHNSCHRIFT_CONDENSED_14}
LABEL_INTRODUCTION_STYLE = {"text": INTRODACTION_MESSAGE,
                            "font": BAHNSCHRIFT_CONDENSED_14}
lABEL_SCORE_STYLE = {"text": "Your score is: " + '0',"width":17,
                     "font": BAHNSCHRIFT_CONDENSED_14,
                     "borderwidth": 3, "relief": "ridge"}
LABEL_CURRENT_WORLD_STYLE = {"text": "Current word: ", "width": 16,
                             "height": 2, "borderwidth": 3, "relief": "ridge"}
LABEL_SHOW_CURRENT_WORLD_STYLE = {"text": "",
                                  "width": 20, "height": 2, "borderwidth": 3,
                                  "relief": "ridge"}
CHECKBUTTON_STYLE = {"text": "CHECK SEQUENCE",
                     "font": BAHNSCHRIFT_CONDENSED_14}
BUTTON_STYLE = {"bg": "light grey",
                "font": BAHNSCHRIFT_CONDENSED_25,
                "width": 5,
                "height": 1}


class BoggleGui:

    def __init__(self, board, func_dict, timer):
        """The constructor of the gui"""
        self.__board = board
        self.command_assignment(func_dict)
        self.timer = timer
        self.root = tkinter.Tk()
        self.root.title(GAME_TITLE)
        self.root.geometry(START_WINDOW_SIZE)
        self.root.resizable(False,False)
        self.__main_frame_init()
        self.reset_data()

    def reset_data(self):
        """This method resets the data of the game"""
        self.__score = 0
        self.__curent_word = ""
        self.__curent_path = []
        self.__buttons = {}
        self.__button_dict = {}
        self.__board_letters = []
        self.found_word_listoy = []

    def mainloop(self):
        """This method is very important.It is responsible for running the gui"""
        self.root.mainloop()

    def __main_frame_init(self):
        """This method initialises the main frame of the game"""
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack()
        self.__label = tkinter.Label(self.main_frame,
                                     **LABEL_WELCOME_STYLE)
        self.__label_introduction = tkinter.Label(self.main_frame,
                                                  **LABEL_INTRODUCTION_STYLE)

        self.__label.pack()
        self.__label_introduction.pack()
        self.__button_startgame = tkinter.Button(self.main_frame,
                                                 command=self.__start_game,
                                                 **START_GAME_BUTTON_STYLE)
        self.__button_startgame.pack()
        self.shit_for_bonus()

    def shit_for_bonus(self):
        """  :)  """
        self.__bonus_frame = tkinter.Frame(self.main_frame)
        self.__bonus_frame.pack(side= BOTTOM)
        self.__img = PhotoImage(file="bonus_photo.png")
        self.__bonus_lable = tkinter.Label(self.__bonus_frame, image=self.__img)
        self.__bonus_lable.pack()
        self.__bonus_lable2 = tkinter.Label(self.__bonus_frame,
                                            **START_GAME_MESSAGE_STYLE)
        self.__bonus_lable2.pack(side=BOTTOM)


    def forget_main_frame(self):
        """This method deletes the main frame of the game(in order to create
         new one in the future)"""
        self.main_frame.pack_forget()

    def initialize_new_game(self):
        """This method is responsible for initialisinf og new game(creates
         frames of the game)"""
        self.root.geometry(PLAY_WINDOW_SIZE)
        self.board_frame_init()
        self.display_frame_init()
        self.current_frame_init()

    def board_frame_init(self):
        """This method initializes the board frame and sets the buttons"""
        self.__button_init_hrlper()
        self.__board_frame = Frame(self.root)
        self.__board_frame.place(x=250, y=0)
        for i in self.__button_dict.keys():
            self.__button_init(self.__board_frame, i)

    def display_frame_init(self):
        """This method initialises the display frame of the game"""
        self.__displayFrame = Frame(self.root)
        self.scroll_bar_frame_init()
        self.__displayFrame.place(x=0, y=0)
        self.__Label_Score = Label(self.__displayFrame, **lABEL_SCORE_STYLE)
        self.__Label_Score.grid(row=1, column=0)
        self.timer.set_root(self.root)
        self.timer.init_timer(self.__displayFrame)
        self.timer.countdown()


    def scroll_bar_frame_init(self):
        self.scroll_bar_frame = Frame(self.__displayFrame)
        self.scroll_bar_frame.grid(row=0, column=0)
        self.words_scrollbar = tkinter.Scrollbar(self.scroll_bar_frame,
                                                 cursor="spider")
        self.words_scrollbar.pack(side=RIGHT, fill=Y)
        self.found_words_list = tkinter.Listbox(self.scroll_bar_frame,
                                                yscrollcommand=
                                                self.words_scrollbar.set,
                                                height=15)
        self.found_words_list.pack(side=LEFT)
        self.words_scrollbar.config(command=self.found_words_list.yview)

    def current_frame_init(self):
        """This method initialises the current frame of the game"""
        self.__currentFrame = Frame(self.root)
        self.__currentFrame.place(x=250, y=300)
        self.__Label_Current_Word = Label(self.__currentFrame,
                                          **LABEL_CURRENT_WORLD_STYLE)
        self.__Label_Current_Word.grid(row=0, column=0)
        self.__Label_show_Current_Word = Label(self.__currentFrame,
                                               **LABEL_SHOW_CURRENT_WORLD_STYLE)
        self.__Label_show_Current_Word.grid(row=0, column=1)
        self.__Checker_Button = Button(self.__currentFrame,
                                       command=lambda: self.__word_checker(),
                                       **CHECKBUTTON_STYLE)

        self.__Checker_Button.grid(row=1, column=0)
        self.__Reset_Button = Button(self.__currentFrame,
                                     command=lambda: self.reset_func(),
                                     **RESET_BUTTON_STYLE)
        self.__Reset_Button.grid(row=1, column=1)

    def __button_init_hrlper(self):
        """This method is responsible for helping to the initializing of the
        buttons function"""
        for row in self.__board:
            for i in row:
                self.__board_letters.append(i)

        for i in range(len(self.__board_letters)):
            self.__button_dict[i + 1] = (
                BOARD_COORDINATES[i], self.__board_letters[i])

    def __button_click(self, letter, coordinate):
        """This method is responsible for the behaviour of the button
         while clicked"""
        if coordinate not in self.__curent_path:
            self.set_curent_word(letter)
            self.__buttons[coordinate]["bg"] = "grey"
            self.__curent_path.append(coordinate)

    def __button_init(self, board_frame, i):
        """This method initialises the buttons using the helping function"""
        coordinate, letter = self.__button_dict.get(i)
        self.i = Button(board_frame,
                        command=lambda: self.__button_click(letter,
                                                            coordinate),
                        text=letter, **BUTTON_STYLE)
        self.i.grid(row=coordinate[0], column=coordinate[1])
        self.__buttons[coordinate] = self.i

    def valid_word_chose_manager(self, word, score):
        """This method is responsible for the behaviour of the game in case
        that the user chose the right word"""
        self.__score += score
        self.__Label_Score["text"] = "Your score is: " + str(self.__score)
        self.found_words_list.insert(END, str(word) + "\n")
        self.found_word_listoy.append(word)
        self.set_curent_word()
        self.__curent_path = []

    def get_curent_guess(self):
        """This method returns guessed word and it"s path"""
        return self.__curent_word, self.__curent_path

    def set_curent_word(self, char='', flag=False):
        """This method adds the chosen letter to the current word,  or resets
        the word according to the function it was called with """
        if not flag:
            self.__Label_show_Current_Word["text"] += char
            self.__curent_word += char
        else:
            self.__Label_show_Current_Word["text"] = ""
            self.__curent_word = ""

    def reset_func(self):
        """This method is responsible for the reseting the board
        (change of the buttons colour) and reseting of the path"""

        self.set_curent_word(flag=True)
        self.__curent_path = []
        for button in self.__buttons.values():
            button["bg"] = "light grey"

    def forget_old_data(self):
        """This method is responsible for deleting of the frames"""
        self.__board_frame.pack_forget()
        self.__displayFrame.pack_forget()
        self.__currentFrame.pack_forget()

    def end_of_the_game(self):
        """This method is responsiple for the game ending with some popping
         windows that asl if the user want to play again"""
        self.__poptest = tkinter.messagebox.showinfo("Game end",
                                                     ENDGAME_MESSAGE + "\n" + "Your word list is:\n" + "\n".join(
                                                         self.found_word_listoy) +
                                                     "\n" +
                                                     self.__Label_Score[
                                                         "text"])
        self.__answer = tkinter.messagebox.askquestion("Question",
                                                       NEW_GAME_QUESTION)
        if self.__answer == "yes":
            self.__new_game()
            self.__time_checker()
        if self.__answer == "no":
            self.root.destroy()

    def command_assignment(self, func_dict):
        """This method assigns some functions thatit recieves from the "Boogle"
         class that  this class is using """
        self.__start_game = func_dict["start"]
        self.__word_checker = func_dict["word_check"]
        self.__new_game = func_dict["new_game"]
        self.__time_checker = func_dict["time_checker"]

    def set_board(self, board):
        """While initializing new game from the "Boogle class" sets the new
         board"""
        self.__board = board
