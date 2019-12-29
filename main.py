# Was made using Python 3.6.2
import sys
import os
import random
try:
	import pyglet
	from pyglet.gl import *
	from pyglet.window import key
	from pyglet.window import mouse
except ImportError as e:
	print("ERROR: Make sure the packages in requirements.txt are installed.")
	print("You can do so with \"pip install -r requirements.txt\"")
	sys.exit(1)

MOVE = {
	(0, -1): [(key.UP   , 0), (key.W, 0), (key.NUM_8, 0)],
	(0,  1): [(key.DOWN , 0), (key.S, 0), (key.NUM_2, 0)],
	(-1, 0): [(key.LEFT , 0), (key.A, 0), (key.NUM_4, 0)],
	(1 , 0): [(key.RIGHT, 0), (key.D, 0), (key.NUM_6, 0)],
}

class Graphics:
	line_width = 1

	def vertex2(x, y):
		glVertex2i(int(x), int(y))

	def rectangle(rect_type, x, y, w, h):
		if w < 0:
			x+=w
			w*=-1
		if h < 0:
			y+=h
			h*=-1
		if rect_type == "fill":
			glBegin(GL_QUADS)
			Graphics.vertex2(x, y)
			Graphics.vertex2(x, y+h)
			Graphics.vertex2(x+w, y+h)
			Graphics.vertex2(x+w, y)
			glEnd()
		elif rect_type == "line":
			# Could be optimized by having intermediary variables, for common calculations
			glBegin(GL_POLYGON)
			Graphics.vertex2(x, y)
			Graphics.vertex2(x, y+h)
			Graphics.vertex2(x+Graphics.line_width, y+h-Graphics.line_width)
			Graphics.vertex2(x+Graphics.line_width, y+Graphics.line_width)
			Graphics.vertex2(x+w-Graphics.line_width, y+Graphics.line_width)
			Graphics.vertex2(x+w, y)
			glEnd()
			glBegin(GL_POLYGON)
			Graphics.vertex2(x+w, y+h)
			Graphics.vertex2(x+w, y)
			Graphics.vertex2(x+w-Graphics.line_width, y+Graphics.line_width)
			Graphics.vertex2(x+w-Graphics.line_width, y+h-Graphics.line_width)
			Graphics.vertex2(x+Graphics.line_width, y+h-Graphics.line_width)
			Graphics.vertex2(x, y+h)
			glEnd()
	
	def line(x1, y1, x2, y2):
		glBegin(GL_LINES)
		glVertex2i(int(x1), int(y1))
		glVertex2i(int(x2), int(y2))
		glEnd()

	def setLineWidth(width):
		glLineWidth(width)
		Graphics.line_width = width

	def getLineWidth():
		return Graphics.line_width

	def setColor(color):
		if len(color) == 4:
			glEnable( GL_BLEND );
			glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); 
			glColor4ub(int(color[0]), int(color[1]), int(color[2]), int(color[3]))
		else:
			glColor4ub(int(color[0]), int(color[1]), int(color[2]), 255)
	
	def setClearColor(color):
		glClearColor(color[0]/255, color[1]/255, color[2]/255 ,1)

class Button:
	base_color = (19, 20, 23)
	hover_color = (29, 30, 23)
	pressed_color = (9, 10, 13)
	text_color = (248, 248, 242, 255)
	font_name = "Arial"

	def __init__(self, x, y, width, height, text=""):
		self.hover = False
		self.pressed = False
		self.onClick = None
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.label = pyglet.text.Label(
			text,
			font_name=Button.font_name, font_size=self.height*0.5,
			x = self.x + self.width/2,
			y = self.y - self.height/2,
			anchor_x='center', anchor_y='center',
			color=Button.text_color
		)

	def draw(self):
		if self.pressed:
			Graphics.setColor(self.pressed_color)
		elif self.hover:
			Graphics.setColor(self.hover_color)
		else:
			Graphics.setColor(self.base_color)
		Graphics.rectangle("fill", self.x, self.y, self.width, -self.height)
		self.label.draw()

	def onMouseMotion(self, x, y, dx, dy):
		self.hover = self.x <= x < self.x+self.width and self.y-self.height<= y < self.y
	
	def onMousePress(self, x, y, button, modifiers):
		self.pressed = self.hover and button & mouse.LEFT

	def onMouseRelease(self, x, y, button, modifiers):
		if self.pressed:
			if self.onClick:
				self.onClick()
			self.pressed = False

class AboutPopup:
	shade_color = (19, 20, 23, 128)
	background_color = (39, 40, 34)
	border_color = (19, 20, 23)
	border_width = 8
	font_name = "Arial"
	font_color = (248, 248, 242, 255)
	font_size = 10
	
	def addLabel(self, text, x, y):
		self.elements.append(pyglet.text.Label(text, x=x, y=y, font_name=self.font_name,font_size=self.font_size,color=self.font_color))
	
	def __init__(self, parent_width, parent_height):
		self.elements = []
		self.visible = False
		self.parent_width = parent_width
		self.parent_height = parent_height
		self.width = 200
		self.height = 150
		self.x = (parent_width  - self.width)/2
		self.y = (parent_height + self.height)/2

		back_button_size = (50, 25)
		padding = 5
		self.back_button = Button(
			self.x+self.width-back_button_size[0]-padding-self.border_width,
			self.y-self.height+back_button_size[1]+padding+self.border_width, 
			back_button_size[0], back_button_size[1], "Back"
		)
		self.back_button.onClick = lambda: self.toggle()

		self.addLabel("Made by Rokas Puzonas ©", self.x+self.border_width+padding, self.y-self.font_size-self.border_width-padding)
		self.addLabel("MIT License", self.x+self.border_width+padding, self.y-self.border_width-2*(padding+self.font_size))

	def toggle(self):
		self.visible = not self.visible		

	def draw(self):
		if not self.visible: return
		Graphics.setColor(self.shade_color)
		Graphics.rectangle("fill", 0, 0, self.parent_width, self.parent_height)

		Graphics.setColor(self.background_color)
		Graphics.rectangle("fill", self.x, self.y, self.width, -self.height)
		Graphics.setColor(self.border_color)
		Graphics.setLineWidth(self.border_width)
		Graphics.rectangle("line", self.x, self.y, self.width, -self.height)

		self.back_button.draw()

		for element in self.elements:
			element.draw()

	def onKeyPress(self, symbol, modifiers):
		if not self.visible: return
		if symbol == key.ESCAPE:
			self.visible = False
		return True

	def onMouseMotion(self, x, y, dx, dy):
		if not self.visible: return
		self.back_button.onMouseMotion(x, y, dx, dy)
		return True

	def onMousePress(self, x, y, button, modifiers):
		if not self.visible: return
		self.back_button.onMousePress(x, y, button, modifiers)
		return True

	def onMouseRelease(self, x, y, button, modifiers):
		if not self.visible: return
		self.back_button.onMouseRelease(x, y, button, modifiers)
		return True

class SudokuSolver:
	@staticmethod
	def findEmpty(board):
		for i in range(81):
			if board[i] == 0:
				return i
		return None

	@staticmethod
	def solve(board):
		if len(board) != 81: return False
		empty_pos = SudokuSolver.findEmpty(board)
		if empty_pos == None: return True

		for i in range(1, 10):
			if SudokuSolver.isValid(board,empty_pos, i):
				board[empty_pos] = i
				if SudokuSolver.solve(board): return True
				board[empty_pos] = 0
		
		return False

	@staticmethod
	def isValid(board, pos, value=None):
		# Get value that is already is board
		if value == None:
			value = board[pos]

		# Zero is always not valid
		if value == 0: return False

		# Check row
		row_start = pos//9*9
		for i in range(row_start, row_start+9):
			if i != pos and board[i] == value:
				return False

		# Check column
		for i in range(pos%9, 81, 9):
			if i != pos and board[i] == value:
				return False

		# Check square
		square_start = pos//3%3*3 + pos//27*27
		for x in range(3):
			for y in range(square_start, square_start+27, 9):
				i = y+x
				if i != pos and board[i] == value:
					return False
		
		return True

	@staticmethod
	def printBoard(board):
		for i in range(0, 81, 9):
			if i % 27 == 0 and i != 0:
				print("- - - - - - - - - - - -")
			print(f" {board[i]} {board[i+1]} {board[i+2]} | {board[i+3]} {board[i+4]} {board[i+5]} | {board[i+6]} {board[i+7]} {board[i+8]}")

class SudokuBoard:
	grid_color = (19, 20, 23)
	border_color = (9, 10, 13)
	selected_color = (230, 219, 116)
	cell_size = 50
	grid_width = 6
	font_name = "Arial"
	default_color = (248, 248, 242, 255)
	user_color = (117, 113, 94, 255)
	mistake_color = (249, 38, 114, 255)
	stepped_solve_speed = 60

	def __init__(self, x=0, y=0, board=None):
		self.stepped_cells = None
		self.current_cell = None
		self.x = x
		self.y = y
		self.selected_cell = (-1, -1)
		self.labels = []
		self.resetBoard(board)

	def resetBoard(self, board=[]):
		if len(board) != 81:
			board = list(0 for _ in range(81))
		self.start_board = board
		self.solution_board = self.start_board.copy()
		SudokuSolver.solve(self.solution_board)
		self.clear()
		
	def draw(self):
		board_size = self.size()

		Graphics.setLineWidth(self.grid_width)
		Graphics.setColor(self.grid_color)
		for i in (1, 2, 4, 5, 7, 8):
			offset = i*self.cell_size+Graphics.line_width*(i+0.5)
			Graphics.line(self.x+offset             , self.y+Graphics.line_width, self.x+offset    , self.y+board_size)
			Graphics.line(self.x+Graphics.line_width, self.y+offset             , self.x+board_size, self.y+offset    )

		Graphics.setColor(self.border_color)
		for i in (3, 6):
			offset = i*self.cell_size+Graphics.line_width*(i+0.5)
			Graphics.line(self.x+offset             , self.y+Graphics.line_width, self.x+offset    , self.y+board_size)
			Graphics.line(self.x+Graphics.line_width, self.y+offset             , self.x+board_size, self.y+offset    )

		Graphics.setColor(self.border_color)
		Graphics.rectangle("line", self.x, self.y, board_size, board_size)

		for label in self.labels:
			if label.text != "0":
				label.draw()

		if not self.isBusy():
			Graphics.setColor(self.selected_color)
			self.highlightCell(self.selected_cell)

	@staticmethod
	def size():
		return int(SudokuBoard.cell_size*9 + SudokuBoard.grid_width*10)

	def getCellAt(self, x, y):
		board_size = self.size()
		left_side = self.x+self.grid_width
		bottom_side = self.y+self.grid_width

		if not (left_side <= x < self.x + board_size-self.grid_width and bottom_side <= y < self.y + board_size-self.grid_width):
			return (-1, -1)
		
		cell_span = (self.cell_size+self.grid_width)
		return (int((x-left_side+self.grid_width/2)/cell_span), int(8-(y-bottom_side+self.grid_width/2)//cell_span))
	
	def highlightCell(self, cell):
		if cell[0] < 0 or cell[1] < 0: return
		highlight_size = self.cell_size+self.grid_width
		x = self.x+self.grid_width/2 + cell[0]*highlight_size
		y = self.y+self.grid_width/2 + (8-cell[1])*highlight_size
		Graphics.setLineWidth(self.grid_width/2)
		Graphics.rectangle("line", x, y, highlight_size, highlight_size)

	def onMousePress(self, x, y, button, modifiers):
		if self.isBusy(): return
		cell = self.getCellAt(x, y)
		if cell == self.selected_cell:
			self.selected_cell = (-1, -1)
		else:
			self.selected_cell = cell

	def onKeyPress(self, symbol, modifiers):
		if self.isBusy(): return
		if key._0 <= symbol <= key._9:
			self.setCell(self.selected_cell[0], self.selected_cell[1], symbol-key._0)
			return
		elif modifiers & key.MOD_NUMLOCK and (key.NUM_0 <= symbol <= key.NUM_9):
			self.setCell(self.selected_cell[0], self.selected_cell[1], symbol-key.NUM_0)
			return
		elif symbol == key.BACKSPACE:
			self.setCell(self.selected_cell[0], self.selected_cell[1], 0)
			return


		for axis in MOVE:
			keybinds = MOVE[axis]
			for keybind in keybinds:
				if symbol == keybind[0] and modifiers & keybind[1] == keybind[1]:
					x, y = self.selected_cell
					if self.selected_cell == (-1, -1):
						x, y = 4, 4
					x, y = x+axis[0], y+axis[1]
					if 0 <= x < 9 and 0 <= y < 9:
						self.selected_cell = (x, y)
						return

	def updateLabels(self):
		for i in range(81):
			self.updateLabel(i)

	def getLabel(self, index):
		if index >= len(self.labels):
			step = self.grid_width + self.cell_size
			self.labels.append(pyglet.text.Label(
				str(self.start_board[index]),
				font_name=self.font_name, font_size=self.cell_size*0.6, 
				x = self.x + (index%9+0.5) * step, 
				y = self.y + (8-index//9+0.5) * step,
				anchor_x='center', anchor_y='center',
				color=self.default_color
			))
		return self.labels[index]

	def updateLabel(self, index):
		label = self.getLabel(index)
		
		if self.start_board[index] != 0:
			label.text = str(self.start_board[index])
			label.color = SudokuBoard.default_color
		else:
			label.text = str(self.user_board[index])
			label.color = SudokuBoard.user_color
		label.italic = False
	
	def setCell(self, x, y, value):
		if self.isBusy(): return
		if not (0 <= x < 9 and 0 <= y < 9): return False
		index = y*9+x
		if self.start_board[index] != 0: return False
		self.user_board[index] = value
		self.updateLabel(index)
		return True

	def checkMistakes(self):
		if self.isBusy(): return
		for i in range(81):
			if self.user_board[i] == 0 or self.user_board[i] == self.solution_board[i]: continue
			label = self.getLabel(i)
			label.color = SudokuBoard.mistake_color
			label.italic = True
	
	def clear(self):
		if self.isBusy(): return
		self.user_board = [0 for _ in range(81)]
		self.updateLabels()

	def solve(self):
		if self.isBusy(): return
		self.user_board = self.solution_board.copy()
		self.updateLabels()

	def steppedSolve(self):
		if self.isBusy():
			pyglet.clock.unschedule(self.step)
			self.stepped_cells = None
			self.current_cell = None
		else:
			pyglet.clock.schedule_interval(self.step, 1/SudokuBoard.stepped_solve_speed)
			self.stepped_cells = []
			self.user_board = self.start_board.copy()
		self.updateLabels()

	def step(self, dt):
		if self.current_cell == None:
			self.current_cell = SudokuSolver.findEmpty(self.user_board)

		if self.current_cell == None:
			self.steppedSolve()
			return

		while True:
			self.user_board[self.current_cell] = (self.user_board[self.current_cell]+1) % 10
			if SudokuSolver.isValid(self.user_board, self.current_cell):
				self.updateLabel(self.current_cell)
				self.stepped_cells.append(self.current_cell)
				self.current_cell = SudokuSolver.findEmpty(self.user_board)
				break
			
			if self.user_board[self.current_cell] == 0:
				self.updateLabel(self.current_cell)
				self.current_cell = self.stepped_cells[-1]
				self.stepped_cells.pop()
				break
	
	def isBusy(self):
		return self.stepped_cells != None

class SudokuApp(pyglet.window.Window):
	background_color = (39, 40, 34)

	def __init__(self, board=[]):
		button_height = 16
		padding = 16

		self.elements = []
		self.board = SudokuBoard(padding, padding, board)
		board_size = SudokuBoard.size()
		super().__init__(board_size+padding*2, board_size+padding*3+button_height, "Sudoku Solver")
		self.about_popup = AboutPopup(self.width, self.height)
		buttons = (
			("Check mistakes", lambda: self.board.checkMistakes() ),
			("Solve"         , lambda: self.board.solve()         ),
			("Stepped solve" , lambda: self.board.steppedSolve()  ),
			("Clear"         , lambda: self.board.clear()         ),
			("About"         , lambda: self.about_popup.toggle()  ),
		)
		
		button_width = (SudokuBoard.size()-padding*(len(buttons)-1))/len(buttons)
		button_y = self.height-padding

		for i in range(len(buttons)):
			button_x = padding*(i+1)+button_width*i
			button = self.addButton(button_x, button_y, button_width, button_height, buttons[i][0])
			button.onClick = buttons[i][1]

	def addButton(self, *args, **kwargs):
		button = Button(*args, **kwargs)
		self.elements.append(button)
		return button
	
	def on_draw(self):
		Graphics.setClearColor(self.background_color)
		self.clear()
		self.board.draw()
		self.emitToElements("draw")
		self.about_popup.draw()

	def on_key_press(self, symbol, modifiers):
		if self.about_popup.onKeyPress(symbol, modifiers): return
		self.board.onKeyPress(symbol, modifiers)
		self.emitToElements("onKeyPress", symbol, modifiers)
	
	def on_mouse_press(self, x, y, button, modifiers):
		if self.about_popup.onMousePress(x, y, button, modifiers): return
		self.board.onMousePress(x, y, button, modifiers)
		self.emitToElements("onMousePress", x, y, button, modifiers)

	def on_mouse_release(self, x, y, button, modifiers):
		if self.about_popup.onMouseRelease(x, y, button, modifiers): return
		self.emitToElements("onMouseRelease", x, y, button, modifiers)

	def on_mouse_motion(self, x, y, dx, dy):
		if self.about_popup.onMouseMotion(x, y, dx, dy): return
		self.emitToElements("onMouseMotion", x, y, dx, dy)
	
	def emitToElements(self, event_name, *args, **kwargs):
		for element in self.elements:
			event_method = getattr(element, event_name, None)
			if callable(event_method):
				event_method(*args, **kwargs)

def boardFromFile(filename):
	if not os.path.isfile(filename): return None
	board = []
	file = open(filename, "r")
	for line in file:
		for value in line.split():
			try:
				board.append(int(value))
			except ValueError:
				pass
	file.close()
	return board

if __name__ == "__main__":
	SudokuApp(boardFromFile("board.txt"))
	pyglet.app.run()