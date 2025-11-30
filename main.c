#include <stdio.h>
#include <stdlib.h>
#include <string.h>

//Tamaño cadena
#define MAX_LONGITUD 100

int validarConAFD(char *cadena);
void ejecutarMaquinaTuring(char *cadena);
void limpiarBuffer();

int main() {
    int opcion;
    char cadenaEntrada[MAX_LONGITUD];

    do {
        //Menu
        printf("MAQUINA DE TURING \n");
        printf("1. Ingresar cadena para descifrar\n");
        printf("2. Salir\n");
        printf("Seleccione una opcion: ");

        //Lee la wea de arriba
        if (scanf("%d", &opcion) != 1) {
            printf("Error. Ingrese un numero valido.\n");
            limpiarBuffer();
            continue;
        }
        limpiarBuffer(); //cleanner

        //Caoss
        switch (opcion) {
            case 1:
                //Ingreso de cadena/cifrado(?)
                printf("\nIngrese la cadena cifrada: ");
                if (fgets(cadenaEntrada, MAX_LONGITUD, stdin) != NULL) {
                    //Eliminar el salto de linea que agrega fgets
                    cadenaEntrada[strcspn(cadenaEntrada, "\n")] = 0;
                    printf("Cadena recibida: \"%s\"\n", cadenaEntrada);

                    //Corrovora con AFD
                    if (validarConAFD(cadenaEntrada)) {
                        printf("La cadena es valida segun el AFD.\n");
                        
                        //DEsifra la wea(MT)
                        ejecutarMaquinaTuring(cadenaEntrada);
                    
                    //Si no, ta mala la cosa
                    } else {
                        printf("La cadena no es valida.\n");
                    }
                } else {
                    printf("Error, no puede leer la cadena.\n");
                }
                break;
            case 2:
                printf("\nCerrando programa.\n");
                break;
            default:
                printf("\nOpcion no valida. Intente otra vez.\n");
        }
    } while (opcion != 2);
    return 0;
}


//AFD
//Retorna 1 si es valida, 0 si no.
int validarConAFD(char *cadena) {
   return 1; 
}

//MT
void ejecutarMaquinaTuring(char *cadena) {
    printf("salida\n", cadena);
}

//CLEANNER
void limpiarBuffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}