import unittest
from PyQt5.QtWidgets import QApplication
from ui.canvas import Canvas
from rendering.renderer import Renderer
from logic.object_manager import ObjectManager

class TestCanvas(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicializa a aplicação PyQt para os testes."""
        cls.app = QApplication([])

    def setUp(self):
        """Configura o ambiente de teste."""
        self.object_manager = ObjectManager()
        self.renderer = Renderer(self.object_manager)
        self.canvas = Canvas(self.renderer)

    def test_draw_rectangle(self):
        """Testa a criação de um retângulo no canvas."""
        self.canvas.draw_rectangle((50, 50), 200, 100)
        self.assertIsNotNone(self.canvas.current_rectangle, "O retângulo não foi criado.")
        self.assertEqual(self.canvas.get_scale_factor(), 1.0, "O fator de escala inicial deve ser 1.0.")

    def test_draw_circle(self):
        """Testa a criação de um círculo no canvas."""
        self.canvas.draw_rectangle((50, 50), 200, 100)  # Cria um retângulo primeiro
        self.canvas.draw_circle(20)
        self.assertTrue(hasattr(self.canvas, "current_circle"), "O círculo não foi criado.")

    def test_distribute_circles(self):
        """Testa a distribuição de círculos dentro de um retângulo."""
        self.canvas.draw_rectangle((50, 50), 200, 100)  # Cria um retângulo primeiro
        self.canvas.distribute_circles(10)
        items = self.canvas.scene.items()
        self.assertGreater(len(items), 1, "Os círculos não foram distribuídos corretamente.")

    def test_clear_scene(self):
        """Testa a limpeza do canvas."""
        self.canvas.draw_rectangle((50, 50), 200, 100)
        self.canvas.clear_scene()
        items = self.canvas.scene.items()
        self.assertEqual(len(items), 0, "O canvas não foi limpo corretamente.")

if __name__ == "__main__":
    unittest.main()