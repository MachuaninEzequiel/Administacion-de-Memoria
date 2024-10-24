import random

# Solicitar al usuario que ingrese una semilla (seed)
semilla = int(input("Ingresa una semilla para generar los números aleatorios: "))

# Establecer la semilla para generar números aleatorios
random.seed(semilla)

# Solicitar al usuario que ingrese la cantidad de números a generar
cantidad = int(input("Ingresa la cantidad de números a generar: "))

# Generar los números y almacenarlos en una lista
numeros = []
for i in range(cantidad):
    # Generar el primer número autoincremental
    primer_numero = i + 1

    # Generar el segundo número aleatorio entre 1 y 100
    segundo_numero = random.randint(1, 100)

    # Generar el tercer número aleatorio entre 1 y 30
    tercer_numero = random.randint(1, 30)

    # Dividir los números entre sí y obtener el resultado como cadena
    resultado = str(primer_numero) + "," + str(segundo_numero) + "," + str(tercer_numero)

    # Agregar el resultado a la lista de números
    numeros.append(resultado)

# Imprimir los números generados
for numero in numeros:
    print(numero)
