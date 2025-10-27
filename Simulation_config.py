
class Simulationconfig:
    def __init__(self, time_simulation, step_simulation, analysis_type,max_interval_step
                 ,initial_conditions=None, step_factor=1000, N=40, M=100, max_tolerance=1e-3):
        self.time_simulation = time_simulation
        self.step_simulation = step_simulation
        self.max_interval_step = max_interval_step
        self.analysis_type = analysis_type
        self.step_factor = step_factor
        self.N = N
        self.M = M
        self.max_tolerance = max_tolerance
        self.initial_conditions = initial_conditions


    def __str__(self):
        return (f"Tempo de Simulação: {self.time_simulation}, "
                f"Passo de Simulação: {self.step_simulation}, "
                f"Máximo de Passos Internos: {self.max_interval_step}, "
                f"Tipo de Análise: {self.analysis_type}, "
                f"Fator de Passo: {self.step_factor}, "
                f"N: {self.N}, M: {self.M}, "
                f"Tolerância Máxima: {self.max_tolerance}")
    