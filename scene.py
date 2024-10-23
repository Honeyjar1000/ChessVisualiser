from model import *
import glm
from brain import brain
import copy
import os
import sys
import time

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.brain = None
        self.white_pieces = {}
        self.black_pieces = {}
        self.load()
        # skybox
        self.skybox = AdvancedSkyBox(app)
        self.move_complete = True
        self.move = None
        self.side = "white"
        self.game_finished = False

        self.check_mate = False
        self.stale_mate = False

        self.b_is_castling = False

        self.end_game_timer = time.time()
        self.end_game_delay = 10.0

    def add_object(self, obj):
        self.objects.append(obj)
        return obj

    def load(self):
        app = self.app
        add = self.add_object

        # floor
        cnt = 0 
        n, s = 24, 6
        for x in range(-n, n, s):
            cnt += 1
            for z in range(-n, n, s):
                cnt += 1
                cur_tex_id = 0
                if cnt%2==0:
                    cur_tex_id = 1
                
                add(Cube(app, pos=(x, -10, z), tex_id=cur_tex_id, scale=(3,3,3)))
            

        
        self.black_pieces['Ro1B'] = add(RookBlack(app, pos=(-24, -7, 18), scale=(2,2,2)))
        self.black_pieces['Ro2B'] = add(RookBlack(app, pos=(-24, -7, -24), scale=(2,2,2)))

        self.white_pieces['Ro1W'] = add(RookWhite(app, pos=(18, -7, 18), scale=(2,2,2)))
        self.white_pieces['Ro2W'] = add(RookWhite(app, pos=(18, -7, -24), scale=(2,2,2)))

        self.black_pieces['Ni1B'] = add(KnightBlack(app, pos=(-24, -7, 12), scale=(2,2,2)))
        self.black_pieces['Ni2B'] = add(KnightBlack(app, pos=(-24, -7, -18), scale=(2,2,2)))

        self.white_pieces['Ni1W'] = add(KnightWhite(app, pos=(18, -7, 12), scale=(2,2,2)))
        self.white_pieces['Ni2W'] = add(KnightWhite(app, pos=(18, -7, -18), scale=(2,2,2)))

        self.black_pieces['Bi1B'] = add(BishopBlack(app, pos=(-24, -7, 6), scale=(2,2,2)))
        self.black_pieces['Bi2B'] = add(BishopBlack(app, pos=(-24, -7, -12), scale=(2,2,2)))

        self.white_pieces['Bi1W'] = add(BishopWhite(app, pos=(18, -7, 6), scale=(2,2,2)))
        self.white_pieces['Bi2W'] = add(BishopWhite(app, pos=(18, -7, -12), scale=(2,2,2)))

        self.black_pieces['Qu1B'] = add(QueenBlack(app, pos=(-24, -7, 0), scale=(2,2,2)))
        self.black_pieces['Ki1B'] = add(KingBlack(app, pos=(-24, -7, -6), scale=(2,2,2)))

        self.white_pieces['Qu1W'] = add(QueenWhite(app, pos=(18, -7, 0), scale=(2,2,2)))
        self.white_pieces['Ki1W'] = add(KingWhite(app, pos=(18, -7, -6), scale=(2,2,2)))

        

        self.black_pieces['Pa1B'] = add(PawnBlack(app, pos=(-18, -7, 18), scale=(2,2,2)))
        self.black_pieces['Pa2B'] = add(PawnBlack(app, pos=(-18, -7, -24), scale=(2,2,2)))

        self.white_pieces['Pa1W'] = add(PawnWhite(app, pos=(12, -7, 18), scale=(2,2,2)))
        self.white_pieces['Pa2W'] = add(PawnWhite(app, pos=(12, -7, -24), scale=(2,2,2)))

        self.black_pieces['Pa3B'] = add(PawnBlack(app, pos=(-18, -7, 12), scale=(2,2,2)))
        self.black_pieces['Pa4B'] = add(PawnBlack(app, pos=(-18, -7, -18), scale=(2,2,2)))

        self.white_pieces['Pa3W'] = add(PawnWhite(app, pos=(12, -7, 12), scale=(2,2,2)))
        self.white_pieces['Pa4W'] = add(PawnWhite(app, pos=(12, -7, -18), scale=(2,2,2)))

        self.black_pieces['Pa5B'] = add(PawnBlack(app, pos=(-18, -7, 6), scale=(2,2,2)))
        self.black_pieces['Pa6B'] = add(PawnBlack(app, pos=(-18, -7, -12), scale=(2,2,2)))

        self.white_pieces['Pa5W'] = add(PawnWhite(app, pos=(12, -7, 6), scale=(2,2,2)))
        self.white_pieces['Pa6W'] = add(PawnWhite(app, pos=(12, -7, -12), scale=(2,2,2)))

        self.black_pieces['Pa7B'] = add(PawnBlack(app, pos=(-18, -7, 0), scale=(2,2,2)))
        self.black_pieces['Pa8B'] = add(PawnBlack(app, pos=(-18, -7, -6), scale=(2,2,2)))

        self.white_pieces['Pa7W'] = add(PawnWhite(app, pos=(12, -7, 0), scale=(2,2,2)))
        self.white_pieces['Pa8W'] = add(PawnWhite(app, pos=(12, -7, -6), scale=(2,2,2)))

        self.brain = brain(self, black_pieces=self.black_pieces, white_pieces=self.white_pieces)

    def update(self):
        #self.print_pieces_obs()
        #print("\n")
        speed = 0.3
        if self.game_finished:
            #print("Game over! Checkmate detected.")
            #self.reset_game("Checkmate or only two kings remaining.")
            return True
        
        if (self.check_mate) or (self.stale_mate):
            if (time.time() - self.end_game_timer < self.end_game_delay):
                return False
            else:
                self.game_finished = True
                return True
            
        if (self.stale_mate):
            diff = [((-pieces[f'{self.move[0]}'].pos[0] + self.move[1][0]) * speed),
                    ((-pieces[f'{self.move[0]}'].pos[2] + self.move[1][1]) * speed)]
            
            pieces[f'{self.move[0]}'].pos = (
                pieces[f'{self.move[0]}'].pos[0]+diff[0], 
                pieces[f'{self.move[0]}'].pos[1], 
                pieces[f'{self.move[0]}'].pos[2]+diff[1])
            
            if (time.time() - self.end_game_timer < self.end_game_delay):
                return False
            else:
                self.game_finished = True
                return True
            
        # Check if only two kings remain
        if self.only_two_kings():
            print("Only two kings remaining. Stalemate...")
            self.stale_mate = True
            self.end_game_timer = time.time()
            return False
        
        if self.b_is_castling:
            self.brain.agent.is_castling(self.side, self.move, speed=speed, b_iter=True)

        if self.side == "white":
            pieces = self.white_pieces
        else:
            pieces = self.black_pieces

        if self.move_complete:
            self.move_complete = False
            self.move, self.b_is_castling = self.brain.next_move(self.side)

            if self.move is None:
                print("Game over! Checkmate detected.")
                self.check_mate = True
                self.end_game_timer = time.time()
                return False
        
        # Handle normal piece movement (non-castling)
        if not self.b_is_castling:
            #print("ln 149: ", pieces)
            #self.brain.print_board()
            diff = [((-pieces[f'{self.move[0]}'].pos[0] + self.move[1][0]) * speed),
                    ((-pieces[f'{self.move[0]}'].pos[2] + self.move[1][1]) * speed)]
            if abs(diff[0]) + abs(diff[1]) < 1e-4:
                self.move_complete = True
                if self.side == "white":
                    self.side = "black"
                else:
                    self.side = "white"
            else:
                pieces[f'{self.move[0]}'].pos = (pieces[f'{self.move[0]}'].pos[0]+diff[0], pieces[f'{self.move[0]}'].pos[1], pieces[f'{self.move[0]}'].pos[2]+diff[1])
        return False
    

    def remove_object(self, piece_name):
        ''''
        Remove a piece from the scene by its object reference, ensuring the exact instance is removed.
        '''
        # Get the actual object reference for the piece
        piece_object = None
        if piece_name in self.white_pieces:
            piece_object = self.white_pieces[piece_name]
            del self.white_pieces[piece_name]  # Remove from white pieces
        elif piece_name in self.black_pieces:
            piece_object = self.black_pieces[piece_name]
            del self.black_pieces[piece_name]  # Remove from black pieces

        if piece_object is not None:
            if piece_object in self.objects:
                self.objects.remove(piece_object)
            else:
                print(f"Object for {piece_name} not found in objects list!")
        else:
            print(f"Could not find {piece_name} in scene.")


    def only_two_kings(self):
        """
        Check if only two kings (one white and one black) remain on the board.
        """
        #print("CHECK STALE MATE : ", self.white_pieces, '\t', self.black_pieces)
        if len(self.white_pieces) == 1 and len(self.black_pieces) == 1:
            return True
        return False

    def promote_pawn(self, pawn_name, pawn_end_pos, side):
        """
        Promote a pawn to a Queen. Could be extended to choose other pieces.
        """
        pieces = self.white_pieces if side == 'white' else self.black_pieces
        
        pawn_pos = pieces[pawn_name].pos
        self.remove_object(pawn_name)

        # Replace it with a new Queen object
        if side == 'white':
            tag = f'Qu{len(self.white_pieces)+1}W'
            new_piece = QueenWhite(self.app, pos=(pawn_pos[0], pawn_pos[1], pawn_pos[2]), scale=(2, 2, 2))
            self.white_pieces[tag] = self.add_object(new_piece)
            self.brain.white_pieces[tag] = new_piece

            self.brain.promote_pawn_in_brain(pawn_name, 'Queen', side='white', tag=tag)  # Inform the brain
        else:
            tag = f'Qu{len(self.white_pieces)+1}B'
            new_piece = QueenBlack(self.app, pos=(pawn_pos[0], pawn_pos[1], pawn_pos[2]), scale=(2, 2, 2))
            self.black_pieces[tag] = self.add_object(new_piece)
            self.brain.black_pieces[tag] = new_piece

            self.brain.promote_pawn_in_brain(pawn_name, 'Queen', side='black', tag=tag)  # Inform the brain

        x, y = pawn_end_pos[0], pawn_end_pos[1]
        '''
        x, y = pawn_pos[0], pawn_pos[2]
        x_val = round(pawn_pos[0],1)
        if x_val == -18:
            x = -24
        elif x_val == 12:
            x = 18
        else:
            print("PROMOTE PAWN ERROR")
        '''

        return [tag, [x,y]]
    

    def print_pieces_obs(self):
        for obj in self.objects:
            if obj.id == 'piece':
                print(obj, obj.pos)