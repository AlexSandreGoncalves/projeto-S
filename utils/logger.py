import logging

def setup_logger():
    """
    Configura o logger para logs da aplicação.
    :return: Instância do logger configurada.
    """
    logger = logging.getLogger("app_logger")
    logger.setLevel(logging.INFO)
    # Configura o formato do log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Cria um handler para escrever logs no console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    # Adiciona o handler ao logger
    logger.addHandler(console_handler)
    return logger