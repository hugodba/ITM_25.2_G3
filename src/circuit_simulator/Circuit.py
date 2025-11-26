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
        self.elements: list[Element] = []
        self.nodes = 0
        self.extra_lines = 0
        self.netlist = netlist.copy() if netlist else []

    def read_netlist(self) -> None:
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

    def add_element(self, element: Element) -> None:
        if element is not None:
            self.elements.append(element)

    def set_extra_lines(self) -> None:
        self.extra_lines = 0
        for element in self.elements:
            if hasattr(element, 'extra_line') and element.extra_line:
                self.extra_lines += 1

    def is_nonlinear(self) -> bool:
        for element in self.elements:
            if isinstance(element, (ResistorNonLinear, Diode, Mosfet)):
                return True
        return False

    def update(self, x_t):
        self.x = x_t.copy()
        for element in self.elements:
            element.update(x_t)

    def create_element(self, line: str, num_nodes: int):
        line = line.strip().split()

        if line[0].startswith("R"):
            return Resistor(self, line[0], int(line[1]), int(line[2]), float(line[3]))

        elif line[0].startswith("C"):
            capacitance = float(line[3])
            ic = float(line[4].split("=")[1]) if len(line) > 4 else 0.0
            return Capacitor(self, line[0], int(line[1]), int(line[2]), capacitance, ic)

        elif line[0].startswith("L"):
            inductance = float(line[3])
            ic = float(line[4].split("=")[1]) if len(line) > 4 else 0.0
            return Inductor(self, line[0], int(line[1]), int(line[2]), inductance, ic)

        elif line[0].startswith("N"):
            return ResistorNonLinear(
                self, line[0],
                int(line[1]), int(line[2]),
                float(line[3]), float(line[4]), float(line[5]),
                float(line[6]), float(line[7]), float(line[8]),
                float(line[9]), float(line[10])
            )

        elif line[0].startswith("E"):
            return VoltageControlledVoltageSource(
                self, line[0],
                int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5])
            )

        elif line[0].startswith("V"):
            if line[3] == "SIN":
                return VoltageSINSource(
                    self, line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]), int(line[10])
                )
            elif line[3] == "PULSE":
                return VoltagePulseSource(
                    self, line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]),
                    float(line[10]), float(line[11])
                )
            else:
                return VoltageDCSource(self, line[0], int(line[1]), int(line[2]), line[3], float(line[4]))

        elif line[0].startswith("I"):
            if line[3] == "SIN":
                return CurrentSINSource(
                    self, line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]), int(line[10])
                )
            elif line[3] == "PULSE":
                return CurrentPulseSource(
                    self, line[0], int(line[1]), int(line[2]), line[3],
                    float(line[4]), float(line[5]), float(line[6]),
                    float(line[7]), float(line[8]), float(line[9]),
                    float(line[10]), float(line[11])
                )
            else:
                return CurrentDCSource(self, line[0], int(line[1]), int(line[2]), line[3], float(line[4]))

        elif line[0].startswith("F"):
            return CurrentControlledCurrentSource(self, line[0], int(line[1]), int(line[2]), int(line[3]), float(line[4]), num_nodes)

        elif line[0].startswith("G"):
            return VoltageControlledCurrentSource(self, line[0], int(line[1]), int(line[2]), int(line[3]), float(line[4]), num_nodes)

        elif line[0].startswith("H"):
            return CurrentControlledVoltageSource(self, line[0], int(line[1]), int(line[2]), int(line[3]), float(line[4]), num_nodes)

        elif line[0].startswith("O"):
            return OperationalAmplifier(self, line[0], int(line[1]), int(line[2]), int(line[3]))

        elif line[0].startswith("D"):
            return Diode(self, line[0], int(line[1]), int(line[2]))

        elif line[0].startswith("M"):
            return Mosfet(self, line[0], int(line[1]), int(line[2]), int(line[3]),line[4], float(line[5]), float(line[6]), float(line[7]),float(line[8]), float(line[9]))

        else:
            print(f"Elemento desconhecido: {line[0]}")
            return None
