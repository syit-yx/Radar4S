# coding:utf-8
import sys

from PySide6.QtCore import Qt, QRect
from PySide6.QtGui import QIcon, QPainter, QImage, QBrush, QColor, QFont
from PySide6.QtWidgets import QApplication, QFrame, QStackedWidget, QHBoxLayout, QLabel

from qfluentwidgets import (NavigationInterface, NavigationItemPosition, NavigationWidget, MessageBox,
                            isDarkTheme)
from qfluentwidgets import FluentIcon as FIF
from qframelesswindow import FramelessWindow, StandardTitleBar

import numpy as np

from view.parameter_setting import parameterSetting_show
# from view.folder_Interface import folderInterface_show, res_data
from view.folder_Interface import folderInterface_show
from view.radar_Setting import radarSetting_show
from view.delta_Painting import drawPainting_show
from app_code.app_code import Target, Radar, Platform

from resource.qss import lightqss



class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__()
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Widget2(QFrame):

    def __init__(self: str, parent=None):
        super().__init__()
        self.hBoxLayout = QHBoxLayout(self)


class AvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.avatar = QImage('resource/kunkun.png').scaled(
            24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            font = QFont('Segoe UI')
            font.setPixelSize(14)
            painter.setFont(font)
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, '团队展示')


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))

        # change the theme color
        # setThemeColor('#0078d4')

        self.hBoxLayout = QHBoxLayout(self)
        self.navigationInterface = NavigationInterface(self, showMenuButton=True)
        self.stackWidget = QStackedWidget(self)

        # create sub interface
        self.searchInterface = parameterSetting_show()
        self.musicInterface = Widget('雷达点迹态势模拟系统', self)
        self.videoInterface = radarSetting_show()
        self.folderInterface = folderInterface_show()
        self.settingInterface = drawPainting_show()
        # self.settingInterface = Widget('33333', self)

        # initialize layout
        self.initLayout()

        # add items to navigation interface
        self.initNavigation()

        self.initWindow()

    def initLayout(self):
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.hBoxLayout.addWidget(self.navigationInterface)
        self.hBoxLayout.addWidget(self.stackWidget)
        self.hBoxLayout.setStretchFactor(self.stackWidget, 1)

    def initNavigation(self):
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.folderInterface, FIF.FOLDER_ADD, '目标参数设置')
        self.addSubInterface(self.videoInterface, FIF.SETTING, '雷达参数设置')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.searchInterface, FIF.VIEW, '结果展示')
        self.navigationInterface.addSeparator()
        self.addSubInterface(self.musicInterface, FIF.HOME, '开始界面')
        # self.navigationInterface.addSeparator()

        # add navigation items to scroll area
        # self.addSubInterface(self.folderInterface, FIF.FOLDER, 'Folder library', NavigationItemPosition.SCROLL)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=AvatarWidget(),
            onClick=self.showMessageBox,
            position=NavigationItemPosition.BOTTOM
        )

        self.addSubInterface(self.settingInterface, FIF.ZOOM_IN, '精度分析', NavigationItemPosition.BOTTOM)

        # !IMPORTANT: don't forget to set the default route key if you enable the return button
        # self.navigationInterface.setDefaultRouteKey(self.musicInterface.objectName())

        # set the maximum width
        # self.navigationInterface.setExpandWidth(300)

        self.stackWidget.currentChanged.connect(self.onCurrentInterfaceChanged)
        self.stackWidget.setCurrentIndex(3)

    def initWindow(self):
        self.resize(1000, 700)
        self.setWindowIcon(QIcon('resource/logo.png'))
        self.setWindowTitle('雷达点迹模拟系统')
        self.titleBar.setAttribute(Qt.WA_StyledBackground)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.setQss()

    def addSubInterface(self, interface, icon, text: str, position=NavigationItemPosition.TOP):
        """ add sub interface """
        self.stackWidget.addWidget(interface)
        self.navigationInterface.addItem(
            routeKey=interface.objectName(),
            icon=icon,
            text=text,
            onClick=lambda: self.switchTo(interface),
            position=position,
            tooltip=text
        )

    def setQss(self):
        color = 'dark' if isDarkTheme() else 'light'
        self.setStyleSheet(lightqss)
        # with open(f'resource/{color}/demo.qss', encoding='utf-8') as f:
        #     self.setStyleSheet(f.read())

    def switchTo(self, widget):
        self.stackWidget.setCurrentWidget(widget)

    def onCurrentInterfaceChanged(self, index):
        widget = self.stackWidget.widget(index)
        self.navigationInterface.setCurrentItem(widget.objectName())

    def showMessageBox(self):
        w = MessageBox(
            '项目介绍',
            '项目编号: S202210701413\n项目名称: 雷达目标点迹态势模拟及其Python实现\n项目成员: 王柯睿 赵云霄 孙佳楠指导教师: 许京伟',
            self
        )
        w.exec()

    def simulation(self):
        # '''
        # 1 写参数到excel
        T = 60 * 10  # 总时间
        fs = 10  # 数据率
        SNR = pow(10, 12 / 10)  # 最小可检测信噪比
        res_v = 100  # 速度分辨率
        rate_r = 100
        theta_width = 5 / 180 * np.pi  # 方位波束宽度
        phi_width = 5 / 180 * np.pi  # 俯仰波束宽度
        p_p0 = [0, 0, 0]  # 平台位置矢量
        v_p0 = [0, 0, 0]  # 平台速度矢量
        p_s0 = [50e3, 50e3, 8e3]  # 目标位置矢量
        v_s0 = [-100, 0, 0]  # 目标速度矢量
        a_s0 = 5  # 目标加速度误差标准差
        t0 = 10  # 目标出现的时刻 (s)
        motion_model_a = 'Singer'

        # 2读出参数到app

        # t_0 = Target(pos = p_s0, vel = v_s0,
        #     posture = np.array([0,0,0]).T, motion_model = motion_model_a,acc = a_s0, t0 = t0)
        # r_0 = Radar(pos = p_p0, vel = v_p0)
        # p_0 = Platform(time = T, fs = fs, SNRO = SNR, res_r = rate_r,
        #     res_v = res_v ,theta_width = theta_width, phi_width = phi_width)
        # p_0.run_1(t_0, r_0)
        Target_lst = []
        for target in res_data:
            range_r = res_data[target]["range"]
            theta = res_data[target]["azimuth"]
            phi = res_data[target]["obliquity"]
            number_n = target
            x, y, z = round(range_r * np.cos(theta) * np.sin(phi)), round(range_r * np.sin(theta) * np.sin(phi)), round(
                range_r * np.cos(phi))

            DuringTime_all = []
            ssum = 0
            for tttime in res_data[target]["DuringTime"]:
                ssum += tttime
                DuringTime_all.append(ssum)
            # print(DuringTime_all)
            t_t = Target(num=number_n,
                         pos=[x, y, z],
                         vel=res_data[target]["speed"],
                         posture=np.array([0, 0, 0]).T,
                         acc=0,
                         t0=res_data[target]["StartTime"],
                         MovementMode=res_data[target]["MovementMode"],
                         parament=res_data[target]["parament"],
                         DuringTime=DuringTime_all

            )
            Target_lst.append(t_t)

            

        # t_0 = Target(pos = p_s0, vel = v_s0,
        #     posture = np.array([0 ,0 ,0]).T, motion_model = motion_model_a ,acc = a_s0, t0 = t0)

        r_0 = Radar(pos=p_p0, vel=v_p0)
        p_0 = Platform(time=T, fs=fs, SNRO=SNR, res_r=rate_r,
                       res_v=res_v, theta_width=theta_width, phi_width=phi_width)

        # p_0.run_1(t_0, r_0)
        p_0.run_1(Target_lst, r_0)

        p_0.draw_gif_pic_2d()
        p_0.draw_delta_xyz()
        p_0.draw_gif()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
