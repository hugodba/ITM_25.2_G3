from circuit_simulator.elements import Resistor, Capacitor, Indutor, ResistorNL, FTCT

class Element_factory:
    @staticmethod
    def create_element(line, contador_extra_lines, num_nodes):
        if line[0].startswith("R"):
            resistor = Resistor(line[0], int(line[1]), int(line[2]), float(line[3]))
            print(resistor, "adicionado com sucesso")
            return resistor, contador_extra_lines
            
        elif line[0].startswith("C"):
            capacitor = Capacitor(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0)
            print(capacitor, "adicionado com sucesso")
            return capacitor, contador_extra_lines
        elif line[0].startswith("L"):
            indutor = Indutor(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4].split("=")[1]) if len(line) > 4 else 0.0, num_nodes + contador_extra_lines)
            contador_extra_lines += 1
            print(indutor, "adicionado com sucesso")
            return indutor , contador_extra_lines
        elif line[0].startswith("N"):
            resistor_nl = ResistorNL(line[0], int(line[1]), int(line[2]), float(line[3]), float(line[4]), float(line[5]), float(line[6]),
                                       float(line[7]), float(line[8]), float(line[9]), float(line[10]))
            print(resistor_nl, "adicionado com sucesso")
            return resistor_nl, contador_extra_lines
        elif line[0].startswith("E"):
            fctc = FTCT(line[0], int(line[1]), int(line[2]), int(line[3]), int(line[4]), float(line[5]), num_nodes + contador_extra_lines)
            contador_extra_lines += 1
            print(fctc, "adicionado com sucesso")
            return fctc, contador_extra_lines
        else:
            print(f"Elemento desconhecido: {line[0]}")
            return None, contador_extra_lines
