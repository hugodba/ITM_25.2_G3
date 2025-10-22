from .Element import Element
import numpy as np


class Circuit:    
    """Class representing an electrical circuit."""
    def __init__(self):
        self.n = None
        self.Gn = None
        self.In = None
        self.e = []
        self.e0 = [] # Initial condition of nodal voltages (time t - deltaT)
        self.w = 0
        self.components = []
        self.Idc = []
        self.Isin = []
        self.Vsin = []
        self.R = []
        self.GmI = []
        self.C = []
        self.L = []
        self.K = []
        self.vars = []        # Name variables of interests (currents)
        self.vars_values = []
        self.i_values = []
        self.i_values0 = [] # Initial condition of i variables (time t - deltaT)
        self.i_vars0 = {} # Initial condition of i variables associating name and values
        self.deltaT = None 
        self.period = None
        self.elements = []


    def get_number_of_nodes(self, content):
        """
        Get number of nodes for creating the Gn and In matrices.
        Eliminates comments and blank lines.

        Args:
            content (list): Full content of netlist file in "readlines" format.

        Returns:
            [int]: Number of nodes.
            [list]: Content of netlist file with useless line removed.
        """
        # TODO: Adapt this function for the current project
        
        # Store only unique elements
        nodes = set()
        
        i = 0
        content_lenght = len(content)
        while(i < content_lenght):
            # Skip and removes blank lines and comments:       
            if content[i][0] == "\n" or content[i][0] == "*" or content[i][0] == " "\
            or content[i][0] == "\0": 
                
                content.remove(content[i])

                # The next element becomes the current one, so doesn't need to add 1 in "i".
                # Content lenght down by 1 
                content_lenght -= 1

            elif content[i][0] == "I" or content[i][0] == "R" or content[i][0] == "G"\
                or content[i][0] == "L" or content[i][0] == "C" or content[i][0] == "K"\
                or content[i][0] == "F" or content[i][0] == "E" or content[i][0] == "H"\
                or content[i][0] == "V" or content[i][0] == "D":

                splitted_line = content[i].split(" ")
                
                # Add node "a" and "b"
                nodes.add(int(splitted_line[1]))
                nodes.add(int(splitted_line[2]))

                if content[i][0] == "G" or content[i][0] == "K" or content[i][0] == "F"\
                    or content[i][0] == "E" or content[i][0] == "H":

                    # nodes "c" and "d" (control nodes for "G", and nodes for the secondary 
                    # inductor of the transformer "K")
                    nodes.add(int(splitted_line[3]))
                    nodes.add(int(splitted_line[4]))

                # Get frequency of sine wave source
                elif splitted_line[3] == "SIN":
                    self.w = 2*np.pi*float(splitted_line[6])        
                i += 1
            
            else:
                raise ValueError(f"\nNetlist com a {i}ª linha inválida")

        self.n = len(nodes)
        return self.n, content


    def add_components(
            self, Yn, In, content, elem_type, method="backward", 
            deltaT=None, e0=None, i_vars0=None, time=None
        ):
        """Calls "Element" class to create object according to the circuit element.
        It also executes its stamps and add it in the Yn and In matrices

        Args:
            Yn (np.ndarray): Admitance matrix
            In (np.ndarray): Current vector
            content (list): Full content of netlist file in "readlines" format.
            elem_type (str): "invariant", "variant" or "non_linear". It defines
                the type of the element to gather execution
            method (str): "backward", "forward" or "trapezio". It defines the method
                of integration for definition of the stamp.
            deltaT (float): Step time (s).
            e0 (np.ndarray): Array of nodal voltages of last time step.
            i_vars0 (np.ndarray): Array of currents of last time step from modified 
                nodal analysis. 
            time (int): current time (s)
            
        Returns:
            np.ndarray, np.ndarray: new Yn and In matrix 
        """

        for component in content:
            self.elements.append(
                Element.create(
                    component.split(" "), Yn, In, method, elem_type, 
                    deltaT=deltaT, e0=e0, i_vars0=i_vars0, time=time
                )
            )
        return Yn, In


    def readlines_netlist(self, netlist_path: str):
        # Get the content of the netlist file
        try:
            with open(netlist_path) as netfile:
                content = netfile.readlines()
        except:
            raise ValueError("Erro. Caminho da netlist inválida.")
        return content

    def analyze(self, netlist, period, step, max_iter, tolerance):
        """Calculates the nodal voltages and variables of interest. 
        Stores values in attributes "e", "i_values", "vars_values".

        Args:
            netlist (str): Path for netlist file.

        Returns:
            np.ndarray: nodal voltages vector 
        """
        # Refresh all variables
        self.__init__()
        
        # Save delta(t) and period
        self.deltaT = step
        self.period = period

        # Lê a netlist e transforma em lista
        content = self.readlines_netlist(netlist)

        # Get the number of nodes for creating Gn and In
        n, content = self.get_number_of_nodes(content) 
        Gn = np.zeros((n, n))
        In = np.zeros((n, 1))

        # Add time invariant components
        invariant_Gn, invariant_In = self.add_components(Gn, In, content, "invariant")
        
        for time in np.arange(0.0, period, step):
            self.vars = [] # Because add_components_time_variant adds the same vars each time

            # Add time variant components
            Gn_variant, In_variant = self.add_components(
                invariant_Gn, 
                invariant_In, 
                content,
                "variant",
                deltaT=step,
                e0=self.e0,
                time=time
            )

            # TODO: Adicionar Newton Raphson para os componentes não lineares

            # TODO: Resolver o sistema matricial de equações 

        return self.e
