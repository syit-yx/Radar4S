lightqss = """
Widget > QLabel {
    font: 24px 'Segoe UI', 'Microsoft YaHei';
}

Widget {
    border: 1px solid rgb(229, 229, 229);
    border-right: none;
    border-bottom: none;
    border-top-left-radius: 10px;
    background-color: rgb(249, 249, 249);
}

Window {
    background-color: rgb(243, 243, 243);
}
"""

darkqss = """
Widget > QLabel {
    font: 24px 'Segoe UI', 'Microsoft YaHei';
}

Widget {
    border: 1px solid rgb(29, 29, 29);
    background-color: rgb(39, 39, 39);
    border-top-left-radius: 10px;
    border-right: none;
    border-bottom: none;
}

Window {
    background-color: rgb(32, 32, 32);
}

StandardTitleBar {
    background-color: rgb(32, 32, 32);
}

StandardTitleBar > QLabel,
Widget > QLabel {
    color: white;
}


MinimizeButton {
    qproperty-normalColor: white;
    qproperty-normalBackgroundColor: transparent;
    qproperty-hoverColor: white;
    qproperty-hoverBackgroundColor: rgba(255, 255, 255, 26);
    qproperty-pressedColor: white;
    qproperty-pressedBackgroundColor: rgba(255, 255, 255, 51)
}


MaximizeButton {
    qproperty-normalColor: white;
    qproperty-normalBackgroundColor: transparent;
    qproperty-hoverColor: white;
    qproperty-hoverBackgroundColor: rgba(255, 255, 255, 26);
    qproperty-pressedColor: white;
    qproperty-pressedBackgroundColor: rgba(255, 255, 255, 51)
}

CloseButton {
    qproperty-normalColor: white;
    qproperty-normalBackgroundColor: transparent;
}
"""