import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import DATABASE_URL
from models.user import Base

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ouroboros Desktop")
        self.setGeometry(100, 100, 600, 400)
        label = QLabel("Bem-vindo ao Ouroboros!", self)
        label.move(200, 200)

if __name__ == '__main__':
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())