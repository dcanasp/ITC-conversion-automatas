from Punto_B.AFPN import AFPN

estados = ['q0','q1','q2','q3']
estados_aceptacion = ['q0','q3']
estado_inicial = 'q0'
sigma = ['a','b']
Gamma = ['A','B']
Delta = {
    ('q0','a','$','A'): ['q1','q2'],
    ('q1','a','$','A'): ['q0'],
    ('q1','b','A','$'): ['q3'],
    ('q2','b','A','$'): ['q2'],
    ('q2','$','$','$'): ['q3'],
}
Pila=AFPN(estados,estado_inicial,estados_aceptacion,sigma,Gamma,Delta)
# print(Pila)
print(Pila.procesarCadena('ab'))
# print(Pila.modificarPila(["a","b","c"],"pop","a"))
#print(Pila.obtenerTransiciones("q0","a","A"))
#print(Pila.leerLetra("bb"))
#print(Pila.procesarCadenaConDetalles("abab"))
# Definir la lista de cadenas a procesar
#listaCadenas = ["abab", "aabb", "abba"]
# Llamar al método procesarListaCadenas
#Pila.procesarListaCadenas(listaCadenas, "resultados.txt", True)3