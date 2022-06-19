from tkinter import Button, Frame

class LabelButton:
	def __init__(self, root, text, command):
		self.command = command
		self.text = text
		self.frame = root
		self.mainButton = Button(self.frame, text=self.text, command=self.command)
		self.killButton = Button(self.mainButton, text='x', command=self.frame.destroy)
		
	def pack(self):
		self.mainButton.pack(side='left', ipadx=40)
		self.killButton.pack(side='right', padx=4)
