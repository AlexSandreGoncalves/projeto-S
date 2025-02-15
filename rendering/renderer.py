from PyQt5.QtCore import QObject

class Renderer(QObject):
    def __init__(self, object_manager):
        """
        Inicializa o renderizador.
        :param object_manager: Gerenciador de objetos para manipulação de dados.
        """
        super().__init__()
        self.object_manager = object_manager

    def render(self):
        """Renderiza os objetos no canvas."""
        for obj in self.object_manager.get_objects():
            print(f"Renderizando objeto: {obj}")