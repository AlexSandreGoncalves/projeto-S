from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLineEdit, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
import logging

# Configurar logger
logger = logging.getLogger("app_logger")


class ToolbarBase(QWidget):
    def __init__(self, canvas, object_manager):
        super().__init__()
        self.canvas = canvas
        self.object_manager = object_manager
        self.polygon_creator = None  # Inicializa como None para evitar o erro
        self.init_ui()

    def init_ui(self):
        logger.info("Inicializando Toolbar...")
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        # Configuração dos botões com tamanho fixo
        button_size = 120  # Tamanho fixo para todos os botões

        # Botão "Demarcar Sobra" (antigo "Criar Polígono")
        btn_create_polygon = QPushButton("Demarcar Sobra")
        btn_create_polygon.setFixedWidth(button_size)
        btn_create_polygon.clicked.connect(self.start_polygon_creation)
        button_layout.addWidget(btn_create_polygon)

        # Botão "Finalizar Sobra" (antigo "Finalizar Polígono")
        btn_finalize_polygon = QPushButton("Finalizar Sobra")
        btn_finalize_polygon.setFixedWidth(button_size)
        btn_finalize_polygon.clicked.connect(self.finalize_polygon)
        button_layout.addWidget(btn_finalize_polygon)

        # Botão "Editar Sobra" (antigo "Editar Polígono")
        btn_edit_polygon = QPushButton("Editar Sobra")
        btn_edit_polygon.setFixedWidth(button_size)
        btn_edit_polygon.clicked.connect(self.edit_polygon)
        button_layout.addWidget(btn_edit_polygon)

        # Botão "Chapa" (antigo "Retângulo")
        btn_create_rectangle = QPushButton("Chapa")
        btn_create_rectangle.setFixedWidth(button_size)
        btn_create_rectangle.clicked.connect(self.create_rectangle)
        button_layout.addWidget(btn_create_rectangle)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Altura")
        button_layout.addWidget(QLabel("A:"))
        button_layout.addWidget(self.height_input)

        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Comprimento")
        button_layout.addWidget(QLabel("C:"))
        button_layout.addWidget(self.length_input)

        # Botão "Peça" (antigo "Círculo")
        btn_create_circle = QPushButton("Peça")
        btn_create_circle.setFixedWidth(button_size)
        btn_create_circle.clicked.connect(self.create_circle)
        button_layout.addWidget(btn_create_circle)

        self.radius_input = QLineEdit()
        self.radius_input.setPlaceholderText("Raio")
        button_layout.addWidget(QLabel("R:"))
        button_layout.addWidget(self.radius_input)

        btn_distribute_circles = QPushButton("Distribuir Peça")
        btn_distribute_circles.setFixedWidth(button_size)
        btn_distribute_circles.clicked.connect(self.distribute_circles)
        button_layout.addWidget(btn_distribute_circles)

        btn_clear_screen = QPushButton("Limpar Tela")
        btn_clear_screen.setFixedWidth(button_size)
        btn_clear_screen.clicked.connect(self.clear_screen)
        button_layout.addWidget(btn_clear_screen)

        main_layout.addLayout(button_layout)

        text_fields_layout = QVBoxLayout()
        self.area_pieces_display = QLabel("Área das Peças: ")
        text_fields_layout.addWidget(self.area_pieces_display)
        self.area_single_piece_display = QLabel("Área Peça: ")
        text_fields_layout.addWidget(self.area_single_piece_display)
        self.multiplo_ideal_display = QLabel("Múltiplo Ideal: ")
        text_fields_layout.addWidget(self.multiplo_ideal_display)
        self.sucata_display = QLabel("Sucata: ")
        text_fields_layout.addWidget(self.sucata_display)
        self.sobra_display = QLabel("Sobra: ")  # Novo campo "Sobra"
        text_fields_layout.addWidget(self.sobra_display)

        main_layout.addLayout(text_fields_layout)
        self.setLayout(main_layout)
        logger.info("Toolbar inicializada com sucesso.")

    def start_polygon_creation(self):
        """Inicia a criação de um polígono."""
        if self.polygon_creator is None:
            try:
                from ui.polygon_creator import PolygonCreator  # Importa aqui para evitar circular imports
                self.polygon_creator = PolygonCreator(self.canvas, self)
            except ImportError as e:
                logger.error(f"Erro ao importar PolygonCreator: {e}")
                return
        self.polygon_creator.start_polygon_creation()

    def finalize_polygon(self):
        """Finaliza a criação do polígono."""
        if self.polygon_creator:
            self.polygon_creator.finalize_polygon()

    def edit_polygon(self):
        """Ativa o modo de edição do último polígono criado."""
        if self.polygon_creator:
            self.polygon_creator.edit_polygon()

    def update_sobra(self, polygon_area):
        """
        Atualiza o campo "Sobra" com a área do polígono em m².
        :param polygon_area: Área do polígono em metros quadrados.
        """
        self.sobra_display.setText(f"Sobra: {polygon_area:.2f} m²")
        logger.info(f"Campo 'Sobra' atualizado com área: {polygon_area:.2f} m²")

    def create_rectangle(self):
        try:
            height = float(self.height_input.text())
            length = float(self.length_input.text())
            if height <= 0 or length <= 0:
                logger.error("Altura e comprimento devem ser valores positivos.")
                return
            logger.info(f"Botão 'Chapa' clicado. Altura={height}, Comprimento={length}")
            self.canvas.draw_rectangle((50, 50), length, height)
            logger.info("Retângulo adicionado ao canvas.")
        except ValueError:
            logger.error("Valores inválidos para altura ou comprimento.")

    def create_circle(self):
        try:
            radius = float(self.radius_input.text())
            if radius <= 0:
                logger.error("O raio deve ser um valor positivo.")
                return
            logger.info(f"Botão 'Peça' clicado. Raio={radius}")
            self.canvas.draw_circle(radius)  # Corrigido para passar apenas o raio
            logger.info("Círculo adicionado ao canvas.")
        except ValueError:
            logger.error("Valor inválido para raio.")

    def distribute_circles(self):
        try:
            radius = float(self.radius_input.text())
            if radius <= 0:
                logger.error("O raio deve ser um valor positivo.")
                return
            if not self.canvas.current_rectangle:
                logger.error("Nenhum retângulo disponível para distribuir círculos.")
                return
            self.canvas.distribute_circles(radius)
            logger.info("Círculos distribuídos dentro do retângulo.")
        except Exception as e:
            logger.error(f"Erro ao distribuir círculos: {e}")

    def clear_screen(self):
        """Limpa todo o conteúdo do canvas."""
        self.canvas.clear_scene()
        logger.info("Tela limpa pelo botão 'Limpar Tela'.")