from Punto_A import alfabeto
from Punto_B import AFD #estos son paquetes, son la union de modulos
from Punto_C import AFN
from Punto_E.procesamiento_automatas import ProcesamientoCadenaAFN
from Punto_F.pruebas import prueba
from Punto_G.aleatorios import claseValidacion
from AFNLambda import AFNLambda
# from prueba.ayuda import final #asi se maneja como un modulo, y modulos dentro de ese mismo modulo, se cachea para mayor velocidad

listaAFN = prueba()
# claseValidacion()
# AFNLambda()
ProcesamientoCadenaAFN()
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