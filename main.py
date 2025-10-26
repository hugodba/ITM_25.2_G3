import argparse
import numpy as np

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
        "tempo_total": float(line[1]),
        "passo_sim": float(line[2]),
        "metodo": line[3],
        "num_passos_internos": int(line[4]),
        "condicoes_iniciais": line[5] if len(line) > 5 else None
    }

    print(f"Configuração da simulação: {configuracao}")
    return configuracao

def time_analysis(circuit, n_variables, step_factor, N, M, max_tolerance, configuracao):
    answer = []
    steps = []
    tmax = configuracao["tempo_total"]
    step_time = configuracao["passo_sim"]
    max_internal_step = configuracao["num_passos_internos"]

    t = 0.0

    while t <= tmax:
        # Ajusta Δt no primeiro passo
        dt = step_time / step_factor if t == 0 else step_time

        internal_step = 0
        while internal_step <= max_internal_step:
            stop_newton_raphson = False
            n_guesses = 0
            n_newton_raphson = 0

            # chute inicial
            x_t = zeros_vector(n_variables)

            while not stop_newton_raphson:
                # Se passou do limite de iterações de Newton
                if n_newton_raphson == N:
                    if n_guesses > M:
                        x_t = randomize(n_variables)  # novo chute
                        n_guesses += 1
                    n_newton_raphson += 1

                Gn = np.zeros([n_variables, n_variables])
                In = np.zeros([n_variables, n_variables])

                # Montagem das estampas
                for element in circuit.elements:
                    A, b = stamp(element, A, b, x_t)

                # Resolve Ax = b
                x_next = solve(A, b, x_t)

                tolerance = np.max(np.abs(x_next - x_t))

                # Verifica convergência
                if circuit.is_nonlinear() and tolerance > max_tolerance:
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

if __name__ == "__main__":
    main()
