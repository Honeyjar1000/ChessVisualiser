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

class heuritic1_agent(base_agent):
    def __init__(self, scene=None, white_pieces=None, black_pieces=None, WHITE_PIECE_DICT=None, BLACK_PIECE_DICT=None, 
                 board=[['BR', 0, 'BB', 'BK', 0, 'BB', 'BN', 'BR'], ['BP', 'BP', 'BP', 0, 0, 'BP', 'BP', 0], [0, 0, 'BN', 'BP', 0, 0, 0, 0], [0, 0, 0, 0, 'BP', 0, 'BQ', 'BP'], [0, 0, 0, 0, 0, 0, 0, 0], ['WN', 0, 0, 0, 'WP', 'WP', 'WP', 0], ['WP', 'WP', 'WP', 'WP', 'WQ', 0, 'WB', 'WP'], [0, 'WR', 'WB', 'WK', 0, 0, 0, 'WR']]
):
        super().__init__(scene, white_pieces, black_pieces, WHITE_PIECE_DICT, BLACK_PIECE_DICT, board)

        self.k_c = 200
        self.k_p = (1/8)*8

    def print_board(self, board=None):

        if board is None:
            board = self.board

        s = '\n----------------------------------------\n'
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
        s += '----------------------------------------\n'
        print(s)

    
    def select_from_legal_moves(self, side="white", 
                                legal_moves = [('Ro1W', [7, 7], [7, 6]), ('Ro1W', [7, 7], [7, 5]), ('Ro1W', [7, 7], [7, 4]), ('Ro2W', [7, 1], [7, 0]), 
                                               ('Ni2W', [5, 0], [3, 1]), ('Ni2W', [5, 0], [4, 2]), ('Bi1W', [6, 6], [5, 7]), ('Bi1W', [6, 6], [7, 5]), 
                                               ('Qu1W', [6, 4], [7, 4]), ('Qu1W', [6, 4], [6, 5]), ('Qu1W', [6, 4], [5, 3]), ('Qu1W', [6, 4], [4, 2]), 
                                               ('Qu1W', [6, 4], [3, 1]), ('Qu1W', [6, 4], [2, 0]), ('Qu1W', [6, 4], [7, 5]), ('Ki1W', [7, 3], [7, 4]), 
                                               ('Ki1W', [7, 3], [7, 5]), ('Pa1W', [6, 7], [5, 7]), ('Pa1W', [6, 7], [4, 7]), ('Pa3W', [5, 6], [4, 6]), 
                                               ('Pa4W', [6, 1], [5, 1]), ('Pa4W', [6, 1], [4, 1]), ('Pa5W', [5, 5], [4, 5]), ('Pa6W', [6, 2], [5, 2]), 
                                               ('Pa6W', [6, 2], [4, 2]), ('Pa7W', [5, 4], [4, 4]), ('Pa8W', [6, 3], [5, 3]), ('Pa8W', [6, 3], [4, 3])]):
        #print(legal_moves)
        #print(self.board)
        #self.print_board()
        move_score = [0 for _ in range(len(legal_moves))]
        for i in range(len(legal_moves)):
            move_score[i] = self.simulate_move(legal_moves[i], side)
        
        move_idx = self.norm_scores(move_score)
        selected_move = legal_moves[move_idx]
        #selected_move = random.choice(legal_moves)
        return selected_move

    def norm_scores(self, scores):
        # Convert to a numpy array
        #print('ln 54: ', scores)
        arr = np.array(scores)

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
        #max_value = np.max(normalized_array)
        #max_indices = np.where(normalized_array == max_value)[0]
        #random_index = random.choice(max_indices)
        random_index = np.random.choice(len(normalized_array), p=normalized_array/np.sum(normalized_array))

        return random_index

    def simulate_move(self, move, side):
        #print("================================================")
        #print("\n\nBoard before: ")
        #self.print_board()

        #print(f'Simulating move {move}')
        start_pos = move[1]
        end_pos = move[2]
        piece_id = f'{move[0][-1]}{move[0][0]}'

        original_piece_at_target = self.board[end_pos[0]][end_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece_id
        self.board[start_pos[0]][start_pos[1]] = 0

        score = self.get_heuristic(side)
        castle_s = self.handle_castle(piece_id, start_pos, end_pos) * self.k_c
        # TODO simulate pawn becoming queen
        # TODO iteraterive movement
        score += castle_s
        self.board[end_pos[0]][end_pos[1]] = original_piece_at_target
        self.board[start_pos[0]][start_pos[1]] = piece_id

        return score

    def get_heuristic(self, side):
        

        total_score_from_piece_position = 0
        total_score_from_piece_position_enemy = 0

        for i in range(len(self.board)):
            for j in range(len(self.board)):
                if self.board[i][j] == 0:
                    continue

                p_side, p_type = self.board[i][j][0], self.board[i][j][1]

                if p_side[0] == side[0].upper():
                    total_score_from_piece_position += self.apply_map_weight(p_side, p_type, i, j)              # position score
                    total_score_from_piece_position += self.apply_ptype_score(p_type)                           # type score
                else:
                    total_score_from_piece_position_enemy += self.apply_map_weight(p_side, p_type, i, j)        # position score
                    total_score_from_piece_position_enemy += self.apply_ptype_score(p_type)*self.k_p             # type score
        
        #print('ln 114: ', total_score_from_piece_position, total_score_from_piece_position_enemy, total_score_from_piece_position - total_score_from_piece_position_enemy)
        return total_score_from_piece_position - total_score_from_piece_position_enemy

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
