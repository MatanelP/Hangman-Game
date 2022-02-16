#################################################################
# WRITER : Matanel Pataki
# DESCRIPTION: A program that runs the 'hangman' game
#################################################################
import hangman_helper as helper


def update_word_pattern(word, pattern, letter):
    """
    This function gets a word a pattern and a letter, then returns
    an updated pattern according to the letter given
    :param word: The word to guess
    :param pattern: The current state of the pattern
    :param letter: Some letter to check in word
    :return: An updated pattern with the letter guessed in place
    """
    pattern_lst = list(pattern)
    for i in range(len(word)):
        if word[i] == letter:
            pattern_lst[i] = letter
    return ''.join(pattern_lst)


def game_not_over(pattern, word, score):
    """
    This function determine if the game is over or not.
    The game is over if the pattern equals word or if there are no points left
    :param pattern: The current pattern
    :param word: The current word to guess
    :param score: The current value of the user's points
    :return: True or False
    """
    if pattern == word or score <= 0:
        return False
    return True


def get_indexes_to_show(filter_words_lst):
    """
    This function determines what words and how many words will be display
     to the user as hints
    :param filter_words_lst: A list of words the correlates with the pattern
    :return: The actual words to be display as hints
    """
    indexes_to_show = []
    if len(filter_words_lst) > helper.HINT_LENGTH:
        for i in range(helper.HINT_LENGTH):
            indexes_to_show.append(
                filter_words_lst[
                    i * len(filter_words_lst) // helper.HINT_LENGTH])
        return indexes_to_show
    return filter_words_lst


def in_case_of_letter_input(user_input, wrong_guess_lst, pattern,
                            word, score):
    """
    This function takes care of when the user inputs a letter. it will update
    the pattern according to the user's guessing
    :param user_input: The letter the user guessed
    :param wrong_guess_lst: The wrong guess list to update
    :param pattern: The current pattern to update
    :param word: The current word to guess
    :param score: The current score to update
    :return: Updated: message, pattern, score, wrong guess list
    """
    letter = user_input[1]
    if len(letter) != 1 or letter.isupper() or not letter.isalpha():
        msg = "\nThe letter you chose is invalid!"
        return msg, pattern, score, wrong_guess_lst
    if letter in wrong_guess_lst or letter in pattern:
        msg = "\nYou have already tried that letter!"
        return msg, pattern, score, wrong_guess_lst
    score -= 1
    if letter in word:
        pattern = update_word_pattern(word, pattern, letter)
        count_letter_in_word = word.count(letter)
        score += count_letter_in_word * (count_letter_in_word + 1) // 2
        msg = "\n"
    else:
        wrong_guess_lst.append(letter)
        msg = "\n"
    return msg, pattern, score, wrong_guess_lst


def in_case_of_word_input(score, user_input, word, pattern):
    """
    This function takes care of when the user inputs a word. it will update
    the pattern accordingly, will cause the game to end if guessed correctly
    :param score: The current score to update
    :param user_input: The word the user guessed
    :param word: The current word to guess
    :param pattern: The current pattern to update
    :return: Updated: message, pattern, score
    """
    score -= 1
    user_word = user_input[1]
    if user_word == word:
        count_new_letters = pattern.count('_')
        score += count_new_letters * (count_new_letters + 1) // 2
        pattern = word
    msg = "\nWrong word!"
    return msg, score, pattern


def in_case_of_hint_input(score, wrong_guess_lst, words_lst, pattern):
    """
    This function takes care of when the user wants a hint. it will generate
    a list of hints and will display them
    :param score:
    :param wrong_guess_lst:
    :param words_lst:
    :param pattern:
    :return: Updated: message, score
    """
    score -= 1
    filter_words_lst = filter_words_list(words_lst, pattern,
                                         wrong_guess_lst)
    indexes_to_show = get_indexes_to_show(filter_words_lst)
    helper.show_suggestions(indexes_to_show)
    msg = "\n"
    return msg, score


def game_flow(word, pattern, score, wrong_guess_lst, words_lst):
    """
    This function runs tha main part of a single game, where the user gives
    input and the function responds accordingly
    :param word: The current word the player need to guess
    :param pattern: The current state of the guessing
    :param score: The current score
    :param wrong_guess_lst: The wrong guess list of characters
    :param words_lst: The list of words to filter for hints
    :return: The score and the pattern after been updated
    """
    msg = "\n"
    while game_not_over(word, pattern, score):
        helper.display_state(pattern, wrong_guess_lst, score, msg)
        user_input = helper.get_input()
        if user_input[0] is helper.LETTER:
            msg, pattern, score, wrong_guess_lst = in_case_of_letter_input(
                user_input, wrong_guess_lst, pattern, word, score)
        if user_input[0] is helper.WORD:
            msg, score, pattern = in_case_of_word_input(score, user_input,
                                                        word, pattern)
        if user_input[0] is helper.HINT:
            msg, score = in_case_of_hint_input(score, wrong_guess_lst,
                                               words_lst, pattern)
    return score, pattern


def game_end(word, pattern, wrong_guess_lst, score):
    """
    This function printing to the user if he had won or not, the shows the
    the current state one last time
    :param word: The current word the player guessed or not
    :param pattern: The current pattern the player needed to guess
    :param wrong_guess_lst: The wrong guess list of characters
    :param score: The current score
    :return: None
    """
    if word == pattern:
        msg = "\nMazal-Tov you won!"
    else:
        msg = "\nI'm sorry, you lost, the word was: " + word
    helper.display_state(pattern, wrong_guess_lst, score, msg)


def run_single_game(words_lst, score):
    """
    This function runs a single game and it includes 3 main parts:
    initializing the game, running the game (in game_flow()) and ending
    the game
    :param words_lst: a list of words from which 1 will be chosen randomly
    :param score: The current value of the user score
    :return: The current value of the user score after it been updated
    """
    # initializing game:
    word = helper.get_random_word(words_lst)
    wrong_guess_lst = []
    pattern = '_' * len(word)
    score, pattern = game_flow(word, pattern, score, wrong_guess_lst,
                               words_lst)
    game_end(word, pattern, wrong_guess_lst, score)
    return score


def no_common_letters(letters_lst, word):
    """
    This function makes sure there are no correlating letters between the
    list if wrongly guessed letters and the word to guess
    :param letters_lst: A list of characters
    :param word: A string
    :return: True when there are no shared letters, False otherwise
    """
    for i in set("".join(letters_lst)):
        for j in set(word):
            if i == j:
                return False
    return True


def filter_words_list(words_lst, pattern, wrong_guess_lst):
    """
    This function filters the words out of the main words list so that the
     only words remaining will correlate with the current state of the pattern
    :param words_lst: a list of words from which 1 will be chosen randomly
    :param pattern: The current state of the guessing
    :param wrong_guess_lst: The wrong guess list of characters
    :return: The list of filtered words suitable
    """
    filter_words_lst = []
    for i in words_lst:
        if len(i) == len(pattern) and no_common_letters(wrong_guess_lst, i):
            a_valid_filtered_word = True
            for j in range(len(i)):
                if i.count(i[j]) > pattern.count(i[j]) and i[j] in pattern or \
                        i[j] != pattern[j] and pattern[j] != '_':
                    a_valid_filtered_word = False
            if a_valid_filtered_word:
                filter_words_lst.append(i)
    return filter_words_lst


def main():
    """
    The main function of the game, the loop will run until the score hits 0
    i.e. the player lost
    :return: None
    """
    score = helper.POINTS_INITIAL
    games_played = 0
    words_lst = helper.load_words()
    while score > 0:
        score = run_single_game(words_lst, score)
        games_played += 1
        if score > 0:
            if not helper.play_again(
                    "\nSo far you played " + str(games_played) +
                    " game(s) and scored " + str(score) +
                    " points!\nWanna play again?"):
                score = 0
        elif not helper.play_again("\nYou survived " + str(games_played) +
                                   " game(s)\nWanna play again?"):
            score = 0
        else:
            score = helper.POINTS_INITIAL
            games_played = 0


if __name__ == "__main__":
    main()
