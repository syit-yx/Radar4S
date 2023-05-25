# coding:utf-8
import sys
import json

from PySide6.QtWidgets import QVBoxLayout, QSizePolicy, QWidget
from qfluentwidgets import MessageBox, StateToolTip, PushButton

import numpy as np
from app_code.app_code import Target, Radar, Platform

import matplotlib

matplotlib.use("Qt5Agg")
from PySide6 import QtCore

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


# with open(r"./locate_data.json", "r") as f:
#     locate_data = json.load(f)


class parameterSetting_show(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUi()

    def initUi(self):
        self.stateTooltip = None
        
        self.layout = QVBoxLayout(self)
        # self.layout2 = QHBoxLayout(self)

        self.mpl = MyMplCanvas(self, width=8, height=7, dpi=100)
        # self.mpl.start_dynamic_plot() # 如果你想要初始化的时候呈现动态图，请把这行注释去掉
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar

        self.button1 = PushButton('开始', self)
        self.button2 = PushButton('停止', self)

        # self.layout2.addWidget(self.button1)
        # self.layout2.addWidget(self.button2)
        # self.layout.addWidget(self.layout2)

        self.layout.addWidget(self.button1)
        self.layout.addWidget(self.button2)
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)
        
        
        self.button2.clicked.connect(self.off_pushButton_clicked)
    
        self.button1.clicked.connect(self.showMessageDialog)
        # self.button1.clicked.connect(self.on_pushButton_clicked)

    def showMessageDialog(self):
        from .folder_Interface import res_data
        from .radar_Setting import radar_data
        title = self.tr('参数确认')
        # content = self.tr(
        #     "将以如下参数进行仿真\n"+
        #     "      雷达个数："+
        #     str(len(locate_data["radar"]))+"\n"+
        #     "      目标个数："+
        #     str(len(locate_data["target"])))
        alltime = 0
        for rd in res_data:
            for rdd in res_data[rd]["DuringTime"]:
                alltime += rdd
        pretime = len(radar_data) * alltime/150
        content = self.tr(
            "将以如下参数进行仿真\n" +
            "   雷达个数: " +
            str(len(radar_data))+"\n" +
            "   目标个数: " +
            str(len(res_data)) + "\n" + "   预计用时约: " + str(round(pretime * (1 - 0.25 * np.random.random()), 2)) + " - " + str(round(pretime * (1 + 0.25 * np.random.random()), 2)) + "  秒"
        )
        w = MessageBox(title, content, self.window())
        if w.exec():
            print('Yes button is pressed')
            # 进度弹窗
            self.on_pushButton_clicked()
        else:
            print('Cancel button is pressed')

    def on_pushButton_clicked(self):
        from .folder_Interface import res_data
        from .radar_Setting import platform_data, radar_data
        print("on_pushButton_clicked 仿真已开始")
        print("共", len(res_data), "个目标")
        for rd in res_data:
            print(rd, "号:", res_data[rd])
        # print(res_data)
        Target_lst = []
        for target in res_data:
            range_r = res_data[target]["range"]
            theta = res_data[target]["azimuth"]
            phi = res_data[target]["obliquity"]
            number_n = target
            attribute = res_data[target]["attribute"]
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
                         motion_model=res_data[target]["MovementMode"],
                         acc=0,
                         t0=res_data[target]["StartTime"],
                         MovementMode=res_data[target]["MovementMode"],
                         parament=res_data[target]["parament"],
                         DuringTime=DuringTime_all,
                         attribute=attribute
            )
            Target_lst.append(t_t)

        Radar_lst = []
        for radar in radar_data:
            pos = radar_data[radar]["pos"]
            r_r = Radar(pos=np.array(pos).T, vel=np.array([0, 0, 0]).T)
            Radar_lst.append(r_r)

        p_0 = Platform(time_t=platform_data["T"],
                       fs=platform_data["fs"],
                       SNRO=platform_data["SNR"],
                       res_r=platform_data["rate_r"],
                       res_v=platform_data["res_v"],
                       theta_width=platform_data["theta_width"],
                       phi_width=platform_data["phi_width"]
                       )
        
        self.onStateButtonClicked()
        p_0.run_1(Target_lst, Radar_lst)
        self.onStateButtonClicked()       
        self.mpl.start_dynamic_plot() # 如果你想要初始化的时候呈现动态图，请把这行注释去掉

        pass

    def off_pushButton_clicked(self):
        global timer
        print("off_pushButton_clicked! 已停止")
        timer.stop()

    def onStateButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent(
                self.tr('模型仿真完成啦!  ') + ' 😆')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip(
                self.tr('正在仿真模型'), self.tr('心机吃不了热豆腐，请耐心等待哦~'), self.window())
            self.stateTooltip.move(self.stateTooltip.getSuitablePos())
            self.stateTooltip.show()

flag_loop = 0

class MyMplCanvas(FigureCanvas):
    """FigureCanvas的最终的父类其实是QWidget。"""

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 新建一个figure
        self.axes = self.fig.add_subplot(111, projection='3d')  # 建立一个子图，如果要建立复合图，可以在这里修改
        self.fig.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)

        # 3.0版本之后已经被移除，用self.axes.clear()替代，见下文。
        # self.axes.hold(False)  # 每次绘图的时候不保留上一次绘图的结果

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        '''定义FigureCanvas的尺寸策略，这部分的意思是设置FigureCanvas，使之尽可能的向外填充空间。'''
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def update_figure(self):
        global flag_loop
        from .folder_Interface import res_data
        # print("res_data:", res_data)
        with open(r"./locate_data.json", "r") as f:
            locate_data = json.load(f)
        # fs = platform_data['fs']
        fs = 10
        flag_loop += 3*fs

        for target in locate_data:
            if locate_data[target]["0_num_radar"]["p_sx"][flag_loop] != 0 and locate_data[target]["0_num_radar"]['p_sx'][flag_loop+fs] !=0 and locate_data[target]["0_num_radar"]['p_sx'][flag_loop+2*fs] !=0:
                if res_data[target]["attribute"] == 0:
                    cc = 'b'
                else:
                    cc = 'r'
                self.axes.scatter(
                    [locate_data[target]["0_num_radar"]['p_sx'][flag_loop],
                      locate_data[target]["0_num_radar"]['p_sx'][flag_loop+fs],
                        locate_data[target]["0_num_radar"]['p_sx'][flag_loop+2*fs]],
                    [locate_data[target]["0_num_radar"]['p_sy'][flag_loop],
                      locate_data[target]["0_num_radar"]['p_sy'][flag_loop+fs],
                        locate_data[target]["0_num_radar"]['p_sy'][flag_loop+2*fs]],
                    [locate_data[target]["0_num_radar"]['p_sz'][flag_loop],
                      locate_data[target]["0_num_radar"]['p_sz'][flag_loop+fs],
                        locate_data[target]["0_num_radar"]['p_sz'][flag_loop+2*fs]],
                    c=cc,
                    s=2,
                    alpha=1,
                    marker='*'
                    )
                self.axes.scatter(
                    [locate_data[target]["0_num_radar"]['data_measure_cartesian_x'][flag_loop],
                     locate_data[target]["0_num_radar"]['data_measure_cartesian_x'][flag_loop + fs],
                     locate_data[target]["0_num_radar"]['data_measure_cartesian_x'][flag_loop + 2 * fs]],
                    [locate_data[target]["0_num_radar"]['data_measure_cartesian_y'][flag_loop],
                     locate_data[target]["0_num_radar"]['data_measure_cartesian_y'][flag_loop + fs],
                     locate_data[target]["0_num_radar"]['data_measure_cartesian_y'][flag_loop + 2 * fs]],
                    [locate_data[target]["0_num_radar"]['data_measure_cartesian_z'][flag_loop],
                     locate_data[target]["0_num_radar"]['data_measure_cartesian_z'][flag_loop + fs],
                     locate_data[target]["0_num_radar"]['data_measure_cartesian_z'][flag_loop + 2 * fs]],
                    c=cc,
                    s=2,
                    alpha=0.4,
                    marker='*'
                )


        self.axes.grid(False)
        self.draw()


    '''启动绘制动态图'''
    def start_dynamic_plot(self, *args, **kwargs):
        global flag_loop ,timer
        flag_loop = 1

        self.axes.cla() 
        self.axes.set_ylabel('动态图：Y轴')
        self.axes.set_xlabel('动态图：X轴')
        self.fig.suptitle('测试动态图')

        timer = QtCore.QTimer(self)
        timer.start(10)  # 触发的时间间隔为0.1秒。
        timer.timeout.connect(self.update_figure)  # 每隔一段时间就会触发一次update_figure函数。








