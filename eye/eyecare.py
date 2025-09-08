import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont, QPixmap


class DemoWin(QMainWindow):
    def __init__(self):
        super(DemoWin, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(474, 600)  # 设置窗口大小
        # 设置最大化按钮，最小化按钮，关闭按钮，以及窗口一直在最顶层
        self.setWindowFlags(
            Qt.WindowMaximizeButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        # 添加窗口标题
        self.setWindowTitle("窗口样式Demo")

        # 添加背景图片标签
        self.image_label = QLabel(self)
        self.image_label.setPixmap(QPixmap("D:/Eyecare/Eyecare/eye/eye.jpg"))  # 加载图片
        self.image_label.setGeometry(0, 0, 600, 500)  # 设置图片标签的位置和大小

        # 添加文字标签
        self.text_label = QLabel("眼睛酸了就眨眨眼\n眼睛累了就歇一会", self)
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
        label_height = 100  # 标签的高度
        label_y = 500  # 标签的垂直位置，刚好与背景图片底部对齐
        self.text_label.setGeometry(0, label_y, 474, label_height)  # 宽度与窗口一致

        self.setWindowFlags(Qt.FramelessWindowHint)  # 设置窗口无边框
    
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()  # 激活窗口
        self.raise_()  # 将窗口提升到最前面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("./eye.jpg"))  # 确保图标文件名正确
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())