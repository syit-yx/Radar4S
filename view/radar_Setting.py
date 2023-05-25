from PySide6.QtCore import QCoreApplication, QMetaObject, QRect,QSize, Qt
from PySide6.QtGui import QCursor,QFont
from PySide6.QtWidgets import (QFrame, QGridLayout, QLabel,
                               QLineEdit, QSizePolicy, QTreeWidgetItem, QWidget)

from qfluentwidgets import (LineEdit, PrimaryPushButton, ProgressBar, PushButton,
                            SpinBox, TreeWidget)

import json

flag_tree_2 = 1
list_number_delete = []



class radarSetting_show(QFrame):
    def __init__(self):
        super().__init__()
        global radar_data, platform_data
        radar_data = json.loads(json.dumps({}))
        platform_data = json.loads(json.dumps({}))

        self.setupUi(self)

        self.PushButton_add.clicked.connect(self.Add_parameter_radar)
        self.PrimaryPushButton_save.clicked.connect(self.Add_parameter_platform)
        self.PrimaryPushButton_delete.clicked.connect(self.Delete_parameter)

    def Add_parameter_radar(self): # 读入雷达初始状态信息
            global flag_tree_2
            
            # 1 读数据
            if list_number_delete == []:
                number_n = flag_tree_2
                flag_tree_2 += 1
            else:
                number_n = list_number_delete[0]
                list_number_delete.remove(number_n)

            radar_pos = self.LineEdit_p_p0.text()

            dit = {
                "pos": [int(x) for x in radar_pos[1:-1].split(",")]
            }
            
            radar_data.update({number_n: dit})
            print("radar_data:", radar_data)

            # 2 写数据到表格

            __qtreewidgetitem = QTreeWidgetItem(self.TreeWidget)
            __qtreewidgetitem.setText(0, str(number_n) + "号雷达")
            font3 = QFont()
            font3.setFamilies([u"Microsoft YaHei UI Light"])
            __qtreewidgetitem.setFont(0, font3)
            __qtreewidgetitem.setText(1, '位置为' + str(radar_pos))
            __qtreewidgetitem.setFont(1, font3)

    def Add_parameter_platform(self): # 读入运动状态信息
        # 1 读数据
        number_n = "Platform"

        dit = {"T": self.SpinBox_T.value(),
               "SNR": eval(self.LineEdit_SNR.text()),
               "fs": self.SpinBox_fs.value(),
               "res_v": self.SpinBox_res_v.value(),
               "rate_r": self.SpinBox_rate_r.value(),
               "theta_width": self.SpinBox_theta_width.value(),
               "phi_width": self.SpinBox_phi_width.value()
                }
        
        # platform_data.update({number_n: dit})
        platform_data.update(dit)
        print("platform_data:", platform_data)



    def Delete_parameter(self): # 删除运动状态信息
        global flag_tree_2
        number_n = self.TreeWidget.currentItem()
        temp = ''.join([x for x in number_n.text(0) if x.isdigit()])

        __qtreewidgetitemName = QTreeWidgetItem(number_n)    
        __qtreewidgetitemName.removeChild(number_n)  # 删除子节点显示
        list_number_delete.append(int(temp)) # 添加到删除列表
        number_n = ''.join([x for x in number_n.text(0) if x.isdigit()]) # 获得节点的索引(字符串取数字)

        del radar_data[int(number_n)] 

        print("radar_data:", radar_data)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form1")
        Form.resize(811, 797)
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        Form.setFont(font)
        Form.setAutoFillBackground(False)
        self.layoutWidget = QWidget(Form)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 40, 612, 605))
        self.gridLayout = QGridLayout(self.layoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.SpinBox_phi_width = SpinBox(self.layoutWidget)
        self.SpinBox_phi_width.setObjectName(u"SpinBox_phi_width")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SpinBox_phi_width.sizePolicy().hasHeightForWidth())
        self.SpinBox_phi_width.setSizePolicy(sizePolicy)
        self.SpinBox_phi_width.setMinimumSize(QSize(120, 33))
        self.SpinBox_phi_width.setMaximum(99999)
        self.SpinBox_phi_width.setSingleStep(1)
        self.SpinBox_phi_width.setValue(5)

        self.gridLayout.addWidget(self.SpinBox_phi_width, 4, 3, 1, 2)

        self.ProgressBar_4 = ProgressBar(self.layoutWidget)
        self.ProgressBar_4.setObjectName(u"ProgressBar_4")

        self.gridLayout.addWidget(self.ProgressBar_4, 13, 0, 1, 5)

        self.label_12 = QLabel(self.layoutWidget)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(150, 0))
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 3, 2, 1, 1)

        self.label_10 = QLabel(self.layoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(150, 0))
        self.label_10.setFont(font)

        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 1)

        self.label_2 = QLabel(self.layoutWidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 6, 2, 1, 2)

        self.SpinBox_fs = SpinBox(self.layoutWidget)
        self.SpinBox_fs.setObjectName(u"SpinBox_fs")
        sizePolicy.setHeightForWidth(self.SpinBox_fs.sizePolicy().hasHeightForWidth())
        self.SpinBox_fs.setSizePolicy(sizePolicy)
        self.SpinBox_fs.setMinimumSize(QSize(120, 33))
        self.SpinBox_fs.setMaximum(99999)
        self.SpinBox_fs.setSingleStep(1)
        self.SpinBox_fs.setValue(10)

        self.gridLayout.addWidget(self.SpinBox_fs, 2, 3, 1, 2)

        self.PushButton_add = PushButton(self.layoutWidget)
        self.PushButton_add.setObjectName(u"PushButton_add")
        self.PushButton_add.setMinimumSize(QSize(120, 0))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setBold(False)
        font1.setItalic(False)
        self.PushButton_add.setFont(font1)

        self.gridLayout.addWidget(self.PushButton_add, 7, 4, 1, 1)

        self.label = QLabel(self.layoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(290, 33))
        font2 = QFont()
        font2.setFamilies([u"Microsoft YaHei UI"])
        font2.setPointSize(12)
        font2.setBold(True)
        self.label.setFont(font2)

        self.gridLayout.addWidget(self.label, 6, 0, 1, 2)

        self.LineEdit_SNR = LineEdit(self.layoutWidget)
        self.LineEdit_SNR.setObjectName(u"LineEdit_SNR")
        self.LineEdit_SNR.setMinimumSize(QSize(120, 33))
        self.LineEdit_SNR.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.LineEdit_SNR, 2, 1, 1, 1)

        self.SpinBox_T = SpinBox(self.layoutWidget)
        self.SpinBox_T.setObjectName(u"SpinBox_T")
        sizePolicy.setHeightForWidth(self.SpinBox_T.sizePolicy().hasHeightForWidth())
        self.SpinBox_T.setSizePolicy(sizePolicy)
        self.SpinBox_T.setMinimumSize(QSize(120, 33))
        self.SpinBox_T.setMaximum(999999)
        self.SpinBox_T.setSingleStep(1)
        self.SpinBox_T.setValue(600)

        self.gridLayout.addWidget(self.SpinBox_T, 1, 3, 1, 2)

        self.label_6 = QLabel(self.layoutWidget)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(150, 0))
        self.label_6.setFont(font)

        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)

        self.SpinBox_theta_width = SpinBox(self.layoutWidget)
        self.SpinBox_theta_width.setObjectName(u"SpinBox_theta_width")
        sizePolicy.setHeightForWidth(self.SpinBox_theta_width.sizePolicy().hasHeightForWidth())
        self.SpinBox_theta_width.setSizePolicy(sizePolicy)
        self.SpinBox_theta_width.setMinimumSize(QSize(120, 33))
        self.SpinBox_theta_width.setMaximum(999999)
        self.SpinBox_theta_width.setValue(5)

        self.gridLayout.addWidget(self.SpinBox_theta_width, 4, 1, 1, 1)

        self.SpinBox_res_v = SpinBox(self.layoutWidget)
        self.SpinBox_res_v.setObjectName(u"SpinBox_res_v")
        sizePolicy.setHeightForWidth(self.SpinBox_res_v.sizePolicy().hasHeightForWidth())
        self.SpinBox_res_v.setSizePolicy(sizePolicy)
        self.SpinBox_res_v.setMinimumSize(QSize(120, 33))
        self.SpinBox_res_v.setMaximum(999999)
        self.SpinBox_res_v.setValue(100)

        self.gridLayout.addWidget(self.SpinBox_res_v, 3, 1, 1, 1)

        self.LineEdit_p_p0 = LineEdit(self.layoutWidget)
        self.LineEdit_p_p0.setObjectName(u"LineEdit_p_p0")
        self.LineEdit_p_p0.setMinimumSize(QSize(120, 33))
        self.LineEdit_p_p0.setLayoutDirection(Qt.LeftToRight)
        self.LineEdit_p_p0.setEchoMode(QLineEdit.Normal)
        self.LineEdit_p_p0.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.LineEdit_p_p0, 6, 4, 1, 1)

        self.SpinBox_rate_r = SpinBox(self.layoutWidget)
        self.SpinBox_rate_r.setObjectName(u"SpinBox_rate_r")
        sizePolicy.setHeightForWidth(self.SpinBox_rate_r.sizePolicy().hasHeightForWidth())
        self.SpinBox_rate_r.setSizePolicy(sizePolicy)
        self.SpinBox_rate_r.setMinimumSize(QSize(120, 33))
        self.SpinBox_rate_r.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.SpinBox_rate_r.setMaximum(99999)
        self.SpinBox_rate_r.setSingleStep(1)
        self.SpinBox_rate_r.setValue(100)

        self.gridLayout.addWidget(self.SpinBox_rate_r, 3, 3, 1, 2)

        self.label_7 = QLabel(self.layoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(150, 0))
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.TreeWidget = TreeWidget(self.layoutWidget)
        self.TreeWidget.setObjectName(u"TreeWidget")
        self.TreeWidget.setMinimumSize(QSize(0, 300))
        self.TreeWidget.setMaximumSize(QSize(16777215, 16777214))
        self.TreeWidget.setFont(font1)
        self.TreeWidget.viewport().setProperty("cursor", QCursor(Qt.ArrowCursor))
        self.TreeWidget.setFocusPolicy(Qt.StrongFocus)
        self.TreeWidget.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.TreeWidget.setLayoutDirection(Qt.LeftToRight)
        self.TreeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.TreeWidget.setTextElideMode(Qt.ElideRight)
        self.TreeWidget.header().setCascadingSectionResizes(False)
        self.TreeWidget.header().setMinimumSectionSize(140)
        self.TreeWidget.header().setDefaultSectionSize(140)
        self.TreeWidget.header().setHighlightSections(True)
        self.TreeWidget.header().setProperty("showSortIndicator", False)

        self.gridLayout.addWidget(self.TreeWidget, 7, 0, 6, 4)

        self.label_13 = QLabel(self.layoutWidget)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setMinimumSize(QSize(150, 0))
        self.label_13.setFont(font)

        self.gridLayout.addWidget(self.label_13, 4, 2, 1, 1)

        self.ProgressBar_2 = ProgressBar(self.layoutWidget)
        self.ProgressBar_2.setObjectName(u"ProgressBar_2")

        self.gridLayout.addWidget(self.ProgressBar_2, 5, 0, 1, 5)

        self.ProgressBar = ProgressBar(self.layoutWidget)
        self.ProgressBar.setObjectName(u"ProgressBar")

        self.gridLayout.addWidget(self.ProgressBar, 0, 0, 1, 5)

        self.label_5 = QLabel(self.layoutWidget)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(150, 0))
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)

        self.label_9 = QLabel(self.layoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(150, 0))
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.label_8 = QLabel(self.layoutWidget)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(280, 33))
        self.label_8.setFont(font2)

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 2)

        self.PrimaryPushButton_delete = PrimaryPushButton(self.layoutWidget)
        self.PrimaryPushButton_delete.setObjectName(u"PrimaryPushButton_delete")
        self.PrimaryPushButton_delete.setMinimumSize(QSize(120, 0))

        self.gridLayout.addWidget(self.PrimaryPushButton_delete, 8, 4, 1, 1)

        self.PrimaryPushButton_save = PrimaryPushButton(self.layoutWidget)
        self.PrimaryPushButton_save.setObjectName(u"PrimaryPushButton_save")
        self.PrimaryPushButton_save.setMinimumSize(QSize(120, 0))

        self.gridLayout.addWidget(self.PrimaryPushButton_save, 12, 4, 1, 1)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
        
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form1", u"Form1", None))
        self.label_12.setText(QCoreApplication.translate("Form", u"\u8ddd\u79bb\u5206\u8fa8\u7387", None))
        self.label_10.setText(QCoreApplication.translate("Form", u"\u603b\u65f6\u95f4", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"\u4f4d\u7f6e", None))
        self.PushButton_add.setText(QCoreApplication.translate("Form", u"\u6dfb\u52a0", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u96f7\u8fbe\u72b6\u6001\u4fe1\u606f", None))
        self.LineEdit_SNR.setText(QCoreApplication.translate("Form", u"pow(10,1.2)", None))
        self.label_6.setText(QCoreApplication.translate("Form", u"\u65b9\u4f4d\u6ce2\u675f\u5bbd\u5ea6\uff08/180*\u03c0\uff09", None))
        self.LineEdit_p_p0.setText(QCoreApplication.translate("Form", u"[0,0,0]", None))
        self.label_7.setText(QCoreApplication.translate("Form", u"\u6700\u5c0f\u4fe1\u566a\u6bd4", None))
        ___qtreewidgetitem = self.TreeWidget.headerItem()
        ___qtreewidgetitem.setText(1, QCoreApplication.translate("Form", u"\u4f4d\u7f6e", None));
        ___qtreewidgetitem.setText(0, QCoreApplication.translate("Form", u"\u7f16\u53f7", None));
        self.label_13.setText(QCoreApplication.translate("Form", u"\u4fef\u4ef0\u6ce2\u675f\u5bbd\u5ea6\uff08/180*\u03c0\uff09", None))
        self.label_5.setText(QCoreApplication.translate("Form", u"\u901f\u5ea6\u5206\u8fa8\u7387", None))
        self.label_9.setText(QCoreApplication.translate("Form", u"\u6570\u636e\u7387", None))
        self.label_8.setText(QCoreApplication.translate("Form", u"\u7cfb\u7edf\u72b6\u6001\u4fe1\u606f", None))
        self.PrimaryPushButton_delete.setText(QCoreApplication.translate("Form", u"\u5220\u9664", None))
        self.PrimaryPushButton_save.setText(QCoreApplication.translate("Form", u"\u4fdd\u5b58\u53c2\u6570", None))
    # retranslateUi