import sys

# 导入QT,其中包含一些常量，例如颜色等
from PyQt5.QtCore import Qt
# 导入常用组件
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
# 使用调色板等
from PyQt5.QtGui import QIcon, QFont


class DemoWin(QMainWindow):
    def __init__(self):
        super(DemoWin, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(600, 550)#(width,height)
        # 设置最大化按钮，最小化按钮，关闭按钮，以及窗口一直在最顶层
        self.setWindowFlags(
            Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        # 为窗口设置一个对象名，方便使用QSS设置样式
        self.setObjectName("MainWindow")
        # 设置QSS样式
        self.setStyleSheet("#MainWindow{border-image:url('D:/Eyecare/drink_water.jpg');}")

        # 添加窗口标题
        self.setWindowTitle("窗口样式Demo")

        # 添加文字标签
        self.text_label = QLabel("喝点水吧，对身体好哦！😘", self)
        self.text_label.setFont(QFont("幼圆", 14, QFont.Bold))  # 设置字体为幼圆，字号为14，并加粗
        self.text_label.setStyleSheet("""
            QLabel {
                color: #FFFFFF;          /* 文字颜色为白色 */
                background-color: #FFB6C1; /* 背景颜色为粉色 */
                border-radius: 10px;     /* 圆角边框 */
                padding: 5px;            /* 内边距 */
            }
        """)  # 设置文字颜色为白色，背景颜色为粉色
        self.text_label.setAlignment(Qt.AlignCenter)  # 文字居中对齐

        # 设置文字标签的位置和大小
        # 假设背景图片的高度为450，将标签放在图片下方，留出一定的间距
        label_height = 50  # 标签的高度
        label_y = 550 - label_height - 10  # 标签的垂直位置，距离底部10像素
        self.text_label.setGeometry(0, label_y, 600, label_height)  # 宽度与窗口一致

        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口无边框
    
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()  # 激活窗口
        self.raise_()  # 将窗口提升到最前面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./drink.png"))
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())