# toolbar_extended.py
from PyQt5.QtWidgets import QPushButton, QHBoxLayout, QWidget, QLineEdit, QLabel, QVBoxLayout, QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import json
import logging
import os
from utils.calculations import calcular_area_retangulo, calcular_area_circulo, calcular_sucata, calcular_multiplo_ideal
from db_manager import buscar_peca_por_codigo, buscar_todas_pecas  # Importa funções do banco de dados

# Configurar logger
logger = logging.getLogger("app_logger")

class ToolbarExtended(QWidget):
    def __init__(self, canvas, object_manager):
        super().__init__()
        self.canvas = canvas
        self.object_manager = object_manager
        self.polygon_creator = None  # Inicializa como None para evitar o erro
        self.config_file = "config.json"  # Arquivo para salvar os últimos dados
        self.load_saved_data()  # Carrega os dados salvos
        self.init_ui_extended()  # Chama o método específico para ToolbarExtended

    def load_saved_data(self):
        """Carrega os últimos dados salvos do arquivo de configuração."""
        self.saved_data = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as file:
                    self.saved_data = json.load(file)
            except Exception as e:
                logger.error(f"Erro ao carregar dados salvos: {e}")

    def save_data(self):
        """Salva os últimos dados no arquivo de configuração."""
        try:
            with open(self.config_file, "w") as file:
                json.dump(self.saved_data, file)
        except Exception as e:
            logger.error(f"Erro ao salvar dados: {e}")

    def init_ui_extended(self):
        """Inicializa a interface específica da barra de ferramentas estendida."""
        logger.info("Configurando ToolbarExtended...")
        main_layout = QVBoxLayout()

        # Layout para botões principais
        button_layout = QHBoxLayout()

        # Configuração dos botões com tamanho fixo
        button_size = 120  # Tamanho fixo para todos os botões

        btn_create_polygon = QPushButton("Demarcar Sobra")
        btn_create_polygon.setFixedWidth(button_size)
        btn_create_polygon.clicked.connect(self.start_polygon_creation)
        button_layout.addWidget(btn_create_polygon)

        btn_finalize_polygon = QPushButton("Finalizar Sobra")
        btn_finalize_polygon.setFixedWidth(button_size)
        btn_finalize_polygon.clicked.connect(self.finalize_polygon)
        button_layout.addWidget(btn_finalize_polygon)

        btn_edit_polygon = QPushButton("Editar Sobra")
        btn_edit_polygon.setFixedWidth(button_size)
        btn_edit_polygon.clicked.connect(self.edit_polygon)
        button_layout.addWidget(btn_edit_polygon)

        btn_create_rectangle = QPushButton("Chapa")
        btn_create_rectangle.setFixedWidth(button_size)
        btn_create_rectangle.clicked.connect(self.create_rectangle)
        button_layout.addWidget(btn_create_rectangle)

        self.height_input = QLineEdit()
        self.height_input.setPlaceholderText("Altura")
        self.height_input.setText(str(self.saved_data.get("height", "")))
        button_layout.addWidget(QLabel("A:"))
        button_layout.addWidget(self.height_input)

        self.length_input = QLineEdit()
        self.length_input.setPlaceholderText("Comprimento")
        self.length_input.setText(str(self.saved_data.get("length", "")))
        button_layout.addWidget(QLabel("C:"))
        button_layout.addWidget(self.length_input)

        btn_create_circle = QPushButton("Peça")
        btn_create_circle.setFixedWidth(button_size)
        btn_create_circle.clicked.connect(self.create_circle)
        button_layout.addWidget(btn_create_circle)

        self.radius_input = QLineEdit()
        self.radius_input.setPlaceholderText("Raio")
        self.radius_input.setText(str(self.saved_data.get("radius", "")))
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

        # Campos para busca no banco de dados
        db_layout = QHBoxLayout()

        self.entry_codigo = QLineEdit()
        self.entry_codigo.setPlaceholderText("Código da Peça")
        db_layout.addWidget(self.entry_codigo)

        btn_medidas = QPushButton("Medidas")
        btn_medidas.setFixedWidth(button_size)
        btn_medidas.clicked.connect(self.buscar_por_codigo)
        db_layout.addWidget(btn_medidas)

        btn_carregar_todos = QPushButton("Carregar Todos")
        btn_carregar_todos.setFixedWidth(button_size)
        btn_carregar_todos.clicked.connect(self.carregar_todos)
        db_layout.addWidget(btn_carregar_todos)

        main_layout.addLayout(db_layout)

        # Campos para exibir comprimento e largura
        fields_layout = QHBoxLayout()

        self.entry_comprimento = QLineEdit()
        self.entry_comprimento.setReadOnly(True)
        fields_layout.addWidget(QLabel("Comprimento:"))
        fields_layout.addWidget(self.entry_comprimento)

        self.entry_largura = QLineEdit()
        self.entry_largura.setReadOnly(True)
        fields_layout.addWidget(QLabel("Largura:"))
        fields_layout.addWidget(self.entry_largura)

        main_layout.addLayout(fields_layout)

        # Tabela para listar peças
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Código", "Comprimento", "Largura"])
        main_layout.addWidget(self.table)

        # Campos de exibição de texto
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
        logger.info("ToolbarExtended configurada com sucesso.")

    def buscar_por_codigo(self):
        """Busca uma peça pelo código no banco de dados."""
        cod_peca = self.entry_codigo.text()
        if not cod_peca:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um código de peça.")
            return

        dado = buscar_peca_por_codigo(cod_peca)
        if dado:
            self.entry_comprimento.setText(str(dado[1]))
            self.entry_largura.setText(str(dado[2]))
            self.atualizar_tabela([dado])
        else:
            QMessageBox.information(self, "Info", "Nenhuma peça encontrada com esse código.")

    def carregar_todos(self):
        """Carrega todas as peças do banco de dados."""
        dados = buscar_todas_pecas()
        self.atualizar_tabela(dados)

    def atualizar_tabela(self, dados):
        """Atualiza a tabela com os dados fornecidos."""
        self.table.setRowCount(len(dados))
        for row, dado in enumerate(dados):
            self.table.setItem(row, 0, QTableWidgetItem(str(dado[0])))
            self.table.setItem(row, 1, QTableWidgetItem(str(dado[1])))
            self.table.setItem(row, 2, QTableWidgetItem(str(dado[2])))

    def start_polygon_creation(self):
        """Inicia a criação de um polígono."""
        if self.polygon_creator is None:
            try:
                from ui.polygon_creator import PolygonCreator  # Importa aqui para evitar circular imports
                self.polygon_creator = PolygonCreator(self.canvas, self)  # Passa o toolbar como argumento
            except ImportError as e:
                logger.error(f"Erro ao importar PolygonCreator: {e}")
                return
        self.polygon_creator.start_polygon_creation()

    def finalize_polygon(self):
        """Finaliza a criação do polígono."""
        if self.polygon_creator:
            self.polygon_creator.finalize_polygon()
            logger.info("Finalização do polígono acionada via Toolbar.")

    def edit_polygon(self):
        """Ativa o modo de edição do último polígono criado."""
        if self.polygon_creator:
            self.polygon_creator.edit_polygon()
            logger.info("Edição de polígono acionada via Toolbar.")

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
            logger.info(f"Botão 'Criar Retângulo' clicado. Altura={height}, Comprimento={length}")
            self.canvas.draw_rectangle((50, 50), length, height)
            logger.info("Retângulo adicionado ao canvas.")
            # Salva os valores no arquivo de configuração
            self.saved_data["height"] = height
            self.saved_data["length"] = length
            self.save_data()
            # Atualiza as informações de área
            rect_area = calcular_area_retangulo(length, height)
            self.update_area_info(rect_area=rect_area)
        except ValueError:
            logger.error("Valores inválidos para altura ou comprimento.")

    def create_circle(self):
        try:
            radius = float(self.radius_input.text())
            if radius <= 0:
                logger.error("O raio deve ser um valor positivo.")
                return
            logger.info(f"Botão 'Criar Círculo' clicado. Raio={radius}")
            self.canvas.draw_circle(radius)  # Corrigido para passar apenas o raio
            logger.info("Círculo adicionado ao canvas.")
            # Salva o valor no arquivo de configuração
            self.saved_data["radius"] = radius
            self.save_data()
            # Atualiza as informações de área
            circle_area = calcular_area_circulo(radius)
            self.update_area_info(circle_radius=radius, circle_area=circle_area)
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
            # Atualiza as informações de área
            rect = self.canvas.current_rectangle.rect()
            rect_area = calcular_area_retangulo(rect.width(), rect.height())
            circle_area = calcular_area_circulo(radius)
            self.update_area_info(rect_area=rect_area, circle_area=circle_area)
        except Exception as e:
            logger.error(f"Erro ao distribuir círculos: {e}")

    def clear_screen(self):
        """Limpa todo o conteúdo do canvas."""
        self.canvas.clear_scene()
        logger.info("Tela limpa pelo botão 'Limpar Tela'.")

    def update_area_info(self, rect_area=None, circle_radius=None, circle_area=None):
        """
        Atualiza as informações de área na interface.
        :param rect_area: Área do retângulo.
        :param circle_radius: Raio do círculo.
        :param circle_area: Área do círculo.
        """
        if rect_area:
            self.area_pieces_display.setText(f"Área das Peças: {rect_area:.2f} m²")
        if circle_radius:
            circle_area = calcular_area_circulo(circle_radius)
            self.area_single_piece_display.setText(f"Área Peça: {circle_area:.2f} m²")
        if circle_area and rect_area:
            multiplo_ideal = calcular_multiplo_ideal(rect_area, circle_area)
            total_pieces_area = multiplo_ideal * circle_area
            sucata = calcular_sucata(rect_area, total_pieces_area)
            self.multiplo_ideal_display.setText(f"Múltiplo Ideal: {multiplo_ideal}")
            self.sucata_display.setText(f"Sucata: {sucata:.2f} m²")
            self.area_pieces_display.setText(f"Área das Peças: {total_pieces_area:.2f} m²")