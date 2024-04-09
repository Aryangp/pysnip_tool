from PyQt5.QtWidgets import QWidget, QApplication, QRubberBand, QLabel, QPushButton
from PyQt5.QtGui import QMouseEvent, QPixmap, QImage
from PyQt5.QtCore import Qt, QPoint, QRect
from PIL import ImageQt
import pytesseract
import sys
from openAiModule import prompt_llama2

class Capture(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main = main_window
        self.main.hide()

        self.setMouseTracking(True)
        desk_size = QApplication.desktop()
        self.setGeometry(0, 0, desk_size.width(), desk_size.height())
        self.setWindowFlags(
            self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint
        )
        self.setWindowOpacity(0.15)

        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

        QApplication.setOverrideCursor(Qt.CrossCursor)
        screen = QApplication.primaryScreen()
        rect = QApplication.desktop().rect()

        self.imgmap = screen.grabWindow(
            QApplication.desktop().winId(),
            rect.x(),
            rect.y(),
            rect.width(),
            rect.height(),
        )

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(
                QRect(self.origin, event.pos()).normalized()
            )
            self.rubber_band.show()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.origin.isNull():
            self.rubber_band.setGeometry(
                QRect(self.origin, event.pos()).normalized()
            )

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.rubber_band.hide()

            rect = self.rubber_band.geometry()
            self.imgmap = self.imgmap.copy(rect)
            QApplication.restoreOverrideCursor()

            img_pil = ImageQt.fromqpixmap(self.imgmap)

            # Perform OCR using pytesseract
            myconfig = r"--psm 6 --oem 3"
            extracted_text = pytesseract.image_to_string(img_pil, config=myconfig)
            print(f"Extracted Text : {extracted_text}")
            answer=prompt_llama2(extracted_text)
            print(f"answer : {answer}")
            self.main.label.setPixmap(self.imgmap)
            self.main.label.setGeometry(150, 150, 350, 250)
            self.main.label.setStyleSheet("font-size: 15px;")
            self.main.label.setText(answer)
            # self.main.label.adjustSize()
            self.main.label.setWordWrap(True)
            # the answer is not fittting on the screen so we need to fix that
            self.main.label.setAlignment(Qt.AlignCenter)
            self.main.label.show()
            self.main.show()
            self.close()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Snipping Tool with OCR")
        self.label = QLabel(self)
        self.label.setGeometry(150, 150, 350, 250)
        self.label.setText("Capture a snip to extract text.")
        self.label.setStyleSheet("font-size: 15px;")
        self.label.setAlignment(Qt.AlignCenter)

        self.capture_button = QPushButton("Capture Snip", self)
        self.capture_button.setGeometry(60, 90, 150, 80)
        # align the button in centre
        self.capture_button.move(250, 400)
        self.capture_button.setStyleSheet("font-size: 15px;")
        self.capture_button.setToolTip("Click to capture a snip.")
        self.capture_button.clicked.connect(self.capture_snip)

    def capture_snip(self):
        self.capture_window = Capture(self)
        self.capture_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
