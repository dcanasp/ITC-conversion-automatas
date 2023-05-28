from Punto_A.alfabeto import alfabeto_class
from Punto_B.AFD import AFD_class #estos son paquetes, son la union de modulos
from Punto_C.AFN import AFN
from Punto_D.AFNLambda import AFNLambda
from Punto_E.procesamiento_automatas import ProcesamientoCadenaAFN
from Punto_F.pruebas import prueba
from Punto_G.aleatorios import claseValidacion

# Automata = AFNLambda("PruebaITC.txt")
# AFNConvertido = Automata.AFN_LambdaToAFN()
# AFNLambda()
# from prueba.ayuda import final #asi se maneja como un modulo, y modulos dentro de ese mismo modulo, se cachea para mayor velocidad

# listaAFN = prueba()
# claseValidacion()
# AFNLambda()
# ProcesamientoCadenaAFN()
# afn_instancia = AFN(['a', 'b'], ['q0', 'q1', 'q2', 'q3'], 'q0', ['q1'], {
#     ('q0', 'a'): ['q0','q1','q3'],
#     ('q0', 'b'): [],
#     ('q1', 'a'): ['q1'],
#     ('q1', 'b'): ['q2'],
#     ('q2', 'a'): [],
#     ('q2', 'b'): ['q1','q2'],
#     ('q3', 'a'): [],
#     ('q3', 'b'): ['q3'],
# })
# cadena = "aaaa"  
# procesamiento = ProcesamientoCadenaAFN(cadena)
# procesamiento.procesar(afn_instancia) 
# procesamiento.imprimirResultados()



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


# Ejemplo de uso
# afn_instancia = AFN(['a', 'b'], ['q0', 'q1', 'q2', 'q3'], 'q0', ['q0'], {
#     ('q0', 'a'): [],
#     ('q0', 'b'): ['q1','q2'],
#     ('q1', 'a'): ['q0'],
#     ('q1', 'b'): [],
#     ('q2', 'a'): ['q3'],
#     ('q2', 'b'): [],
#     ('q3', 'a'): [],
#     ('q3', 'b'): ['q0'],
# })

# print(afn_instancia.toString())
# afd_instancia = afn_instancia.AFNtoAFD()


# print("alfabeto")
# print(afd_instancia.alfabeto)
# print(afd_instancia.estados)
# print(afd_instancia.estadoInicial)
# print(afd_instancia.estadosAceptados)
# print(afd_instancia.transicion)

afn = AFN(['a', 'b','c'], ['q0', 'q1', 'q2'], 'q0', ['q0'], {
    ('q0', 'a'): [],
    ('q0', 'b'): ['q1', 'q2'],
    ('q1', 'a'): ['q0'],
    ('q1', 'b'): [],
    ('q2', 'a'): ['q3'],
    ('q2', 'b'): [],
    ('q3', 'a'): [],
    ('q3', 'b'): ['q0'],
    ('q3','c'): ['q1']
})


print("AFN AFD")
afd = afn.AFNtoAFD()
afd.pasarStringAFNtoAFD()


listaCadenas = ["abababa", "aaaab", "aabbcc","a"]

# Especificar el nombre del archivo de resultados
nombreArchivo = "resultados.txt"

# Indicar si se imprimirán los resultados en pantalla
imprimirPantalla = True

# Procesar la lista de cadenas con detalles y guardar los resultados en el archivo
afn.procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)
print("###################################")

# delta = {
#     'q0': {'a': 'q1', 'b': 'q2'},
#     'q1': {'a': '', 'b': 'q2'},
#     'q2': {'a': 'q2', 'b': 'q3'},
#     'q3': {'a':'','b':''}
# }

# afd1 = AFD_class(['a', 'b'], ['q0','q1','q2','q3'], ['q0'], ['q0'], delta)
# # afd.pasarString()
# afd1.pasarString()##instancia nativa de afd
# afd.pasarStringAFNtoAFD() #instancia de afd a partir de una de afn
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
# afn_instancia.toString()
# afn_instancia.imprimirAFNSimplificado()
# afn_instancia.exportar("prueba")
# afn_instancia.procesarCadena("aaaa")
# afn_instancia.procesarCadenaConDetalles("aaa")
# nuevainstancia = constructor("prueba")
# nuevainstancia.computarTodosLosProcesamientos("aaa","prueba")

listaCadenas = ["ab", "abc", "abcd"]
afn_instancia.procesarListaCadenas(listaCadenas, "resultados.txt", imprimirPantalla=True)


listaCadenas = ["abababa", "aaaab", "aabbcc","a"]

# Especificar el nombre del archivo de resultados
nombreArchivo = "resultados.txt"

# Indicar si se imprimirán los resultados en pantalla
imprimirPantalla = True

# Procesar la lista de cadenas con detalles y guardar los resultados en el archivo
afn_instancia.procesarListaCadenas(listaCadenas, nombreArchivo, imprimirPantalla)

afn_instancia.graficar()