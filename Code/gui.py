import sys
import os
from PyQt5 import QtWidgets
import design
import presentation


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self) # Это нужно для инициализации нашего дизайна
        self.chooseDirectory.clicked.connect(self.browse_folder)
        self.chooseFile.clicked.connect(self.browse_file)
        self.processFile.clicked.connect(self.launch_analysis)
        self.path_to_har_file = ""
        self.path_to_pptx = ""

    def browse_folder(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")

        if directory:
            self.lineEditFolder.setText(directory.split('/')[-1])
            self.path_to_pptx = directory
            self.readyLabel.clear()

    def browse_file(self):
        filename, filter = QtWidgets.QFileDialog.getOpenFileName(parent=self, caption='Open file', directory=os.getcwd(),
                                                                 filter='HAR Files (*.har)')

        if filename:
            self.lineEditFile.setText(filename.split('/')[-1])
            self.path_to_har_file = filename
            self.readyLabel.clear()

    def launch_analysis(self):
        presentation.create_presentation(self.path_to_har_file, self.path_to_pptx)
        self.readyLabel.setText('Analysis is done!')


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

