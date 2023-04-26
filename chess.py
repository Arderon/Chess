import pygame
import os

WIDTH = 885
HEIGHT = 891
FPS = 60
timer = 0

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, "imgs")
sound_folder = os.path.join(game_folder, "sounds")
background = pygame.image.load(os.path.join(img_folder, "board.png")).convert_alpha()
background_rect = background.get_rect()
wKing_img = pygame.image.load(os.path.join(img_folder, "white_king.png")).convert_alpha()
wQueen_img = pygame.image.load(os.path.join(img_folder, "white_queen.png")).convert_alpha()
wRock_img = pygame.image.load(os.path.join(img_folder, "white_rock.png")).convert_alpha()
wBishop_img = pygame.image.load(os.path.join(img_folder, "white_bishop.png")).convert_alpha()
wKnight_img = pygame.image.load(os.path.join(img_folder, "white_knight.png")).convert_alpha()
wPawn_img = pygame.image.load(os.path.join(img_folder, "white_pawn.png")).convert_alpha()
bKing_img = pygame.image.load(os.path.join(img_folder, "black_king.png")).convert_alpha()
bQueen_img = pygame.image.load(os.path.join(img_folder, "black_queen.png")).convert_alpha()
bRock_img = pygame.image.load(os.path.join(img_folder, "black_rock.png")).convert_alpha()
bBishop_img = pygame.image.load(os.path.join(img_folder, "black_bishop.png")).convert_alpha()
bKnight_img = pygame.image.load(os.path.join(img_folder, "black_knight.png")).convert_alpha()
bPawn_img = pygame.image.load(os.path.join(img_folder, "black_pawn.png")).convert_alpha()
point_img = pygame.image.load(os.path.join(img_folder, "point.png")).convert_alpha()

BLACK = (0, 0, 0)

board_X0 = 30
board_Yend = HEIGHT - 36
length = (WIDTH - board_X0) / 8

sqOccupied = {}
sq_attacked_w = []
sq_attacked_b = []
turn = "w"
white_lines_of_attack = []
black_lines_of_attack = []
white_attacking_pieces = []
black_attacking_pieces = []


def attacked_squares_fill():
    for sprite in pieces.sprites():
        if sprite.color == "w":
            if sprite.type == "p":
                sq_attacked_w.extend(sprite.attacked_squares)
            else:
                sq_attacked_w.extend(sprite.available_squares)
        else:
            if sprite.type == "p":
                sq_attacked_b.extend(sprite.attacked_squares)
            else:
                sq_attacked_b.extend(sprite.available_squares)


class Point(pygame.sprite.Sprite):
    def __init__(self, c, r):
        pygame.sprite.Sprite.__init__(self)
        self.image = point_img
        self.rect = self.image.get_rect()
        self.rect.center = sqCenter((c, r))

    def update(self):
        if not tryToMove:
            self.kill()


def add_point(c, r):
    point = Point(c, r)
    all_sprites.add(point)


def sqCenter(cr):
    x = (cr[0] * length) - (length / 2) + board_X0
    y = (cr[1] * length) - (length / 2)
    return (x, y)


def sqFromCoords(xy):
    col = int((xy[0] - board_X0) / length + 1)
    row = int((xy[1]) / length + 1)
    return (col, row)


def sqCenterByCoords(xy):
    final = sqCenter((sqFromCoords((xy[0], xy[1]))))
    return final


def sqIsOccupied(cr):
    a = (cr[0], cr[1]) in sqOccupied
    return a


def clear_available_squares():
    for sprite in pieces.sprites():
        sprite.available_squares.clear()
        sprite.attacked_squares.clear()


def shah_to_white():
    if king_w.lastPos in sq_attacked_b:
        return True
    return False


def shah_to_black():
    if king_b.lastPos in sq_attacked_w:
        return True
    return False


# def parsing_guardian_lines():
# for sprite in pieces.sprites():
# for second_sprite in pieces.sprites():
# if sprite.color == second_sprite.color:
# if sprite.guardian_line == second_sprite.guardian_line and sprite.guardian_line != []:
# sprite.guardian = False
#  sprite.guardian_line.clear()
#   second_sprite.guardian = False
#  second_sprite.guardian_line.clear()

class Pieces(pygame.sprite.Sprite):
    def __init__(self, color, c, r, piece):
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        self.available_squares = []
        self.attacked_squares = []
        self.type = None
        self.line_of_attack = []
        self.guardian_line = []
        self.guardian = False
        self.current_danger = False
        self.attacker = 0
        if color == "w":
            if piece == "p":
                self.image = wPawn_img
            elif piece == "r":
                self.image = wRock_img
            elif piece == "k":
                self.image = wKing_img
            elif piece == "n":
                self.image = wKnight_img
            elif piece == "q":
                self.image = wQueen_img
            elif piece == "b":
                self.image = wBishop_img

        else:
            if piece == "p":
                self.image = bPawn_img
            elif piece == "r":
                self.image = bRock_img
            elif piece == "k":
                self.image = bKing_img
            elif piece == "n":
                self.image = bKnight_img
            elif piece == "q":
                self.image = bQueen_img
            elif piece == "b":
                self.image = bBishop_img
        self.rect = self.image.get_rect()
        self.rect.center = sqCenter((c, r))
        sqOccupied[(c, r)] = self
        self.lastPos = sqFromCoords(self.rect.center)

    def move(self, c, r, ):
        self.rect.center = sqCenter((c, r))

    def update(self):
        self.lastPos = sqFromCoords(self.rect.center)
        self.is_guardian()
        self.is_pieces_on_guardian_line()
        self.available_sq()

    def isAlly(self):
        if sqIsOccupied(click_cr):
            if sqOccupied[click_cr].color == self.color:
                return True

    def is_ally(self, c, r):
        if sqIsOccupied((c, r)):
            if sqOccupied[(c, r)].color == self.color:
                return True
        return False

    def available_sq(self):
        for i in range(1, 9):
            for k in range(1, 9):
                if self.isLegalMove(i, k) and not self.is_ally(i, k) and (i, k) not in self.available_squares:
                    self.available_squares.append((i, k))

                elif self.isLegalMoveToAlly(i, k) and self.type != "p":
                    if self.color == "w":
                        sq_attacked_w.append((i, k))
                    else:
                        sq_attacked_b.append((i, k))

    def draw_points(self):
        for c in range(1, 9):
            for r in range(1, 9):
                if self.isLegalMove(c, r):
                    add_point(c, r)

    def is_legal_move(self, c, r):
        if self.legalMove(c, r):
            return True
        else:
            return False

    def who_on_square(self, c, r):
        if sqIsOccupied((c, r)):
            return sqOccupied[(c, r)]
        else:
            return False

    def is_guardian(self):
        self.guardian_line.clear()
        self.attacker = 0
        for sprite in pieces.sprites():
            if self.color != sprite.color:
                if self.lastPos in sprite.line_of_attack:
                    self.guardian_line.extend(sprite.line_of_attack)
                    self.guardian = True
                    sprite.current_danger = True
                    if sprite.color == "w":
                        white_attacking_pieces.append(sprite)
                    else:
                        black_attacking_pieces.append(sprite)
                    self.attacker = sprite
                    return True
        self.guardian = False

    def is_pieces_on_guardian_line(self):
        for sprite in pieces.sprites():
            if sprite.lastPos in self.guardian_line and sprite.lastPos != self.lastPos:
                self.guardian = False
                self.guardian_line.clear()
                return False
        return True

    def clear_current_danger(self):
        for sprite in pieces.sprites():
            if len(self.line_of_attack) == 0 or (
                    sprite.lastPos in self.line_of_attack and len(self.line_of_attack) > 0):
                self.current_danger = False
                if self in white_attacking_pieces:
                    white_attacking_pieces.remove(self)
                    return False
                if self in black_attacking_pieces:
                    black_attacking_pieces.remove(self)
                    return False
                break
        else:
            if len(self.line_of_attack) > 0:
                self.current_danger = True
                if self.color == "w":
                    if self not in white_attacking_pieces:
                        white_attacking_pieces.append(self)
                else:
                    if self not in black_attacking_pieces:
                        black_attacking_pieces.append(self)


class Pawn(Pieces):
    def __init__(self, color, c, r):
        Pieces.__init__(self, color, c, r, "p")
        self.first_move = True
        self.type = "p"

    def update(self):
        Pieces.update(self)
        self.at_sq()

    def at_sq(self):
        if self.color == "w":
            self.attacked_squares = [(self.lastPos[0] - 1, self.lastPos[1] - 1),
                                     (self.lastPos[0] + 1, self.lastPos[1] - 1)]
        else:
            self.attacked_squares = [(self.lastPos[0] - 1, self.lastPos[1] + 1),
                                     (self.lastPos[0] + 1, self.lastPos[1] + 1)]

    def draw_points(self):
        Pieces.draw_points(self)

    def legalMove(self, c, r):
        if self.color == "w":
            if self.first_move and c == self.lastPos[0] and (r == self.lastPos[1] - 2) and not sqIsOccupied(
                    (c, r)) and not sqIsOccupied((c, r + 1)):
                return True
            elif c == self.lastPos[0] and r == self.lastPos[1] - 1 and not sqIsOccupied((c, r)):
                return True
            elif sqIsOccupied((c, r)) and abs(c - self.lastPos[0]) == 1 and self.lastPos[1] - r == 1:
                return True
            else:
                return False
        else:
            if self.first_move and c == self.lastPos[0] and (r == self.lastPos[1] + 2) and not sqIsOccupied(
                    (c, r)) and not sqIsOccupied((c, r - 1)):
                return True
            elif c == self.lastPos[0] and r == self.lastPos[1] + 1 and not sqIsOccupied((c, r)):
                return True
            elif sqIsOccupied((c, r)) and abs(c - self.lastPos[0]) == 1 and self.lastPos[1] - r == -1:
                return True
            else:
                return False

    def isLegalMove(self, c, r):
        if self.guardian:
            if Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r) and (
                    (c, r) in self.guardian_line or (c, r) == self.attacker.lastPos):
                return True
            else:
                return False

        elif self.color == "w" and shah_to_white():
            if len(black_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r) and len(
                    black_attacking_pieces) > 0:
                if (c, r) in black_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r) and len(
                    black_attacking_pieces) > 0:
                if (c, r) == black_attacking_pieces[0].lastPos:
                    return True
        elif self.color == "b" and shah_to_black():
            if len(white_attacking_pieces) > 1:
                return False
            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r) and len(
                    white_attacking_pieces) > 0:
                if (c, r) in white_attacking_pieces[0].line_of_attack:
                    return True
            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r) and len(
                    white_attacking_pieces) > 0:
                if (c, r) == white_attacking_pieces[0].lastPos:
                    return True
        elif Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r):
            return True
        return False

    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r):
            return True
        return False


class Rock(Pieces):
    def __init__(self, color, c, r):
        Pieces.__init__(self, color, c, r, "r")

    def update(self):
        Pieces.update(self)
        self.creating_line_of_attack()
        self.clear_current_danger()

    def legalMove(self, c, r):
        if (c == self.lastPos[0] or r == self.lastPos[1]) and self.lastPos != (c, r):
            return True
        return False

    def is_clear_path(self, c, r):
        x = self.lastPos[0] - c
        y = self.lastPos[1] - r
        if x > 0:
            for i in range(1, x):
                if sqIsOccupied((self.lastPos[0] - i, self.lastPos[1])):
                    if not (sqOccupied[(self.lastPos[0] - i, self.lastPos[1])].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0] - i, self.lastPos[1])].color):
                        return False
        if x < 0:
            for i in range(1, abs(x)):
                if sqIsOccupied((self.lastPos[0] + i, self.lastPos[1])):
                    if not (sqOccupied[(self.lastPos[0] + i, self.lastPos[1])].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0] + i, self.lastPos[1])].color):
                        return False
        if y > 0:
            for i in range(1, y):
                if sqIsOccupied((self.lastPos[0], self.lastPos[1] - i)):
                    if not (sqOccupied[(self.lastPos[0], self.lastPos[1] - i)].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0], self.lastPos[1] - i)].color):
                        return False
        if y < 0:
            for i in range(1, abs(y)):
                if sqIsOccupied((self.lastPos[0], self.lastPos[1] + i)):
                    if not (sqOccupied[(self.lastPos[0], self.lastPos[1] + i)].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0], self.lastPos[1] + i)].color):
                        return False
        return True

    def creating_line_of_attack(self):
        self.line_of_attack.clear()
        tested_squares = []
        x = self.lastPos[0]
        y = self.lastPos[1]
        if self.color == "w":
            king = king_b
        else:
            king = king_w

        def main(a, b):
            if self.who_on_square(a, b) == king:
                self.line_of_attack.extend(tested_squares)
                return True
            tested_squares.append((a, b))

        for a in range(x - 1, 0, -1):
            main(a, y)
        tested_squares.clear()
        for a in range(x + 1, 9, ):
            main(a, y)
        tested_squares.clear()
        for b in range(y - 1, 0, -1):
            main(x, b)
        tested_squares.clear()
        for b in range(y + 1, 9, ):
            main(x, b)

    def isLegalMove(self, c, r):
        if self.guardian:
            if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c, r) and (
                    (c, r) in self.guardian_line or (c, r) == self.attacker.lastPos):
                return True
            else:
                return False
        elif self.color == "w" and shah_to_white():
            if len(black_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                    self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) in black_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                    self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) == black_attacking_pieces[0].lastPos:
                    return True
        elif self.color == "b" and shah_to_black():
            if len(white_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                    self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) in white_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                    self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) == white_attacking_pieces[0].lastPos:
                    return True
        elif Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c,
                                                                                                  r) and not self.guardian:
            return True
        return False

    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r):
            return True
        return False

    def draw_points(self):
        Pieces.draw_points(self)


class Knight(Pieces):
    def __init__(self, color, c, r):
        Pieces.__init__(self, color, c, r, "n")

    def update(self):
        Pieces.update(self)

    def legalMove(self, c, r):
        if round((abs(c - self.lastPos[0]) ** 2) + (abs(r - self.lastPos[1]) ** 2), 1) == 5:
            return True

    def isLegalMove(self, c, r):
        if self.guardian:
            if Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r) and (
                    (c, r) in self.guardian_line or (c, r) == self.attacker.lastPos):
                return True
            else:
                return False
        elif self.color == "w" and shah_to_white():
            if len(black_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(
                    self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) in black_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(
                    self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) == black_attacking_pieces[0].lastPos:
                    return True
        elif self.color == "b" and shah_to_black():
            if len(white_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(
                    self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) in white_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(
                    self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) == white_attacking_pieces[0].lastPos:
                    return True
        elif Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c,
                                                                     r) and not self.guardian:
            return True
        return False

    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r):
            return True
        return False

    def draw_points(self):
        Pieces.draw_points(self)


class Bishop(Pieces):
    def __init__(self, color, c, r):
        Pieces.__init__(self, color, c, r, "b")

    def update(self):
        Pieces.update(self)
        self.creating_line_of_attack()
        self.clear_current_danger()

    def legalMove(self, c, r):
        if (c - self.lastPos[0] == r - self.lastPos[1] or c - self.lastPos[0] == self.lastPos[
            1] - r) and click_cr != self.lastPos:
            return True
        return False

    def isLegalMove(self, c, r):
        if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c,
                                                                                                r) and not self.guardian:
            return True
        return False

    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r):
            return True
        return False

    def draw_points(self):
        Pieces.draw_points(self)

    def is_clear_path(self, c, r):
        x = self.lastPos[0] - c
        y = self.lastPos[1] - r
        if x > 0 and y > 0:
            for i in range(1, x):
                if sqIsOccupied((self.lastPos[0] - i, self.lastPos[1] - i)):
                    if not (sqOccupied[(self.lastPos[0] - i, self.lastPos[1] - i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] - i, self.lastPos[1] - i)].color):
                        return False
        if x < 0 and y > 0:
            for i in range(1, abs(x)):
                if sqIsOccupied((self.lastPos[0] + i, self.lastPos[1] - i)):
                    if not (sqOccupied[(self.lastPos[0] + i, self.lastPos[1] - i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] + i, self.lastPos[1] - i)].color):
                        return False
        if x > 0 and y < 0:
            for i in range(1, x):
                if sqIsOccupied((self.lastPos[0] - i, self.lastPos[1] + i)):
                    if not (sqOccupied[(self.lastPos[0] - i, self.lastPos[1] + i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] - i, self.lastPos[1] + i)].color):
                        return False
        if x < 0 and y < 0:
            for i in range(1, abs(y)):
                if sqIsOccupied((self.lastPos[0] + i, self.lastPos[1] + i)):
                    if not (sqOccupied[(self.lastPos[0] + i, self.lastPos[1] + i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] + i, self.lastPos[1] + i)].color):
                        return False
        return True

    def creating_line_of_attack(self):
        self.line_of_attack.clear()
        tested_squares = []
        x = self.lastPos[0]
        y = self.lastPos[1]
        if self.color == "w":
            king = king_b
        else:
            king = king_w

        def main(a, b):
            if self.who_on_square(a, b) == king:
                self.line_of_attack.extend(tested_squares)
                return True
            tested_squares.append((a, b))

        for a in range(x - 1, 0, -1):
            b = y - (x - a)
            main(a, b)
        tested_squares.clear()
        for a in range(x + 1, 9):
            b = y - (x - a)
            main(a, b)
        tested_squares.clear()
        for a in range(x - 1, 0, -1):
            b = y + (x - a)
            main(a, b)
        tested_squares.clear()
        for a in range(x + 1, 9):
            b = y + (x - a)
            main(a, b)

    def isLegalMove(self, c, r):
        if self.guardian:
            if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c, r) and (
                    (c, r) in self.guardian_line or (c, r) == self.attacker.lastPos):
                return True
            else:
                return False
        elif self.color == "w" and shah_to_white():
            if len(black_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) in black_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) == black_attacking_pieces[0].lastPos:
                    return True
        elif self.color == "b" and shah_to_black():
            if len(white_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) in white_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) == white_attacking_pieces[0].lastPos:
                    return True
        elif Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c,
                                                                                                  r) and not self.guardian:
            return True
        return False

    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r):
            return True
        return False

    def draw_points(self):
        Pieces.draw_points(self)


class Queen(Pieces):
    def __init__(self, color, c, r):
        Pieces.__init__(self, color, c, r, "q")

    def update(self):
        Pieces.update(self)
        self.creating_line_of_attack()
        self.clear_current_danger()
        print(self.lastPos, self.current_danger)

    def legalMove(self, c, r):
        if (c - self.lastPos[0] == r - self.lastPos[1] or c - self.lastPos[0] ==
            self.lastPos[1] - r or c == self.lastPos[0] or r == self.lastPos[1]) and (c, r) != self.lastPos:
            return True
        return False

    def draw_points(self):
        Pieces.draw_points(self)

    def is_clear_path(self, c, r):
        x = self.lastPos[0] - c
        y = self.lastPos[1] - r
        if x > 0 and y > 0:
            for i in range(1, x):
                if sqIsOccupied((self.lastPos[0] - i, self.lastPos[1] - i)):
                    if not (sqOccupied[(self.lastPos[0] - i, self.lastPos[1] - i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] - i, self.lastPos[1] - i)].color):
                        return False
        elif x < 0 and y > 0:
            for i in range(1, abs(x)):
                if sqIsOccupied((self.lastPos[0] + i, self.lastPos[1] - i)):
                    if not (sqOccupied[(self.lastPos[0] + i, self.lastPos[1] - i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] + i, self.lastPos[1] - i)].color):
                        return False
        elif x > 0 and y < 0:
            for i in range(1, x):
                if sqIsOccupied((self.lastPos[0] - i, self.lastPos[1] + i)):
                    if not (sqOccupied[(self.lastPos[0] - i, self.lastPos[1] + i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] - i, self.lastPos[1] + i)].color):
                        return False
        elif x < 0 and y < 0:
            for i in range(1, abs(y)):
                if sqIsOccupied((self.lastPos[0] + i, self.lastPos[1] + i)):
                    if not (sqOccupied[(self.lastPos[0] + i, self.lastPos[1] + i)].type == "k" and self.color !=
                            sqOccupied[(self.lastPos[0] + i, self.lastPos[1] + i)].color):
                        return False
        elif x > 0:
            for i in range(1, x):
                if sqIsOccupied((self.lastPos[0] - i, self.lastPos[1])):
                    if not (sqOccupied[(self.lastPos[0] - i, self.lastPos[1])].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0] - i, self.lastPos[1])].color):
                        return False
        elif x < 0:
            for i in range(1, abs(x)):
                if sqIsOccupied((self.lastPos[0] + i, self.lastPos[1])):
                    if not (sqOccupied[(self.lastPos[0] + i, self.lastPos[1])].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0] + i, self.lastPos[1])].color):
                        return False
        elif y > 0:
            for i in range(1, y):
                if sqIsOccupied((self.lastPos[0], self.lastPos[1] - i)):
                    if not (sqOccupied[(self.lastPos[0], self.lastPos[1] - i)].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0], self.lastPos[1] - i)].color):
                        return False
        elif y < 0:
            for i in range(1, abs(y)):
                if sqIsOccupied((self.lastPos[0], self.lastPos[1] + i)):
                    if not (sqOccupied[(self.lastPos[0], self.lastPos[1] + i)].type == "k" and self.color != sqOccupied[
                        (self.lastPos[0], self.lastPos[1] + i)].color):
                        return False
        return True

    def creating_line_of_attack(self):
        self.line_of_attack.clear()
        tested_squares = []
        x = self.lastPos[0]
        y = self.lastPos[1]
        if self.color == "w":
            king = king_b
        else:
            king = king_w

        def main(a, b):
            if self.who_on_square(a, b) == king:
                self.line_of_attack.extend(tested_squares)
                return True
            tested_squares.append((a, b))

        for a in range(x - 1, 0, -1):
            main(a, y)
        tested_squares.clear()
        for a in range(x + 1, 9, ):
            main(a, y)
        tested_squares.clear()
        for b in range(y - 1, 0, -1):
            main(x, b)
        tested_squares.clear()
        for b in range(y + 1, 9, ):
            main(x, b)
        tested_squares.clear()
        for a in range(x - 1, 0, -1):
            b = y - (x - a)
            main(a, b)
        tested_squares.clear()
        for a in range(x + 1, 9):
            b = y - (x - a)
            main(a, b)
        tested_squares.clear()
        for a in range(x - 1, 0, -1):
            b = y + (x - a)
            main(a, b)
        tested_squares.clear()
        for a in range(x + 1, 9):
            b = y + (x - a)
            main(a, b)

    def isLegalMove(self, c, r):
        if self.guardian:
            if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c, r) and (
                    (c, r) in self.guardian_line or (c, r) == self.attacker.lastPos):
                return True
            else:
                return False
        elif self.color == "w" and shah_to_white():
            if len(black_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) in black_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(black_attacking_pieces) > 0:
                if (c, r) == black_attacking_pieces[0].lastPos:
                    return True
        elif self.color == "b" and shah_to_black():
            if len(white_attacking_pieces) > 1:
                return False

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) in white_attacking_pieces[0].line_of_attack:
                    return True

            if not self.guardian and Pieces.is_legal_move(self, c, r) and self.is_clear_path(c,
                                                                                             r) and not Pieces.is_ally(
                self, c, r) and len(white_attacking_pieces) > 0:
                if (c, r) == white_attacking_pieces[0].lastPos:
                    return True
        elif Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r) and not Pieces.is_ally(self, c,
                                                                                                  r) and not self.guardian:
            return True
        return False
    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r) and self.is_clear_path(c, r):
            return True
        return False


class King(Pieces):
    def __init__(self, color, c, r):
        Pieces.__init__(self, color, c, r, "k")
        self.type = "k"

    def update(self):
        Pieces.update(self)
        self.delete_attacked_squares()

    def legalMove(self, c, r):
        if self.color == "w":
            if round((abs(c - self.lastPos[0]) ** 2) + (abs(r - self.lastPos[1]) ** 2), 1) < 4 and (
            c, r) not in sq_attacked_b:
                return True
        else:
            if round((abs(c - self.lastPos[0]) ** 2) + (abs(r - self.lastPos[1]) ** 2), 1) < 4 and (
            c, r) not in sq_attacked_w:
                return True
        return False

    def isLegalMove(self, c, r):
        if Pieces.is_legal_move(self, c, r) and not Pieces.is_ally(self, c, r):
            return True
        return False

    def draw_points(self):
        Pieces.draw_points(self)

    def isLegalMoveToAlly(self, c, r):
        if Pieces.is_legal_move(self, c, r):
            return True
        return False

    def delete_attacked_squares(self):
        for square in self.available_squares:
            if self.color == "w":
                if square in sq_attacked_b:
                    self.available_squares.remove(square)
            else:
                if square in sq_attacked_w:
                    self.available_squares.remove(squere)


def change_turn():
    global turn
    if turn == "w":
        turn = "b"
    elif turn == "b":
        turn = "w"


def move():
    global tryToMove
    if selectedPiece.isLegalMove(click_cr[0], click_cr[1]):
        if selectedPiece.type == "p" and selectedPiece.first_move:
            selectedPiece.first_move = False
        if sqIsOccupied(click_cr):
            sqOccupied.pop(click_cr).kill()
        selectedPiece.rect.center = sqCenterByCoords(pos)
        sqOccupied[click_cr] = selectedPiece
        sqOccupied.pop(selectedPiece.lastPos)
        selectedPiece.lastPos = sqFromCoords(selectedPiece.rect.center)
        change_turn()
        clear_available_squares()



pieces = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()

for i in range(1, 9):
    pawn_w = Pawn("w", i, 7)
    all_sprites.add(pawn_w)
    pieces.add(pawn_w)

for i in range(1, 9):
    pawn_b = Pawn("b", i, 2)
    all_sprites.add(pawn_b)
    pieces.add(pawn_b)

rock_1w = Rock("w", 1, 8)
rock_2w = Rock("w", 8, 8)
rock_1b = Rock("b", 1, 1)
rock_2b = Rock("b", 8, 1)
all_sprites.add(rock_1w)
all_sprites.add(rock_2w)
all_sprites.add(rock_1b)
all_sprites.add(rock_2b)
pieces.add(rock_1w)
pieces.add(rock_2w)
pieces.add(rock_1b)
pieces.add(rock_2b)

knight_1w = Knight("w", 2, 8)
knight_2w = Knight("w", 7, 8)
knight_1b = Knight("b", 2, 1, )
knight_2b = Knight("b", 7, 1)
all_sprites.add(knight_1w)
all_sprites.add(knight_2w)
all_sprites.add(knight_1b)
all_sprites.add(knight_2b)
pieces.add(knight_1w)
pieces.add(knight_2w)
pieces.add(knight_1b)
pieces.add(knight_2b)

bishop_1w = Bishop("w", 3, 8)
bishop_2w = Bishop("w", 6, 8)
bishop_1b = Bishop("b", 3, 1)
bishop_2b = Bishop("b", 6, 1)
all_sprites.add(bishop_1w)
all_sprites.add(bishop_2w)
all_sprites.add(bishop_1b)
all_sprites.add(bishop_2b)
pieces.add(bishop_1w)
pieces.add(bishop_2w)
pieces.add(bishop_1b)
pieces.add(bishop_2b)

queen_w = Queen("w", 4, 8)
queen_b = Queen("b", 4, 1)
all_sprites.add(queen_w)
all_sprites.add(queen_b)
pieces.add(queen_w)
pieces.add(queen_b)

king_w = King("w", 5, 8)
king_b = King("b", 5, 1)
all_sprites.add(king_w)
all_sprites.add(king_b)
pieces.add(king_w)
pieces.add(king_b)

running = True
tryToMove = False
tryToMove_sq = 0
selectedPiece = 0

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        pressed = pygame.mouse.get_pressed()
        pos = pygame.mouse.get_pos()
        click_cr = sqFromCoords((pos[0], pos[1]))
        # if event.type == pygame.MOUSEBUTTONUP:
        # pawn_1w.rect.center = sqCenterByCoords(pos)
        if event.type == pygame.MOUSEBUTTONDOWN and not tryToMove:
            if sqIsOccupied(click_cr):
                if selectedPiece == 0:
                    selectedPiece = sqOccupied[click_cr]
                if selectedPiece != 0:
                    selectedPiece.draw_points()

            if selectedPiece != 0:
                if selectedPiece.color == turn:
                    tryToMove = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if sqIsOccupied(click_cr):
                if selectedPiece.color == sqOccupied[click_cr].color:
                    tryToMove = False
                    selectedPiece = sqOccupied[click_cr]
            else:
                move()
                selectedPiece = 0
    sq_attacked_w.clear()
    sq_attacked_b.clear()
    attacked_squares_fill()
    all_sprites.update()
    print(white_attacking_pieces)
    timer += 0.016

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
