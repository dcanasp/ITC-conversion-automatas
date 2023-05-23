import random
class alfabeto_class:
    def __init__(self,simbolos):
        setattr(self,'simbolos',simbolos)
    
    def generarCadenaAleatoria(self,n):
        nuevaCadena = ''
        for i in range(n):
            nuevaCadena += (self.simbolos[random.randint(0,len(self.simbolos)-1)])
        return nuevaCadena
    
# instancia = alfabeto_class(["a","b","c","d"])
# instancia.simbolos
# print( instancia.generarCadenaAleatoria(7))
