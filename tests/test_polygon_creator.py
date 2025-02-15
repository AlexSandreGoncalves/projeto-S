import unittest
from PyQt5.QtCore import QPointF
from ui.canvas import Canvas
from ui.polygon_creator import PolygonCreator
from logic.object_manager import ObjectManager
from rendering.renderer import Renderer

class TestPolygonCreator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicializa a aplicação PyQt para os testes."""
        cls.app = QApplication([])

    def setUp(self):
        """Configura o ambiente de teste."""
        self.object_manager = ObjectManager()
        self.renderer = Renderer(self.object_manager)
        self.canvas = Canvas(self.renderer)
        self.toolbar = None  # Simula uma toolbar simples
        self.polygon_creator = PolygonCreator(self.canvas, self.toolbar)

    def test_start_polygon_creation(self):
        """Testa o início da criação de um polígono."""
        self.polygon_creator.start_polygon_creation()
        self.assertEqual(len(self.polygon_creator.points), 0, "Os pontos do polígono não foram reiniciados.")

    def test_add_points(self):
        """Testa a adição de pontos ao polígono."""
        self.polygon_creator.start_polygon_creation()
        self.polygon_creator.points.append(QPointF(0, 0))
        self.polygon_creator.points.append(QPointF(100, 0))
        self.assertEqual(len(self.polygon_creator.points), 2, "Os pontos não foram adicionados corretamente.")

    def test_finalize_polygon(self):
        """Testa a finalização de um polígono válido."""
        self.polygon_creator.start_polygon_creation()
        self.polygon_creator.points.append(QPointF(0, 0))
        self.polygon_creator.points.append(QPointF(100, 0))
        self.polygon_creator.points.append(QPointF(100, 100))
        self.polygon_creator.finalize_polygon()
        self.assertTrue(self.polygon_creator.is_finalized, "O polígono não foi finalizado corretamente.")

    def test_invalid_polygon(self):
        """Testa a finalização de um polígono inválido."""
        self.polygon_creator.start_polygon_creation()
        self.polygon_creator.points.append(QPointF(0, 0))
        self.polygon_creator.points.append(QPointF(100, 0))
        self.polygon_creator.finalize_polygon()
        self.assertFalse(self.polygon_creator.is_finalized, "Um polígono inválido foi finalizado.")

    def test_calculate_polygon_area(self):
        """Testa o cálculo da área de um polígono."""
        points = [QPointF(0, 0), QPointF(100, 0), QPointF(100, 100)]
        area = self.polygon_creator.calculate_polygon_area(points)
        self.assertAlmostEqual(area, 0.01, places=4, msg="A área do polígono foi calculada incorretamente.")

if __name__ == "__main__":
    unittest.main()