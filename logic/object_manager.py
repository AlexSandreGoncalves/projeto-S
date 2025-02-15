import json
import logging
from typing import List, Dict, Any
import os

# Configurar logger
logger = logging.getLogger("app_logger")


class ObjectManager:
    def __init__(self):
        """
        Inicializa o gerenciador de objetos.
        """
        self.objects: List[Dict[str, Any]] = []  # Lista para armazenar objetos com metadados
        self.config_file = "objects.json"  # Arquivo para persistir os dados
        self.load_saved_objects()  # Carrega os objetos salvos
        logger.info("ObjectManager inicializado com sucesso.")

    def load_saved_objects(self):
        """
        Carrega os objetos salvos do arquivo de configuração.
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as file:
                    self.objects = json.load(file)
                    logger.info(f"{len(self.objects)} objetos carregados do arquivo.")
            except Exception as e:
                logger.error(f"Erro ao carregar objetos salvos: {e}")

    def save_objects(self):
        """
        Salva os objetos atuais no arquivo de configuração.
        """
        try:
            with open(self.config_file, "w") as file:
                json.dump(self.objects, file, indent=4)
                logger.info(f"{len(self.objects)} objetos salvos no arquivo.")
        except Exception as e:
            logger.error(f"Erro ao salvar objetos: {e}")

    def add_object(self, obj_type: str, data: Dict[str, Any]):
        """
        Adiciona um novo objeto à lista.
        :param obj_type: Tipo do objeto (ex.: "rectangle", "circle", "polygon").
        :param data: Dados do objeto (ex.: dimensões, coordenadas).
        """
        obj = {"type": obj_type, "data": data}
        self.objects.append(obj)
        self.save_objects()
        logger.info(f"Objeto adicionado: tipo={obj_type}, dados={data}")

    def remove_object(self, index: int):
        """
        Remove um objeto da lista pelo índice.
        :param index: Índice do objeto a ser removido.
        """
        if 0 <= index < len(self.objects):
            removed_obj = self.objects.pop(index)
            self.save_objects()
            logger.info(f"Objeto removido: {removed_obj}")
        else:
            logger.error(f"Índice inválido para remoção: {index}")

    def clear_objects(self):
        """
        Limpa todos os objetos da lista.
        """
        self.objects.clear()
        self.save_objects()
        logger.info("Todos os objetos foram removidos.")

    def get_objects(self) -> List[Dict[str, Any]]:
        """
        Retorna a lista de objetos.
        :return: Lista de objetos.
        """
        return self.objects

    def count_objects(self) -> int:
        """
        Retorna o número total de objetos.
        :return: Contagem de objetos.
        """
        return len(self.objects)

    def get_object_by_type(self, obj_type: str) -> List[Dict[str, Any]]:
        """
        Retorna uma lista de objetos de um tipo específico.
        :param obj_type: Tipo de objeto a ser filtrado.
        :return: Lista de objetos do tipo especificado.
        """
        return [obj for obj in self.objects if obj["type"] == obj_type]

    def render_objects(self, renderer):
        """
        Renderiza todos os objetos usando o renderizador fornecido.
        :param renderer: Instância do renderizador.
        """
        for obj in self.objects:
            renderer.render(obj)
            logger.info(f"Renderizando objeto: {obj}")