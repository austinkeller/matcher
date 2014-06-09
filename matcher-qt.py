#!/usr/bin/python

import sys
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

# Select file for output
fileOutputLayout.addWidget(QtGui.QLabel("Select Output File: "))
fileOutputText = QtGui.QLineEdit()
fileOutputLayout.addWidget(fileOutputText)
fileOutputButton = QtGui.QPushButton("...")
fileOutputLayout.addWidget(fileOutputButton)
fileOutputText.setDisabled(True) # TODO: implement output file selection

# Classifiers 
class Classifier:
    def __init__(self, label):
        self.label = QtGui.QLabel(label) # This should match the classifier's name
        self.checkBox = QtGui.QCheckBox()
        self.lineEdit = QtGui.QLineEdit()
        self.checkBox.setChecked(True) # checkbox defaults to on

labelLabel = QtGui.QLabel("Classifier")
checkBoxLabel = QtGui.QLabel("Use?")
errorValueLabel = QtGui.QLabel("Error Value")
errorTypeLabel = QtGui.QLabel("Error Type")
classifiersLayout.addWidget(labelLabel,0,0)
classifiersLayout.addWidget(checkBoxLabel,0,1)
classifiersLayout.addWidget(errorValueLabel,0,2)
classifiersLayout.addWidget(errorTypeLabel,0,3)
classifiersLayout.setAlignment(QtCore.Qt.AlignBottom)

classifiers = {}

for i,key in enumerate(matcher.SORT_ORDER):
    classifiers[key] = Classifier(key)
    classifiersLayout.addWidget(classifiers[key].label, i+1, 0)
    classifiersLayout.addWidget(classifiers[key].checkBox, i+1, 1)
    classifiersLayout.addWidget(classifiers[key].lineEdit, i+1, 2)
    try:
        classifiers[key].lineEdit.setText(str(matcher.ERROR_RANGES[key]))
    except KeyError:
        classifiers[key].lineEdit.setDisabled(True)
    try:
        classifiersLayout.addWidget(QtGui.QLabel(matcher.ERROR_TYPES[key]), i+1, 3)
    except KeyError:
        classifiersLayout.addWidget(QtGui.QLabel(''), i+1, 3)
mainLayout.addLayout(fileOutputLayout)
mainLayout.addLayout(classifiersLayout)
mainLayout.addWidget(button)

@QtCore.pyqtSlot()
def clicked_go():
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
    matcher.matcher(sortOrder=sortOrder,errorRanges=errorRanges)
    print("Done!")

button.clicked.connect(clicked_go)

dialog.show()
sys.exit(app.exec_())
