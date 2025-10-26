from src.circuit_simulator.Element import Element
from src.circuit_simulator.elements.Resistor import Resistor
from src.circuit_simulator.elements.Capacitor import Capacitor
from src.circuit_simulator.elements.Indutor import Indutor

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
            resistor_nl = Resistor_nl(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4]))
        else:
            print(f"Elemento desconhecido: {line[0]}")
