import sys
import os
import json

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *


class AddressBar(QLineEdit):
    def __init__(self):
        super().__init__()

    def mousePressEvent(self, e):
        self.selectAll()


class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Zac lit Browser")
        self.setWindowIcon(QIcon("zain.png"))
        self.setBaseSize(1366, 768)
        self.setMinimumSize(1000, 700)
        self.CreateApp()

    def CreateApp(self):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Keep track of tabs
        self.tabcount = 0
        self.tabs = []

        # Create Address bar
        self.Toolbar = QWidget()
        self.Toolbar.setObjectName("Toolbar")
        self.ToolbarLayout = QHBoxLayout()
        self.addressbar = AddressBar()
        self.addressbar.setObjectName("addressbar")

        # New tab button
        # self.tabbar.addTab("New Tab")


        self.AddTabButton = QPushButton(QIcon("add.jpg"), None)
        self.addressbar.returnPressed.connect(self.BrowseTo)
        self.AddTabButton.clicked.connect(self.AddTab)


        # set toolbar buttons
        self.BackButton = QPushButton(QIcon("lefty.png"), None)
        self.BackButton.clicked.connect(self.GoBack)

        self.ForwardButton = QPushButton(QIcon("right.jpg"), None)
        self.ForwardButton.clicked.connect(self.GoForward)

        self.ReloadButton = QPushButton(QIcon("reload.png"), None)
        self.ReloadButton.clicked.connect(self.ReloadPage)

        # Create tabs
        self.tabbar = QTabBar(movable=True, tabsClosable=True)
        self.tabbar.tabCloseRequested.connect(self.CloseTab)
        self.tabbar.tabBarClicked.connect(self.SwitchTab)
        self.tabbar.setCurrentIndex(0)
        self.tabbar.setDrawBase(False)
        self.tabbar.setLayoutDirection(Qt.LeftToRight)
        self.tabbar.setElideMode(Qt.ElideLeft)



        self.shortcutNewTab = QShortcut(QKeySequence("Ctrl+T"), self)
        self.shortcutNewTab.activated.connect(self.AddTab)

        self.shortcutReload = QShortcut(QKeySequence("Ctrl+R"), self)
        self.shortcutReload.activated.connect(self.ReloadPage)

        self.Toolbar.setLayout(self.ToolbarLayout)
        self.ToolbarLayout.addWidget(self.BackButton)
        self.ToolbarLayout.addWidget(self.ForwardButton)
        self.ToolbarLayout.addWidget(self.ReloadButton)
        self.ToolbarLayout.addWidget(self.addressbar)
        self.ToolbarLayout.addWidget(self.AddTabButton)

        # set main view
        self.container = QWidget()
        self.container.layout = QStackedLayout()
        self.container.setLayout(self.container.layout)
        if self.tabcount == 0:
            self.AddTab()

        self.layout.addWidget(self.tabbar)
        self.layout.addWidget(self.Toolbar)
        self.layout.addWidget(self.container)

        self.setLayout(self.layout)
        self.show()

    def CloseTab(self, i):
        self.tabcount -= 1
        self.tabbar.removeTab(i)

    def AddTab(self):
        i = self.tabcount
        self.tabs.append(QWidget())
        self.tabs[i].layout = QVBoxLayout()
        self.tabs[i].layout.setContentsMargins(0, 0, 0, 0)
        self.tabs[i].setObjectName("tab" + str(i))

        # Open web view
        self.tabs[i].content = QWebEngineView()
        self.tabs[i].content.load(QUrl.fromUserInput("https://www.google.com"))

        self.tabs[i].content1 = QWebEngineView()
        self.tabs[i].content1.load(QUrl.fromUserInput("https://www.google.com"))

        # set tab at top of the screen
        self.tabbar.addTab("New Tab")
        self.tabbar.setTabData(i, {"object": "tab" + str(i), "initial": i})

        self.tabs[i].content.titleChanged.connect(lambda: self.SetTabContent(i, "title"))
        self.tabs[i].content.iconChanged.connect(lambda: self.SetTabContent(i, "icon"))
        self.tabs[i].content.urlChanged.connect(lambda: self.SetTabContent(i, "url"))

        # Add Widget to tab layout
        self.tabs[i].splitview = QSplitter()
        # self.tabs[i].splitview.setOrientation(Qt.Vertical)
        self.tabs[i].layout.addWidget(self.tabs[i].splitview)

        self.tabs[i].splitview.addWidget(self.tabs[i].content)
        self.tabs[i].splitview.addWidget(self.tabs[i].content1)

        # set top level tab from [] to layout
        self.tabs[i].setLayout(self.tabs[i].layout)

        # Add Tab to top level stacked widget
        self.container.layout.addWidget(self.tabs[i])
        self.container.layout.setCurrentWidget(self.tabs[i])

        self.tabbar.setCurrentIndex(i)

        self.tabcount += 1

    def SwitchTab(self, i):

        if self.tabbar.tabData(i):
            td = self.tabbar.tabData(i)["object"]
            print(td)
            tc = self.findChild(QWidget, td)
            self.container.layout.setCurrentWidget(tc)
            new_url = tc.content.url().toString()
            self.addressbar.setText(new_url)


    def BrowseTo(self):
        text = self.addressbar.text()
        print(text)
        i = self.tabbar.currentIndex()
        tab = self.tabbar.tabData(i)["object"]
        wv = self.findChild(QWidget, tab).content

        if "http" not in text:
            if "." not in text:
                url = "https://www.google.ca/#q=" + text
            else:
                url = "https://" + text

        else:
            url = text

        wv.load(QUrl.fromUserInput(url))

    def SetTabContent(self, i, type):
        '''
        self.tabs[i].objectName()= tab1
        self.tabbar.tabData(i)["object"]=tab1
        '''

        tab_name = self.tabs[i].objectName()
        count = 0
        running = True
        current_tab = self.tabbar.tabData(self.tabbar.currentIndex())["object"]

        if current_tab == tab_name and type == "url":
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.addressbar.setText(new_url)
            return False
        if current_tab is None:
            new_url = self.findChild(QWidget, tab_name).content.url().toString()
            self.addressbar.setText(new_url)
            return False

        while running:
            tab_data_name = self.tabbar.tabData(count)

            if count >= 99:
                running = False
            if tab_data_name:
                if tab_name == tab_data_name["object"]:
                    if type == "title":
                        newTitle = self.findChild(QWidget, tab_name).content.title()
                        self.tabbar.setTabText(count, newTitle)
                    elif type == "icon":
                        new_icon = self.findChild(QWidget, tab_name).content.icon()
                        self.tabbar.setTabIcon(count, new_icon)
                    running = False
                else:
                    count += 1


    def GoBack(self):
        if self.tabcount == 0:
            return False

        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.back()

    def GoForward(self):
        if self.tabcount == 0:
            return False
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.forward()

    def ReloadPage(self):
        if self.tabcount == 0:
            return False
        activeIndex = self.tabbar.currentIndex()
        tab_name = self.tabbar.tabData(activeIndex)["object"]
        tab_content = self.findChild(QWidget, tab_name).content

        tab_content.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    os.environ['QTWEBENGINE_REMOTE_DEBUGGING'] = "400"
    window = App()

    with open("style.css", "r") as style:
        app.setStyleSheet(style.read())
    sys.exit(app.exec())
