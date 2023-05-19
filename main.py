# from  'Punto_B' import AFD 
# import sys
# sys.path.insert(0, './Punto_B/AFD/') 
# from __init__ import AFD_clase

from Punto_A import alfabeto_class
from Punto_B import AFD_class
from Punto_C import AutomataNoDeterminista


class prueba:
    def __init__(self): 
        self.main()
        return
    def probarAFD(self):
        
        return
    def probarAFN(self):
        return
    def probarAFNLambda(self):
        return
    def main(self):
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
afd2 = AFD_class(['a','b'],['q0','q1','q2'],['q0'],['q0','q1'],delta2)

delta3 = {
    'q0':{'a': 'q3','a': 'q1', 'b': 'q1'},
    'q1':{'a': 'q1', 'b': 'q3'},
    'q2':{'a': 'q2', 'b': 'q0'},
    'q3':{'a': 'q2', 'b': ''},
}

afd3 = AFD_class(['a','b'],['q0','q1','q2','q3'],['q0'],['q2','q3'],delta3)




# (self,alfabeto,estados,estadoInicial,estadosAceptados,delta)
afd1 = AFD_class(['a', 'b'], ['q0','q1','q2','q3'], ['q0'], ['q0'], delta)


afd1.exportar('nombre')
afd1.graficar()
afd2.graficar()
afd3.graficar()


'''
print(afd1.hallarEstadosLimbo())
print(afd1.imprimirAFDSimplificado()) #
print(afd1.hallarEstadosInaccesibles()) 
print(afd1.eliminarEstadosInaccesibles())
print(afd1.pasarString())
print(afd1.procesarCadena('abbaab'))
print(afd1.procesarCadenaConDetalles('abbaab'))
print(afd1.procesarListaCadenas('abbaab','prueba','no')) #
print(afd1.simplificarAFD('abbaab')) #
'''