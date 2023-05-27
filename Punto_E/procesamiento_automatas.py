from Punto_C.AFN_Experimental import AFD_Experimental
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



