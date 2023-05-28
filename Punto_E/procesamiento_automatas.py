from Punto_C.AFN import AFN
from Punto_B.AFD import AFD_class

class ProcesamientoCadenaAFN:
    def __init__(self, cadena):
        self.cadena = cadena
        self.esAceptada = False
        self.listaProcesamientosAbortados = []
        self.listaProcesamientosAceptacion = []
        self.listaProcesamientosRechazados = []

    def procesar(self, automata):
        self.procesarRecursivo(self.cadena, automata.estadoInicial, "", automata)

    def procesarRecursivo(self, cadena, estado_actual, procesamiento, automata):
        procesamiento += f"-> {estado_actual}"
        if not cadena:
            if estado_actual in automata.estadosAceptados:
                self.esAceptada = True
                self.listaProcesamientosAceptacion.append(procesamiento)
            else:
                self.listaProcesamientosRechazados.append(procesamiento)
            return

        simbolo = cadena[0]
        simbolo_str = str(simbolo)
        restante = cadena[1:]

        if (estado_actual, simbolo_str) in automata.transicion:
            for estado_siguiente in automata.transicion[(estado_actual, simbolo_str)]:
                self.procesarRecursivo(restante, estado_siguiente, procesamiento + f"({simbolo_str})", automata)
        else:
            self.listaProcesamientosAbortados.append(procesamiento + f"({simbolo_str})")

    def imprimirResultados(self):
        print(f"Cadena: {self.cadena}")
        print(f"Es aceptada: {self.esAceptada}")
        print("Procesamientos de aceptación:")
        for procesamiento in self.listaProcesamientosAceptacion:
            print(procesamiento)
        print("Procesamientos rechazados:")
        for procesamiento in self.listaProcesamientosRechazados:
            print(procesamiento)
        print("Procesamientos abortados:")
        for procesamiento in self.listaProcesamientosAbortados:
            print(procesamiento)
            
            
class ProcesamientoCadenaAFD:
    def __init__(self, cadena):
        self.cadena = cadena
        self.esAceptada = False
        self.listaEstadoSimboloDeProcesamiento = []

    def procesar(self, automata):
        estado_actual = automata.estadoInicial[0]
        for simbolo in self.cadena:
            if simbolo in automata.transicion[estado_actual]:
                estado_siguiente = automata.transicion[estado_actual][simbolo]
                self.listaEstadoSimboloDeProcesamiento.append((estado_actual, simbolo))
                estado_actual = estado_siguiente
            else:
                self.listaEstadoSimboloDeProcesamiento.append((estado_actual, simbolo))
                break
        else:
            if estado_actual in automata.estadosAceptados:
                self.esAceptada = True

    def imprimirResultados(self):
        print(f"Cadena: {self.cadena}")
        print(f"Es aceptada: {self.esAceptada}")
        print("Procesamiento de estados y símbolos:")
        procesamiento_str = "->".join([f"{estado}({simbolo})" for estado, simbolo in self.listaEstadoSimboloDeProcesamiento])
        print(procesamiento_str)

