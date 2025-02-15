# db_manager.py
import sqlite3
from PyQt5.QtWidgets import QMessageBox

def conectar_bd():
    """Conecta ao banco de dados SQLite."""
    try:
        conexao = sqlite3.connect("peças.db")
        return conexao
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

def buscar_peca_por_codigo(cod_peca):
    """Busca uma peça pelo código no banco de dados."""
    conexao = conectar_bd()
    if not conexao:
        return None

    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT cod_peca, comprimento, largura FROM pecas WHERE cod_peca = ?", (cod_peca,))
        dado = cursor.fetchone()
        return dado
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Erro", f"Erro ao buscar peça: {e}")
    finally:
        conexao.close()

def buscar_todas_pecas():
    """Busca todas as peças no banco de dados."""
    conexao = conectar_bd()
    if not conexao:
        return []

    cursor = conexao.cursor()
    try:
        cursor.execute("SELECT cod_peca, comprimento, largura FROM pecas")
        dados = cursor.fetchall()
        return dados
    except sqlite3.Error as e:
        QMessageBox.critical(None, "Erro", f"Erro ao buscar peças: {e}")
    finally:
        conexao.close()