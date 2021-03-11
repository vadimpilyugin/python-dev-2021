import tkinter as tk
import math
import random
import tkinter.messagebox as msgbox

# def update_board():

class State():
  def __init__(self, size=16):

    self.buttons = []
    # self.frames = []
    self.frame = None
    self.size = size
    length = int(math.sqrt(size))
    if length ** 2 > size:
      length -= 1
    self.length = length
    self.init_window()

  def init_window(self):
    self.window = tk.Tk()
    controls = tk.Frame(master=self.window)
    new = tk.Button(text="New", height=2, width=5, master=controls, command=self.randomize)
    easy = tk.Button(text="Easy", height=2, width=5, master=controls, command=self.easymode)
    exit = tk.Button(text="Exit", height=2, width=5, master=controls, command=self.window.destroy)
    new.grid(row=0, column=0)
    easy.grid(row=0, column=1)
    exit.grid(row=0, column=2)
    controls.pack()
    self.frame = tk.Frame(master=self.window)
    self.frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

  def __getitem__(self, idx):
    row, col = idx
    return self.buttons[row * self.length + col]

  def __setitem__(self, idx, elem):
    row, col = idx
    self.buttons[row * self.length + col] = elem

  def get_neighbours(self, row, col):
    nbrs = []

    print("where", row, col)

    for rw, cl in [
      (row-1,col),
      (row,col-1),
      (row,col+1),
      (row+1,col),
    ]:
      if rw >= 0 and rw < self.length:
        if cl >= 0 and cl < self.length:
          nbrs.append((rw,cl))

    return nbrs

  def handle_click(self, row, col):
    moved = False
    print("handle where", (row,col))
    btn = self[row,col]
    print("which btn:", btn)

    for nbr in self.get_neighbours(row, col):
      rw, cl = nbr
      print(rw,cl)
      nbr_btn = self[rw,cl]
      if nbr_btn["state"] == "disabled":
        moved = True
        self[row,col], self[rw,cl] = self[rw,cl], self[row,col]
    if not moved:
      print("Nothing happens")
    else:
      self.update()
      if self.has_won():
        msgbox.showinfo(title="Victory", message="You win!")
        self.randomize()

  def update(self):
    for i, btn in enumerate(self.buttons):
      row, col = i // self.length, i % self.length
      btn["command"] = self.handle(row,col)
      btn.grid(row=row, column=col)

  def handle(self, row, col):
    return lambda: self.handle_click(row, col)

  def randomize(self):
    # перемешиваем все кроме последней
    copy = self.buttons[:-1]
    random.shuffle(copy)
    self.buttons[:-1] = copy

    self.update()

  def easymode(self):
    for i,btn in enumerate(self.buttons):
      if btn["state"] == "disabled":
        self.buttons.append(self.buttons.pop(i))
        break

    copy = self.buttons[:-1]
    copy.sort(key=lambda btn: int(btn["text"]))
    self.buttons[:-1] = copy
    self.buttons[-1],self.buttons[-2] = self.buttons[-2], self.buttons[-1]

    self.update()

  def fill(self):
    # создаем кнопки
    for i in range(self.size):
      state = "normal"
      text = f"{i+1}"
      if i == self.size-1:
        state = "disabled"
        text = ""
      btn = tk.Button(
        text=text,
        width=7,
        height=5,
        master=self.frame,
        state=state,
      )
      self.buttons.append(btn)

    self.randomize()

  def has_won(self):
    if self.buttons[-1]["state"] != "disabled":
      return False
    # список номеров кнопок на доске
    ar = list(map(lambda btn: int(btn["text"]), self.buttons[:-1]))
    print(ar)
    if ar == list(range(1, self.size)):
      return True

  def start(self):
    self.fill()
    self.window.mainloop()

s = State(16)
s.start()