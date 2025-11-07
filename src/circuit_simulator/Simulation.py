
from circuit_simulator import Circuit
import numpy as np

class Simulation:
    """Class representing a circuit simulation."""

    def __init__(self, netlist: list[str] = None):
        self.config = {
            "analysis_type": None,
            "time_simulation": None,
            "step_simulation": None,
            "integration_method": None,
            "internal_steps": None,

            "step_factor": 1000,
            "N": 40,
            "M": 100,
            "max_tolerance": 1e-3,
            "initial_conditions": None,
        }

        self.netlist = netlist.copy()

    def read_netlist(self) -> None:
        def extract_and_validate_parameters_sim(cleaned_content: list[str]) -> tuple:
            """Lida e valida os parâmetros de simulação extraídos da netlist."""

            sim_config = cleaned_content[-1].split()
            analysis_type = sim_config[0]

            match analysis_type:
                
                case ".TRAN":
                    print("Análise transiente detectada.")

                    try:
                        analysis_type, time_simulation, step_simulation, integration_method, internal_steps = sim_config[0:5] # ignore 'UIC' if present
                    except:
                        raise ValueError(
                            "Definição inválida dos parâmetros de simulação. " 
                            "Os parâmetros de simulação transiente devem ser inseridos na "
                            "última linha da netlist, no formato:\n"
                            '\t.TRAN <tempo_total(float)> <step_time(float)> '
                            '<metodo_integracao(str)> <n_internal_steps(int)>\n'
                        )

                    if analysis_type != ".TRAN":
                        raise ValueError(
                            "Definição inválida dos parâmetros de simulação. " 
                            "Os parâmetros de simulação devem começar com '.TRAN'."
                        )

                    try:
                        time_simulation = float(time_simulation)
                        step_simulation = float(step_simulation)
                        internal_steps = float(internal_steps)
                    except:
                        raise ValueError(
                            "Definição inválida dos parâmetros de simulação. " 
                            "O tempo total e o passo de tempo devem ser números "
                            "reais e o número de steps deve ser um inteiro."
                        )

                    if integration_method not in ["BE", "FE", "TRAP"]:
                        raise ValueError(
                            "Método de integração inválido. "
                            "Opções válidas: 'BE', 'FE', 'TRAP'."
                        )
                    
                    return analysis_type, time_simulation, step_simulation, integration_method, internal_steps
                
                case ".AC":
                    print("Análise AC detectada.")
                    raise NotImplementedError("Análise AC ainda não implementada.")

                case _:
                    raise ValueError(
                        "Tipo de análise desconhecido. "
                    )

        (
            self.config['analysis_type'],
            self.config['time_simulation'],
            self.config['step_simulation'],
            self.config['integration_method'],
            self.config['internal_steps']
        ) = extract_and_validate_parameters_sim(self.netlist)
    
    def time_analysis(self, circuit: Circuit):

        answer = []
        steps = []
        n_variables = circuit.nodes + circuit.extra_lines

        t = 0.0

        while t <= self.config['time_simulation']:
            # Ajusta Δt no primeiro passo
            dt = self.config['step_simulation'] / self.config['step_factor'] if t == 0 else self.config['step_simulation']

            internal_step = 0
            while internal_step <= self.config['internal_steps']:
                stop_newton_raphson = False
                n_guesses = 0
                n_newton_raphson = 0

                # chute inicial
                x_t = np.zeros(n_variables + 1)

                while not stop_newton_raphson:
                    # Se passou do limite de iterações de Newton
                    if n_newton_raphson == self.config['N']:
                        if n_guesses > self.config['M']:
                            x_t = np.random.rand(n_variables)  # novo chute
                            n_guesses += 1
                        n_newton_raphson += 1

                    Gn = np.zeros((n_variables + 1, n_variables + 1))
                    In = np.zeros(n_variables + 1)

                    # Montagem das estampas
                    for element in circuit.elements:
                        Gn, In = element.add_conductance(Gn, In, x_t, dt, self.config['integration_method'],t)

                    # Resolve Ax = b
                    try:
                        x_next = np.linalg.solve(Gn[1:,1:], In[1:])
                        x_next = np.insert(x_next, 0, 0.0)  # Insere o valor do nó terra 

                    except np.linalg.LinAlgError:
                        raise ValueError("Matriz de condutância singular.")

                    tolerance = np.max(np.abs(x_next - x_t))

                    # Verifica convergência
                    if circuit.is_nonlinear() and tolerance > self.config['max_tolerance']:
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
            
        return np.array(answer)[1:,1:], np.array(steps)[1:]
