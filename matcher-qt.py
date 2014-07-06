#!/usr/bin/python

import sys
import textwrap
from PyQt4 import QtGui
from PyQt4 import QtCore
import matcher

app = QtGui.QApplication(sys.argv)
mainLayout = QtGui.QVBoxLayout()
fileOutputLayout = QtGui.QHBoxLayout()
classifiersLayout = QtGui.QGridLayout()
dialog = QtGui.QDialog()
dialog.setLayout(mainLayout)
dialog.setWindowTitle("Matcher")
button = QtGui.QPushButton("Go")
helpButton = QtGui.QPushButton("Help")
helpLayout = QtGui.QVBoxLayout()
helpDialog = QtGui.QDialog()
safeString = ', '.join(matcher.safe_list)
helpLabel = QtGui.QLabel(textwrap.fill(
    "The error function is the range (+/-) in which patient records are included and all records outside this range are excluded. To define the error function used for each variable, you may use numbers, any basic math functions (+, -, *, /, or **), and the classifier variable itself (represented by 'x' in the function). Additionally, the following python math functions may be used: \n" + safeString,79))
helpDialog.setLayout(helpLayout)
helpDialog.setWindowTitle("Matcher Help")
helpLayout.addWidget(helpLabel)

# Select file for output
fileOutputLayout.addWidget(QtGui.QLabel("Select Output Folder: "))
fileOutputText = QtGui.QLineEdit()
fileOutputLayout.addWidget(fileOutputText)
fileOutputButton = QtGui.QPushButton("...")
fileOutputLayout.addWidget(fileOutputButton)
selectedDir = ""

# Classifiers 
class Classifier:
    def __init__(self, label):
        self.label = QtGui.QLabel(label) # This should match the classifier's name
        self.checkBox = QtGui.QCheckBox()
        self.lineEdit = QtGui.QLineEdit()
        self.checkBox.setChecked(True) # checkbox defaults to on

labelLabel = QtGui.QLabel("Classifier")
checkBoxLabel = QtGui.QLabel("Use?")
errorValueLabel = QtGui.QLabel("Error Function")
classifiersLayout.addWidget(labelLabel,0,0)
classifiersLayout.addWidget(checkBoxLabel,0,1)
classifiersLayout.addWidget(errorValueLabel,0,2)
classifiersLayout.setAlignment(QtCore.Qt.AlignBottom)

classifiers = {}

for i,key in enumerate(matcher.SORT_ORDER):
    classifiers[key] = Classifier(key)
    classifiersLayout.addWidget(classifiers[key].label, i+1, 0)
    classifiersLayout.addWidget(classifiers[key].checkBox, i+1, 1)
    classifiersLayout.addWidget(classifiers[key].lineEdit, i+1, 2)
    try:
        classifiers[key].lineEdit.setText(str(matcher.ERROR_FUNCTIONS[key]))
    except KeyError:
        classifiers[key].lineEdit.setDisabled(True)
mainLayout.addLayout(fileOutputLayout)
mainLayout.addWidget(helpButton)
mainLayout.addLayout(classifiersLayout)
mainLayout.addWidget(button)

@QtCore.pyqtSlot()
def clicked_go():
    if (selectedDir is ""):
        msgBox = QtGui.QMessageBox()
        msgBox.setText("Please select output folder.")
        msgBox.setWindowTitle(" ")
        msgBox.exec_()
        return
    sortOrder = []
    errorRanges = {}
    for key in classifiers:
        if (classifiers[key].checkBox.isChecked()):
            sortOrder.append(str(classifiers[key].label.text()))
            try:
                errorRanges[key] = float(classifiers[key].lineEdit.text())
            except ValueError:
                try:
                    errorRanges[key] = matcher.ERROR_RANGES[key]
                except KeyError:
                    pass
    print sortOrder
    print errorRanges
    print("Matching...")
    matcher.matcher(sortOrder=sortOrder,errorRanges=errorRanges,outDir=selectedDir)
    print("Done!")

@QtCore.pyqtSlot()
def clicked_select_file():
    global selectedDir
    selectedDir = QtGui.QFileDialog.getExistingDirectory(None, QtCore.QString("Select Save Directory"), QtCore.QString("/home"), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
    fileOutputText.setText(selectedDir)

@QtCore.pyqtSlot()
def clicked_help():
    helpDialog.show()

fileOutputButton.clicked.connect(clicked_select_file)

helpButton.clicked.connect(clicked_help)

button.clicked.connect(clicked_go)

dialog.show()
sys.exit(app.exec_())

    
