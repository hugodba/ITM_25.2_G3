import argparse

from ElementFactory import Element_factory


def main():
    # Criar o parser de argumentos
    parser = argparse.ArgumentParser(description="Programa que lê um arquivo netlist de um circuito e executa calculos.")

    # Adicionar o argumento --netlist
    parser.add_argument(
        "--netlist",
        type=str,
        required=True,   # Torna obrigatório
        help="Caminho para o arquivo .txt do netlist"
    )

    # Fazer o parse dos argumentos digitados
    args = parser.parse_args()

    # Acessar o caminho do arquivo passado pelo usuário
    netlist_path = args.netlist
    print(f"Lendo arquivo netlist em: {netlist_path}")

    elements = elements_from_netlist(netlist_path)
    #print(f"Elementos lidos do netlist: {elements}")

    process_lines(elements)

def elements_from_netlist(netlist_path):
    """Função fictícia para ilustrar a leitura de elementos do netlist."""
    elements = []
    with open(netlist_path, "r") as file:
        for line in file:
            line = line.strip()
            elements.append(line)  # Aqui você pode criar objetos de elementos reais
    return elements

def process_lines(lines):
    elements = []
    numero_nos = int(lines[0])
    print(f"Número de nós no circuito: {numero_nos}")

    for line in lines[1:]:
        line = line.split()
        
        if line and not line[0].startswith("*"):  # Ignorar linhas vazias e comentários
            elements.append(line)  # Aqui você pode criar objetos de elementos reais

        if line[0] == ".TRAN":
            configuracao = parametros_simulacao(line)
            break
        
        Element_factory.create_element(line)
    
    return elements

def parametros_simulacao(line):

    configuracao = {
        "tempo_total": line[1],
        "passo_sim": float(line[2]),
        "metodo": line[3],
        "iteracoes": int(line[4]),
        "condicoes_iniciais": line[5] if len(line) > 5 else None
    }

    print(f"Configuração da simulação: {configuracao}")
    return configuracao


if __name__ == "__main__":
    main()
