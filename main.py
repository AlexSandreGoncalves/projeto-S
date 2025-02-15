from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from ui.toolbar_extended import ToolbarExtended
from ui.canvas import Canvas
from logic.object_manager import ObjectManager
from rendering.renderer import Renderer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Editor de Gráficos Vetoriais")
        # Define o estado da janela como maximizado
        self.setWindowState(Qt.WindowMaximized)

        # Inicializa gerenciador de objetos
        self.object_manager = ObjectManager()

        # Cria o canvas
        self.canvas = Canvas(None)  # Passa None temporariamente, pois o renderer ainda não foi criado

        # Cria o renderizador, passando o object_manager e o canvas
        self.renderer = Renderer(self.object_manager)

        # Atualiza o canvas com o renderizador
        self.canvas.renderer = self.renderer

        # Cria a barra de ferramentas
        self.toolbar = ToolbarExtended(self.canvas, self.object_manager)

        # Configura o layout principal
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()