from .Element import Element
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
np.set_printoptions(precision=3, linewidth=150)


class Circuit:    
    """Classe que representa um circuito elétrico."""
    def __init__(self):
        self.n = None
        self.Gn = None
        self.In = None
        self.e = []
        self.e0 = [] # Condição inicial das tensões nodais (tempo t - deltaT)
        self.deltaT = None 
        self.period = None
        self.vars_t = None
        self.elems_info = {}


    def add_components(
            self, Yn, In, content, elem_type, method="backward", 
            deltaT=None, e0=None
        ):
        """Chama a classe "Element" para criar o objeto de acordo com o tipo de elemento.
        Também executa o stamp do elemento e o adiciona nas matrizes Yn e In.

        Args:
            Yn (np.ndarray): Matriz de admitância.
            In (np.ndarray): Vetor de correntes.
            content (list): Conteúdo completo do arquivo de netlist em formato "readlines".
            elem_type (str): "invariant", "variant" ou "non_linear". Define o tipo
                de elemento para determinar a execução.
            method (str): "backward", "forward" ou "trapezio". Define o método
                de integração para definição do stamp.
            deltaT (float): Passo de tempo (s).
            e0 (np.ndarray): Array de tensões nodais do passo de tempo anterior.
            
        Returns:
            np.ndarray, np.ndarray: novas matrizes Yn e In
        """

        for component in content:
            element = Element.create(
                component.split(" "), Yn, In, self.elems_info, method, elem_type, 
                deltaT=deltaT, e0=e0
            )
            if element is not None:
                Yn, In = element.Yn, element.In
                # Salvar as informações do elemento
                self.elems_info = element.elems_info
        return Yn, In

    def clean_netlist(self, content):
        """Remove comentários e linhas em branco do conteúdo da netlist.

        Args:
            content (list): Conteúdo completo do arquivo de netlist em formato "readlines".

        Returns:
            list: Conteúdo limpo da netlist.
        """
        cleaned_content = []

        for i in range(len(content)):
            if content[i][0] == "" or content[i][0] == "\n" or content[i][0] == "*":
                continue
            cleaned_content.append(content[i].strip("\n "))

        return cleaned_content

    def extract_and_validate_parameters_sim(self, cleaned_content):
        """Lida e valida os parâmetros de simulação extraídos da netlist."""

        try:
            n = int(cleaned_content[0])
        except:
            raise ValueError("Definição inválida do número de nós. " 
                             "O número de nós deve ser definido na primeira linha da netlist como um número inteiro. "
                             'Exemplo: linha 1: "3", linha 2: "R1000 1 2 1000", ...')
        
        # Extrai os parâmetros de simulação
        try:
            tran, total_time, step_time, \
                method, n_internal_steps = cleaned_content[-1].split(" ")
        except:
            raise ValueError("Definição inválida dos parâmetros de simulação. " 
                             "Os parâmetros de simulação devem ser inseridos na "
                             "última linha da netlist, no formato:\n"
                             '\t.TRAN <tempo_total(float)> <step_time(float)> '
                             '<metodo_integracao(str)> <n_internal_steps(int)>\n')

        if tran != ".TRAN":
            raise ValueError("Definição inválida dos parâmetros de simulação. " 
                             "Os parâmetros de simulação devem começar com '.TRAN'.")

        try:
            total_time = float(total_time)
            step_time = float(step_time)
            n_internal_steps = int(n_internal_steps)
        except:
            raise ValueError("Definição inválida dos parâmetros de simulação. " 
                             "O tempo total e o passo de tempo devem ser números "
                             "reais e o número de steps deve ser um inteiro.")

        if method not in ["BE", "FE", "TRAP"]:
            raise ValueError("Método de integração inválido. "
                             "Opções válidas: 'BE', 'FE', 'TRAP'.")
        
        tran = True
        return n, tran, total_time, step_time, method, n_internal_steps


    def read_netlist(self, netlist_path: str):
        # Lê o conteúdo do arquivo de netlist
        try:
            with open(netlist_path) as netfile:
                content = netfile.readlines()
        except:
            raise ValueError("Erro. Caminho da netlist inválido.")
        
        cleaned_content = self.clean_netlist(content)

        n, tran, total_time, step_time, method, n_internal_steps = \
            self.extract_and_validate_parameters_sim(cleaned_content)
        
        cleaned_content.pop(0)          # Remove a primeira linha (número de nós)
        cleaned_content.pop(-1)         # Remove a última linha (parâmetros de simulação)

        return cleaned_content, n, tran, total_time, step_time, method, n_internal_steps
        
    def plot(self, node: int, multiplier: float = 10e-3):
        # Plota o gráfico da tensão nodal desejada ao longo do tempo
        subunit = "ms" if multiplier == 10e-3 else "s"
        
        plt.plot(multiplier*np.arange(0.0, self.total_time + self.step_time, self.step_time), self.vars_t[node - 1, :])
        plt.title(f"e(t) - Nó {node}")
        plt.xlabel(f"Tempo ({subunit})")
        plt.ylabel("Tensão (V)")
        plt.grid()
        plt.show()


    def analyze(self, netlist):
        """Calcula as tensões nodais e variáveis de interesse. 
        Armazena os valores nos atributos "e", "i_values", "vars_values".

        Args:
            netlist (str): Caminho do arquivo de netlist.

        Returns:
            np.ndarray: vetor de tensões nodais 
        """
        # Reinicializa todas as variáveis
        self.__init__()
        
        # Lê a netlist e extrai a lista de elementos e os parâmetros de simulação
        content, self.n, self.tran, self.total_time, self.step_time, \
            self.method, self.n_internal_steps = self.read_netlist(netlist)

        # Inicializa as matrizes Gn e In
        Gn = np.zeros((self.n + 1, self.n + 1))
        In = np.zeros((self.n + 1, 1))

        # Adiciona os componentes invariantes no tempo
        invariant_Gn, invariant_In = self.add_components(Gn, In, content, "invariant")

        # Análise no domínio do tempo
        self.vars_t = [] # Para armazenar todas as tensões nodais e variáveis de saída ao longo do tempo
        self.e0 = None # Vazio no primeiro passo
        for time in tqdm(np.arange(0.0, self.total_time + self.step_time, self.step_time)):

            # Adiciona os componentes variantes no tempo
            Gn_variant, In_variant = self.add_components(
                invariant_Gn, 
                invariant_In, 
                content,
                "variant",
                deltaT=self.step_time,
                e0=self.e0
            )

            # TODO: Adicionar Newton-Raphson para os componentes não lineares

            # Resolve o sistema linear
            self.e = np.linalg.solve(Gn_variant[1:, 1:], In_variant[1:])
            self.e0 = self.e.copy()   # Salva as tensões nodais para o próximo passo
            self.vars_t.append(self.e.flatten()) # Armazena todas as variáveis de interesse ao longo do tempo

        # Converte vars_t em um array numpy
        self.vars_t = np.array(self.vars_t).T # Transpõe para facilitar o acesso por nó (n, steps)

        return self.vars_t
