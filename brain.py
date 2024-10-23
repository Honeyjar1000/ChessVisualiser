import numpy as np
import copy
import random
from agents.random1 import random_agent
from agents.heuritic1 import heuritic1_agent
SEED = 5
random.seed(SEED)
np.random.seed(SEED)


class brain:

    def __init__(self, scene, black_pieces:dict, white_pieces:dict):
        
        self.WHITE_PIECE_DICT = {
            'Ro1W': ["WR", [0, 0], False], 
            'Ro2W': ["WR", [0, 0], False], 
            'Ni1W': ["WN", [0, 0], False], 
            'Ni2W': ["WN", [0, 0], False], 
            'Bi1W': ["WB", [0, 0], False], 
            'Bi2W': ["WB", [0, 0], False], 
            'Qu1W': ["WQ", [0, 0], False], 
            'Ki1W': ["WK", [0, 0], False], 
            'Pa1W': ["WP", [0, 0], False], 
            'Pa2W': ["WP", [0, 0], False], 
            'Pa3W': ["WP", [0, 0], False], 
            'Pa4W': ["WP", [0, 0], False], 
            'Pa5W': ["WP", [0, 0], False], 
            'Pa6W': ["WP", [0, 0], False], 
            'Pa7W': ["WP", [0, 0], False], 
            'Pa8W': ["WP", [0, 0], False]}

        self.BLACK_PIECE_DICT = {
            'Ro1B': ["BR", [0, 0], False], 
            'Ro2B': ["BR", [0, 0], False], 
            'Ni1B': ["BN", [0, 0], False], 
            'Ni2B': ["BN", [0, 0], False], 
            'Bi1B': ["BB", [0, 0], False], 
            'Bi2B': ["BB", [0, 0], False], 
            'Qu1B': ["BQ", [0, 0], False], 
            'Ki1B': ["BK", [0, 0], False], 
            'Pa1B': ["BP", [0, 0], False], 
            'Pa2B': ["BP", [0, 0], False], 
            'Pa3B': ["BP", [0, 0], False], 
            'Pa4B': ["BP", [0, 0], False], 
            'Pa5B': ["BP", [0, 0], False], 
            'Pa6B': ["BP", [0, 0], False], 
            'Pa7B': ["BP", [0, 0], False], 
            'Pa8B': ["BP", [0, 0], False]}


        self.white_pieces=white_pieces
        self.black_pieces=black_pieces
        self.scene = scene

        self.b_is_castling = False
        self.b_first_tick_castle = False

        self.board = self.create_board_arr()
        self.agent = heuritic1_agent(
            scene=self.scene, 
            white_pieces=self.white_pieces, 
            black_pieces=self.black_pieces, 
            WHITE_PIECE_DICT=self.WHITE_PIECE_DICT, 
            BLACK_PIECE_DICT=self.BLACK_PIECE_DICT, 
            board=self.board)
        
        self.print_board()

    def print_board(self, board=None):

        if board is None:
            board = self.board

        s = '\n'
        s += '\t'
        for _ in range(8):
            s += str(_)
            s += '\t'
        s +='\n\n'

        for i in range(8):
            s += str(i) + '\t'
            for j in range(8):
                    
                    if board[i][j] != 0:
                        s += board[i][j]
                    else:
                        s += '-'
                    s += '\t'
            s += '\n'
        print(s)

    
    def create_board_arr(self):

        board = [[0 for i in range(8)] for j in range(8)]

        for (key, val) in self.white_pieces.items():
            
            #print(val.pos[0]/6, val.pos[2]/6)
            x, y = int((val.pos[0]/6)+4), int((val.pos[2]/6)+4)
            self.WHITE_PIECE_DICT[f'{key}'][1][0] = x
            self.WHITE_PIECE_DICT[f'{key}'][1][1] = y
            
            board[x][y] = self.WHITE_PIECE_DICT[f'{key}'][0]

        for (key, val) in self.black_pieces.items():
            #print(val.pos[0]/6, val.pos[2]/6)
            x, y = int((val.pos[0]/6)+4), int((val.pos[2]/6)+4)
            self.BLACK_PIECE_DICT[f'{key}'][1][0] = x
            self.BLACK_PIECE_DICT[f'{key}'][1][1] = y
            
            board[x][y] = self.BLACK_PIECE_DICT[f'{key}'][0]

        return board

    def next_move(self, side):

        self.print_board()
        out, b_is_castling = self.agent.make_move(side)
        if out[0] is None:      # Game Over
            return  None, False
        
        

        return out, b_is_castling
    


    def promote_pawn_in_brain(self, pawn_name, new_piece_type, side, tag):
        """
        Promote the pawn to the specified piece (e.g., Queen, Rook, Bishop, or Knight).
        Update the piece dictionary and board state.
        """
        if side == "white":
            piece_dict = self.WHITE_PIECE_DICT
        else:
            piece_dict = self.BLACK_PIECE_DICT

        # Get the pawn's position before promotion
        pawn_pos = piece_dict[pawn_name][1]

        # Remove the pawn from the piece dictionary
        del piece_dict[pawn_name]

        # Add the new piece to the piece dictionary at the same position
        piece_dict[tag] = [f'{tag[-1]}{tag[0]}', pawn_pos, True]

        # Update the board to reflect the new piece
        self.board[pawn_pos[0]][pawn_pos[1]] = f'{tag[0]}{tag[-1]}'
