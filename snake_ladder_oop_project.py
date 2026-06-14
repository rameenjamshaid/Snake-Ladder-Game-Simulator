import tkinter as tk
from tkinter import messagebox, simpledialog
import random
class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.position = 1
        self.rolls = 0
        self.snakes = 0
        self.ladders = 0
class Dice:
    def roll(self):
        return random.randint(1, 6)
class Board:
    def __init__(self):
        self.snakes = {99:54,95:72,70:55,52:42,25:2}
        self.ladders = {6:25,11:40,17:69,46:90,60:85}
    def check(self, pos):
        if pos in self.snakes:
            return self.snakes[pos], "snake"
        if pos in self.ladders:
            return self.ladders[pos], "ladder"
        return pos, None
class SnakeLadderGame:
    COLORS = ["red","blue","green","orange"]
    def __init__(self, root):
        self.root = root
        self.root.title("Snake & Ladder OOP Project")
        self.root.geometry("1100x720")
        self.root.configure(bg="#1f2430")
        self.board = Board()
        self.dice = Dice()
        n = simpledialog.askinteger("Players","Enter number of players (2-4)",minvalue=2,maxvalue=4)
        if not n:
            n = 2
        self.players = []
        for i in range(n):
            name = simpledialog.askstring("Player",f"Enter Player {i+1} Name")
            self.players.append(Player(name or f"Player {i+1}", self.COLORS[i]))
        self.turn = 0
        self.turns_played = 0
        self.highest_roll = 0
        left = tk.Frame(root,bg="#1f2430")
        left.pack(side="left",padx=10,pady=10)
        right = tk.Frame(root,bg="#1f2430")
        right.pack(side="right",fill="y",padx=10,pady=10)
        self.canvas = tk.Canvas(left,width=600,height=600,bg="white")
        self.canvas.pack()
        self.info = tk.Label(right,text="",font=("Arial",16,"bold"),bg="#1f2430",fg="white")
        self.info.pack(pady=10)
        self.dice_label = tk.Label(right,text="🎲",font=("Arial",40),bg="#1f2430",fg="gold")
        self.dice_label.pack()
        tk.Button(right,text="ROLL DICE",font=("Arial",14,"bold"),
                  command=self.roll_dice,bg="#4CAF50",fg="white").pack(fill="x",pady=5)
        tk.Button(right,text="RESTART",font=("Arial",14,"bold"),
                  command=self.restart,bg="#2196F3",fg="white").pack(fill="x",pady=5)
        self.stats_label = tk.Label(right,bg="#1f2430",fg="white",justify="left")
        self.stats_label.pack(pady=10)
        tk.Label(right,text="Move History",bg="#1f2430",fg="white",
                 font=("Arial",12,"bold")).pack()
        self.history = tk.Text(right,height=18,width=35)
        self.history.pack()
        self.draw_board()
        self.draw_players()
        self.update_labels()
    def restart(self):
        for p in self.players:
            p.position = 1
            p.rolls = p.snakes = p.ladders = 0
        self.turn = 0
        self.turns_played = 0
        self.highest_roll = 0
        self.history.delete("1.0", tk.END)
        self.draw_players()
        self.update_labels()
    def get_center(self, n):
        n -= 1
        row = 9 - (n // 10)
        col = n % 10 if (n // 10) % 2 == 0 else 9 - (n % 10)
        return col * 60 + 30, row * 60 + 30
    def draw_board(self):
        colors = ["#F7DC6F","#AED6F1","#ABEBC6","#F5B7B1"]
        num = 100
        for r in range(10):
            cols = range(10) if r % 2 == 0 else range(9,-1,-1)
            for c in cols:
                x1,y1 = c*60,r*60
                x2,y2 = x1+60,y1+60
                self.canvas.create_rectangle(x1,y1,x2,y2,
                                             fill=colors[(r+c)%4],
                                             outline="black")
                self.canvas.create_text(x1+30,y1+20,text=str(num),
                                        font=("Arial",10,"bold"))
                num -= 1
        for s,e in self.board.snakes.items():
            x1,y1 = self.get_center(s)
            x2,y2 = self.get_center(e)
            self.canvas.create_line(x1,y1,x2,y2,width=8,fill="red",smooth=True)
            self.canvas.create_text(x1,y1,text="🐍",font=("Arial",16))
        for s,e in self.board.ladders.items():
            x1,y1 = self.get_center(s)
            x2,y2 = self.get_center(e)
            self.canvas.create_line(x1-6,y1,x2-6,y2,width=3,fill="brown")
            self.canvas.create_line(x1+6,y1,x2+6,y2,width=3,fill="brown")
            for i in range(1,6):
                t = i/6
                rx = (x1*(1-t)+x2*t)
                ry = (y1*(1-t)+y2*t)
                self.canvas.create_line(rx-6,ry,rx+6,ry,width=2,fill="brown")
    def draw_players(self):
        self.canvas.delete("token")
        offsets = [(-12,-12),(12,-12),(-12,12),(12,12)]
        for i,p in enumerate(self.players):
            x,y = self.get_center(p.position)
            dx,dy = offsets[i]
            self.canvas.create_oval(
                x-10+dx,y-10+dy,x+10+dx,y+10+dy,
                fill=p.color,tags="token"
            )
    def update_labels(self):
        current = self.players[self.turn]
        self.info.config(text=f"{current.name}'s Turn")
        stats = []
        for p in self.players:
            stats.append(f"{p.name}: {p.position}")
        stats.append(f"Turns: {self.turns_played}")
        stats.append(f"Highest Roll: {self.highest_roll}")
        self.stats_label.config(text="\n".join(stats))
    def animate_dice(self, count=10):
        faces = ["⚀","⚁","⚂","⚃","⚄","⚅"]
        if count > 0:
            self.dice_label.config(text=random.choice(faces))
            self.root.after(80, lambda:self.animate_dice(count-1))
        else:
            self.finish_roll()
    def roll_dice(self):
        self.animate_dice()
    def finish_roll(self):
        player = self.players[self.turn]
        roll = self.dice.roll()
        self.dice_label.config(text=["⚀","⚁","⚂","⚃","⚄","⚅"][roll-1])
        player.rolls += 1
        self.turns_played += 1
        self.highest_roll = max(self.highest_roll, roll)
        new_pos = player.position + roll
        if new_pos <= 100:
            player.position = new_pos
            checked, event = self.board.check(player.position)
            if event == "snake":
                player.snakes += 1
                self.history.insert(tk.END,
                    f"{player.name} rolled {roll} 🐍 {player.position}->{checked}\n")
                player.position = checked
            elif event == "ladder":
                player.ladders += 1
                self.history.insert(tk.END,
                    f"{player.name} rolled {roll} 🪜 {player.position}->{checked}\n")
                player.position = checked
            else:
                self.history.insert(tk.END,
                    f"{player.name} rolled {roll} → {player.position}\n")
        self.draw_players()
        self.update_labels()
        if player.position == 100:
            self.show_winner(player)
            return
        self.turn = (self.turn + 1) % len(self.players)
        self.update_labels()
    def show_winner(self, player):
        stats = (
            f"🏆 {player.name} Wins!\n\n"
            f"Rolls: {player.rolls}\n"
            f"Snakes: {player.snakes}\n"
            f"Ladders: {player.ladders}\n"
        )
        messagebox.showinfo("Winner", stats)
if __name__ == "__main__":
    root = tk.Tk()
    SnakeLadderGame(root)
    root.mainloop()