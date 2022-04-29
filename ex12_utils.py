DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0),
              (1, 1)]


def is_valid_path(board, path, words):
    """The function checks if the route is a valid route that describes a word that exists in the word collection.
    If so, the function returns the found word. If the route is invalid or the corresponding word does not exist in the
    dictionary, the function will return None.
    """
    if path_validy(board, path):
        word_lst = [board[coordinate[0]][coordinate[1]] for coordinate in path]
        word = "".join(word_lst)
        if word not in words:
            return
        else:
            return word
    else:
        return


def path_validy(board, path):
    """The function checks if the given path is valid in frame of limits of the board, that means is continuous and does
     not exceed the limits of the board"""
    cell_lst = board_coordinates(board)
    for index in range(len(path) - 1):
        coordinate = path[index]
        if coordinate in cell_lst:
            if path[index + 1] not in neighbors_finder(coordinate, cell_lst):
                return
        else:
            return
    return True


def neighbors_finder(coordinate, cell_lst):
    """This function gets the coordinate on the board, seeks it's neighbour cells and adds them to the list.
     Returns the list"""
    x, y = coordinate
    nieghbors_lst = []
    for direction in DIRECTIONS:
        new_x, new_y = direction
        nieghbor = (x + new_x, y + new_y)
        if nieghbor in cell_lst:
            nieghbors_lst.append((x + new_x, y + new_y))
    return nieghbors_lst


def max_score_paths(board, words):
    """The function returns a list of tracks that provide the maximum score per game for the board and the collection
     of words given. Note that there should not be more than one track for the same word and that there may be tracks
     with a different score for the same word."""
    path_list = []
    for word in words:
        n = len(word)
        paths_of_word = find_length_n_words(n, board, [word])
        if paths_of_word:
            path_list.append(max(paths_of_word, key=lambda x: len(x)))
    return path_list


def board_coordinates(board):
    """This function returns the list of cell coordinates"""
    cell_lst = []
    for i in range(len(board)):
        for j in range(len(board)):
            cell_lst.append((i, j))
    return cell_lst


def read_wordlist(filename):
    """
    This function creates the the wordlist"""

    with open(filename, "r") as word_list:
        word_list = word_list.readlines()
    for index, word in enumerate(word_list):
        word_list[index] = word[0:-1]

    return word_list


def list_of_letters(board):
    """This function returns list of lottors that are placed on the board"""
    lst_of_letters = []
    for row in board:
        for letter in row:
            lst_of_letters.append(letter)
    return lst_of_letters


def find_length_n_paths(n, board, words):
    """The function returns a list of all n-length tracks that describe words in the word collection. If there are
     several tracks of length corresponding to the same word, all of them must be returned."""
    paths = []
    if n > 16:
        return []
    board_cells = board_coordinates(board)
    for coordinate in board_cells:
        current_word = board[coordinate[0]][coordinate[1]]
        paths.extend(
            find_length_n_paths_helper(n, current_word, words, board,
                                       [coordinate], board_cells))
    return paths


def find_length_n_paths_helper(n, current_word, old_suitable_words, board,
                               path,
                               board_cells):
    """This function is the helper of the find_length_n_paths"""
    new_suitable_words = word_filter(current_word, old_suitable_words)

    if not new_suitable_words:
        return []
    if len(path) == n and current_word in new_suitable_words:
        return [path[:]]

    x = []

    for coordinate in neighbors_finder(path[-1], board_cells):
        if len(path) + 1 <= n:
            if not coordinate in path:
                new_word = current_word + board[coordinate[0]][coordinate[1]]
                x.extend(
                    find_length_n_paths_helper(n, new_word, new_suitable_words,
                                               board,
                                               path + [coordinate],
                                               board_cells))
    return x


def find_length_n_words(n, board, words):
    """The function returns a list of all the paths that describe words in the collection of words that are of length n.
    If there are multiple routes to the same word, all of them must be returned. """
    paths = []
    suitable_words = initial_word_filter(n, words)
    board_cells = board_coordinates(board)
    for coordinate in board_cells:
        current_word = board[coordinate[0]][coordinate[1]]
        paths.extend(
            find_length_n_words_helper(current_word, suitable_words, board,
                                       [coordinate], board_cells))
    return paths


def find_length_n_words_helper(current_word, old_suitable_words, board, path,
                               board_cells):
    """This function is the helper of the find_length_n_words function"""
    new_suitable_words = word_filter(current_word, old_suitable_words)

    if not new_suitable_words:
        return []
    if current_word in new_suitable_words:
        return [path[:]]

    x = []

    for coordinate in neighbors_finder(path[-1], board_cells):
        if len(path) + 1 <= 16:
            if not coordinate in path:
                new_word = current_word + board[coordinate[0]][coordinate[1]]
                x.extend(
                    find_length_n_words_helper(new_word, new_suitable_words,
                                               board,
                                               path + [coordinate],
                                               board_cells))
    return x


def initial_word_filter(n, words):
    """This function checks if the words in list of words matches the length n"""
    suitable_words = []

    for word in words:
        if len(word) == n:
            suitable_words.append(word)

    return suitable_words


def word_filter(current_word, suitable_words):
    """ This function checks if the part of the word that was composed untill now matches the beginning of some word in
    the words that are placed in the dict.The function appends the matching words to the list and returns this list
    """
    words = []
    for word in suitable_words:
        if current_word in word:
            words.append(word)
    return words


