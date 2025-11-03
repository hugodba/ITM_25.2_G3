from circuit_simulator.elements import ResistorNonLinear
from circuit_simulator import Element
from circuit_simulator.ElementFactory import ElementFactory

class Circuit:
    """Base class for circuits."""

    def __init__(self, netlist_path: str):
        self.elements: list[Element] = []
        self.nodes = 0
        self.extra_lines = 0
        self.netlist = None

        self.netlist_path = netlist_path
       
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

    def read_netlist(self) -> None:
        def clean_netlist(content: list[str]) -> list[str]:
            """Remove comentários e linhas em branco do conteúdo da netlist.

            Args:
                content (list): Conteúdo completo do arquivo de netlist em formato "readlines".

            Returns:
                list: Conteúdo limpo da netlist.
            """
            cleaned_content = []

            for line in content:
                if line[0] == "" or line[0] == "\n" or line[0] == "*":
                    continue
                cleaned_content.append(line.strip("\n "))

            return cleaned_content
        
        def extract_and_validate_parameters_sim(cleaned_content: list[str]) -> tuple:
            """Lida e valida os parâmetros de simulação extraídos da netlist."""

            try:
                n = int(cleaned_content[0])
            except:
                raise ValueError(
                    "Definição inválida do número de nós. " 
                    "O número de nós deve ser definido na primeira linha da netlist como um número inteiro. "
                    'Exemplo: linha 1: "3", linha 2: "R1000 1 2 1000", ...'
                )
            
            sim_config = cleaned_content[-1].split(" ")
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
                        internal_steps = int(internal_steps)
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
                    
                    return n, analysis_type, time_simulation, step_simulation, integration_method, internal_steps
                
                case ".AC":
                    print("Análise AC detectada.")
                    raise NotImplementedError("Análise AC ainda não implementada.")

                case _:
                    raise ValueError(
                        "Tipo de análise desconhecido. "
                    )

        try:
            with open(self.netlist_path) as netfile:
                content = netfile.readlines()
        except:
            raise ValueError("Erro. Caminho da netlist inválido.")
        
        cleaned_content = clean_netlist(content)

        (
            self.nodes,
            self.config['analysis_type'],
            self.config['time_simulation'],
            self.config['step_simulation'],
            self.config['integration_method'],
            self.config['internal_steps']
        ) = extract_and_validate_parameters_sim(cleaned_content)

        cleaned_content.pop(0) # Remove a primeira linha (número de nós)
        cleaned_content.pop(-1) # Remove a última linha (parâmetros de simulação)

        counter_extra_lines = 0
        for line in cleaned_content:
            element, counter_extra_lines = ElementFactory.create_element(line, counter_extra_lines, self.nodes)
            self.add_element(element)

        self.extra_lines = counter_extra_lines               

    def add_element(self, element: Element) -> None:
        self.elements.append(element)

    def is_nonlinear(self) -> bool:
        for element in self.elements:
            if isinstance(element, ResistorNonLinear):
                return True
        return False

    def update(self, x_t) -> None:
        for element in self.elements:
            element.update(x_t)

    
    def generate_netlist(self) -> str:
        """Generate a netlist representation of the circuit."""
        # TODO: Implement netlist generation
        # iterate over self.elements and create netlist lines
        # self.netlist = generated_netlist_string
        pass
    
    def export_netlist(self) -> str:
        """Export the circuit to a netlist file."""
        # TODO: Implement export functionality
        # read from self.netlist and write to self.netlist_path
        pass
