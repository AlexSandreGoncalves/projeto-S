import math

def calcular_area_retangulo(comprimento, altura):
    """
    Calcula a área de um retângulo em m².
    :param comprimento: Comprimento do retângulo em milímetros.
    :param altura: Altura do retângulo em milímetros.
    :return: Área do retângulo em metros quadrados.
    """
    return (comprimento / 1000) * (altura / 1000)

def calcular_area_circulo(raio):
    """
    Calcula a área de um círculo em m².
    :param raio: Raio do círculo em milímetros.
    :return: Área do círculo em metros quadrados.
    """
    return math.pi * ((raio / 1000) ** 2)

def calcular_sucata(area_retangulo, area_total_circulos):
    """
    Calcula a área de sucata (área não ocupada pelos círculos) em m².
    :param area_retangulo: Área total do retângulo em metros quadrados.
    :param area_total_circulos: Área total ocupada pelos círculos em metros quadrados.
    :return: Área de sucata em metros quadrados.
    """
    return area_retangulo - area_total_circulos



def calcular_multiplo_ideal(area_retangulo, largura_retangulo, altura_retangulo, largura_objeto, altura_objeto, formato="retangular"):
    """
    Calcula o número máximo de objetos que cabem no retângulo considerando sua forma geométrica.
    :param area_retangulo: Área total do retângulo.
    :param largura_retangulo: Largura do retângulo.
    :param altura_retangulo: Altura do retângulo.
    :param largura_objeto: Largura do objeto.
    :param altura_objeto: Altura do objeto.
    :param formato: Forma geométrica do objeto ("retangular", "circular", "hexagonal").
    :return: Número inteiro de objetos que cabem no retângulo.
    """
    if formato == "retangular":
        # Disposição simples em grade
        colunas = largura_retangulo // largura_objeto
        linhas = altura_retangulo // altura_objeto
        return int(colunas * linhas)
    
    elif formato == "circular":
        # Empacotamento hexagonal otimizado para círculos
        diametro = largura_objeto  # Supondo que largura_objeto seja o diâmetro do círculo
        colunas = largura_retangulo // diametro
        linhas = altura_retangulo // (diametro * 0.866)  # Fator de empacotamento hexagonal
        return int(colunas * linhas)
    
    elif formato == "hexagonal":
        # Empacotamento otimizado para hexágonos
        lado = largura_objeto  # Supondo que largura_objeto seja o lado do hexágono
        colunas = largura_retangulo // (1.5 * lado)
        linhas = altura_retangulo // (math.sqrt(3) * lado)
        return int(colunas * linhas)
    
    else:
        raise ValueError("Formato não suportado. Escolha entre 'retangular', 'circular' ou 'hexagonal'.")
