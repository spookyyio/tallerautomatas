import sys
import time
import os


class AFD:
    def __init__(self):
        #estados finales validos
        self.estados_finales = {'q1', 'q2', 'q3'}
        
    def validar(self, cadena):
        estado_actual = 'q0'
        
        for char in cadena:
            if estado_actual == 'q0':
                if char.isdigit(): estado_actual = 'q1'
                else: return False
                
            elif estado_actual == 'q1':
                if char.isdigit(): estado_actual = 'q2'
                elif char.isalpha(): estado_actual = 'q3'
                else: return False
                
            elif estado_actual == 'q2':
                if char.isalpha(): estado_actual = 'q3'
                else: return False 
                
            elif estado_actual == 'q3':
                if char.isalpha(): estado_actual = 'q3'
                else: return False

        return estado_actual in self.estados_finales


class MaquinaTuring:
    def __init__(self, cinta_input):
        #cinta con # al inicio y final
        self.cinta = ['#'] + list(cinta_input) + ['#']
        self.cabezal = 1 
        self.estado = 'q0' 
        self.alfabeto = 'abcdefghijklmnopqrstuvwxyz'

    def escribir(self, char):
        self.cinta[self.cabezal] = char

    def mover(self, direccion):
        if direccion == 'R': self.cabezal += 1
        elif direccion == 'L': self.cabezal -= 1
        
        #expandir cinta si es necesario
        if self.cabezal >= len(self.cinta): self.cinta.append('#')
        if self.cabezal < 0: self.cinta.insert(0, '#'); self.cabezal = 0

    def shift_caracter(self, char):
        #logica de cifrado cesar inverso
        idx = self.alfabeto.index(char)
        return self.alfabeto[(idx - 1) % 26]

    #Mostrorar las trancisones del MT
    def mostrar(self, paso):
        print("\n" + "-"*20)
        print(f"Paso: {paso}, Estado: {self.estado}")
        cinta_str = "".join(self.cinta)
        indicador = " " * self.cabezal + "^"
        print(f"Cinta: {cinta_str}\n       {indicador}")

    def ejecutar(self, mostrar_pasos=False):
        pasos = 0
        
        #ejecuta hasta llegar al estado de final q3
        while self.estado != 'q3' and pasos < 10000:
            if mostrar_pasos:
                self.mostrar(pasos)
                time.sleep(0.2)

            char = self.cinta[self.cabezal]
            
            
            #q0: estado inicial
            if self.estado == 'q0':
                if char.isdigit():
                    #verificar si hay un segundo digito
                    if self.cinta[self.cabezal + 1].isdigit():
                        self.estado = 'q1'
                        self.mover('R')
                    else:
                        #es un solo digito
                        if char == '0': self.estado = 'q2' #ir a limpiar
                        else: self.estado = 'q4' #ir a restar
                elif char == '#':
                    pass

            #q1: posicionamiento en la unidad (segundo digito)
            elif self.estado == 'q1':
                prev = self.cinta[self.cabezal - 1]
                #verificar si el numero completo es 00
                if prev == '0' and char == '0': self.estado = 'q2'
                else: self.estado = 'q4'

            #q4: logica de resta y reserva
            elif self.estado == 'q4':
                if char.isdigit():
                    val = int(char)
                    if val > 0:
                        self.escribir(str(val - 1))
                        self.estado = 'q5' 
                        self.mover('R')
                    else:
                        #caso reserva de decenas
                        self.escribir('9')
                        self.mover('L') 
                        self.estado = 'q4_reserva' 

            #q4_reserva: restar a la decena
            elif self.estado == 'q4_reserva':
                if char.isdigit():
                    val = int(char)
                    self.escribir(str(val - 1))
                    self.mover('R')
                    self.estado = 'q5' 

            #q5: avanzar hacia las letras
            elif self.estado == 'q5':
                if char.isdigit(): self.mover('R')
                elif char.isalpha(): self.estado = 'q8'
                elif char == '#': 
                    self.mover('L')
                    self.estado = 'q9'

            #q8: transformacion de letras
            elif self.estado == 'q8':
                if char.isalpha():
                    nuevo_char = self.shift_caracter(char)
                    self.escribir(nuevo_char)
                    self.mover('R')
                elif char == '#':
                    self.mover('L')
                    self.estado = 'q9'

            #q9: retorno al inicio de los numeros
            elif self.estado == 'q9':
                if char.isdigit():
                    #si hay decena a la izquierda ajustar cabezal
                    if self.cinta[self.cabezal - 1].isdigit(): 
                        self.mover('L')
                    self.estado = 'q0' 
                else:
                    self.mover('L')

            #q2: limpieza de ceros restantes
            elif self.estado == 'q2':
                if char.isdigit():
                    self.escribir('#')
                    self.mover('R')
                else:
                    self.estado = 'q3' 

            pasos += 1
            
        return "".join(self.cinta).replace("#", "")


def main():
    afd = AFD()
    
    while True:
        print("\n" + "="*40)
        print("   LABORATORIO 2: AUTOMATAS Y MT")
        print("="*40)
        print("1. Ingresar cadena encriptada")
        print("2. Salir")
        
        opcion = input("\nSeleccione una opcion: ")
        
        if opcion == '1':
            cadena = input("Ingrese la cadena (ej: 2jqnc): ").strip()
            
            if afd.validar(cadena):
                print(f"\n[AFD] Cadena '{cadena}' VALIDA. Ejecutando MT...")
                time.sleep(1)
                
                mt = MaquinaTuring(cadena)
                resultado = mt.ejecutar(mostrar_pasos=True)
                
                print("\n" + "="*40)

                print(f"\nResultados:")
                print(f" -> Entrada: {cadena}")
                print(f" -> Salida:  {resultado}")
            else:
                print(f"\n[ERROR] Cadena invalida segun el AFD.")
                
        elif opcion == '2':
            print("Saliendo...")
            break
        else:
            print("Opcion invalida.")

if __name__ == "__main__":
    main()