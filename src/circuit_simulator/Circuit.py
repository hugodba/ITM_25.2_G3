from circuit_simulator.Element import Element

from circuit_simulator.elements import (
    CurrentControlledCurrentSource,
    CurrentControlledVoltageSource,
    Resistor, 
    Capacitor,
    Inductor,
    ResistorNonLinear,
    VoltageControlledCurrentSource,
    VoltageControlledVoltageSource,
    VoltagePulseSource,
    VoltageSINSource,
    VoltageDCSource,
    CurrentDCSource,
    CurrentSINSource,
    CurrentPulseSource,
    OperationalAmplifier,
    Diode,
    Mosfet
)

class Circuit:
    """Base class for circuits."""

    def __init__(self, netlist: list[str]):
        '''Initialize the Circuit with a netlist.'''

        self.elements: list[Element] = []
        self.nodes = 0
        self.extra_lines = 0
        self.netlist = netlist.copy() if netlist else []

    def read_netlist(self) -> None:
        """Read the netlist and create circuit elements."""

        # Número de nós
        try:
            self.nodes = int(self.netlist[0])
        except:
            raise ValueError(
                "Definição inválida do número de nós. Deve ser um inteiro na primeira linha da netlist."
            )

        # Remove primeira e última linha
        self.netlist.pop(0)
        self.netlist.pop(-1)

        for line in self.netlist:
            element = self.create_element(line, self.nodes)
            self.add_element(element)

        self.set_extra_lines()

    def __iadd__(self, element: Element) -> "Circuit":
        '''Add an element to the circuit.'''
        if element is None:
            return self
        
        element.parent_circuit = self
        self.elements.append(element)

        element.on_add()

        return self
    
    def add_element(self, element: Element) -> None:
        '''Just a wrapper for += operator.'''
        self += element

    def set_extra_lines(self) -> None:
        '''Set the number of extra lines required by certain elements.'''

        self.extra_lines = 0
        for element in self.elements:
            if hasattr(element, 'extra_line') and element.extra_line:
                self.extra_lines += 1

    def is_nonlinear(self) -> bool:
        '''Check if the circuit contains any nonlinear elements.'''

        for element in self.elements:
            if isinstance(element, (ResistorNonLinear, Diode, Mosfet)):
                return True
        return False

    def update(self, x_t: list[float]) -> None:
        '''Update the state of all elements in the circuit.'''

        self.x = x_t.copy()
        for element in self.elements:
            element.update(x_t)

    def create_element(self, line: str, num_nodes: int) -> Element:
        """Create an element from a netlist line."""
        
        line = line.strip().split()

        if line[0].startswith("R"):
            return Resistor(line[0], int(line[1]), int(line[2]), float(line[3]))

        elif line[0].startswith("C"):
            capacitance = float(line[3])
            ic = float(line[4].split("=")[1]) if len(line) > 4 else 0.0
            return Capacitor(line[0], int(line[1]), int(line[2]), capacitance, ic)

        elif line[0].startswith("L"):
            inductance = float(line[3])
            ic = float(line[4].split("=")[1]) if len(line) > 4 else 0.0
            return Inductor(line[0], int(line[1]), int(line[2]), inductance, ic)

        elif line[0].startswith("N"):
            return ResistorNonLinear(
                line[0],
                int(line[1]), int(line[2]),
                float(line[3]), float(line[4]), float(line[5]),
                float(line[6]), float(line[7]), float(line[8]),
                float(line[9]), float(line[10])
            )

        elif line[0].startswith("E"):
            return VoltageControlledVoltageSource(
                line[0],
                int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            )

        elif line[0].startswith("V"):
            if line[3] == "SIN":
                return VoltageSINSource(
                    line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]), int(line[10])
                )
            elif line[3] == "PULSE":
                return VoltagePulseSource(
                    line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]),
                    float(line[10]), float(line[11])
                )
            else:
                return VoltageDCSource(line[0], int(line[1]), int(line[2]), line[3], float(line[4]))

        elif line[0].startswith("I"):
            if line[3] == "SIN":
                return CurrentSINSource(
                    line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]), int(line[10])
                )
            elif line[3] == "PULSE":
                return CurrentPulseSource(
                    line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]),
                    float(line[10]), float(line[11])
                )
            else:
                return CurrentDCSource(self, line[0], int(line[1]), int(line[2]), line[3], float(line[4]))

        elif line[0].startswith("F"):
            return CurrentControlledCurrentSource(line[0], int(line[1]), int(line[2]), int(line[3]), float(line[4]), num_nodes)

        elif line[0].startswith("G"):
            return VoltageControlledCurrentSource(line[0], int(line[1]), int(line[2]), int(line[3]), float(line[4]), num_nodes)

        elif line[0].startswith("H"):
            return CurrentControlledVoltageSource(line[0], int(line[1]), int(line[2]), int(line[3]), float(line[4]), num_nodes)

        elif line[0].startswith("O"):
            return OperationalAmplifier(line[0], int(line[1]), int(line[2]), int(line[3]))

        elif line[0].startswith("D"):
            return Diode(line[0], int(line[1]), int(line[2]))

        elif line[0].startswith("M"):
            return Mosfet(line[0], int(line[1]), int(line[2]), int(line[3]),line[4], float(line[5]), float(line[6]), float(line[7]),float(line[8]), float(line[9]))

        else:
            print(f"Elemento desconhecido: {line[0]}")
            return None
