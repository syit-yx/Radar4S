from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, Qt)

from PySide6.QtGui import QCursor, QFont
from PySide6.QtWidgets import (QFrame, QGridLayout,QLabel, QSizePolicy, QTreeWidgetItem, QWidget)

from qfluentwidgets import (ComboBox, PrimaryPushButton, ProgressBar, PushButton,
                            SpinBox, TreeWidget, LineEdit)

import numpy as np
import json

flag_tree = 5
# a = res_data["1"]["attribute"] 取数方法

class folderInterface_show(QFrame):
    def __init__(self):
        super().__init__()
        global res_data
        res_data = json.loads(json.dumps({}))
        print("res_data已创建")

        self.setupUi(self)

        self.PushButton.clicked.connect(self.Add_parameter_1)
        self.PrimaryPushButton.clicked.connect(self.Add_parameter_2)
        self.PrimaryPushButton_2.clicked.connect(self.Delete_parameter)

    def Add_parameter_1(self): # 读入目标属性&初始状态信息
        global flag_tree
        
        # 1 读数据
        number_n = str(self.SpinBox_number.value())
        attribute_n = self.comboBox_attribute.currentText()
        if self.comboBox_attribute.currentText() == '敌方':
            attribute_n = 0
        else:
            attribute_n = 1

        range_r = self.SpinBox_range.value()

        theta = self.SpinBox_azimuth.value() * np.pi / 180
        phi = self.SpinBox_obliquity.value() * np.pi / 180

        dit = {"attribute": attribute_n,
                "StartTime": self.SpinBox_StartTime.value(),
                "speed": self.LineEdit_speed.text(),
                "range": range_r,
                "azimuth": theta,
                "obliquity": phi,
                "MovementMode": [],
                "parament": [],
                "DuringTime": []
                }
        
        res_data.update({number_n: dit})
        print("res_data:", res_data)

        # x = r cosθsinφ    y = r sinθsinφ    z = rcosφ
        x, y, z = round(range_r * np.cos(theta) * np.sin(phi)), round(range_r * np.sin(theta) * np.sin(phi)), round(
            range_r * np.cos(phi))

        # 2 写数据到表格
        flag_tree += 1
        self.SpinBox_number.setValue(1 + flag_tree - 5)
        __qtreewidgetitem = QTreeWidgetItem(self.TreeWidget)
        __qtreewidgetitem.setText(0, number_n + "号目标：" + self.comboBox_attribute.currentText())
        font3 = QFont()
        font3.setFamilies([u"Microsoft YaHei UI Light"])
        __qtreewidgetitem.setFont(0, font3)
        __qtreewidgetitem.setText(1, '' + str(self.SpinBox_StartTime.value()) + 's出现于' + '(' + str(x) + ',' + str(
            y) + ',' + str(z) + ')')
        __qtreewidgetitem.setFont(1, font3)
        __qtreewidgetitem.setText(2, '速度为' + str(self.LineEdit_speed.text()) + 'm/s')
        __qtreewidgetitem.setFont(2, font3)

    def Add_parameter_2(self): # 读入运动状态信息
        # 1 读数据
        number_n = self.TreeWidget.currentItem()
        number_n = ''.join([x for x in number_n.text(0) if x.isdigit()])  # 从一串文字中提取数字
        Move_Mode = self.comboBox_MovementMode.currentText()
        res_data[number_n]["MovementMode"].append(self.comboBox_MovementMode.currentText())
        res_data[number_n]["parament"].append(self.LineEdit_parament.text())
        res_data[number_n]["DuringTime"].append(self.SpinBox_DuringTime.value())
        print("res_data:", res_data)
        # print(res_data)
        # # 2 写数据到表格
        __qtreewidgetitemName = QTreeWidgetItem(self.TreeWidget.currentItem())
        font3 = QFont()
        font3.setFamilies([u"Microsoft YaHei UI Light"])
        __qtreewidgetitemName.setFont(0, font3)
        __qtreewidgetitemName.setText(0, self.comboBox_MovementMode.currentText())
        __qtreewidgetitemName.setText(1, self.SpinBox_DuringTime.text() + 's')
        __qtreewidgetitemName.setFont(1, font3)
        if Move_Mode == '匀速':
            __qtreewidgetitemName.setText(2, self.LineEdit_parament.text() + 'm/s')
        elif Move_Mode == '匀加速':
            __qtreewidgetitemName.setText(2, self.LineEdit_parament.text() + 'm/s²')
        elif Move_Mode == '随机':
            print('随机')
        elif Move_Mode == '静止':
            print('静止')
        __qtreewidgetitemName.setFont(2, font3)

    def Delete_parameter(self): # 删除运动状态信息
        # number_n = self.TreeWidget.currentItem()
        # print(number_n)
        # print(number_n.text(0)) 
        
        number_n = self.TreeWidget.currentItem()
        temp = ''.join([x for x in number_n.text(0) if ~x.isdigit()])
        if '号目标：' in temp:
            __qtreewidgetitemName = QTreeWidgetItem(number_n)    
            __qtreewidgetitemName.removeChild(number_n)  # 删除子节点显示

            number_n = ''.join([x for x in number_n.text(0) if x.isdigit()]) # 获得节点的索引(字符串取数字)
            del res_data[number_n] 
        else:
            number_p = number_n.parent() # 获得父节点 
            number_n_index = number_n.parent().indexOfChild(number_n) # 获得子节点的索引(取其父节点再寻找子节点目录)
            number_p_index =''.join([x for x in number_p.text(0) if x.isdigit()]) # 获得父节点的索引(字符串取数字)
            number_p.removeChild(number_n)  # 删除子节点显示

            del res_data[number_p_index]["MovementMode"][number_n_index] 
            del res_data[number_p_index]["parament"][number_n_index] 
            del res_data[number_p_index]["DuringTime"][number_n_index] 

        print("res_data:", res_data)

    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form2")
        Form.resize(687, 798)
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        Form.setFont(font)
        Form.setAutoFillBackground(False)

        self.widget = QWidget(Form)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(24, 44, 901, 586))
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.ProgressBar = ProgressBar(self.widget)
        self.ProgressBar.setObjectName(u"ProgressBar")
        self.gridLayout.addWidget(self.ProgressBar, 0, 0, 1, 4)


        self.label_8 = QLabel(self.widget) # [文字]目标属性信息
        self.label_8.setObjectName(u"label_8")
        self.label_8.setMinimumSize(QSize(440, 33))
        font1 = QFont()
        font1.setFamilies([u"Microsoft YaHei UI"])
        font1.setPointSize(12)
        font1.setBold(True)
        self.label_8.setFont(font1)

        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 3)

        self.PushButton = PushButton(self.widget) # [按钮]添加基础参数
        self.PushButton.setObjectName(u"PushButton")
        self.PushButton.setMinimumSize(QSize(120, 0))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setBold(False)
        font2.setItalic(False)
        self.PushButton.setFont(font2)

        self.gridLayout.addWidget(self.PushButton, 1, 3, 1, 1)

        self.label_7 = QLabel(self.widget) # [文字]目标编号
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(150, 0))
        self.label_7.setFont(font)

        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)

        self.SpinBox_number = SpinBox(self.widget) # [输入框]目标编号
        self.SpinBox_number.setObjectName(u"SpinBox_number")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.SpinBox_number.sizePolicy().hasHeightForWidth())
        self.SpinBox_number.setSizePolicy(sizePolicy)
        self.SpinBox_number.setMinimumSize(QSize(120, 33))
        self.SpinBox_number.setMaximum(9999)
        self.SpinBox_number.setValue(1)

        self.gridLayout.addWidget(self.SpinBox_number, 2, 1, 1, 1)

        self.label_9 = QLabel(self.widget) # [文字]敌我属性
        self.label_9.setObjectName(u"label_9")
        self.label_9.setMinimumSize(QSize(150, 0))
        self.label_9.setFont(font)

        self.gridLayout.addWidget(self.label_9, 2, 2, 1, 1)

        self.comboBox_attribute = ComboBox(self.widget) # [下拉框]敌我属性
        self.comboBox_attribute.addItem("")
        self.comboBox_attribute.addItem("")
        self.comboBox_attribute.setObjectName(u"comboBox_attribute")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.comboBox_attribute.sizePolicy().hasHeightForWidth())
        self.comboBox_attribute.setSizePolicy(sizePolicy1)
        self.comboBox_attribute.setMinimumSize(QSize(120, 33))

        self.gridLayout.addWidget(self.comboBox_attribute, 2, 3, 1, 1)

        self.ProgressBar_2 = ProgressBar(self.widget) 
        self.ProgressBar_2.setObjectName(u"ProgressBar_2")

        self.gridLayout.addWidget(self.ProgressBar_2, 3, 0, 1, 4)

        self.label = QLabel(self.widget) # [文字]初始状态信息
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(290, 33))
        self.label.setFont(font1)

        self.gridLayout.addWidget(self.label, 4, 0, 1, 2)

        self.label_2 = QLabel(self.widget) # [文字]初始斜距（m)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(150, 0))
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 5, 0, 1, 1)

        self.SpinBox_range = SpinBox(self.widget) # [输入框]初始斜距（m)
        self.SpinBox_range.setObjectName(u"SpinBox_range")
        sizePolicy.setHeightForWidth(
            self.SpinBox_range.sizePolicy().hasHeightForWidth())
        self.SpinBox_range.setSizePolicy(sizePolicy)
        self.SpinBox_range.setMinimumSize(QSize(120, 33))
        self.SpinBox_range.setMaximum(9999999)
        self.SpinBox_range.setValue(71300)

        self.gridLayout.addWidget(self.SpinBox_range, 5, 1, 1, 1)

        self.label_3 = QLabel(self.widget) # [文字]初始方位（°）
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMinimumSize(QSize(150, 0))
        self.label_3.setFont(font)

        self.gridLayout.addWidget(self.label_3, 5, 2, 1, 1)

        self.SpinBox_azimuth = SpinBox(self.widget) # [输入框]初始方位（°）
        self.SpinBox_azimuth.setObjectName(u"SpinBox_azimuth")
        self.SpinBox_azimuth.setMinimumSize(QSize(120, 33))
        self.SpinBox_azimuth.setMaximum(360)
        self.SpinBox_azimuth.setValue(45)

        self.gridLayout.addWidget(self.SpinBox_azimuth, 5, 3, 1, 1)

        self.label_5 = QLabel(self.widget) # [文字]初始速度（m/s)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setMinimumSize(QSize(150, 0))
        self.label_5.setFont(font)

        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)

        self.LineEdit_speed = LineEdit(self.widget) # [输入框]初始速度（m/s)
        self.LineEdit_speed.setObjectName(u"LineEdit_speed")
        sizePolicy.setHeightForWidth(
            self.LineEdit_speed.sizePolicy().hasHeightForWidth())
        self.LineEdit_speed.setSizePolicy(sizePolicy)
        self.LineEdit_speed.setMinimumSize(QSize(120, 33))
        self.LineEdit_speed.setText(u"[-100, 0, 0]")

        self.gridLayout.addWidget(self.LineEdit_speed, 6, 1, 1, 1)

        self.label_4 = QLabel(self.widget) # [文字]初始仰角（°）
        self.label_4.setObjectName(u"label_4")
        self.label_4.setMinimumSize(QSize(150, 0))
        self.label_4.setFont(font)

        self.gridLayout.addWidget(self.label_4, 6, 2, 1, 1)

        self.SpinBox_obliquity = SpinBox(self.widget) # [输入框]初始仰角（°）
        self.SpinBox_obliquity.setObjectName(u"SpinBox_obliquity")
        self.SpinBox_obliquity.setMinimumSize(QSize(120, 33))
        self.SpinBox_obliquity.setMaximum(360)
        self.SpinBox_obliquity.setValue(84)

        self.gridLayout.addWidget(self.SpinBox_obliquity, 6, 3, 1, 1)

        self.ProgressBar_3 = ProgressBar(self.widget)
        self.ProgressBar_3.setObjectName(u"ProgressBar_3")

        self.gridLayout.addWidget(self.ProgressBar_3, 7, 0, 1, 4)

        self.label_6 = QLabel(self.widget) # [文字]运动状态信息
        self.label_6.setObjectName(u"label_6")
        self.label_6.setMinimumSize(QSize(440, 33))
        self.label_6.setFont(font1)

        self.gridLayout.addWidget(self.label_6, 8, 0, 1, 3)

        self.comboBox_MovementMode = ComboBox(self.widget) # [下拉框]运动模式
        self.comboBox_MovementMode.addItem("")
        self.comboBox_MovementMode.addItem("")
        self.comboBox_MovementMode.addItem("")
        self.comboBox_MovementMode.addItem("")
        self.comboBox_MovementMode.setObjectName(u"comboBox_MovementMode")
        sizePolicy1.setHeightForWidth(
            self.comboBox_MovementMode.sizePolicy().hasHeightForWidth())
        self.comboBox_MovementMode.setSizePolicy(sizePolicy1)
        self.comboBox_MovementMode.setMinimumSize(QSize(120, 33))

        self.gridLayout.addWidget(self.comboBox_MovementMode, 8, 3, 1, 1)

        self.label_10 = QLabel(self.widget) # [文字]参数
        self.label_10.setObjectName(u"label_10")
        sizePolicy.setHeightForWidth(
            self.label_10.sizePolicy().hasHeightForWidth())
        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QSize(120, 30))
        self.label_10.setFont(font)
        self.label_10.setFocusPolicy(Qt.NoFocus)
        self.label_10.setContextMenuPolicy(Qt.ActionsContextMenu)
        self.label_10.setLayoutDirection(Qt.LeftToRight)
        self.label_10.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_10, 9, 3, 1, 1)

        self.LineEdit_parament = LineEdit(self.widget) # [输入框]参数
        self.LineEdit_parament.setObjectName(u"LineEdit_parament")
        sizePolicy.setHeightForWidth(
            self.LineEdit_parament.sizePolicy().hasHeightForWidth())
        self.LineEdit_parament.setSizePolicy(sizePolicy)
        self.LineEdit_parament.setMinimumSize(QSize(120, 33))
        self.LineEdit_parament.setText(u"[5,0,0]")


        self.gridLayout.addWidget(self.LineEdit_parament, 10, 3, 1, 1)

        self.label_11 = QLabel(self.widget) # [文字]持续时间（s）
        self.label_11.setObjectName(u"label_11")
        sizePolicy.setHeightForWidth(
            self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QSize(120, 30))
        self.label_11.setFont(font)
        self.label_11.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.label_11, 11, 3, 1, 1)

        self.SpinBox_DuringTime = SpinBox(self.widget) # [输入框]持续时间（s）
        self.SpinBox_DuringTime.setObjectName(u"SpinBox_DuringTime")
        sizePolicy.setHeightForWidth(
            self.SpinBox_DuringTime.sizePolicy().hasHeightForWidth())
        self.SpinBox_DuringTime.setSizePolicy(sizePolicy)
        self.SpinBox_DuringTime.setMinimumSize(QSize(120, 33))
        self.SpinBox_DuringTime.setMaximum(99999)
        self.SpinBox_DuringTime.setSingleStep(1)
        self.SpinBox_DuringTime.setValue(200)

        self.gridLayout.addWidget(self.SpinBox_DuringTime, 12, 3, 1, 1)

        self.PrimaryPushButton = PrimaryPushButton(self.widget) # [按钮]保存参数
        self.PrimaryPushButton.setObjectName(u"PrimaryPushButton")
        self.PrimaryPushButton.setMinimumSize(QSize(120, 0))

        self.gridLayout.addWidget(self.PrimaryPushButton, 13, 3, 1, 1)

        self.PrimaryPushButton_2 = PrimaryPushButton(self.widget) # [按钮]删除
        self.PrimaryPushButton_2.setObjectName(u"PrimaryPushButton_2")
        self.PrimaryPushButton_2.setMinimumSize(QSize(120, 0))

        self.gridLayout.addWidget(self.PrimaryPushButton_2, 14, 3, 1, 1)

        self.ProgressBar_4 = ProgressBar(self.widget)
        self.ProgressBar_4.setObjectName(u"ProgressBar_4")

        self.gridLayout.addWidget(self.ProgressBar_4, 15, 0, 1, 4)

        self.TreeWidget = TreeWidget(self.widget) # [树形列表]运动轨迹
        self.TreeWidget.setObjectName(u"TreeWidget")
        self.TreeWidget.setMinimumSize(QSize(0, 300))
        self.TreeWidget.setMaximumSize(QSize(16777215, 16777214))
        self.TreeWidget.setFont(font2)
        self.TreeWidget.viewport().setProperty("cursor", QCursor(Qt.UpArrowCursor))
        self.TreeWidget.setFocusPolicy(Qt.StrongFocus)
        self.TreeWidget.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.TreeWidget.setLayoutDirection(Qt.LeftToRight)
        self.TreeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.TreeWidget.setTextElideMode(Qt.ElideRight)
        self.TreeWidget.header().setCascadingSectionResizes(False)
        self.TreeWidget.header().setMinimumSectionSize(200)
        self.TreeWidget.header().setDefaultSectionSize(200)
        self.TreeWidget.header().setHighlightSections(True)
        self.TreeWidget.header().setProperty("showSortIndicator", False)

        self.gridLayout.addWidget(self.TreeWidget, 9, 0, 6, 3)

        self.label_12 = QLabel(self.widget) # [文字]出现时间（s）
        self.label_12.setObjectName(u"label_12")
        self.label_12.setMinimumSize(QSize(150, 0))
        self.label_12.setFont(font)

        self.gridLayout.addWidget(self.label_12, 4, 2, 1, 1)

        self.SpinBox_StartTime = SpinBox(self.widget) # [输入框]出现时间（s）
        self.SpinBox_StartTime.setObjectName(u"SpinBox_StartTime")
        sizePolicy.setHeightForWidth(
            self.SpinBox_StartTime.sizePolicy().hasHeightForWidth())
        self.SpinBox_StartTime.setSizePolicy(sizePolicy)
        self.SpinBox_StartTime.setMinimumSize(QSize(120, 33))
        self.SpinBox_StartTime.setMaximum(99999)
        self.SpinBox_StartTime.setSingleStep(1)
        self.SpinBox_StartTime.setValue(0)

        self.gridLayout.addWidget(self.SpinBox_StartTime, 4, 3, 1, 1)

        self.retranslateUi(Form)

        # self.setLayout(self.gridLayout)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form2", u"Form2", None))
        self.label_8.setText(QCoreApplication.translate(
            "Form", u"\u76ee\u6807\u5c5e\u6027\u4fe1\u606f", None))
        self.PushButton.setText(QCoreApplication.translate(
            "Form", u"\u6dfb\u52a0", None))
        self.label_7.setText(QCoreApplication.translate(
            "Form", u"\u76ee\u6807\u7f16\u53f7", None))
        self.label_9.setText(QCoreApplication.translate(
            "Form", u"\u654c\u6211\u5c5e\u6027", None))
        self.comboBox_attribute.setItemText(
            0, QCoreApplication.translate("Form", u"\u654c\u65b9", None))
        self.comboBox_attribute.setItemText(
            1, QCoreApplication.translate("Form", u"\u53cb\u65b9", None))
        self.comboBox_attribute.setCurrentIndex(0)

        self.label.setText(QCoreApplication.translate(
            "Form", u"\u521d\u59cb\u72b6\u6001\u4fe1\u606f", None))
        self.label_2.setText(QCoreApplication.translate(
            "Form", u"\u521d\u59cb\u659c\u8ddd\uff08m):", None))
        self.label_3.setText(QCoreApplication.translate(
            "Form", u"\u521d\u59cb\u65b9\u4f4d\uff08\u00b0):", None))
        self.label_5.setText(QCoreApplication.translate(
            "Form", u"\u521d\u59cb\u901f\u5ea6\uff08m/s):", None))
        self.label_4.setText(QCoreApplication.translate(
            "Form", u"\u521d\u59cb\u503e\u5411\uff08\u00b0):", None))
        self.label_6.setText(QCoreApplication.translate(
            "Form", u"\u8fd0\u52a8\u72b6\u6001\u4fe1\u606f", None))
        self.comboBox_MovementMode.setItemText(
            0, QCoreApplication.translate("Form", u"\u5300\u901f", None))
        self.comboBox_MovementMode.setItemText(
            1, QCoreApplication.translate("Form", u"\u5300\u52a0\u901f", None))
        self.comboBox_MovementMode.setItemText(
            2, QCoreApplication.translate("Form", u"\u968f\u673a", None))
        self.comboBox_MovementMode.setItemText(
            3, QCoreApplication.translate("Form", u"\u9759\u6b62", None))
        self.comboBox_MovementMode.setCurrentIndex(0)

        self.label_10.setText(QCoreApplication.translate(
            "Form", u"\u53c2\u6570", None))
        self.label_11.setText(QCoreApplication.translate(
            "Form", u"\u6301\u7eed\u65f6\u95f4", None))
        self.PrimaryPushButton.setText(QCoreApplication.translate(
            "Form", u"\u4fdd\u5b58\u53c2\u6570", None))
        self.PrimaryPushButton_2.setText(
            QCoreApplication.translate("Form", u"\u5220\u9664", None))
        ___qtreewidgetitem = self.TreeWidget.headerItem()
        ___qtreewidgetitem.setText(2, QCoreApplication.translate(
            "Form", u"\u8fd0\u52a8\u53c2\u6570", None))
        ___qtreewidgetitem.setText(1, QCoreApplication.translate(
            "Form", u"\u6301\u7eed\u65f6\u95f4", None))
        ___qtreewidgetitem.setText(0, QCoreApplication.translate(
            "Form", u"\u76ee\u6807\u7f16\u53f7", None))

        __sortingEnabled = self.TreeWidget.isSortingEnabled()

        self.label_12.setText(QCoreApplication.translate(
            "Form", u"\u51fa\u73b0\u65f6\u95f4\uff08s):", None))
    # retranslateUi

   