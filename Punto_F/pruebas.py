from Punto_B.AFD import AFD_class
from Punto_C.AFN import AFN
from Punto_D.AFNLambda import AFNLambda
from Punto_E.procesamiento_automatas import ProcesamientoCadenaAFN,ProcesamientoCadenaAFD

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


        afd1 = AFD_class(['a', 'b'], ['q0','q1','q2','q3'], ['q0'], ['q0'], delta)

        # Crear una instancia de la clase ProcesamientoCadenaAFD
        cadena = "ababa"
        procesamiento = ProcesamientoCadenaAFD(cadena)

        # Procesar la cadena utilizando el autómata
        procesamiento.procesar(afd1)

        # Imprimir los resultados
        procesamiento.imprimirResultados()

        # (self,alfabeto,estados,estadoInicial,estadosAceptados,delta)
        # afd1 = AFD_class(['a', 'b'], ['q0','q1','q2','q3'], ['q0'], ['q0'], delta)
        # afd2 = AFD_class(['a','b'],['q0','q1','q2'],['q0'],['q0','q1'],delta2)
        # afd3 = AFD_class(['a','b'],['q0','q1','q2','q3'],['q0'],['q2','q3'],delta3)
        
        print(afd1.procesarCadenaConDetalles('abbaabaab'))
        print("grafica AFD")
        afd1.graficar()
        return
    def probarAFN(self):

        afn_instancia = AFN(['a', 'b'], ['q0', 'q1', 'q2', 'q3'], 'q0', ['q1'], {
            ('q0', 'a'): ['q0','q1','q3'],
            ('q0', 'b'): [],
            ('q1', 'a'): ['q1'],
            ('q1', 'b'): ['q2'],
            ('q2', 'a'): [],
            ('q2', 'b'): ['q1','q2'],
            ('q3', 'a'): [],
            ('q3', 'b'): ['q3'],
        })
        cadena = "aaaa"  
        procesamiento = ProcesamientoCadenaAFN(cadena)
        procesamiento.procesar(afn_instancia) 
        procesamiento.imprimirResultados()
        afn_instancia.graficar()

        return
    def probarAFNLambda(self):
        return
    def main(self):
        self.probarAFD()
        self.probarAFN()
        self.probarAFNLambda()
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
