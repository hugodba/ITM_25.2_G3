
from src.circuit_simulator.Element import Element
from src.circuit_simulator.elements.Resistor import Resistor
from src.circuit_simulator.elements.Capacitor import Capacitor
from src.circuit_simulator.elements.Indutor import Indutor
from src.circuit_simulator.elements.Resistor_nl import Resistor_nl
from src.circuit_simulator.elements.FTCT import FTCT

class Element_factory:
    @staticmethod
    def create_element(line):
        if line[0].startswith("R"):
            resistor = Resistor(line[0], int(line[1]), int(line[2]), float(line[3]))
            print(resistor)
        elif line[0].startswith("C"):
            capacitor = Capacitor(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0)
            print(capacitor)
        elif line[0].startswith("L"):
            indutor = Indutor(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0)
            print(indutor)
        elif line[0].startswith("N"):
            resistor_nl = Resistor_nl(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]),
                                       float(line[7]), float(line[8]), float(line[9]), float(line[10]))
            print(resistor_nl)
        elif line[0].startswith("E"):
            fctc = FTCT(line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5]))
            print(fctc)
        else:
            print(f"Elemento desconhecido: {line[0]}")
