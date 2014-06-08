#!/usr/bin/python

import sys
from PyQt4 import QtGui
import matcher

app = QtGui.QApplication(sys.argv)
mainLayout = QtGui.QVBoxLayout()
classifiersLayout = QtGui.QHBoxLayout()
dialog = QtGui.QDialog()
dialog.setLayout(mainLayout)
dialog.setWindowTitle("Matcher")
button = QtGui.QPushButton("Go")

# Classifiers 
class Classifier:
    def __init__(self, label):
        self.label = QtGui.QLabel(label) # This should match the classifier's name
        self.checkBox = QtGui.QCheckBox()
        self.lineEdit = QtGui.QLineEdit()
        self.checkBox.setChecked(True) # checkbox defaults to on


labelLayout = QtGui.QVBoxLayout()
checkBoxLayout = QtGui.QVBoxLayout()
errorValueLayout = QtGui.QVBoxLayout()
errorTypeLayout = QtGui.QVBoxLayout()

classifiersLayout.addLayout(labelLayout)
classifiersLayout.addLayout(checkBoxLayout)
classifiersLayout.addLayout(errorValueLayout)
classifiersLayout.addLayout(errorTypeLayout)
labelLayout.addWidget(QtGui.QLabel("Classifier"))
checkBoxLayout.addWidget(QtGui.QLabel("Use?"))
errorValueLayout.addWidget(QtGui.QLabel("Error Value"))
errorTypeLayout.addWidget(QtGui.QLabel("Error Type"))

classifiers = {}

for key in matcher.SORT_ORDER:
    classifiers[key] = Classifier(key)
    labelLayout.addWidget(classifiers[key].label)
    checkBoxLayout.addWidget(classifiers[key].checkBox)
    errorValueLayout.addWidget(classifiers[key].lineEdit)
    try:
        errorTypeLayout.addWidget(QtGui.QLabel(matcher.ERROR_TYPES[key]))
    except KeyError:
        errorTypeLayout.addWidget(QtGui.QLabel(''))

mainLayout.addLayout(classifiersLayout)
mainLayout.addWidget(button)


dialog.show()
sys.exit(app.exec_())
