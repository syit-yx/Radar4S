<p align="center">
  <img width="18%" align="center" src="https://pic1.imgdb.cn/item/646f81a6f024cca17313b6a0.png" alt="logo">
</p>
  <h1 align="center">
  雷达目标点迹态势模拟系统
</h1>

<p align="center">
  <!-- <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a> -->
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>
</p>

<p align="center">
简体中文 | <a href="README_en.md">English</a>
</p>

![Interface](https://pic1.imgdb.cn/item/646f81aef024cca17313c093.png)

## 介绍

雷达是战场信息获取的重要传感器设备，基于雷达的战场态势模拟具有重要的科学意义和应用价值。本项目面向大范围战场环境下多部雷达同时对空中多批目标进行跟踪的背景，针对雷达态势建模中的运动目标点迹模拟问题进行研究，开发了基于 Python 工具的雷达目标态势模拟演示软件。该软件系统具有目标参数可重构、雷达参数可灵活配置、点迹数据保真度高、实时动态显示等特点。并与雷达数据处理相结合，可实现态势模拟与信息处理综合评估设计。

## 使用

```commandline
git glone https://github.com/syit-yx/Radar4S.git
pip install -r requirements.txt
python demo.py
```
或者下载release中的[安装包](https://github.com/syit-yx/Radar4S/releases/tag/v1.4)，将其安装到您的电脑上


## 特别感谢

[**PyQt-Fluent-Widgets**: 基于 PyQt5 的 Fluent Design 风格组件库](https://github.com/zhiyiYo/PyQt-Fluent-Widgets)

## 许可证

雷达目标点迹态势模拟系统 使用 [GPLv3](./LICENSE) 许可证.

Copyright © 2023 by wkr.