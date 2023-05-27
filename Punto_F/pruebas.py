from Punto_B.AFD import AFD_class
from Punto_C.AFN import AFN
class prueba:
    def __init__(self): 
        self.main()
        return
    def probarAFD(self):
        delta = {
            'q0': {'a': 'q1', 'b': 'q2'},
            'q1': {'a': '', 'b': 'q2'},
            'q2': {'a': 'q2', 'b': 'q3'},
            'q3': {'a':'','b':''}
        }
        delta2 ={
            'q0': {'a': 'q1', 'b': 'q2'},
            'q1': {'a': 'q1', 'b': 'q2'},
            'q2': {'a':'a','b':''}
        }
        delta3 = {
            'q0':{'a': 'q3','a': 'q1', 'b': 'q1'},
            'q1':{'a': 'q1', 'b': 'q3'},
            'q2':{'a': 'q2', 'b': 'q0'},
            'q3':{'a': 'q2', 'b': ''},
        }

        # (self,alfabeto,estados,estadoInicial,estadosAceptados,delta)
        afd1 = AFD_class(['a', 'b'], ['q0','q1','q2','q3'], ['q0'], ['q0'], delta)
        afd2 = AFD_class(['a','b'],['q0','q1','q2'],['q0'],['q0','q1'],delta2)
        afd3 = AFD_class(['a','b'],['q0','q1','q2','q3'],['q0'],['q2','q3'],delta3)
        
        print(afd1.procesarCadenaConDetalles('abbaabaab'))
        return
    def probarAFN(self):
        alfabeto = {'0', '1'}
        estados = {'q0', 'q1', 'q2', 'q3'}
        estado_inicial = 'q0'
        estados_aceptacion = {'q3','q0'}
        estados_inaccesibles = set()
        delta = {
            'q0': {'0': {'q1'}, '1': {'q0', 'q1'}},
            'q1': {'0': {'q2'}, '1': {'q0'}},
            'q2': {'0': {'q2'}, '1': {'q3'}},
            'q3': {'0': {'q3'}, '1': {'q3'}}
        }
        # (self,alfabeto,estados,estadoInicial,estadosAceptados,delta)
        afn1 = AFN(alfabeto,estados, estado_inicial,estados_aceptacion, delta)
        afn1.procesarCadena
        print(afn1.procesarCadena('0001'))
        return
    def probarAFNLambda(self):
        return
    def main(self):
        # self.probarAFD()
        self.probarAFN()
        return
    def probarAFNtoAFD(self):
        return
    def probarAFNLambdaToAFN(self):
        return
    def probarComplemento(self):
        return
    def probarProductoCartesiano(self):
        return
    def probarSimplificacion(self):
        return
