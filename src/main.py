import sys
from PyQt5.QtWidgets import QApplication
from View.Window_Qt import Window_Qt

def main():
	app = QApplication(sys.argv)
  
	window = Window_Qt()
	window.show()
  
	sys.exit(app.exec_())

if __name__ == '__main__':
   main()