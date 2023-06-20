from Punto_A.alfabeto import alfabeto_class
from Punto_B.AFD import AFD_class,constructor,hallarComplemento,hallarProductoCartesianoY,hallarProductoCartesianoO,hallarProductoCartesianoDiferencia,hallarProductoCartesianoDiferenciaSimetrica,simplificarAFD #estos son paquetes, son la union de modulos
from Punto_C.AFN import AFN
from Punto_D.AFNLambda import AFNLambda
from Punto_E.procesamiento_automatas import ProcesamientoCadenaAFN,ProcesamientoCadenaAFD
from Punto_F.pruebas import prueba
from Punto_G.aleatorios import claseValidacion


##################################################################################################################################################################
#INICIO DE PRESENTACIÓN

#AFD
# alfabeto = ['a', 'b']
# estados = ['q0', 'q1']
# estado_inicial = ['q0']
# estados_aceptados = ['q0']
# transiciones = {'q0': {'a': 'q1', 'b': 'q0'}, 'q1': {'a': 'q0', 'b': 'q1'}}

# afd = AFD_class(alfabeto, estados, estado_inicial, estados_aceptados, transiciones)

# afd2 = constructor("afd2")
# print("pasar string")
# afd2.pasarString()
# print("verificar completitud")
# afd.verificarCorregirCompletitudAFD()
# print("hallar estados limbo")
# afd.hallarEstadosLimbo()
# print("to   string")
# afd.pasarString()
# print("afd simplificado")
# afd.imprimirAFDSimplificado()
# print("exportar")
# afd.exportar("afd")
# print("procesar cadena")
# print(afd.procesarCadena("abbbabaaabbaaa"))
# print("procesar cadena con detalles")
# print(afd.procesarCadenaConDetalles("abbbabaaabbaaa"))
# print("procesar lista cadena con detalles")
# afd.procesarListaCadenas(["abbbabaaabbaaa","abbbabaaa","abbbbaaa"],"resultadoslistaafd",imprimirPantalla=True)
# print("COMPLEMENTO")
# complemento = hallarComplemento(afd).pasarString()
# print("Producto cartesiano Y")
# hallarProductoCartesianoY(afd,afd2).pasarString()
# print("Producto cartesiano O")
# hallarProductoCartesianoO(afd,afd2).pasarString()
# print("producto cartesiano diferencia")
# hallarProductoCartesianoDiferencia(afd,afd2).pasarString()
# print("producto cartesiano diferencia simetrica")
# hallarProductoCartesianoDiferenciaSimetrica(afd,afd2).pasarString()
# print("simplificar AFD")
# simplificarAFD(afd).pasarString()

# print("graficar")
# afd.graficar()

##################################################################################################################################################################
#AFN


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
# print("to string")
# afn_instancia.toString()
# print("imprimir afn simplificado")
# afn_instancia.imprimirAFNSimplificado()
# print("exportar")
# afn_instancia.exportar("pruebaAFNEXPORTADO")
# print("procesar cadena")
# afn_instancia.procesarCadena("aaaa")
# print("procesar cadena con detalles")
# afn_instancia.procesarCadenaConDetalles("aaa")
# print("computar")
# afn_instancia.computarTodosLosProcesamientos("aaa","pruebaCOMPUTAR")
# print("procesar lista cadenas")
# listaCadenas = ["ab", "abc", "abcd"]
# afn_instancia.procesarListaCadenas(listaCadenas, "resultados.txt", imprimirPantalla=True)
# print("AFNTOAFD")
# afd_instancia = afn_instancia.AFNtoAFD()
# print("procesar cadena conversion")
# afn_instancia.procesarCadenaConversion("aaaa")
# print("procesar cadena con detalles conversion")
# afn_instancia.procesarCadenaConDetallesConversion("aaaa")
# print("procesar lista cadenas conversion")
# afn_instancia.procesarListaCadenasConversion(listaCadenas,"resultadosCONVERSION.txt",imprimirPantalla=True)

# print("graficar")
# afn_instancia.graficar()

##################################################################################################################################################################
# #AFNLAMBDA
# AFN_Lambda = AFNLambda("PruebaITC.nfe")
# #AFN_Lambda = AFNLambda("a-c",["s0","s1","s2","s3"],"s0",["s0","s1","s3"],["s0:b>s1","s0:$>s0;s1","s1:a>s0","s1:b>s2;s3","s1:$>s2;s3","s2:a>s2;s3","s2:$>s2","s3:$>s1;s2"])
# # print(AFN_Lambda.imprimirAFNLSimplificado())
# # AFN_Lambda.exportar("PruebaITC")
# # print(AFN_Lambda.procesarCadena("aaaa"))
# # print(AFN_Lambda.procesarCadenaConDetalles("aaa"))
# # AFN_Lambda.computarTodosLosProcesamientos("aaa","prueba")
# listaCadenas = ["ab", "abc", "abcd"]
# AFN_Lambda.procesarListaCadenas(listaCadenas, "resultados.txt", imprimirPantalla=True)
# AFN_Lambda.graficar()
##################################################################################################################################################################

