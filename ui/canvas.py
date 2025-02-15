from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QSizePolicy
from PyQt5.QtGui import QPen
from PyQt5.QtCore import Qt
import logging

# Configurar logger
logger = logging.getLogger("app_logger")

class Canvas(QGraphicsView):
    def __init__(self, renderer):
        """
        Inicializa o canvas onde os elementos gráficos serão desenhados.
        :param renderer: Instância do renderizador para processamento de objetos.
        """
        super().__init__()
        self.renderer = renderer
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.current_rectangle = None  # Armazena o retângulo atual
        self.scale_factor = 1.0  # Fator de escala aplicado ao retângulo
        self.original_width = None  # Largura original do retângulo
        self.original_height = None  # Altura original do retângulo
        # Configura o canvas para redimensionar automaticamente
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setAlignment(Qt.AlignCenter)  # Centraliza o conteúdo no canvas
        logger.info("Canvas inicializado com sucesso.")

    def resizeEvent(self, event):
        """Redimensiona o canvas e ajusta os elementos para manter a escala."""
        super().resizeEvent(event)
        if self.current_rectangle:
            self.redraw_rectangle()

    def clear_scene(self):
        """Limpa todos os itens do canvas, exceto o retângulo atual."""
        try:
            if self.current_rectangle:
                # Remove todos os itens, exceto o retângulo atual
                for item in self.scene.items():
                    if item != self.current_rectangle:
                        self.scene.removeItem(item)
            else:
                # Se não houver retângulo, limpa tudo
                self.scene.clear()
            logger.info("Canvas limpo.")
        except Exception as e:
            logger.error(f"Erro ao limpar o canvas: {e}")

    def draw_rectangle(self, position, width, height):
        """Desenha um retângulo no canvas, ajustando a escala para caber dentro do canvas."""
        self.clear_scene()  # Limpa o canvas antes de desenhar um novo retângulo
        self.original_width = width
        self.original_height = height
        self.redraw_rectangle()

    def redraw_rectangle(self):
        """Redesenha o retângulo com base nas dimensões originais e no tamanho atual do canvas."""
        if not self.original_width or not self.original_height:
            return
        canvas_width = self.width()
        canvas_height = self.height()
        margin_x = canvas_width * 0.15
        margin_y = canvas_height * 0.15
        available_width = canvas_width - 2 * margin_x
        available_height = canvas_height - 2 * margin_y
        scale_x = available_width / self.original_width
        scale_y = available_height / self.original_height
        self.scale_factor = min(scale_x, scale_y)
        scaled_width = self.original_width * self.scale_factor
        scaled_height = self.original_height * self.scale_factor
        x = margin_x + (available_width - scaled_width) / 2
        y = margin_y + (available_height - scaled_height) / 2
        if self.current_rectangle:
            self.scene.removeItem(self.current_rectangle)
        pen = QPen(Qt.black)
        rect = self.scene.addRect(x, y, scaled_width, scaled_height, pen)
        self.current_rectangle = rect
        logger.info(f"Retângulo redesenhado com dimensões reais: {self.original_width}x{self.original_height}, escala: {self.scale_factor}")

    def get_scale_factor(self):
        """Retorna o fator de escala aplicado ao retângulo."""
        return self.scale_factor

    def draw_circle(self, radius):
        """Desenha um círculo no centro do retângulo atual."""
        if not self.current_rectangle:
            logger.error("Nenhum retângulo disponível para desenhar círculos.")
            return
        if hasattr(self, "current_circle") and self.current_circle:
            self.scene.removeItem(self.current_circle)
        rect = self.current_rectangle.rect()
        center_x = rect.x() + rect.width() / 2
        center_y = rect.y() + rect.height() / 2
        scaled_radius = radius * self.scale_factor
        pen = QPen(Qt.black)
        self.current_circle = self.scene.addEllipse(
            center_x - scaled_radius, center_y - scaled_radius, scaled_radius * 2, scaled_radius * 2, pen
        )
        logger.info(f"Círculo desenhado com raio real: {radius}, escala: {self.scale_factor}")

    def distribute_circles(self, radius):
        """Distribui círculos dentro do retângulo atual."""
        if not self.current_rectangle:
            logger.error("Nenhum retângulo disponível para distribuir círculos.")
            return
        self.clear_scene()
        rect = self.current_rectangle.rect()
        spacing = radius * 2
        cols = int(rect.width() // (spacing * self.scale_factor))
        rows = int(rect.height() // (spacing * self.scale_factor))
        logger.info(f"Distribuindo círculos: {cols} colunas, {rows} linhas")
        for row in range(rows):
            for col in range(cols):
                x = rect.x() + col * spacing * self.scale_factor + radius * self.scale_factor
                y = rect.y() + row * spacing * self.scale_factor + radius * self.scale_factor
                self.draw_circle_for_distribution(radius, x, y)

    def draw_circle_for_distribution(self, radius, x, y):
        """Desenha um círculo nas coordenadas especificadas sem apagar o anterior."""
        scaled_radius = radius * self.scale_factor
        pen = QPen(Qt.black)
        self.scene.addEllipse(x - scaled_radius, y - scaled_radius, scaled_radius * 2, scaled_radius * 2, pen)
        logger.info(f"Círculo distribuído com raio real: {radius}, escala: {self.scale_factor}")