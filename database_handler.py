import sqlite3
import logging

# Configurar logger
logger = logging.getLogger("app_logger")


class DatabaseHandler:
    def __init__(self, db_path="banco_de_dados.db"):
        """
        Inicializa o manipulador do banco de dados.
        :param db_path: Caminho para o arquivo do banco de dados SQLite.
        """
        self.db_path = db_path

    def conectar_bd(self):
        """
        Conecta ao banco de dados SQLite.
        :return: Conexão ao banco de dados ou None em caso de erro.
        """
        try:
            conexao = sqlite3.connect(self.db_path)
            logger.info("Conexão ao banco de dados estabelecida com sucesso.")
            return conexao
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {e}")
            return None

    def buscar_peca_por_codigo(self, codigo):
        """
        Busca uma peça no banco de dados pelo código.
        :param codigo: Código da peça a ser buscada.
        :return: Dicionário com os dados da peça ou None se não encontrado.
        """
        conexao = self.conectar_bd()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute("SELECT comprimento, largura FROM pecas WHERE cod_peca = ?", (codigo,))
                resultado = cursor.fetchone()
                if resultado:
                    comprimento, largura = resultado
                    logger.info(f"Dados encontrados para o código {codigo}: Comprimento={comprimento}, Largura={largura}")
                    return {"comprimento": comprimento, "largura": largura}
                else:
                    logger.warning(f"Nenhum registro encontrado para o código: {codigo}")
                    return None
            except Exception as e:
                logger.error(f"Erro ao consultar o banco de dados: {e}")
            finally:
                conexao.close()
        return None