
# coding:utf-8
import sys
import json
import numpy as np

from PySide6.QtCore import Qt, QMetaObject, QCoreApplication
from PySide6.QtWidgets import QHBoxLayout, QVBoxLayout, QSizePolicy, QWidget
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar, PushButton, FluentIcon, InfoBarPosition

import matplotlib

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

flag_now = 0

class drawPainting_show(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.stateTooltip = None

        self.PushButton.clicked.connect(self.on_pushButton_clicked)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1101, 425)
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.PushButton = PushButton('开始', self)
        self.PushButton.setObjectName(u"PushButton")

        self.verticalLayout.addWidget(self.PushButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.mpl1 = MyMplCanvas_2d(self, width=8, height=7, dpi=100)       
        # self.mpl_ntb1 = NavigationToolbar(self.mpl1, self)  # 添加完整的 toolbar
        self.horizontalLayout.addWidget(self.mpl1)
        # self.horizontalLayout.addWidget(self.mpl_ntb1)

        self.mpl2 = MyMplCanvas_2d(self, width=8, height=7, dpi=100)  
        self.horizontalLayout.addWidget(self.mpl2)

        self.mpl3 = MyMplCanvas_2d(self, width=8, height=7, dpi=100)  
        self.horizontalLayout.addWidget(self.mpl3)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi


    def on_pushButton_clicked(self):
        global flag_now, target_lst, flag_num, target_m0, locate_data
        with open(r"./target_m0.json", "r", encoding="utf-8") as m0:
            target_m0 = json.load(m0)

        # 加载位置信息
        with open(r"./locate_data.json", "r", encoding="utf-8") as m0:
            locate_data = json.load(m0)

        # 遍历每一个目标
        target_lst = []
        for tt in target_m0:
            target_lst.append(tt)
        # print("共", len(target_lst), "个目标")
        # print(target_lst)

        flag_num = len(target_lst)

        aaa = self.mpl1.update_figure('1')
        aaa = self.mpl2.update_figure('2')
        aaa = self.mpl3.update_figure('3')

        aaaa = "现在是："+ str(aaa) + '号目标'

        self.createCustomInfoBar(aaaa)
        flag_now += 1
        if flag_now >= flag_num:
            flag_now = 0
    
    def createCustomInfoBar(self,content_aaaa):
        w = InfoBar.new(
            icon=FluentIcon.CARE_RIGHT_SOLID,
            title='目标索引',
            content=content_aaaa,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,
            parent=self
        )
        w.setCustomBackgroundColor('white', '#202020')


class MyMplCanvas_2d(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(111)  # 建立一个子图，如果要建立复合图，可以在这里修改
        # self.fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def draw_pic_2d(self, x_value, y_value, color_c, ss, x_label='', y_label='',
                    title='', t0=0):
        self.axes.clear()
        plt.clf()
        self.axes.set_ylabel(y_label)
        self.axes.set_xlabel(x_label)
        self.fig.suptitle(title)
        self.axes.scatter(x_value,
                        y_value, 
                        color=color_c, 
                        s=ss,)
        self.axes.set_xlim(t0 + 5, max(x_value))
        self.axes.set_ylim(min(y_value[int(t0) + 5:]), max(y_value))
        self.draw() 

    def draw_add_range(self, x_value, y_value, color_c, ss, name):

        from .folder_Interface import res_data
        from .radar_Setting import platform_data
        now_t = 0
        fs = platform_data["fs"]
        y_lst = []
        DuringTime_lst = res_data[name]["DuringTime"]
        for num_d in range(len(DuringTime_lst)):
            frame = int(DuringTime_lst[num_d] * fs / 20)

            linear_model=np.polyfit(x_value[now_t:now_t+frame], y_value[now_t:now_t+frame], 4)
            linear_model_fn=np.poly1d(linear_model)

            for m in linear_model_fn(x_value[now_t:now_t + frame]):
                y_lst.append(m)
            now_t += frame

        self.axes.plot(x_value,
                       y_lst,
                       color=color_c,
                       linewidth=ss, )
        self.draw()


    def update_figure(self, i_name):
        global flag_num, target_m0, locate_data, flag_now
        name = target_lst[flag_now]
        t = target_m0[name]["t"]
        m0 = target_m0[name]["m0"]
        p_deltax = locate_data[name]["0_num_radar"]["p_deltax"]
        p_deltay = locate_data[name]["0_num_radar"]["p_deltay"]
        p_deltaz = locate_data[name]["0_num_radar"]["p_deltaz"]
        if i_name == '1':
            self.draw_pic_2d(t, p_deltax, x_label="t(s)", y_label="x(m)", t0=m0, 
                    title="x轴模拟误差", color_c='green', ss=0.05)
        elif i_name == '2':
            self.draw_pic_2d(t, p_deltay, x_label="t(s)", y_label="y(m)", t0=m0, 
                    title="y轴模拟误差", color_c='green', ss=0.05)
        else:
            self.draw_pic_2d(t, p_deltaz, x_label="t(s)", y_label="z(m)", t0=m0, 
                    title="z轴模拟误差", color_c='green', ss=0.05)

        deltax_max_show, deltax_min_show, deltay_max_show, deltay_min_show, deltaz_max_show, deltaz_min_show ,tt= [[] for x in range(7)]

        for i in range(1,len(p_deltax),20):
            if abs(p_deltax[i])+abs(p_deltay[i])+abs(p_deltaz[i]) >10:
                x_sort = p_deltax[i-1:i+20].copy()
                x_sort.sort()
                y_sort = p_deltay[i-1:i+20].copy()
                y_sort.sort()
                z_sort = p_deltaz[i-1:i+20].copy()
                z_sort.sort()
                # max_parament = 0.93
                # min_parament = 1.07
                max_parament = 0.97
                deltax_max_show.append(x_sort[-1]*max_parament)
                # deltax_min_show.append(x_sort[3]*min_parament)
                deltay_max_show.append(y_sort[-1]*max_parament)
                # deltay_min_show.append(y_sort[3]*min_parament)
                deltaz_max_show.append(z_sort[-1]*max_parament)
                # deltaz_min_show.append(z_sort[3]*min_parament)
                tt.append(t[i])

        line_ss = 1.3
        if i_name == '1':
            self.draw_add_range(tt, deltax_max_show, color_c='orange', ss=line_ss, name=name)
            # self.draw_add_range(tt, deltax_min_show, color_c='orange', ss=line_ss)
        elif i_name == '2':
            self.draw_add_range(tt, deltay_max_show, color_c='orange', ss=line_ss, name=name)
            # self.draw_add_range(tt, deltay_min_show, color_c='orange', ss=line_ss)
        else:
            self.draw_add_range(tt, deltaz_max_show, color_c='orange', ss=line_ss, name=name)
            # self.draw_add_range(tt, deltaz_min_show,color_c='orange', ss=line_ss)

        return name
                    
