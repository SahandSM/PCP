import numpy as np

from agents.game_utils import *
from typing import Optional, Callable

def extract_windows(array: list,pivot_position: int) -> list:
    """
    Extracts a sliding window of size 4 from the given list 'array' centered around the 'pivot_position'.

    Parameters:
    - array (list): The input list from which windows are to be extracted.
    - pivot_position (int): The index around which the sliding window is centered.

    Returns:
    list: A list of sublists, each representing a sliding window of size 4 around the 'pivot_position'.
    
    Example:
    >>> array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> pivot_position = 4
    >>> extract_windows(array, pivot_position)
    [[2, 3, 4, 5], [3, 4, 5, 6], [4, 5, 6, 7]]
    """
    start = max(0,pivot_position-3)
    last_window = len(array)-3
    end = min(pivot_position+1,last_window)
    windows = []
    for w in range(start,end):
        window = list(array[w:w+4])
        windows.append(window)
    return windows

def pivot_row(board,pivot):
    row_window = board[pivot[0]]
    position = pivot[1]
    return row_window,position

def pivot_col(board,pivot):
    col_window = board[:,pivot[1]]
    position = pivot[0]
    return col_window,position

def pivot_diag(board,pivot):
    diag_window = np.diag(board,pivot[1]-pivot[0])
    position = min(pivot)
    return diag_window,position

def pivot_opp_diag(board,pivot):
    borad_flipped = np.fliplr(board)
    pivot = pivot[0],6-pivot[1]
    opp_daig_window = np.diag(borad_flipped,pivot[1]-pivot[0])
    position = min(pivot)
    return opp_daig_window,position

def evaluate_at_pivot(board,pivot,player):
    score = []
    score_row = evaluate_row(board,pivot,player)
    score_col = evaluate_col(board,pivot,player)
    score_diag = evaluate_diag(board,pivot,player)
    score_opp_diag = evaluate_opp_diag(board,pivot,player)
    score = score_row + score_col + score_diag + score_opp_diag
    return score

def evaluate_row(board,pivot_point,player):
    array,position = pivot_row(board,pivot_point)
    windows_row = extract_windows(array,position)
    score_row = evaluate_one_direction(windows_row,player)
    return score_row

def evaluate_col(board,pivot_point,player):
    array,position = pivot_col(board,pivot_point)
    windows_col = extract_windows(array,position)
    score_col = evaluate_one_direction(windows_col,player)
    return score_col

def evaluate_diag(board,pivot_point,player):
    array,position = pivot_diag(board,pivot_point)
    windows_diag = extract_windows(array,position)
    sccore_diag = evaluate_one_direction(windows_diag,player)
    return sccore_diag

def evaluate_opp_diag(board,pivot_point,player):
    array,position = pivot_opp_diag(board,pivot_point)
    windows_opp_diag = extract_windows(array,position)
    score_opp_diag = evaluate_one_direction(windows_opp_diag,player)
    return score_opp_diag

def evaluate_one_direction(windows,player):
    # I need to evlaute each direction separately to catch if for example therer is both horizontal and diagonal score 3.
    score = []
    for window in windows:
        player_new_score = evaluate_window_for_player(window,player)
        score = score + player_new_score
        if player_new_score: break

    for window in windows:
        opponent_new_score = evaluate_window_for_opponent(window,player)
        score = score + opponent_new_score
        if opponent_new_score: break
    return score

def evaluate_window_for_player(window,player):
    score = []
    n_pieces = window.count(player)
    n_zeros = window.count(0)

    if n_pieces == 3: score.append(3)
    elif n_pieces == 2 and n_zeros == 2: score.append(2)
    return score

def evaluate_window_for_opponent(window,player):
    score = []
    n_pieces = window.count(player)
    n_zeros = window.count(0)

    if n_pieces == 0 and n_zeros == 1: score.append(-3)
    elif n_pieces == 0 and n_zeros == 2: score.append(-2)
    return score

def get_pivots(board):
    #remember to mask tpivots with the is_open_rows
    pass

def get_free_row(board):
    free_row = [np.count_nonzero(board[:,i]) for i in range(7)]
    return free_row

def is_open_row(board):
    is_open = board[-1, :] == 0
    return is_open

def evaluate_board(board,player):
    # pivots = get_pivots(board)
    # score =[]
    # for pivot in pivots:
    #       windows = get_windows_at_pivot(board,pivot)
    #       new_score = evaluate_at_pivot(windows)
    #       score = score + new_score
    # return score
    pass


    
    