import argparse
import numpy as np
import matplotlib.pyplot as plt

from ElementFactory import Element_factory
from Simulation_config import Simulationconfig
from src.circuit_simulator.Circuit import Circuit


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

    answer, step = time_analysis(circuit)

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
    contador_extra_lines = 0

    for line in lines[1:]:
        line = line.split()
        
        if not line and line[0].startswith("*"):  # Ignorar linhas vazias e comentários
            continue

        if line[0] == ".TRAN":
            configuracao = Simulationconfig(float(line[1]), float(line[2]), line[3], float(line[4]),line[5] if len(line) > 5 else None)
            break
        
        element, contador_extra_lines = Element_factory.create_element(line, contador_extra_lines, num_nodes)
        elements.append(element)
    
    return elements, configuracao, num_nodes, contador_extra_lines

def randomize(n):
    return np.random.rand(n)

def time_analysis(circuit:Circuit):
    answer = []
    steps = []
    n_variables = circuit.nodes + circuit.extra_lines

    t = 0.0

    while t <= circuit.config.time_simulation:
        # Ajusta Δt no primeiro passo
        dt = circuit.config.step_simulation / circuit.config.step_factor if t == 0 else circuit.config.step_simulation

        internal_step = 0
        while internal_step <= circuit.config.max_interval_step:
            stop_newton_raphson = False
            n_guesses = 0
            n_newton_raphson = 0

            # chute inicial
            x_t = np.zeros(n_variables)

            while not stop_newton_raphson:
                # Se passou do limite de iterações de Newton
                if n_newton_raphson == circuit.config.N:
                    if n_guesses > circuit.config.M:
                        x_t = randomize(n_variables)  # novo chute
                        n_guesses += 1
                    n_newton_raphson += 1

                Gn = np.zeros((n_variables, n_variables))
                In = np.zeros(n_variables)

                # Montagem das estampas
                for element in circuit.elements:
                    Gn, In = element.add_conductance(Gn, In, dt)

                # Resolve Ax = b
                x_next = np.linalg.solve(Gn, In)

                tolerance = np.max(np.abs(x_next - x_t))

                # Verifica convergência
                if circuit.is_nonlinear() and tolerance > circuit.config.max_tolerance:
                    x_t = x_next.copy()
                    n_newton_raphson += 1
                else:
                    stop_newton_raphson = True

            # Atualiza o circuito para o próximo passo de tempo
            circuit.update(x_next)

            internal_step += 1

        # Armazena resultados deste tempo
        answer.append(x_next.copy())
        steps.append(t)

        t += dt

    return np.array(answer), np.array(steps)

def plot_answer_vs_steps(answer, steps):
    print(answer[0:20])
    # Pega o 5º elemento de cada linha (índice 4)
    y_values = answer[:, 5]  

    # Faz o gráfico
    plt.plot(steps, y_values, label="answer[ :, 5 ] vs time (steps)")
    plt.xlabel("Tempo (steps)")
    plt.ylabel("Valor da 5ª variável (answer[:, 5])")
    plt.title("Resposta no tempo")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
