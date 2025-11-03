from typing import Literal, Optional, List

from circuit_simulator import CircuitSimulator

def main(
    mode: Literal['netlist', 'programatic'],
    netlist_path: Optional[str] = None,
    node_plot: Literal['all'] | List[int] = 'all',
):
    
    CircuitSimulator(
        mode=mode,
        netlist_path=netlist_path,
        node_plot=node_plot,
    )
    
if __name__ == "__main__":
    main(
        mode='netlist',
        netlist_path=r'C:\Users\hugob\Documents\ITM_25.2_G3\netlists\examples\lc.net',
        node_plot=5,
    )
