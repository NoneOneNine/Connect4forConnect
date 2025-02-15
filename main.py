import pygame
import sys
import math
from piece import Piece
from qualities import QUALITIES

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

textAlignLeft = 0
textAlignRight = 1
textAlignCenter = 2
textAlignBlock = 3

# The original version had the indexes in reverse
row_keys = {-1: 5,
            0: 5,
            1: 4,
            2: 3,
            3: 2,
            4: 1,
            5: 0}


def create_board():
    new_board = []
    for r in range(ROW_COUNT):
        new_board.append([])
        for c in range(COLUMN_COUNT):
            new_board[r].append(0)
    return new_board


def drop_piece(current_row, current_col, piece):
    board[current_row][current_col] = piece


def is_valid_location(current_col):
    return board[ROW_COUNT - 1][current_col] == 0


def get_next_open_row(current_col):
    for r in range(ROW_COUNT):
        if board[r][current_col] == 0:
            return r


def winning_move(piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] != 0 and board[r][c + 1] != 0 and board[r][c + 2] != 0 and board[r][c + 3] != 0:
                if (board[r][c].color == piece.color and
                        board[r][c + 1].color == piece.color and
                        board[r][c + 2].color == piece.color and
                        board[r][c + 3].color == piece.color):
                    return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] != 0 and board[r + 1][c] != 0 and board[r + 2][c] != 0 and board[r + 3][c] != 0:
                if (board[r][c].color == piece.color and
                        board[r + 1][c].color == piece.color and
                        board[r + 2][c].color == piece.color and
                        board[r + 3][c].color == piece.color):
                    return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] != 0 and board[r + 1][c + 1] != 0 and board[r + 2][c + 2] != 0 and board[r + 3][c + 3] != 0:
                if (board[r][c].color == piece.color and
                        board[r + 1][c + 1].color == piece.color and
                        board[r + 2][c + 2].color == piece.color and
                        board[r + 3][c + 3].color == piece.color):
                    return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] != 0 and board[r - 1][c + 1] != 0 and board[r - 2][c + 2] != 0 and board[r - 3][c + 3] != 0:
                if (board[r][c].color == piece.color and
                        board[r - 1][c + 1].color == piece.color and
                        board[r - 2][c + 2].color == piece.color and
                        board[r - 3][c + 3].color == piece.color):
                    return True


def draw_text(surface, text, color, rect, font, align=textAlignCenter, aa=False, bkg=None):
    lineSpacing = -2
    spaceWidth, fontHeight = font.size(" ")[0], font.size("Tg")[1]

    listOfWords = text.split(" ")
    if bkg:
        imageList = [font.render(word, 1, color, bkg) for word in listOfWords]
        for image in imageList: image.set_colorkey(bkg)
    else:
        imageList = [font.render(word, aa, color) for word in listOfWords]

    maxLen = rect[2]
    lineLenList = [0]
    lineList = [[]]
    for image in imageList:
        text_width = image.get_width()
        lineLen = lineLenList[-1] + len(lineList[-1]) * spaceWidth + text_width
        if len(lineList[-1]) == 0 or lineLen <= maxLen:
            lineLenList[-1] += text_width
            lineList[-1].append(image)
        else:
            lineLenList.append(text_width)
            lineList.append([image])

    lineBottom = rect[1]
    lastLine = 0
    for lineLen, lineImages in zip(lineLenList, lineList):
        lineLeft = rect[0]
        if align == textAlignRight:
            lineLeft += + rect[2] - lineLen - spaceWidth * (len(lineImages)-1)
        elif align == textAlignCenter:
            lineLeft += (rect[2] - lineLen - spaceWidth * (len(lineImages)-1)) // 2
        elif align == textAlignBlock and len(lineImages) > 1:
            spaceWidth = (rect[2] - lineLen) // (len(lineImages)-1)
        if lineBottom + fontHeight > rect[1] + rect[3]:
            break
        lastLine += 1
        for i, image in enumerate(lineImages):
            x, y = lineLeft + i*spaceWidth, lineBottom
            surface.blit(image, (round(x), y))
            lineLeft += image.get_width()
        lineBottom += fontHeight + lineSpacing

    if lastLine < len(lineList):
        drawWords = sum([len(lineList[i]) for i in range(lastLine)])
        remainingText = ""
        for text in listOfWords[drawWords:]: remainingText += text + " "
        return remainingText
    return ""


def draw_board():
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, WHITE, (
                int(c * SQUARE_SIZE + SQUARE_SIZE / 2), int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2)), RADIUS)
            draw_text(screen, QUALITIES[r][c], BLACK,
                      pygame.Rect(c * SQUARE_SIZE + 7, r * SQUARE_SIZE + RADIUS / 1.4 + SQUARE_SIZE, RADIUS * 2,
                                  RADIUS * 2), pygame.font.SysFont("arial", 17))

    for c in range(COLUMN_COUNT):
        for r1 in range(ROW_COUNT):
            r = row_keys[r1]
            if board[r][c] != 0:
                if board[r][c].is_visible:
                    if board[r][c].color == 0:
                        pygame.draw.circle(screen, RED, (
                            int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                           RADIUS)
                        draw_text(screen, board[r][c].name, BLACK,
                                  pygame.Rect(c * SQUARE_SIZE + 7, r1 * SQUARE_SIZE + RADIUS + SQUARE_SIZE, RADIUS * 2,
                                  RADIUS * 2), name_font)
                    elif board[r][c].color == 1:
                        pygame.draw.circle(screen, YELLOW, (
                            int(c * SQUARE_SIZE + SQUARE_SIZE / 2), height - int(r * SQUARE_SIZE + SQUARE_SIZE / 2)),
                                           RADIUS)
                        draw_text(screen, board[r][c].name, BLACK,
                                  pygame.Rect(c * SQUARE_SIZE + 7, r1 * SQUARE_SIZE + RADIUS + SQUARE_SIZE, RADIUS * 2,
                                  RADIUS * 2), name_font)
    pygame.display.update()


def get_row_col_from_mouse(mouse_pos):
    x, y = mouse_pos
    r = (y - SQUARE_SIZE) // SQUARE_SIZE
    r = row_keys[r]
    c = x // SQUARE_SIZE
    return r, c


board = create_board()
game_over = False
turn = 0

pygame.init()

SQUARE_SIZE = 110

width = COLUMN_COUNT * SQUARE_SIZE
height = (ROW_COUNT + 1) * SQUARE_SIZE

size = (width, height)

RADIUS = int(SQUARE_SIZE / 2 - 5)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect 4 for Connect")
draw_board()
pygame.display.update()

my_font = pygame.font.SysFont("monospace", 75)
name_font = pygame.font.Font(None, 24)

user_text = ''
name = ''

while not game_over:
    pos_x, pos_y = pygame.mouse.get_pos()

    if turn == 0:
        pygame.draw.circle(screen, RED, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)
    else:
        pygame.draw.circle(screen, YELLOW, (pos_x, int(SQUARE_SIZE / 2)), RADIUS)

    text_surface = name_font.render(user_text, True, BLACK)
    screen.blit(text_surface, (0,0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        pygame.draw.rect(screen, WHITE, (0, 0, width, SQUARE_SIZE))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                name = user_text
                user_text = ''
            else:
                user_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Change colour with right click
                turn += 1
                turn = turn % 2
            elif event.button == 1:
                # Ask for red input
                if turn == 0:
                    col = int(math.floor(pos_x / SQUARE_SIZE))
                    row = get_next_open_row(col)

                    mouse_row, mouse_col = get_row_col_from_mouse((pos_x, pos_y))
                    if is_valid_location(col) and board[mouse_row][mouse_col] == 0:
                        new_piece = Piece(turn, name, True)
                        drop_piece(row, col, new_piece)

                        turn += 1
                        turn = turn % 2

                        if winning_move(new_piece):
                            label = my_font.render("Red wins!!", 1, RED)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        if board[mouse_row][mouse_col].is_visible:
                            board[mouse_row][mouse_col].is_visible = False
                        else:
                            board[mouse_row][mouse_col].is_visible = True
                # Ask for yellow input
                else:
                    col = int(math.floor(pos_x / SQUARE_SIZE))
                    row = get_next_open_row(col)

                    mouse_row, mouse_col = get_row_col_from_mouse((pos_x, pos_y))
                    if is_valid_location(col) and board[mouse_row][mouse_col] == 0:
                        new_piece = Piece(turn, name, True)
                        drop_piece(row, col, new_piece)

                        turn += 1
                        turn = turn % 2

                        if winning_move(new_piece):
                            label = my_font.render("Yellow wins!!", 1, YELLOW)
                            screen.blit(label, (40, 10))
                            game_over = True
                    else:
                        if board[mouse_row][mouse_col].is_visible:
                            board[mouse_row][mouse_col].is_visible = False
                        else:
                            board[mouse_row][mouse_col].is_visible = True

                draw_board()

            if game_over:
                pygame.time.wait(10000)