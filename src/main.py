from typing import Literal

from circuit_simulator import CircuitSimulator

# general TODO: add log prints, typehints, docstrings, progress bars, error handling
def main(
    mode: Literal['netlist', 'programatic'],
    netlist_path: str,
    node_plot_x1: int | Literal['time'] = 'time',
    node_plot_y1: int | Literal['time'] = 1,
    node_plot_x2: int | Literal['time'] | None = None,
    node_plot_y2: int | Literal['time'] | None = None,
) -> None:
    '''
    Main function to run the circuit simulator.

    Parameters:
        mode (Literal['netlist', 'programatic']): Mode of operation, either 'netlist' to read from a netlist file or 'programatic' to create the circuit programmatically.
        netlist_path (str, optional): Path to read the netlist file if mode is 'netlist'. Path to save the generated netlist if mode is 'programatic'.
        node_plot_x (list[int] | Literal['time'], optional): Node to plot on the x-axis or 'time' for time axis. Default is 'time'.
        node_plot_y (list[int] | Literal['time'], optional): Node to plot on the y-axis or 'time' for time axis. Default is 1.
    '''
    
    CircuitSimulator(
        mode=mode,
        netlist_path=netlist_path,
        node_plot_x1=node_plot_x1,
        node_plot_y1=node_plot_y1,
        node_plot_x2=node_plot_x2,
        node_plot_y2=node_plot_y2
    )
    
if __name__ == "__main__":

    # # PULSE
    # main(
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\pulse.net',
    #     node_plot_x1='time',
    #     node_plot_y1=1
    # )

    # # SIN
    # main(
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\sinusoidal.net',
    #     node_plot_x1='time',
    #     node_plot_y1=1
    # )

    # # CHUA
    # main(
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\chua.net',
    #     node_plot_x1=1,
    #     node_plot_y1=2
    # )

    # # LC
    # main(
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\lc.net',
    #     node_plot_x1='time',
    #     node_plot_y1=6
    # )
    
    # #dc_source
    # main (
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\dc_source.net',
    #     node_plot_x1='time',
    #     node_plot_y1=1,
    #     node_plot_x2='time',
    #     node_plot_y2=2
    # )

    # #OPamp_rectifier
    # main (
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\opamp_rectifier.net',
    #     node_plot_x1='time',
    #     node_plot_y1=1,
    #     node_plot_x2='time',
    #     node_plot_y2=7
    # )

    # Oscilator
    # main(
    #     mode='netlist',
    #     netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\oscilator.net',
    #     node_plot_x1='time',
    #     node_plot_y1=1
    # )

    # Mosfet
    main(
        mode='netlist',
        netlist_path=r'C:\Users\fabri\OneDrive\Escritorio\UFRJ\Instrumentações e Técnicas de Medidas\Trabalho 2\ITM_25.2_G3\netlists\examples\mosfet_curve.net',
        node_plot_x1=1,
        node_plot_y1=3
    )

    # main(
    #     mode='programatic',
    #     netlist_path=r'C:\Users\hugob\Documents\ITM_25.2_G3\netlists\out\programatic_circuit.net', # identic to lc.net
    #     node_plot_x='time',
    #     node_plot_y=6
    # )
    
