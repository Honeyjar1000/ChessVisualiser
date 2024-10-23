import random

try:
    from agents.agent_base import base_agent
except ModuleNotFoundError:
    from agent_base import base_agent

class random_agent(base_agent):
    def __init__(self, scene, white_pieces, black_pieces, WHITE_PIECE_DICT, BLACK_PIECE_DICT, board):
        super().__init__(scene, white_pieces, black_pieces, WHITE_PIECE_DICT, BLACK_PIECE_DICT, board)
    
    def select_from_legal_moves(self, side, legal_moves):
        selected_move = random.choice(legal_moves)
        return selected_move

        


if __name__ == "__main__":
    r = random_agent()
    r.select_from_legal_moves()
