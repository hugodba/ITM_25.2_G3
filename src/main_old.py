import argparse
import matplotlib.pyplot as plt

from circuit_simulator.ElementFactory import Element_factory
from circuit_simulator import SimulationConfig, Simulation, Circuit


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

    lines_elements, configuracao, num_nodes, contador_linhas_extras = process_lines(elements)

    circuit = Circuit(num_nodes)
    for element in lines_elements:
        circuit.add_element(element)
    
    circuit.extra_lines = contador_linhas_extras
    circuit.set_config(configuracao)

    simulation = Simulation()
    try:
        answer, step = simulation.time_analysis(circuit)
    except ValueError as e:
        print(f"Erro durante a simulação: {e}")
        return

    plot_answer_vs_steps(answer, step)


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
    num_nodes = int(lines[0])
    print(f"Número de nós no circuito: {num_nodes}")
    counter_extra_lines = 0

    for line in lines[1:]:
        line = line.split()
        
        if not line and line[0].startswith("*"):  # Ignorar linhas vazias e comentários
            continue

        if line[0] == ".TRAN":
            configuracao = SimulationConfig(float(line[1]), float(line[2]), line[3], float(line[4]),line[5] if len(line) > 5 else None)
            break
        
        element, counter_extra_lines = Element_factory.create_element(line, counter_extra_lines, num_nodes)
        elements.append(element)
    
    return elements, configuracao, num_nodes, counter_extra_lines

def plot_answer_vs_steps(answer, steps):
    
    x_values = answer[:, 0]  # plot do nó 1 (índice 1)
    y_values = answer[:, 5]  # plot do nó 6 (índice 6)

    # Faz o gráfico
    #plt.plot(x_values, y_values, label="node1 vs node2") # plot teste chua.net
    plt.plot(steps, y_values, label="node6 vs time") # plot node x pelo tempo
    plt.xlabel("Node 1 (V)")
    plt.ylabel("Node 2 (V)")
    plt.title("Resposta no tempo")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
