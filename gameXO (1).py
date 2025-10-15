from tkinter import *
import copy


board = [['', '', ''],
         ['', '', ''],
         ['', '', '']]

window = Tk()
window.title("لعبة XO")

player = 'X'
ai = 'O'
mode = None  



def check_winner(b):
    for row in range(3):
        if b[row][0] == b[row][1] == b[row][2] != '':
            return b[row][0]
    for col in range(3):
        if b[0][col] == b[1][col] == b[2][col] != '':
            return b[0][col]
    if b[0][0] == b[1][1] == b[2][2] != '':
        return b[0][0]
    if b[0][2] == b[1][1] == b[2][0] != '':
        return b[0][2]

    for row in b:
        for cell in row:
            if cell == '':
                return None
    return 'تعادل'



def minimax(b, depth, is_maximizing):
    winner = check_winner(b)
    if winner == ai:
        return 1
    elif winner == player:
        return -1
    elif winner == 'تعادل':
        return 0

    if is_maximizing:
        best_score = -100
        for i in range(3):
            for j in range(3):
                if b[i][j] == '':
                    b[i][j] = ai
                    score = minimax(b, depth + 1, False)
                    b[i][j] = ''
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = 100
        for i in range(3):
            for j in range(3):
                if b[i][j] == '':
                    b[i][j] = player
                    score = minimax(b, depth + 1, True)
                    b[i][j] = ''
                    best_score = min(score, best_score)
        return best_score



def ai_move():
    best_score = -100
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                board[i][j] = ai
                score = minimax(board, 0, False)
                board[i][j] = ''
                if score > best_score:
                    best_score = score
                    move = (i, j)
    if move:
        i, j = move
        board[i][j] = ai
        game_btns[i][j]['text'] = ai
        game_btns[i][j]['state'] = DISABLED
        check_game_over()



def check_game_over():
    winner = check_winner(board)
    if winner:
        if winner == 'تعادل':
            label.config(text="تعادل! 🟡", fg="orange")
        elif winner == 'X':
            label.config(text="فاز اللاعب X 🟢", fg="green")
        else:
            label.config(text="فاز اللاعب O 🔴", fg="red")
        for row in game_btns:
            for btn in row:
                btn['state'] = DISABLED
        return True
    return False



def clicked(row, col):
    global player
    if board[row][col] == '' and not check_game_over():
        board[row][col] = player
        game_btns[row][col]['text'] = player
        game_btns[row][col]['state'] = DISABLED

        if not check_game_over():
            if mode == "AI": 
                ai_move()
            else:
                player_switch()



def player_switch():
    global player
    if player == 'X':
        player = 'O'
        label.config(text="دور اللاعب O 🔵", fg="blue")
    else:
        player = 'X'
        label.config(text="دور اللاعب X 🟢", fg="green")


def start_new_game():
    global board, player
    board = [['', '', ''], ['', '', ''], ['', '', '']]
    player = 'X'
    label.config(text="ابدأ اللعب، دور X 🟢", fg="black")
    for i in range(3):
        for j in range(3):
            game_btns[i][j].config(text="", state=NORMAL, bg="#F0F0F0")



def choose_mode():
    def vs_friend():
        global mode
        mode = "Friend"
        mode_window.destroy()
        label.config(text="دور اللاعب X 🟢")

    def vs_ai():
        global mode
        mode = "AI"
        mode_window.destroy()
        label.config(text="دورك أنت (X) ضد الكمبيوتر 🤖")

    mode_window = Toplevel(window)
    mode_window.title("اختيار طريقة اللعب")
    Label(mode_window, text="من تريد أن تلعب معه؟",
          font=('consolas', 16)).pack(pady=10)
    Button(mode_window, text="👬 العب مع صديق", font=(
        'consolas', 14), command=vs_friend).pack(pady=5)
    Button(mode_window, text="🤖 العب مع الكمبيوتر", font=(
        'consolas', 14), command=vs_ai).pack(pady=5)


# --- واجهة المستخدم ---
label = Label(text="اختر طريقة اللعب من القائمة 👇", font=('consolas', 20))
label.pack(side="top")

restart_btn = Button(text="إعادة التشغيل 🔄", font=('consolas', 16),
                     command=start_new_game)
restart_btn.pack(side="top")

choose_btn = Button(text="اختيار طريقة اللعب 🎮", font=('consolas', 16),
                    command=choose_mode)
choose_btn.pack(side="top")

btns_frame = Frame(window)
btns_frame.pack()

game_btns = [[None for _ in range(3)] for _ in range(3)]

for i in range(3):
    for j in range(3):
        btn = Button(btns_frame, text="", font=('consolas', 24),
                     width=5, height=2,
                     command=lambda i=i, j=j: clicked(i, j))
        btn.grid(row=i, column=j)
        game_btns[i][j] = btn

window.mainloop()
