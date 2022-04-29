import boggle_board_randomizer
import ex12_utils
import timer
from boggle_gui import BoggleGui


WORDS_LIST = 'boggle_dict.txt'
GAME_DURATION = 180


class BoggleGame:
    """"""

    def __init__(self):
        """The constructor of the game"""
        self.__board = boggle_board_randomizer.randomize_board()
        self.__words = ex12_utils.read_wordlist(WORDS_LIST)
        self.__func_dict = {"start": self.start_game,
                            "word_check": self.word_checker,
                            "new_game": self.new_game,
                            "time_checker": self.time_checker}
        self.__timer = timer.Timer(GAME_DURATION)
        self.__gui = BoggleGui(self.__board, self.__func_dict, self.__timer)
        self.time_checker()

    def run(self):
        """This method is very important.It is responsible for running the game"""
        self.__gui.mainloop()

    def word_checker(self):
        """This method is responsible for the check whether the word that the
         user is trying to ques is in the game dictionary or not.
         If it is, the method manages the process od updating the score and
         other data.if it is not, method resets the guessing string"""
        word, path = self.__gui.get_curent_guess()
        if ex12_utils.is_valid_path(self.__board, path,
                                     ex12_utils.read_wordlist(
                                        'boggle_dict.txt')) and word not in self.__gui.found_word_listoy:
            score = self.__score_calc(path)
            self.__gui.valid_word_chose_manager(word, score)
            self.__gui.reset_func()

        else:
            self.__gui.reset_func()

    def __score_calc(self, path):

        """This method calculates the score"""
        return len(path) ** 2

    def start_game(self):
        """This method manages the beginning of the game"""
        self.__gui.forget_main_frame()
        self.__gui.initialize_new_game()

    def time_checker(self):
        """This is the timer of the game. If the time has ended, calls to
         method that manages the following processes"""
        if not self.__timer.get_time() == 0:
            self.__gui.root.after(3000, self.time_checker)
        else:
            self.__gui.end_of_the_game()

    def new_game(self):
        """This method sets new game"""
        self.__gui.forget_old_data()
        self.__gui.reset_data()
        self.__board = boggle_board_randomizer.randomize_board()
        self.__gui.set_board(self.__board)
        self.__timer.set_time(GAME_DURATION)
        self.__gui.initialize_new_game()


if __name__ == "__main__":
    game = BoggleGame()
    game.run()
