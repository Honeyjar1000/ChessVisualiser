from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.vaos['cube'] = self.get_vao(
            program=self.program.programs['default'],
            vbo = self.vbo.vbos['cube'])

        # shadow cube vao
        self.vaos['shadow_cube'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo = self.vbo.vbos['cube'])

        # cat vao
        self.vaos['cat'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['cat'])

        # shadow cat vao
        self.vaos['shadow_cat'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['cat'])
        


        # black bishop vao
        self.vaos['black_bishop'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['black_bishop'])
        
        # white bishop vao
        self.vaos['white_bishop'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['white_bishop'])
        
        # black knight vao
        self.vaos['black_knight'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['black_knight'])
        
        # white knight vao
        self.vaos['white_knight'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['white_knight'])
        
        # black rook vao
        self.vaos['black_rook'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['black_rook'])
        
        # white rook vao
        self.vaos['white_rook'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['white_rook'])
        
        # black king vao
        
        self.vaos['black_king'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['black_king'])
        
        # white king vao
        self.vaos['white_king'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['white_king'])
        
        # black queen vao
        self.vaos['black_queen'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['black_queen'])
        
        # white queen vao
        self.vaos['white_queen'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['white_queen'])
        
        # black pawn vao
        self.vaos['black_pawn'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['black_pawn'])
        
        # white queen vao
        self.vaos['white_pawn'] = self.get_vao(
            program=self.program.programs['default'],
            vbo=self.vbo.vbos['white_pawn'])
        
        ### SHADOWS ###

        # black bishop vao
        self.vaos['shadow_black_bishop'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['black_bishop'])
        
        # white bishop vao
        self.vaos['shadow_white_bishop'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['white_bishop'])
        
        # black knight vao
        self.vaos['shadow_black_knight'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['black_knight'])
        
        # white knight vao
        self.vaos['shadow_white_knight'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['white_knight'])
        
        # black rook vao
        self.vaos['shadow_black_rook'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['black_rook'])
        
        # white rook vao
        self.vaos['shadow_white_rook'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['white_rook'])
        
        # black king vao
        self.vaos['shadow_black_king'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['black_king'])
        
        # white king vao
        self.vaos['shadow_white_king'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['white_king'])
        
        # black queen vao
        self.vaos['shadow_black_queen'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['black_queen'])
        
        # white queen vao
        self.vaos['shadow_white_queen'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['white_queen'])
        
        # black pawn vao
        self.vaos['shadow_black_pawn'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['black_pawn'])
        
        # white queen vao
        self.vaos['shadow_white_pawn'] = self.get_vao(
            program=self.program.programs['shadow_map'],
            vbo=self.vbo.vbos['white_pawn'])
        





        # skybox vao
        self.vaos['skybox'] = self.get_vao(
            program=self.program.programs['skybox'],
            vbo=self.vbo.vbos['skybox'])

        # advanced_skybox vao
        self.vaos['advanced_skybox'] = self.get_vao(
            program=self.program.programs['advanced_skybox'],
            vbo=self.vbo.vbos['advanced_skybox'])

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)], skip_errors=True)
        return vao

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()