import sys

def read_numbers_from_string(string):
	accum = ""
	numbers = []
	for char in string:
		if char.isdigit():
			accum += char
		else:
			if len(accum) > 0:
				numbers.append(int(accum))
				accum = ""
	return numbers

class Sudoku(object):
	def __init__(self, file):
		sizes_str = file.readline()
		self.empties = []
		self.table = []
		self.rows, self.columns = read_numbers_from_string(sizes_str)
		i = 0
		for line in file:
			j = 0
			numbers = []
			for char in line:
				if char.isdigit():
					numbers.append(int(char))
					j += 1
				elif char == "x":
					numbers.append(0)
					self.empties.append([i,j])
					j += 1
			self.table.append(numbers)
			i += 1

	def show_table(self):
		for row in self.table:
			print row
		print " "

	def table_columns(self):
		result = []
		for j in xrange(0, self.columns):
			column = []
			for i in xrange(0, self.rows):
				column.append(self.table[i][j])
			result.append(column)
		return result

	def small_square(self,row,column):
		sm_row = row // (self.rows/3)
		sm_col = column // (self.columns/3)
		result = []
		for i in xrange(sm_row*3, sm_row*3 + (self.rows/3)):
			for j in xrange(sm_col*3, sm_col*3 + (self.columns/3)):
				result.append(self.table[i][j])
		return result

	def check_table(self):
		#Check rows
		for row in self.table:
			for digit in xrange(1,10):
				if row.count(digit) > 1:
					return -1
		#Check columns
		for column in self.table_columns():
			for digit in xrange(1,10):
				if column.count(digit) > 1:
					return -1
		#Check small square
		for i in xrange(0, self.rows, self.rows/3):
			for j in xrange(0, self.columns, self.columns/3):
				for digit in xrange(1,10):
					if self.small_square(i,j).count(digit) > 1:
						return -1
		return 0

	def try_digits(self, i):
		if i == len(self.empties):
			print "Solved!"
			self.show_table()
			return 0
		else:
			empty = self.empties[i]
			for digit in xrange(1,10):
				self.table[empty[0]][empty[1]] = digit
				#self.show_table()
				value = self.check_table()
				if value == 0:
					if self.try_digits(i+1) == 0:
						return 0
			self.table[empty[0]][empty[1]] = 0
			return -1

file = open("in.txt","r")
sudoku = Sudoku(file)
sudoku.show_table()
sudoku.try_digits(0)
#Ideas to optimize: 
#	-Don't create the column table everytime you check for repeated values
#	-Same with the small squares
#	-Don't try the same digits on a small square, with this we can not check it on check()
#	-Non recursive approach?


