import random
try:
    from agents.agent_base import base_agent
    from agents.heuritic_maps.pawn_map import get_pawn_map
    from agents.heuritic_maps.knight_map import get_knight_map
    from agents.heuritic_maps.bishop_map import get_bishop_map
    from agents.heuritic_maps.king_map import get_king_map
    from agents.heuritic_maps.rook_map import get_rook_map
    from agents.heuritic_maps.queen_map import get_queen_map
except ModuleNotFoundError:
    from agent_base import base_agent
    from heuritic_maps.pawn_map import get_pawn_map
    from heuritic_maps.knight_map import get_knight_map
    from heuritic_maps.bishop_map import get_bishop_map
    from heuritic_maps.king_map import get_king_map
    from heuritic_maps.rook_map import get_rook_map
    from heuritic_maps.queen_map import get_queen_map
import numpy as np
import copy 

class heuritic1_agent(base_agent):
    def __init__(self, scene=None, white_pieces=None, black_pieces=None, WHITE_PIECE_DICT=None, BLACK_PIECE_DICT=None, 
                 board=[[0, 0, 0, 0, 0, 0, 0, 0], [0, 'BB', 0, 0, 0, 0, 'WP', 0], [0, 0, 0, 0, 'BK', 0, 'BP', 0], [0, 0, 'BP', 0, 0, 0, 0, 0], [0, 0, 'BP', 0, 0, 0, 0, 'WK'], [0, 0, 0, 0, 0, 0, 0, 0], [0, 'BP', 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
    ):
        super().__init__(scene, white_pieces, black_pieces, WHITE_PIECE_DICT, BLACK_PIECE_DICT, board)

        self.k_c = 200
        self.k_p = (1/8)*8
        self.max_depth = 1
        self.side = None

    def select_from_legal_moves(self, side="white", legal_moves=None):
        self.side = side
        if legal_moves is None:
            legal_moves = [
                ('Pa4B', [6, 1], [7, 1]), ('Bi2B', [1, 1], [0, 0]), ('Bi2B', [1, 1], [0, 2]), 
                # Add more example moves here if needed
            ]
        
        move_score = [0 for _ in range(len(legal_moves))]
        print("side : ", side)
        for i in range(len(legal_moves)):
            move_score[i] = self.simulate_move(legal_moves[i], side, depth=0, maximize=(side == "white"))
        
        print(move_score)
        move_idx = self.norm_scores(move_score)
        selected_move = legal_moves[move_idx]
        return selected_move

    def simulate_move(self, move, side, depth=0, maximize=True):
        op_side = "black" if side == "white" else "white"

        if depth >= self.max_depth:
            score = self.simulate_move_root(move, side)
            return score

        start_pos, end_pos = move[1], move[2]
        piece_id = f'{move[0][-1]}{move[0][0]}'

        # Backup the current state of the board
        original_piece_at_target = self.board[end_pos[0]][end_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece_id
        self.board[start_pos[0]][start_pos[1]] = 0

        if move[0][0] == 'P':  # Handle promotion
            self.board[end_pos[0]][end_pos[1]] = f'{move[0][-1]}Q'

        legal_moves = []
        for i in range(8):
            for j in range(8):
                if self.board[i][j] != 0:
                    moves_for_pieces = self.get_legal_moves(piece_type=self.board[i][j], position=[i, j], side=op_side)
                    for move in moves_for_pieces:
                        legal_moves.append([f'{self.board[i][j][-1]}{j}{i}{self.board[i][j][0]}', [i, j], move])

        move_score = [self.simulate_move(move=legal_moves[i], side=op_side, depth=depth+1, maximize=not maximize) for i in range(len(legal_moves))]

        # Restore the original board state
        self.board[end_pos[0]][end_pos[1]] = original_piece_at_target
        self.board[start_pos[0]][start_pos[1]] = piece_id

        if maximize:
            return max(move_score) if move_score else 0  # Maximizer tries to maximize score
        else:
            return min(move_score) if move_score else 0  # Minimizer tries to minimize score

    def simulate_move_root(self, move, side):
        start_pos, end_pos = move[1], move[2]
        piece_id = f'{move[0][-1]}{move[0][0]}'

        original_piece_at_target = self.board[end_pos[0]][end_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece_id
        self.board[start_pos[0]][start_pos[1]] = 0
        
        if move[0][0] == 'P':  # Handle promotion
            self.board[end_pos[0]][end_pos[1]] = f'{move[0][-1]}Q'

        score = self.get_heuristic(self.board, side)
        castle_s = self.handle_castle(piece_id, start_pos, end_pos) * self.k_c

        score += castle_s
        self.board[end_pos[0]][end_pos[1]] = original_piece_at_target
        self.board[start_pos[0]][start_pos[1]] = piece_id

        return score if side == self.side else -score  # Flip score for the opponent side

    def get_heuristic(self, board, side):
        total_score_from_piece_position = 0
        total_score_from_piece_position_enemy = 0

        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 0:
                    continue

                p_side, p_type = board[i][j][0], board[i][j][1]
                if p_side[0] == side[0].upper():
                    total_score_from_piece_position += self.apply_map_weight(p_side, p_type, i, j)  # position score
                    total_score_from_piece_position += self.apply_ptype_score(p_type)  # type score
                else:
                    total_score_from_piece_position_enemy += self.apply_map_weight(p_side, p_type, i, j)  # position score
                    total_score_from_piece_position_enemy += self.apply_ptype_score(p_type) * self.k_p  # type score
        
        return total_score_from_piece_position - total_score_from_piece_position_enemy

    def norm_scores(self, scores):
        # Convert to a numpy array
        arr = np.array(scores)
        #print("scores: ", scores)
        # Find the minimum and maximum values
        min_val = np.min(arr)
        max_val = np.max(arr)

        # Normalize the array
        if max_val > min_val:
            normalized_array = (arr - min_val) / (max_val - min_val)
        else:
            normalized_array = arr/arr
            #print("!!!", normalized_array)

        #print('ln 68: ', scores, normalized_array)
        max_value = np.max(normalized_array)
        max_indices = np.where(normalized_array == max_value)[0]
        random_index = random.choice(max_indices)
        #random_index = np.random.choice(len(normalized_array), p=normalized_array/np.sum(normalized_array))

        return random_index

    def apply_map_weight(self, side, p_type, x, y):

        score = 0
        if p_type == "P":
            s_map = get_pawn_map(side)
            score += s_map[x][y]
        elif  p_type == "N":
            s_map = get_knight_map(side)
            score += s_map[x][y]
        elif  p_type == "B":
            s_map = get_bishop_map(side)
            score += s_map[x][y]
        elif  p_type == "K":
            s_map = get_king_map(side)
            score += s_map[x][y]
        elif  p_type == "R":
            s_map = get_rook_map(side)
            score += s_map[x][y]
        elif  p_type == "Q":
            s_map = get_queen_map(side)
            score += s_map[x][y]
            
            

        return score
    
    def apply_ptype_score(self, p_type):
        if p_type == "P":
            return 1
        elif p_type == "R":
            return 5
        elif (p_type == "N") or (p_type == "B"):
            return 3
        elif (p_type == "Q"):
            return 8
        else:
            return 0

    def handle_castle(self, piece_id, start_pos, end_pos):
        if piece_id[-1] != 'K':
            return 0
        
        side = piece_id[0]
        
        #print(f'Try {side} castle {start_pos} -> {end_pos}')
        if (side=='B'):
            if (start_pos == [0, 3]):
                if not ((end_pos == [0, 5]) or (end_pos == [0, 1])):
                    return 0
            else:
                return 0
        else:
            if (start_pos == [7, 3]):
                if not ((end_pos == [7, 5]) or (end_pos == [7, 1])):
                    return 0
            else:
                return 0
        
        
        #print("CAN CASTLE", side, start_pos, end_pos)
        return 1



if __name__ == "__main__":

    r = heuritic1_agent()
    r.select_from_legal_moves()
