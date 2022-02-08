import aqt
from aqt import QUrl, QWebEngineView, mw, DialogManager
from aqt.qt import QDialog, QAction
from PyQt5 import QtWidgets

from .web import Ui_Dialog

config = mw.addonManager.getConfig(__name__)

class QSearchDialog(QDialog, Ui_Dialog):
    def __init__(self, mw):
        super().__init__(mw)
        self.urlSelected = ""
        self.removeTabsOnSave = True

        self.setupUi(self)

        self.pushButton.clicked.connect(self.load_views)

        self.pushButton_2.clicked.connect(self.add_url)

        self.listWidget_2.itemDoubleClicked.connect(self.select_url)

        self.pushButton_3.hide()
        self.pushButton_3.clicked.connect(self.remove_url)
        self.tabWidget.tabCloseRequested.connect(lambda index: self.tabWidget.removeTab(index))

        self.checkBox.setChecked(self.removeTabsOnSave)
        self.checkBox.stateChanged.connect(self.changed_remove_tabs_on_save)

        self.populate_urls()
        self.show()

    def changed_remove_tabs_on_save(self, v):
        self.removeTabsOnSave = v

    def remove_all_tabs(self):
        self.tabWidget.clear()
        

    def populate_urls(self):
        for url in config["urls"]:
            self.listWidget_2.addItem(url)
        

    def select_url(self):
        self.urlSelected = self.listWidget_2.currentItem().text()
        self.pushButton_3.show()

    def remove_url(self):
        del config["urls"][self.listWidget_2.currentRow()]
        mw.addonManager.writeConfig(__name__, config)
        self.listWidget_2.takeItem(self.listWidget_2.currentRow())
        self.pushButton_3.hide()
        self.urlSelected = ""

    def add_url(self):
        self.listWidget_2.addItem(self.lineEdit_2.text())
        config["urls"].append(self.lineEdit_2.text())
        mw.addonManager.writeConfig(__name__, config)
        self.lineEdit_2.setText("")

    # create a foreach in the listWidget_2 items
    def load_views(self):
        if self.removeTabsOnSave:
            self.remove_all_tabs()

        textValue = self.lineEdit.text()
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)

        for i in range(self.listWidget_2.count()):
            value = self.listWidget_2.item(i)

            url = value.text()
            finalUrl = url.replace("{{word}}", textValue)
            tabName = finalUrl[:10]+"..."

            webView = QWebEngineView()
            webView.setSizePolicy(sizePolicy)
            webView.load(QUrl(finalUrl))

            tabWebView = QtWidgets.QWidget()
            tabWebView.setObjectName(finalUrl)
            hboxWebView = QtWidgets.QHBoxLayout(tabWebView)
            hboxWebView.addWidget(webView)
            self.tabWidget.addTab(tabWebView, tabName)

    def closeWithCallback(self, callback):
        callback()

def qSearchLauncher():
    QSearchDialog(mw).show()


a = QAction("Language Search", mw)
a.triggered.connect(qSearchLauncher)
mw.form.menuTools.addAction(a)
