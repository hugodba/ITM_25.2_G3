from circuit_simulator.elements import (
    Resistor, 
    Capacitor,
    Inductor,
    ResistorNonLinear,
    VoltageControlledVoltageSource,
    VoltageSource,
    CurrentSource
)
from circuit_simulator import Circuit

class ElementFactory:
    
    @staticmethod
    def create_element(line:str, num_nodes:int):
        line = line.strip().split()

        if line[0].startswith("R"):
            resistor = Resistor(line[0], int(line[1]), int(line[2]), float(line[3]))
            print(resistor, "adicionado com sucesso")
            return resistor
        
        elif line[0].startswith("C"):
            capacitor = Capacitor(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0)
            print(capacitor, "adicionado com sucesso")
            return capacitor
        
        elif line[0].startswith("L"):
            indutor = Inductor(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0, num_nodes + counter_extra_lines + 1)
            Circuit.counter_extra_lines += 1
            print(indutor, "adicionado com sucesso")
            return indutor
        
        elif line[0].startswith("N"):
            resistor_nl = ResistorNonLinear(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]),
                                       float(line[7]), float(line[8]), float(line[9]), float(line[10]))
            print(resistor_nl, "adicionado com sucesso")
            return resistor_nl
        
        elif line[0].startswith("E"):
            fctc = VoltageControlledVoltageSource(line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5]), num_nodes + counter_extra_lines + 1)
            Circuit.counter_extra_lines += 1
            print(fctc, "adicionado com sucesso")
            return fctc
        
        elif line[0].startswith("V"):
            voltage_source = VoltageSource(line[0], int(line[1]), int(line[2]), line[3], float(line[4]), num_nodes + counter_extra_lines + 1)
            Circuit.counter_extra_lines += 1
            print(voltage_source, "adicionado com sucesso")
            return voltage_source
        
        elif line[0].startswith("I"):
            current_source = CurrentSource(line[0],int(line[1]), int(line[2]), line[3], float(line[4]))
            print(current_source, "adicionado com sucesso")
            return current_source

        else:
            print(f"Elemento desconhecido: {line[0]}")
            return None
