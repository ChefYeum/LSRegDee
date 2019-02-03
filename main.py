from PySide2.QtWidgets import QApplication, QDialog, QHBoxLayout, QVBoxLayout, QTableWidget, QPushButton, QTableWidgetItem, QHeaderView

import sys
import lsr_stats as LSR

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

#Define a window class inheritted from QDialog class from PyQt5 module
class window(QDialog):
    def __init__(self):
        super().__init__()#UI initialisation
        self.setup() #Call the setup method
        self.show() #Display window

    def init_table(self, rowLen): #Initialise  items to empty strings
        self.widget_table.clear()
        for r in range(rowLen):
            self.widget_table.setItem(r,0,QTableWidgetItem(''))
            self.widget_table.setItem(r,1,QTableWidgetItem(''))


    def setup(self):
        #Set the size of the window to 960x540 initiallly at (20,20)
        self.setGeometry(20,20,960,540)

        #Setup table with 2 rows and 2 columns
        self.widget_table = QTableWidget(2,2,self)

        # Initialise table with 2 rows (all items to empty strings)
        self.init_table(2)

        #Set column labels to 'X' and 'Y'
        self.widget_table.setHorizontalHeaderLabels(['X','Y'])
        self.widget_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.widget_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        #Create figure, figure canvas and a navigation bar for the graph
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.navigationBar = NavigationToolbar(self.canvas, self)
        self.axis = self.figure.add_subplot(111)

        #Setup each button and link each of them to corresponding method
        button_addRow = QPushButton('Add Row', self)
        button_addRow.clicked.connect(self.addRow)
        button_plot = QPushButton('Plot', self)
        button_plot.clicked.connect(self.plot)

        #Setup UI layout and add widgets
        mainLayout = QHBoxLayout()
        vLeft = QVBoxLayout()
        vRight = QVBoxLayout()
        mainLayout.addLayout(vLeft)
        mainLayout.addLayout(vRight)
        self.setLayout(mainLayout)

        vLeft.addWidget(self.widget_table)
        vLeft.addWidget(button_addRow)

        vRight.addWidget(self.navigationBar)
        vRight.addWidget(self.canvas)
        vRight.addWidget(button_plot)

    def addRow(self):
        lastRow = self.widget_table.rowCount() #Get the index of the last row
        self.widget_table.insertRow(lastRow) #Insert another row below the last row
        self.widget_table.setItem(lastRow,0,QTableWidgetItem('')) #Set the contents the items on the new row to empty strings
        self.widget_table.setItem(lastRow,1,QTableWidgetItem('')) #"

    def plot(self):
        validVal = [] #Create an array of records
        rowCount = self.widget_table.rowCount()
        for r in range(rowCount):
            x = self.widget_table.item(r,0).text() #Get x value from the current row
            y = self.widget_table.item(r,1).text() #Get y value from the current row
            if x.replace('.', '', 1).isdigit() and y.replace('.','',1).isdigit():#If both values are valid...
                validVal.append([float(x),float(y)]) #append it to the array of records

        #Bubble sort the values
        for outer in range(len(validVal)-1,0,-1):
            for inner in range(outer):
                if validVal[inner][0] > validVal[inner+1][0]:
                    validVal[inner], validVal[inner+1] = validVal[inner+1], validVal[inner]

        #Re-initialise table
        self.init_table(rowCount)

        #Replace the table with the validated/sorted values
        for r, i in enumerate(validVal):
            self.widget_table.setItem(r,0,QTableWidgetItem(str(i[0])))
            self.widget_table.setItem(r,1,QTableWidgetItem(str(i[1])))

        if len(validVal) < 2:#Check if there is enough pairs of coordinates to carry out the regression
            print ("Not enough data") #If not, send an error message to display
        else:
            #Get x values and the y values in separate arrays from the array of records
            xvalues = [validVal[i][0] for i in range(len(validVal))]
            yvalues = [validVal[i][1] for i in range(len(validVal))]

            #Plot scatterplot
            self.axis.cla() #clear axis
            self.axis.plot(xvalues,yvalues, ".")
            self.canvas.draw()

            #Calculate required values for the regression line
            a = LSR.lse_a(xvalues,yvalues)
            b = LSR.lse_b(xvalues,yvalues)
            print("a: ", a)
            print("b: ", b)

            #Get the x values for the starting point and the ending point of the line
            xlim = (self.axis.get_xlim())

            leftlimx = xlim[0]
            rightlimx = xlim[1]

            #Calculate the corresponding y values
            leftlimy = a + leftlimx * b
            rightlimy = a + rightlimx * b

            #Plot the regression line on the canvas
            self.axis.plot([leftlimx, rightlimx], [leftlimy, rightlimy], "-")
            self.axis.autoscale_view(True,True,True)
            self.canvas.draw()


if __name__ == '__main__': #Main program
    app = QApplication(sys.argv) #Create an application object with a system variable
    w = window() #Create a UI window object
    sys.exit(app.exec_()) #Start the event loop