from circuit_simulator.Element import Element

from circuit_simulator.elements import (
    Resistor, 
    Capacitor,
    Inductor,
    ResistorNonLinear,
    VoltageControlledVoltageSource,
    VoltageSource,
    CurrentSource
)

class Circuit:
    """Base class for circuits."""

    def __init__(self, netlist: list[str]):
        self.elements: list[Element] = []
        self.nodes = 0
        self.extra_lines = 0

        self.netlist = netlist.copy()

    def read_netlist(self) -> None:

        try:
            self.nodes = int(self.netlist[0])
        except:
            raise ValueError(
                "Definição inválida do número de nós. " 
                "O número de nós deve ser definido na primeira linha da netlist como um número inteiro. "
                'Exemplo: linha 1: "3", linha 2: "R1000 1 2 1000", ...'
            )
        
        self.netlist.pop(0) # Remove a primeira linha (número de nós)
        self.netlist.pop(-1) # Remove a última linha (parâmetros de simulação)

        for line in self.netlist:
            element = self.create_element(line, self.nodes)
            self.add_element(element)

    def add_element(self, element: Element) -> None:
        self.elements.append(element)

    def set_extra_lines(self) -> None:
        for element in self.elements:
            if hasattr(element, 'extra_line'):
                self.extra_lines += 1

    def is_nonlinear(self) -> bool:
        for element in self.elements:
            if isinstance(element, ResistorNonLinear):
                return True
        return False

    def update(self, x_t) -> None:
        for element in self.elements:
            element.update(x_t)

    def create_element(self, line:str, num_nodes:int):
        line = line.strip().split()

        if line[0].startswith("R"):
            resistor = Resistor(self, line[0], int(line[1]), int(line[2]), float(line[3]))
            print(resistor, "adicionado com sucesso")
            return resistor
        
        elif line[0].startswith("C"):
            capacitor = Capacitor(self, line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0)
            print(capacitor, "adicionado com sucesso")
            return capacitor
        
        elif line[0].startswith("L"):
            indutor = Inductor(self, line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0)
            print(indutor, "adicionado com sucesso")
            return indutor
        
        elif line[0].startswith("N"):
            resistor_nl = ResistorNonLinear(self, line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]),
                                       float(line[7]), float(line[8]), float(line[9]), float(line[10]))
            print(resistor_nl, "adicionado com sucesso")
            return resistor_nl
        
        elif line[0].startswith("E"):
            fctc = VoltageControlledVoltageSource(self, line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5]))
            print(fctc, "adicionado com sucesso")
            return fctc
        
        elif line[0].startswith("V"):
            if line[3] == "SIN":
                voltage_source = VoltageSource(self, line[0], int(line[1]), int(line[2]), line[3], float(line[4]),float(line[5]),float(line[6]),
                                               float(line[7]),float(line[8]),float(line[9]),float(line[10]))
            else:
                voltage_source = VoltageSource(self, line[0], int(line[1]), int(line[2]), line[3], float(line[4]), None, None, None, None, None, None)
            print(voltage_source, "adicionado com sucesso")
            return voltage_source
        
        elif line[0].startswith("I"):
            current_source = CurrentSource(self, line[0], int(line[1]), int(line[2]), line[3], float(line[4]))
            print(current_source, "adicionado com sucesso")
            return current_source

        else:
            print(f"Elemento desconhecido: {line[0]}")
            return None