
from circuit_simulator import Circuit
import numpy as np

class Simulation:
    """Class representing a circuit simulation."""
    
    def time_analysis(self,circuit:Circuit):

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
                            x_t = np.random.rand(n_variables)  # novo chute
                            n_guesses += 1
                        n_newton_raphson += 1

                    Gn = np.zeros((n_variables, n_variables))
                    In = np.zeros(n_variables)

                    # Montagem das estampas
                    for element in circuit.elements:
                        Gn, In = element.add_conductance(Gn, In, x_t, dt)

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
