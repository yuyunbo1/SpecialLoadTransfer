# -*- coding: utf-8 -*-
from app.ui_window import Ui_MovieDownloadAndTransfer
from app.download_mod import MovieDownMod
from app.transfer_mod import MovieTransMod

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow


#定义一个主窗口类,继承了QMainWindow及Ui_Form
class MainWindow(QMainWindow, Ui_MovieDownloadAndTransfer):
    def __init__(self, parent = None):
        # 调用父类QMainWindow进行初始化
        super(MainWindow, self).__init__(parent)
        # 调用继承类Ui_MovieDownloadAndTransfer的方法setupUi
        self.setupUi(self)
        #视频下载模块自定义槽函数
        self.movieAddrLineEdit.returnPressed.connect(self.movieAddrLineEditFinishSlotFunc)
        self.movieLocalAddrLineEdit.returnPressed.connect(self.movieLocalAddrLineEditFinishSlotFunc)
        self.startDownBut.clicked['bool'].connect(self.startDownButSlotFunc)
        self.cancelDownBut.clicked['bool'].connect(self.cancelDownButSlotFunc)
        #格式转换 模块自定义槽函数
        self.sourceLocalAddrLineEdit.returnPressed.connect(self.sourceLocalAddrLineEditSlotFunc)
        self.targetLocalAddrLineEdit.returnPressed.connect(self.targetLocalAddrLineEditSlotFunc)
        self.saveSourceTranBut.clicked['bool'].connect(self.saveSourceTranButSlotFunc)
        self.notSaveSourceTranBut.clicked['bool'].connect(self.notSaveSourceTranButSlotFunc)

        self.printfText('welcom to come to movie downLoad and transfer')

        #数据定义与处理
        self.movieDownMod = MovieDownMod()
        self.movieTransMod = MovieTransMod()

    #槽函数start
    def movieAddrLineEditFinishSlotFunc(self):
        text = "" + self.movieAddrLineEdit.text()
        self.movieDownMod.SetMovieEditStr(text, self)
    def movieLocalAddrLineEditFinishSlotFunc(self):
        text = "" + self.movieLocalAddrLineEdit.text()
        self.movieDownMod.SetMovieLocalEditStr(text, self)
    def startDownButSlotFunc(self):
        self.printfText("startDownBut is pressend and enter pro")
        self.movieDownMod.DownLoadPro(1, self)
    def cancelDownButSlotFunc(self):
        self.printfText("cancelDownBut is pressend")
        self.movieDownMod.DownLoadPro(0, self)

    def sourceLocalAddrLineEditSlotFunc(self):
        self.printfText(self.sourceLocalAddrLineEdit.text())
    def targetLocalAddrLineEditSlotFunc(self):
        self.printfText(self.targetLocalAddrLineEdit.text())
    def saveSourceTranButSlotFunc(self):
        self.printfText("saveSourceTranBut is pressend")
    def notSaveSourceTranButSlotFunc(self):
        self.printfText("notSaveSourceTranBut is pressend")
    # 槽函数end

    # 在指定的区域显示提示信息
    def printfText(self, str):
        self.runStatusTextBro.append(str)
        self.cursor = self.runStatusTextBro.textCursor()
        # 光标移到最后，这样就会自动显示出来
        self.runStatusTextBro.moveCursor(self.cursor.End)
        # 一定加上这个功能，不然有卡顿
        QApplication.processEvents()

if __name__ == '__main__':
    # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
    print('welcom to come to movie downLoad and transfer')
    movieDownLoadApp = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    # 程序运行，sys.exit方法确保程序完整退出。
    sys.exit(movieDownLoadApp.exec_())