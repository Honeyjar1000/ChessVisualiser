import random
import numpy as np
import copy

class base_agent:
    def __init__(self, scene, white_pieces, black_pieces, WHITE_PIECE_DICT, BLACK_PIECE_DICT, board):
        
        self.WHITE_PIECE_DICT = WHITE_PIECE_DICT
        self.BLACK_PIECE_DICT = BLACK_PIECE_DICT

        self.white_pieces = white_pieces
        self.black_pieces = black_pieces

        self.board = board
        self.scene = scene

        
        
    def select_from_legal_moves(self, side, legal_moves): ...
    
    def make_move(self, side):
        pieces, piece_dict, opponent_pieces, opponent_dict = self.get_pieces_arr(side)
        print("\n------------------------------------------------------------\n")
        legal_moves = []
        for piece_name, piece_data in pieces.items():
            piece_type, position, b_moved = piece_dict[piece_name]
            possible_moves = self.get_legal_moves(piece_type, position, side)
            for move in possible_moves:
                legal_moves.append((piece_name, position, move))  # Store piece, current position, and move
                
        if not legal_moves:
            print(f"No legal moves available for {side}")
            return [None, []], False
        
        selected_move = self.select_from_legal_moves(side, legal_moves)
         
        piece_name, position, new_position = selected_move

        # Handle capturing opponent pieces
        opponent_piece_code = self.board[new_position[0]][new_position[1]]
        if opponent_piece_code != 0:  # If there is an opponent's piece in the target square
            for opp_piece_name, opp_piece_data in opponent_pieces.items():
                if opponent_dict[opp_piece_name][0] == opponent_piece_code and opponent_dict[opp_piece_name][1] == new_position:
                    self.scene.remove_object(opp_piece_name)   
                    del opponent_dict[opp_piece_name]  # Remove from the piece abbreviation dictionary
                    break
        
        # Move the piece on the board
        self.board[position[0]][position[1]] = 0  # Remove piece from old position
        self.board[new_position[0]][new_position[1]] = piece_dict[piece_name][0]  # Place piece on new position using abbreviation
        piece_dict[piece_name][1] = new_position  # Update the piece's position in the dictionary
        
        # Handle Castling
        x, y = int((new_position[0]-4)*6), int((new_position[1]-4)*6)
        out = [piece_name, [x, y]]
        b_is_castling = False
        if piece_name[0:2] == "Ki":
            b_is_castling = self.is_castling(side, out)

        if out[0] is None:      # Game Over
            return out, False
        
        # Check if the piece to move is a pawn and if it has reached the promotion row
        if out[0].startswith("Pa"):  # Pawn detected
            promotion_row = 0 if side == 'white' else 7
            current_pos = self.scene.brain.WHITE_PIECE_DICT[out[0]][1] if side == 'white' else self.scene.brain.BLACK_PIECE_DICT[out[0]][1]
            
            if current_pos[0] == promotion_row:
                # Call scene promotion method before moving the pawn
                out = self.scene.promote_pawn(out[0], out[1], side)  # You can ask for promotion choice or default to Queen
                print("promote pawn instruction:",  out)
                return out, False  # Return early after promotion
            
        if side == "white":
            self.WHITE_PIECE_DICT[out[0]][2] = True
        else:
            self.BLACK_PIECE_DICT[out[0]][2] = True

        return out, b_is_castling
    

    
    def get_pieces_arr(self, side):
        if side == 'white':
            pieces = self.white_pieces
            piece_dict = self.WHITE_PIECE_DICT
            opponent_pieces = self.black_pieces
            opponent_dict = self.BLACK_PIECE_DICT
        else:
            pieces = self.black_pieces
            piece_dict = self.BLACK_PIECE_DICT
            opponent_pieces = self.white_pieces
            opponent_dict = self.WHITE_PIECE_DICT
        return pieces, piece_dict, opponent_pieces, opponent_dict

    def get_legal_moves(self, piece_type, position, side, b_second_move=False):
        #print(piece_type)
        moves = []
        row, col = position
        # print(f"side {side} | checking {piece_type} at {position}")
        if piece_type == "WP":  # White Pawn
            if row > 0 and (self.board[row - 1][col] == 0):  # Move forward
                moves.append([row - 1, col])
            if row == 6 and (self.board[row - 1][col] == 0) and (self.board[row - 2][col] == 0):  # Two steps forward if not blocked
                moves.append([row - 2, col])
            # Capture diagonally
            if row > 0 and col > 0 and self.board[row - 1][col - 1] in [val[0] for val in self.BLACK_PIECE_DICT.values()]:
                moves.append([row - 1, col - 1])
            if row > 0 and col < 7 and self.board[row - 1][col + 1] in [val[0] for val in self.BLACK_PIECE_DICT.values()]:
                moves.append([row - 1, col + 1])

        elif piece_type == "BP":  # Black Pawn
            if row < 7 and (self.board[row + 1][col] == 0):  # Move forward
                moves.append([row + 1, col])
            if row == 1 and (self.board[row + 1][col] == 0) and (self.board[row + 2][col] == 0):  # Two steps forward if not blocked
                moves.append([row + 2, col])
            # Capture diagonally
            if row < 7 and col > 0 and self.board[row + 1][col - 1] in [val[0] for val in self.WHITE_PIECE_DICT.values()]:
                moves.append([row + 1, col - 1])
            if row < 7 and col < 7 and self.board[row + 1][col + 1] in [val[0] for val in self.WHITE_PIECE_DICT.values()]:
                moves.append([row + 1, col + 1])
        
        elif piece_type == "WR" or piece_type == "BR":  # Rook
            # Horizontal and vertical moves
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
            for d in directions:
                r, c = row, col
                while 0 <= r + d[0] <= 7 and 0 <= c + d[1] <= 7:
                    r += d[0]
                    c += d[1]
                    if self.board[r][c] == 0:
                        moves.append([r, c])
                    elif (side == 'white' and self.board[r][c] in [val[0] for val in self.BLACK_PIECE_DICT.values()]) or (side == 'black' and self.board[r][c] in [val[0] for val in self.WHITE_PIECE_DICT.values()]):
                        moves.append([r, c])  # Capture
                        break  # Stop after encountering a piece (whether capturing or blocked)
                    else:
                        break  # Blocked by own piece

        elif piece_type == "WB" or piece_type == "BB":  # Bishop
            # Diagonal moves
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Top-left, top-right, bottom-left, bottom-right
            for d in directions:
                r, c = row, col
                while 0 <= r + d[0] <= 7 and 0 <= c + d[1] <= 7:
                    r += d[0]
                    c += d[1]
                    if self.board[r][c] == 0:
                        moves.append([r, c])
                    elif (side == 'white' and self.board[r][c] in [val[0] for val in self.BLACK_PIECE_DICT.values()]) or (side == 'black' and self.board[r][c] in [val[0] for val in self.WHITE_PIECE_DICT.values()]):
                        moves.append([r, c])  # Capture
                        break  # Stop after encountering a piece (whether capturing or blocked)
                    else:
                        break  # Blocked by own piece

        elif piece_type == "WQ" or piece_type == "BQ":  # Queen (combines rook and bishop moves)
            #print("CHECKING QUEEN")
            # Horizontal, vertical, and diagonal moves
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
            for d in directions:
                r, c = row, col
                while 0 <= r + d[0] <= 7 and 0 <= c + d[1] <= 7:
                    r += d[0]
                    c += d[1]
                    if self.board[r][c] == 0:
                        moves.append([r, c])
                    elif (side == 'white' and self.board[r][c] in [val[0] for val in self.BLACK_PIECE_DICT.values()]) or (side == 'black' and self.board[r][c] in [val[0] for val in self.WHITE_PIECE_DICT.values()]):
                        moves.append([r, c])  # Capture
                        break  # Stop after encountering a piece (whether capturing or blocked)
                    else:
                        break  # Blocked by own piece

        elif piece_type == "WN" or piece_type == "BN":  # Knight
            knight_moves = [
                (-2, -1), (-2, 1), (2, -1), (2, 1),
                (-1, -2), (-1, 2), (1, -2), (1, 2)
            ]
            for d in knight_moves:
                r, c = row + d[0], col + d[1]
                if 0 <= r <= 7 and 0 <= c <= 7:
                    if (self.board[r][c] == 0) or (side == 'white' and self.board[r][c] in [val[0] for val in self.BLACK_PIECE_DICT.values()]) or (side == 'black' and self.board[r][c] in [val[0] for val in self.WHITE_PIECE_DICT.values()]):
                        moves.append([r, c])

        elif piece_type == "WK" or piece_type == "BK":  # King
            king_moves = [
                (-1, 0), (1, 0), (0, -1), (0, 1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)
            ]
            for d in king_moves:
                r, c = row + d[0], col + d[1]
                if 0 <= r <= 7 and 0 <= c <= 7:
                    if (self.board[r][c] == 0) or \
                    (side == 'white' and self.board[r][c] in [val[0] for val in self.BLACK_PIECE_DICT.values()]) or \
                    (side == 'black' and self.board[r][c] in [val[0] for val in self.WHITE_PIECE_DICT.values()]):
                        # Simulate the move to ensure the king is not moving into check
                        original_piece_at_target = self.board[r][c]
                        self.board[r][c] = piece_type
                        self.board[row][col] = 0  # Remove the king from the old position

                        # Pass the new position of the king to is_in_check
                        if not self.is_in_check(side, [r, c], piece_type):
                            moves.append([r, c])

                        # Revert the board to its original state
                        self.board[r][c] = original_piece_at_target
                        self.board[row][col] = piece_type
            moves.extend(self.can_castle(side))

        #print(f"Before check - Legal moves available for {piece_type} at {position}: {moves} | second move: {b_second_move}")
        # Filter the moves: Only allow moves that do not result in check
        if not b_second_move:
            legal_moves = []
            for move in moves:
                # Simulate the move
                original_piece_at_target = self.board[move[0]][move[1]]
                self.board[move[0]][move[1]] = piece_type
                self.board[row][col] = 0  # Empty the old square

                # Temporarily remove the captured piece from the dictionary, if applicable
                removed_piece = None
                if side == 'white':  # If the current side is white
                    for piece_name, piece_data in self.BLACK_PIECE_DICT.items():
                        if piece_data[1] == move:  # If this black piece is in the target move position
                            removed_piece = piece_name  # Mark the captured piece
                            b_moved = piece_data[2]
                            del self.BLACK_PIECE_DICT[piece_name]  # Remove it from the dictionary
                            break
                else:  # If the current side is black
                    for piece_name, piece_data in self.WHITE_PIECE_DICT.items():
                        if piece_data[1] == move:  # If this white piece is in the target move position
                            removed_piece = piece_name  # Mark the captured piece
                            b_moved = piece_data[2]
                            del self.WHITE_PIECE_DICT[piece_name]  # Remove it from the dictionary
                            break

                # Check if the move leaves the king in check
                king_position = move if piece_type in ['WK', 'BK'] else None
                if not self.is_in_check(side, king_position, piece_type):
                    legal_moves.append(move)

                # Revert the move
                self.board[move[0]][move[1]] = original_piece_at_target
                self.board[row][col] = piece_type

                # Re-add the captured piece to the dictionary if there was one
                if removed_piece:
                    piece_dict = self.BLACK_PIECE_DICT if side == 'white' else self.WHITE_PIECE_DICT
                    piece_dict[removed_piece] = [original_piece_at_target, move, b_moved]  # Restore the captured piece

            return legal_moves
        else:
            return moves
    
    def is_in_check(self, side, king_position=None, piece_type=None):
        # Get the position of the current player's king, unless it's provided (e.g., when the king is moving)
        if king_position is None:
            king_position = self.get_king_position(side)

        if king_position is None:
            print(f"Error: {side} king not found!")
            return False

        # Determine the opponent's side and pieces
        opponent_side = 'black' if side == 'white' else 'white'
        opponent_pieces = self.BLACK_PIECE_DICT if side == 'white' else self.WHITE_PIECE_DICT

        opponent_king_position = self.get_king_position(opponent_side)

        # Check if any opponent piece can attack the king's position, but exclude the captured piece
        for opp_piece_name, opp_piece_data in opponent_pieces.items():
            opp_piece_type, opp_position, b_moved = opp_piece_data
            #print(opp_piece_type)
            if opp_piece_type == "BK" or opp_piece_type == "WK":  # Check if the piece is a king
                # Special case for checking the opponent king's immediate surroundings
                dist = (abs(opponent_king_position[0] - king_position[0]), abs(opponent_king_position[1] - king_position[1]))
                if max(dist) <= 1:  # Check if the kings are next to each other (horizontally, vertically, or diagonally)
                    return True
            else:
                # Get all legal moves of the opponent piece, but ignore if the piece was taken during the simulation
                if self.board[opp_position[0]][opp_position[1]] == 0:  # Check if the piece has been captured
                    continue

                legal_moves = self.get_legal_moves(opp_piece_type, opp_position, opponent_side, b_second_move=True)
                if king_position in legal_moves:
                    return True

        return False
    
    def get_king_position(self, side):
        pieces = self.WHITE_PIECE_DICT if side == 'white' else self.BLACK_PIECE_DICT
        for piece_name, piece_data in pieces.items():
            # piece_data[0] contains the piece type (e.g., 'WK' or 'BK')
            # piece_data[1] contains the position
            if piece_data[0] == 'WK' and side == 'white':
                return piece_data[1]  # Return the position of the white king
            elif piece_data[0] == 'BK' and side == 'black':
                return piece_data[1]  # Return the position of the black king
        return None
    
    def can_castle(self, side):
        """
        Check if castling is possible for the given side.
        Returns a list of castling moves if valid, otherwise an empty list.
        """
        moves = []
        if side == 'white':
            king_pos = [7, 3]  # White King initial position
            rook_k_pos = [7, 7]  # White Rook kingside position
            rook_q_pos = [7, 0]  # White Rook queenside position
        else:
            king_pos = [0, 3]  # Black King initial position
            rook_k_pos = [0, 7]  # Black Rook kingside position
            rook_q_pos = [0, 0]  # Black Rook queenside position

        # Check kingside castling
        if self.is_castling_valid(king_pos, rook_k_pos, side):
            moves.append([king_pos[0], 5])  # Move king to kingside castling square

        # Check queenside castling
        if self.is_castling_valid(king_pos, rook_q_pos, side):
            moves.append([king_pos[0], 1])  # Move king to queenside castling square

        return moves
        
    def is_castling_valid(self, king_pos, rook_pos, side):
        """
        Checks whether castling between the king and rook is valid.
        1. Neither the king nor the rook should have moved.
        2. There should be no pieces between them.
        3. The king should not pass through or land on squares under attack.
        """
        # Ensure neither piece has moved (you can track this with a 'has_moved' flag on the pieces)
        # print("is casting valid?")
        if side == 'white':
            if (self.scene.brain.WHITE_PIECE_DICT['Ki1W'][2]):
                return False
            elif (rook_pos == [7, 7]):
                if 'Ro1W' in self.scene.brain.WHITE_PIECE_DICT:
                    if (self.scene.brain.WHITE_PIECE_DICT['Ro1W'][2]):
                        return False
                else:
                    return False
            elif (rook_pos == [7, 0]):
                if 'Ro2W' in self.scene.brain.WHITE_PIECE_DICT:
                    if (self.scene.brain.WHITE_PIECE_DICT['Ro2W'][2]):
                        return False
                else:
                    return False
        else:
            if self.scene.brain.BLACK_PIECE_DICT['Ki1B'][2]:
                return False
            elif (rook_pos == [0, 7]):
                if 'Ro1B' in self.scene.brain.BLACK_PIECE_DICT:
                    if (self.scene.brain.BLACK_PIECE_DICT['Ro1B'][2]):
                        return False
                else:
                    return False
            elif (rook_pos == [0, 0]):
                if 'Ro2B' in self.scene.brain.BLACK_PIECE_DICT:
                    if (self.scene.brain.BLACK_PIECE_DICT['Ro2B'][2]):
                        return False 
                else:
                    return False
        #print(" past test 1 ")
        if (self.board[rook_pos[0]][rook_pos[1]] not in ['WR', 'BR']) or \
        (self.board[king_pos[0]][king_pos[1]] not in ['WK', 'BK']):
            #print("Cant castle because piece moved")
            return False

        # Check if there are pieces between the king and rook
        step = 1 if rook_pos[1] > king_pos[1] else -1
        for col in range(king_pos[1] + step, rook_pos[1], step):
            if self.board[king_pos[0]][col] != 0:
                #print("Cant castle because piece between rook and king", rook_pos, king_pos)
                return False

        # Ensure the king does not move through or into check
        for col in range(min(king_pos[1], rook_pos[1]), max(king_pos[1], rook_pos[1]) + 1):
            if self.is_in_check(side, [king_pos[0], col], 'WK' if side == 'white' else 'BK'):
                #print("Cant castle accross check")
                return False
        #print(" CASTLE VALID ")
        return True
    
    def is_castling(self, side, move, speed=0.2, b_iter=False):
        move = [move[0], int((move[1][0]/6)+4), int((move[1][1]/6)+4)]

        

        if side == 'white':
            piece_dict = self.scene.brain.white_pieces
            pieces = self.scene.brain.WHITE_PIECE_DICT
            
        else:
            piece_dict = self.scene.brain.black_pieces
            pieces = self.scene.brain.BLACK_PIECE_DICT

        

        if move[0][0:2] != 'Ki':
            return False
        
        b_found = False
        if not b_iter:
            if side == 'white':
                if ([move[1], move[2]] == [7, 5]) and (self.scene.brain.board[7][7] == "WR"):
                    king_start, rook_start, king_target, rook_target = (7, 3), (7, 7), (7, 5), (7, 4)
                    piece_name = 'Ro1W'
                    b_found = True
                elif ([move[1], move[2]] == [7, 1]) and (self.scene.brain.board[7][0] == "WR"):
                    king_start, rook_start, king_target, rook_target = (7, 3), (7, 0), (7, 1), (7, 2)
                    piece_name = 'Ro2W'
                    b_found = True

            else:
                if ([move[1], move[2]] == [0, 5]) and (self.scene.brain.board[0][7] == "BR"):
                    king_start, rook_start, king_target, rook_target = (0, 3), (0, 7), (0, 5), (0, 4)
                    piece_name = 'Ro1B'
                    b_found = True
                elif ([move[1], move[2]] == [0, 1]) and (self.scene.brain.board[0][0] == "BR"):
                    king_start, rook_start, king_target, rook_target = (0, 3), (0, 0), (0, 1), (0, 2)
                    piece_name = 'Ro2B'
                    b_found = True
        else:
            if side == 'white':
                if ([move[1], move[2]] == [7, 5]):
                    king_start, rook_start, king_target, rook_target = (7, 3), (7, 7), (7, 5), (7, 4)
                    piece_name = 'Ro1W'
                    b_found = True
                elif ([move[1], move[2]] == [7, 1]):
                    king_start, rook_start, king_target, rook_target = (7, 3), (7, 0), (7, 1), (7, 2)
                    piece_name = 'Ro2W'
                    b_found = True

            else:
                if ([move[1], move[2]] == [0, 5]):
                    king_start, rook_start, king_target, rook_target = (0, 3), (0, 7), (0, 5), (0, 4)
                    piece_name = 'Ro1B'
                    b_found = True
                elif ([move[1], move[2]] == [0, 1]):
                    king_start, rook_start, king_target, rook_target = (0, 3), (0, 0), (0, 1), (0, 2)
                    piece_name = 'Ro2B'
                    b_found = True
        
        if not b_found:
            return False 
        
        if not b_iter:
            self.scene.brain.board[rook_start[0]][rook_start[1]] = 0  # Remove piece from old position
            self.scene.brain.board[rook_target[0]][rook_target[1]] = pieces[piece_name][0]
            pieces[piece_name][1] = rook_target  # Update the piece's position in the dictionary
            pieces[piece_name][2] = True    # Rook moves when castle
            # BUG rook can still be taken on move after castle?

        move[1], move[2] = int((move[1]-4)*6), int((move[2]-4)*6)
        rook_target2 = [int((rook_target[0]-4)*6), int((rook_target[1]-4)*6)]

        # move king
        diff1 = [(  (-piece_dict[f'{move[0]}'].pos[0] + move[1])* speed), 
                (   (-piece_dict[f'{move[0]}'].pos[2] + move[2]) * speed)] 
        # move Rook
        diff2 = [(  (-piece_dict[f'{piece_name}'].pos[0] + rook_target2[0]) * speed), 
                (   (-piece_dict[f'{piece_name}'].pos[2] + rook_target2[1]) * speed) ] 
        
        cond1 = (abs(diff1[0]) + abs(diff1[1]) < 1e-4)
        cond2 = (abs(diff2[0]) + abs(diff2[1]) < 1e-4)
    
        if cond1 and cond2:
            if self.scene.brain.scene.check_mate:
                self.scene.brain.scene.game_finished = True
                return True
            self.scene.b_is_castling = False
            self.scene.move_complete = True
            if self.scene.side =="white":
                self.scene.side ="black"
            else:
                self.scene.side ="white"
            return False
        else:
            # move king
            
            piece_dict[f'{move[0]}'].pos = (
                piece_dict[f'{move[0]}'].pos[0]+diff1[0],           
                piece_dict[f'{move[0]}'].pos[1],        
                piece_dict[f'{move[0]}'].pos[2]+diff1[1]
            )

            # move Rook
            piece_dict[f'{piece_name}'].pos = (
                piece_dict[f'{piece_name}'].pos[0]+diff2[0],     
                piece_dict[f'{piece_name}'].pos[1],     
                piece_dict[f'{piece_name}'].pos[2]+diff2[1]
            )
        
        return True