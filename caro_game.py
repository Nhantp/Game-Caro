import pygame
import sys
import random
from tkinter import *
from tkinter import messagebox

# Khởi tạo Pygame
pygame.init()

# Định nghĩa các màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Kích thước màn hình
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Caro Game")

# Font chữ
font = pygame.font.SysFont(None, 50)

# Hàm hiển thị văn bản
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Khởi tạo bàn chơi và trạng thái
def init_board(grid_size):
    return [['' for _ in range(grid_size)] for _ in range(grid_size)]

# Vẽ lưới caro
def draw_grid(grid_size):
    screen.fill(WHITE)
    cell_size = SCREEN_HEIGHT // grid_size
    for row in range(grid_size):
        for col in range(grid_size):
            pygame.draw.rect(screen, BLACK, (col * cell_size, row * cell_size, cell_size, cell_size), 1)

# Vẽ dấu X và O
def draw_move(board, grid_size, cell_size):
    for row in range(grid_size):
        for col in range(grid_size):
            if board[row][col] == 'X':
                pygame.draw.line(screen, RED, (col * cell_size + 10, row * cell_size + 10),
                                 (col * cell_size + cell_size - 10, row * cell_size + cell_size - 10), 5)
                pygame.draw.line(screen, RED, (col * cell_size + 10, row * cell_size + cell_size - 10),
                                 (col * cell_size + cell_size - 10, row * cell_size + 10), 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, BLUE, (col * cell_size + cell_size // 2, row * cell_size + cell_size // 2),
                                   cell_size // 2 - 10, 5)

# Kiểm tra chiến thắng
def check_winner(board, player, grid_size, win_condition):
    for row in range(grid_size):
        for col in range(grid_size - win_condition + 1):
            if all(board[row][col + i] == player for i in range(win_condition)):
                return True

    for col in range(grid_size):
        for row in range(grid_size - win_condition + 1):
            if all(board[row + i][col] == player for i in range(win_condition)):
                return True

    for row in range(grid_size - win_condition + 1):
        for col in range(grid_size - win_condition + 1):
            if all(board[row + i][col + i] == player for i in range(win_condition)):
                return True

    for row in range(grid_size - win_condition + 1):
        for col in range(win_condition - 1, grid_size):
            if all(board[row + i][col - i] == player for i in range(win_condition)):
                return True

    return False

# Hàm minimax cho AI
def minimax(board, depth, is_maximizing, win_condition, grid_size):
    scores = {'X': -1, 'O': 1, 'tie': 0}
    if check_winner(board, 'O', grid_size, win_condition):
        return scores['O']
    elif check_winner(board, 'X', grid_size, win_condition):
        return scores['X']
    elif all(board[row][col] != '' for row in range(grid_size) for col in range(grid_size)):
        return scores['tie']

    if depth >= 3:  # Giới hạn độ sâu
        return scores['tie']

    if is_maximizing:
        best_score = -float('inf')
        for row in range(grid_size):
            for col in range(grid_size):
                if board[row][col] == '':
                    board[row][col] = 'O'
                    score = minimax(board, depth + 1, False, win_condition, grid_size)
                    board[row][col] = ''
                    best_score = max(best_score, score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(grid_size):
            for col in range(grid_size):
                if board[row][col] == '':
                    board[row][col] = 'X'
                    score = minimax(board, depth + 1, True, win_condition, grid_size)
                    board[row][col] = ''
                    best_score = min(best_score, score)
        return best_score

def ai_move(board, grid_size, win_condition):
    best_score = -float('inf')
    best_move = (-1, -1)
    for row in range(grid_size):
        for col in range(grid_size):
            if board[row][col] == '':
                board[row][col] = 'O'
                score = minimax(board, 0, False, win_condition, grid_size)
                board[row][col] = ''
                if score > best_score:
                    best_score = score
                    best_move = (row, col)
    return best_move

# Logic chính của trò chơi
def start_game(grid_size, mode):
    board = init_board(grid_size)
    current_player = 'X'  # Người chơi X luôn đi trước
    game_over = False
    cell_size = SCREEN_HEIGHT // grid_size
    win_condition = 3 if grid_size == 3 else 4 if grid_size == 5 else 5

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over and event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                col = mouse_x // cell_size
                row = mouse_y // cell_size

                if board[row][col] == '':
                    board[row][col] = current_player
                    if check_winner(board, current_player, grid_size, win_condition):
                        game_over = True
                        draw_winner_screen(current_player)
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

                if mode == 'ai' and not game_over and current_player == 'O':
                    row, col = ai_move(board, grid_size, win_condition)
                    board[row][col] = 'O'  # Đặt dấu O vào vị trí được chọn
                    if check_winner(board, 'O', grid_size, win_condition):  # Kiểm tra xem AI có thắng không
                        game_over = True
                        draw_winner_screen('O')
                    current_player = 'X'  # Sau khi máy đi, đổi lượt về cho người chơi

        draw_grid(grid_size)
        draw_move(board, grid_size, cell_size)
        pygame.display.flip()

def play_screen():
    window = Tk()
    window.title("Caro Game - Play")

    def start_choose_mode():
        window.destroy()
        choose_mode_screen()

    Label(window, text="Welcome to Caro Game", font=("Arial", 24)).pack(pady=20)
    Button(window, text="Play", command=start_choose_mode, font=("Arial", 18), width=10, height=2).pack(pady=20)

    window.mainloop()

# Hàm hiển thị màn hình kết thúc trò chơi
def draw_winner_screen(winner):
    if winner == 'X':
        messagebox.showinfo("Game Over", "Player X wins!")
    elif winner == 'O':
        messagebox.showinfo("Game Over", "Player O wins!")
    else:
        messagebox.showinfo("Game Over", "It's a tie!")

    # Hiển thị nút Restart để quay về màn hình chọn chế độ
    if messagebox.askyesno("Restart", "Do you want to restart the game?"):
        choose_mode_screen()
    else:
        pygame.quit()
        sys.exit()

# Màn hình chọn chế độ chơi (Tkinter)
def choose_mode_screen():
    window = Tk()
    window.title("Caro Game - Choose Mode")

    def start_game_with_mode(mode):
        window.destroy()  # Đóng cửa sổ chọn chế độ
        choose_grid_size_screen(mode)

    Label(window, text="Choose Mode", font=("Arial", 24)).pack(pady=20)
    Button(window, text="Player vs Player", command=lambda: start_game_with_mode('pvp')).pack(pady=10)
    Button(window, text="Player vs AI", command=lambda: start_game_with_mode('ai')).pack(pady=10)

    window.mainloop()

# Màn hình chọn kích thước lưới (Tkinter)
def choose_grid_size_screen(mode):
    window = Tk()
    window.title("Caro Game - Choose Grid Size")

    def start_game_with_size(size):
        window.destroy()  # Đóng cửa sổ chọn kích thước lưới
        start_game(size, mode)

    Label(window, text="Choose Grid Size", font=("Arial", 24)).pack(pady=20)
    Button(window, text="3x3", command=lambda: start_game_with_size(3), width=20, height=3).pack(pady=10)
    Button(window, text="5x5", command=lambda: start_game_with_size(5), width=20, height=3).pack(pady=10)
    Button(window, text="7x7", command=lambda: start_game_with_size(7), width=20, height=3).pack(pady=10)
    window.mainloop()

# Bắt đầu trò chơi
play_screen()
