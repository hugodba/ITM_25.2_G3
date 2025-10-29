import click

from src.circuit_simulator.Circuit import Circuit
from src.circuit_simulator.elements.Resistor import Resistor
from src.circuit_simulator.elements.Capacitor import Capacitor
from src.circuit_simulator.elements.Indutor import Indutor
from src.circuit_simulator.elements.VoltageSourceDC import VoltageSourceDC
from src.circuit_simulator.elements.FonteTensaoControlDC import FonteTensaoControlTensao
from src.circuit_simulator.elements.ResistorNonLinear import ResistorNonLinear


@click.command()
@click.option("--netlist", help="Netlist file path", prompt=True)
def main(netlist):
    """
    Calculates the nodal voltages of the circuit provided by the netlist.
    """
    print("Circuit Simulator")
    ckt = Circuit()
    ckt.analyze(netlist)

    # Solicitar o nó desejado para plot
    end = False
    while not end:
        node = input('Digite o nó desejado para plotar a tensão ("N" para encerrar): ')
        if node == "N":
            end = True
        else:
            try:
                node = int(node)
                if node < 1 or node > ckt.n:
                    raise ValueError(f"Nó inválido. Deve estar entre 1 e {ckt.n}.")

                multiplier = input('Deseja que o tempo seja em "ms"? (Y)/N: ')
                multiplier = 10e-3 if multiplier.upper() in ["Y", ""] else 1.0
                ckt.plot(node, multiplier)
            except:
                print("\nNó inválido. Deve ser um número inteiro.")
            

if __name__ == "__main__":
    main()
