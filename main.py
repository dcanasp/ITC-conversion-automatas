import random
class alfabeto:
    def __init__(self,simbolos):
        setattr(self,'simbolos',simbolos)
    
    def generarCadenaAleatoria(self,n):
        nuevaCadena = []
        for i in range(n):
            nuevaCadena.append(self.simbolos[random.randint(0,n-1)])
        return nuevaCadena
    
instancia = alfabeto(["a","b","c","d"])
# instancia.simbolos
print( instancia.generarCadenaAleatoria(5))
