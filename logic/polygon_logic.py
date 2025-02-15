from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsEllipseItem
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QObject, QPointF
import logging

# Configurar logger
logger = logging.getLogger("app_logger")

class PolygonLogic(QObject):
    def __init__(self, canvas, toolbar):
        """
        Inicializa a lógica de criação de polígonos.
        :param canvas: Instância do Canvas onde os polígonos serão desenhados.
        :param toolbar: Instância da Toolbar para interação.
        """
        super().__init__()
        self.canvas = canvas
        self.toolbar = toolbar
        self.points = []  # Lista para armazenar os pontos do polígono
        self.current_polygon = None  # Armazena o polígono atual em construção
        self.vertex_circles = []  # Lista para armazenar os círculos que representam os vértices
        self.pen = QPen(Qt.black)  # Define a cor da borda do polígono
        self.brush = QBrush(QColor(255, 255, 0, 128))  # Preenchimento amarelo com 50% de transparência
        self.is_finalized = False  # Indica se o polígono foi finalizado
        self.edit_mode = False  # Indica se o modo de edição está ativado

    def start_polygon_creation(self):
        """
        Inicia o modo de criação de polígonos.
        """
        if self.is_finalized:
            self.reset_polygon_creation()  # Reinicia a criação de polígonos se o anterior foi finalizado
        logger.info("Iniciando criação de polígono...")
        self.points.clear()
        if self.current_polygon:
            self.canvas.scene.removeItem(self.current_polygon)
        self.current_polygon = None
        self.canvas.scene.installEventFilter(self)  # Ativa o filtro de eventos para capturar cliques
        logger.info("Modo de criação de polígono ativado.")

    def reset_polygon_creation(self):
        """
        Reinicia a criação de polígonos após finalizar o anterior.
        """
        self.is_finalized = False
        self.points.clear()
        if self.current_polygon:
            self.canvas.scene.removeItem(self.current_polygon)
        self.current_polygon = None
        logger.info("Criação de polígono reiniciada.")

    def eventFilter(self, obj, event):
        """
        Captura eventos do mouse para criar ou editar os vértices do polígono.
        """
        if self.edit_mode:
            return self.handle_edit_mode(obj, event)

        if self.is_finalized:
            return super(PolygonLogic, self).eventFilter(obj, event)

        if event.type() == event.GraphicsSceneMousePress:
            # Captura o clique do mouse
            pos = event.scenePos()
            # Verifica se o ponto está dentro do retângulo ou ajusta para a borda mais próxima
            if self.canvas.current_rectangle:
                rect = self.canvas.current_rectangle.rect()
                pos = self.adjust_point_to_rectangle(pos, rect)
            self.points.append(pos)
            logger.info(f"Ponto adicionado: ({pos.x()}, {pos.y()})")
            # Desenha o polígono temporário apenas se houver mais de um ponto
            if len(self.points) > 1:
                if self.current_polygon:
                    self.canvas.scene.removeItem(self.current_polygon)
                polygon = QPolygonF(self.points)
                self.current_polygon = QGraphicsPolygonItem(polygon)
                self.current_polygon.setPen(self.pen)
                self.current_polygon.setBrush(self.brush)  # Aplica o preenchimento amarelo
                self.canvas.scene.addItem(self.current_polygon)
        return super(PolygonLogic, self).eventFilter(obj, event)

    def handle_edit_mode(self, obj, event):
        """
        Manipula o modo de edição dos vértices do polígono.
        """
        if event.type() == event.GraphicsSceneMousePress:
            pos = event.scenePos()
            for i, circle in enumerate(self.vertex_circles):
                if circle.contains(pos):
                    self.selected_vertex_index = i
                    logger.info(f"Vértice selecionado para edição: índice {i}")
                    return True
        elif event.type() == event.GraphicsSceneMouseMove and hasattr(self, "selected_vertex_index"):
            pos = event.scenePos()
            self.points[self.selected_vertex_index] = pos
            self.update_polygon()
            logger.info(f"Vértice editado: índice {self.selected_vertex_index}, nova posição ({pos.x()}, {pos.y()})")
        elif event.type() == event.GraphicsSceneMouseRelease:
            if hasattr(self, "selected_vertex_index"):
                del self.selected_vertex_index
                logger.info("Edição de vértice concluída.")
        return super(PolygonLogic, self).eventFilter(obj, event)

    def adjust_point_to_rectangle(self, point, rect):
        """
        Ajusta o ponto para ficar dentro ou na borda do retângulo.
        """
        x, y = point.x(), point.y()
        rect_x, rect_y, rect_width, rect_height = rect.x(), rect.y(), rect.width(), rect.height()
        # Limita o ponto às bordas do retângulo
        x = max(rect_x, min(x, rect_x + rect_width))
        y = max(rect_y, min(y, rect_y + rect_height))
        return QPointF(x, y)

    def finalize_polygon(self):
        """
        Finaliza a criação do polígono.
        """
        if len(self.points) < 3:
            logger.error("Polígono inválido: são necessários pelo menos 3 pontos.")
            self.cancel_polygon_creation()
            return
        logger.info("Polígono finalizado com sucesso.")
        self.canvas.scene.removeEventFilter(self)  # Remove o filtro de eventos
        self.is_finalized = True  # Marca o polígono como finalizado
        # Calcula a área do polígono
        polygon_area = self.calculate_polygon_area(self.points)
        logger.info(f"Área do polígono calculada: {polygon_area:.2f} m²")
        # Atualiza o campo "Sobra" na toolbar
        self.toolbar.update_sobra(polygon_area)
        self.points.clear()

    def edit_polygon(self):
        """
        Ativa o modo de edição do último polígono criado.
        """
        if not self.current_polygon or not self.is_finalized:
            logger.error("Nenhum polígono disponível para edição.")
            return
        logger.info("Modo de edição de polígono ativado.")
        self.edit_mode = True
        self.canvas.scene.installEventFilter(self)
        self.draw_vertex_circles()

    def draw_vertex_circles(self):
        """
        Desenha círculos nos vértices do polígono para edição.
        """
        self.vertex_circles.clear()
        polygon = self.current_polygon.polygon()
        for point in polygon:
            circle = QGraphicsEllipseItem(point.x() - 5, point.y() - 5, 10, 10)
            circle.setPen(QPen(Qt.red))
            circle.setBrush(QBrush(Qt.red))
            self.canvas.scene.addItem(circle)
            self.vertex_circles.append(circle)
            logger.info(f"Círculo de edição adicionado no vértice ({point.x()}, {point.y()})")

    def update_polygon(self):
        """
        Atualiza o polígono com base nos novos pontos.
        """
        if not self.current_polygon:
            return
        polygon = QPolygonF(self.points)
        self.current_polygon.setPolygon(polygon)
        self.clear_vertex_circles()
        self.draw_vertex_circles()
        logger.info("Polígono atualizado após edição de vértices.")

    def clear_vertex_circles(self):
        """
        Remove os círculos dos vértices do polígono.
        """
        for circle in self.vertex_circles:
            self.canvas.scene.removeItem(circle)
        self.vertex_circles.clear()
        logger.info("Círculos de edição removidos.")

    def calculate_polygon_area(self, points):
        """
        Calcula a área de um polígono usando a fórmula do determinante.
        :param points: Lista de pontos (QPointF) que formam o polígono.
        :return: Área do polígono em metros quadrados.
        """
        n = len(points)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += points[i].x() * points[j].y()
            area -= points[j].x() * points[i].y()
        area = abs(area) / 2.0
        return area / 1e6  # Converte de mm² para m²

    def cancel_polygon_creation(self):
        """
        Cancela a criação do polígono atual.
        """
        logger.info("Criação de polígono cancelada.")
        if self.current_polygon:
            self.canvas.scene.removeItem(self.current_polygon)
        self.current_polygon = None
        self.points.clear()
        self.canvas.scene.removeEventFilter(self)