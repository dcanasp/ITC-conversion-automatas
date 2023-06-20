from Punto_A.AFPD import AFPD
from Punto_B.AFPN import AFPN
from Punto_C.AF2P import AF2P
from Punto_D.MT import MT, construirMTDesdeArchivo, construirMT

# '''
# AFPD
# '''
# Pila=AFPD(["q0","q1","q2","q3"], "q0", "q3", "a-b", "A-B", ["q0:a:$>q0:A","q0:b:$>q0:B","q0:a:B>q0:$","q0:b:A>q0:$"])
# print(Pila)

# Pila.Pila=["$"]
# print(Pila.modificarPila(Pila.Pila,"$","B"))
# print(Pila)

# print(Pila.obtenerTransiciones("q0","a","$"))

# Pila.estadoActual="q0"
# print(Pila.leerLetra("bb"))

# print(Pila.procesarCadenaConDetalles("abab"))
# listaCadenas = ["abab", "aabb", "abba"]
# Pila.procesarListaCadenas(listaCadenas, "resultados.txt", True)

# pila = AFPD("Taller_3/Punto_A/AFPD.pda")
# print(pila)


# '''
# AFPN
# '''
# archivo=AFPN("Taller_3/Punto_B/AFPN.pda")
# estados = ['q0','q1','q2','q3']
# estados_aceptacion = ['q0','q3']
# estado_inicial = 'q0'
# sigma = ['a','b']
# Gamma = ['A','B']
# Delta = {
#     ('q0','a','$','A'): ['q1','q2'],
#     ('q1','a','$','A'): ['q0'],
#     ('q1','b','A','$'): ['q3'],
#     ('q2','b','A','$'): ['q2'],
#     ('q2','$','$','$'): ['q3'],
# }
# afpn=AFPN(estados,estado_inicial,estados_aceptacion,sigma,Gamma,Delta)
# # print(afpn)
# print(afpn.procesarCadena('ab'))
# print(afpn.procesarCadenaConDetalles('aba'))
# # print(afpn.modificarPila(["a","b","c"],"pop","a"))
# #print(afpn.obtenerTransiciones("q0","a","A"))
# #print(afpn.leerLetra("bb"))
# #print(afpn.procesarCadenaConDetalles("abab"))
# # Definir la lista de cadenas a procesar
# #listaCadenas = ["abab", "aabb", "abba"]
# # Llamar al método procesarListaCadenas
# #afpn.procesarListaCadenas(listaCadenas, "resultados.txt", True)3

######################################################################

Pila=AF2P("AF2P.msm")
# Pila=AF2P(["q0","q1","q2","q3"],"q0","q3","a-c","A-B",["q0:a:$:$>q0:A:$","q0:b:A:$>q1:A:B","q1:b:A:$>q1:A:B","q1:a:A:B>q2:$:B","q2:a:A:B>q2:$:B","q2:c:$:B>q3:$:$","q3:c:$:B>q3:$:$"])
# print(Pila)

# Pila.estadoActual=Pila.estadoInicial
# print(Pila.leerLetra("acc"))

# Pila.estadoActual=Pila.estadoInicial
# Pila.procesarCadena("aabbcc")

# Pila.estadoActual=Pila.estadoInicial
# print(Pila.procesarCadenaConDetalles("aababbaaacc"))

# Pila.Pila=["$"]
# Pila.Pila2=["$"]
# Pila.modificarPila(Pila.Pila,"$","$","A","A")

# print(Pila.obtenerTransiciones("q0","a","$","$"))

Pila.procesarListaCadenas(["aaabbaaacc","aaabbaaaccc"], "resultados.txt", True)

#########################################################################

# '''
# # MT
# '''
# #mt = construirMTDesdeArchivo("prueba2.tm")
# # Definición de la máquina de Turing
# estados = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
# estadoInicial = 'q0'
# estadosAceptacion = ['q5']
# alfabetoEntrada = ['a', 'b', 'c']
# alfabetoCinta = ['X', 'Y', 'Z']
# delta = {
#     ('q0', 'a'): ('q1', 'X', '>'),
#     ('q0', 'Y'): ('q4', 'Y', '>'),
#     ('q0', '!'): ('q5', '!', '-'),
#     ('q1', 'b'): ('q2', 'Y', '>'),
#     ('q1', 'a'): ('q1', 'a', '>'),
#     ('q1', 'Y'): ('q1', 'Y', '>'),
#     ('q1', 'b'): ('q2', 'Y', '>'),
#     ('q2', 'b'): ('q2', 'b', '>'),
#     ('q2', 'Z'): ('q2', 'Z', '>'),
#     ('q2', 'c'): ('q3', 'Z', '<'),
#     ('q3', 'a'): ('q3', 'a', '<'),
#     ('q3', 'b'): ('q3', 'b', '<'),
#     ('q3', 'Y'): ('q3', 'Y', '<'),
#     ('q3', 'Z'): ('q3', 'Z', '<'),
#     ('q3', 'X'): ('q0', 'X', '>'),
#     ('q4', 'Y'): ('q4', 'Y', '>'),
#     ('q4', 'Z'): ('q4', 'Z', '>'),
#     ('q4', '!'): ('q5', '!', '-')
# }

# # Crear una instancia de la máquina de Turing
# mt = MT(estados, estadoInicial, estadosAceptacion, alfabetoEntrada, alfabetoCinta, delta)

# # Procesar una cadena de ejemplo
# cadena = 'aabc'
# # aceptada = mt.procesarCadenaConDetalles(cadena)

# # if aceptada:
# #     print("La cadena es aceptada por la MT.")
# # else:
# #     print("La cadena es rechazada por la MT.")

# #(q0)aabbcc->X(q1)abbcc->Xa(q1)abcc->XaY(q2)bcc->XaYb(q2)bc->XaY(q3)cZc
# #(q0)aabbcc->X(q1)abbcc->Xa(q1)bbcc->XaY(q2)bcc->XaYb(q2)cc->XaYb(q3)bZc->…

# # print(mt.toString())
# print("EXPORTAR")
# mt.exportar("prueba2")
# print("TOSTRING")
# mt.toString()
# print("PROCESAR CADENA")
# mt.procesarCadena(cadena)
# print("PROCESAR CADENA CON DETALLES")
# mt.procesarCadenaConDetalles(cadena)
# print("PROCESAR FUNCION")
# mt.procesarFuncion(cadena)
# print("procesar lista cadenas")
# mt.procesarListaCadenas(["aabc","aabbcc","aabbccc","aabbcccc","aabbcccccc","aabbcccccccc"], "resultados.txt", True)
