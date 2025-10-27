import click
from src.circuit_simulator.Circuit import Circuit


@click.command()
@click.option("--netlist", help="Netlist file path", prompt=True)
def main(netlist):
    """
    Calculates the nodal voltages of the circuit provided by the netlist.
    """
    
    ckt = Circuit()
    ckt.analyze(netlist)
    ckt.show("e")


if __name__ == "__main__":
    main()
