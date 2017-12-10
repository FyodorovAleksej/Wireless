import re
import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QTableWidgetItem, QAbstractItemView

from WifiAdapter import WifiAdapter
from mainwindow import Ui_MainWindow


# Main Window class
class MyWin(QtWidgets.QMainWindow):
    # USB Adapter for working with USB devices
    wifiAdapter = WifiAdapter()

    # construct window
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # default column size
        self.ui.wifiTable.setColumnCount(4)
        self.ui.wifiTable.insertRow(self.ui.wifiTable.rowCount())
        # initialize headers of table
        header1 = QTableWidgetItem("name")
        header2 = QTableWidgetItem("address")
        header3 = QTableWidgetItem("quality")
        header4 = QTableWidgetItem("security")
        # set headers
        self.ui.wifiTable.setHorizontalHeaderItem(0, header1)
        self.ui.wifiTable.setHorizontalHeaderItem(1, header2)
        self.ui.wifiTable.setHorizontalHeaderItem(2, header3)
        self.ui.wifiTable.setHorizontalHeaderItem(3, header4)
        # settings for table items
        self.ui.wifiTable.setSelectionBehavior(QAbstractItemView.SelectRows)
        headers = self.ui.wifiTable.horizontalHeader()
        headers.setStretchLastSection(True)
        # set 0 rows as default
        self.ui.wifiTable.setRowCount(0)
        # connecting eject button
        self.ui.connectButton.clicked.connect(self.connect)
        self.ui.pingButton.clicked.connect(self.ping)

    # close action
    def closeEvent(self, event):
        event.accept()

    # append 3 strings in table in 3 columns
    def appendText(self, name, address, quality, security, use):
        # creating new TableItem and setting it parametres
        item1 = QTableWidgetItem(name)
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(address)
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(quality)
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item4 = QTableWidgetItem(security)
        item4.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        # validate last item
        table = self.ui.wifiTable
        item = table.item(table.rowCount() - 1, 0)
        if (item != None):
            # adding new row in table
            table.insertRow(table.rowCount())
        # if table is empty
        if (table.rowCount() == 0):
            table.setRowCount(1)
        table.setItem(table.rowCount() - 1, 0, item1)
        table.setItem(table.rowCount() - 1, 1, item2)
        table.setItem(table.rowCount() - 1, 2, item3)
        table.setItem(table.rowCount() - 1, 3, item4)

    def refreshWifi(self):
        # getting flesh-memory
        wifiList = self.wifiAdapter.getWifiList()
        nameList = []
        # flag for finding this device
        flag = -1
        for wifiInfo in wifiList:
            nameList.append(wifiInfo["name"])
            # iterate all names in table
            for index in range(self.ui.wifiTable.rowCount()):
                if (self.ui.wifiTable.item(index, 0) != None):
                    if (self.ui.wifiTable.item(index, 0).text() == wifiInfo["name"]):
                        # save index of equals item
                        flag = index
            # if table don't contain this device
            if (flag == -1):
                if (wifiInfo != None):
                    self.appendText(wifiInfo["name"], wifiInfo["address"], str(wifiInfo["quality"]), wifiInfo["security"], wifiInfo["use"])
            else:
                # update device information (size)
                self.updateRow(flag, wifiInfo)
        # checking ejecting devices
        for i in range(0, self.ui.wifiTable.rowCount()):
            if (self.ui.wifiTable.item(i, 0) != None):
                if (not (self.ui.wifiTable.item(i, 0).text() in nameList)):
                    # remove device from table
                    self.ui.wifiTable.removeRow(i)

    def connect(self):
        # getting selected row
        indexes = self.ui.wifiTable.selectionModel().selectedRows()
        for index in sorted(indexes):

            if (self.ui.wifiTable.item(index.row(), 0).background() == QColor(225, 125, 125)):
                message = self.wifiAdapter.disconnect(self.ui.wifiTable.item(index.row(),0).text())
                self.errorInfo(message)
            else:
                # eject selected device
                message = self.wifiAdapter.connect(self.ui.wifiTable.item(index.row(), 0).text())
                # print error message if can't eject device
                self.errorInfo(message)

    def ping(self):
        # getting selected row
        indexes = self.ui.wifiTable.selectionModel().selectedRows()
        for index in sorted(indexes):
            # eject selected device
            message = self.wifiAdapter.ping(self.ui.wifiTable.item(index.row(), 0).text())
            # print error message if can't eject device
            self.errorInfo(message)

    # print info about ejecting
    def errorInfo(self, message):
        if (message != None):
            self.ui.infoLabel.setText("info: " + message)

    # update information about input device
    def updateRow(self, row, wifiInfo):
        # creating new item
        item1 = QTableWidgetItem(wifiInfo["name"])
        item1.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item2 = QTableWidgetItem(wifiInfo["address"])
        item2.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item3 = QTableWidgetItem(str(wifiInfo["quality"]))
        item3.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        item4 = QTableWidgetItem(wifiInfo["security"])
        item4.setFlags(QtCore.Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        if wifiInfo["use"]:
            item1.setBackground(QColor(225, 125, 125))
            item2.setBackground(QColor(225, 125, 125))
            item3.setBackground(QColor(225, 125, 125))
            item4.setBackground(QColor(225, 125, 125))
        # setting items
        table = self.ui.wifiTable
        if (row < table.rowCount()):
            table.setItem(row, 0, item1)
            table.setItem(row, 1, item2)
            table.setItem(row, 2, item3)
            table.setItem(row, 3, item4)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWin()
    window.show()

    # creating timer for refresh main window
    timer = QTimer()
    timer.timeout.connect(window.refreshWifi)
    timer.start(1000)

    sys.exit(app.exec_())
    exit()
