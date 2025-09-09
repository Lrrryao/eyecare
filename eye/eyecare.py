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
        # 设置窗口标志：无边框 + 置顶
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        # 添加窗口标题
        self.setWindowTitle("眼睛休息提醒")

        # 添加背景图片标签
        self.image_label = QLabel(self)
        # 加载图片并缩放到合适大小
        import os
        image_path = "eye/eye.jpg"
        print(f"尝试加载图片: {image_path}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"图片文件是否存在: {os.path.exists(image_path)}")
        
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():
            print(f"图片加载成功，原始尺寸: {pixmap.width()}x{pixmap.height()}")
            # 缩放到窗口宽度，保持宽高比
            scaled_pixmap = pixmap.scaled(474, 500, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            print(f"缩放后尺寸: {scaled_pixmap.width()}x{scaled_pixmap.height()}")
            self.image_label.setPixmap(scaled_pixmap)
        else:
            print("警告：无法加载eye.jpg图片")
        self.image_label.setGeometry(0, 0, 474, 500)  # 设置图片标签的位置和大小

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
    
    def showEvent(self, event):
        super().showEvent(event)
        self.activateWindow()  # 激活窗口
        self.raise_()  # 将窗口提升到最前面


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("eye/eye.jpg"))  # 确保图标文件名正确
    # 创建一个主窗口
    mainWin = DemoWin()
    # 显示
    mainWin.show()
    # 主循环
    sys.exit(app.exec_())