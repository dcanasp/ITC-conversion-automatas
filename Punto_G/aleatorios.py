from Punto_A.alfabeto import alfabeto_class
class claseValidacion:
    def __init__(self):
        self.validarAFNtoAFD()
    def validarAFNtoAFD(self):
        lenguaje = ["a","b","c","d"]
        n=6
        todo = []
        for x in range(10):
            todo.append(alfabeto_class(lenguaje).generarCadenaAleatoria(n))
        print(todo)
        return
    def validarAFNLambdaToAFN(self):
        return