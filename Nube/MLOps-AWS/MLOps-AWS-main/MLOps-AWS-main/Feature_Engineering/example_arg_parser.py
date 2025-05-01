import argparse

def main():
    parser = argparse.ArgumentParser(description='Realiza operaciones aritméticas simples entre dos números.')

    # Agregar argumentos
    parser.add_argument('num1', type=float, help='El primer número.')
    parser.add_argument('num2', type=float, help='El segundo número.')
    parser.add_argument('--operation', type=str, choices=['add', 'subtract', 'multiply', 'divide'], default='add', help='La operación a realizar (por defecto, suma).')

    # Parsear los argumentos
    args = parser.parse_args()

    # Realizar la operación basada en el argumento
    if args.operation == 'add':
        result = args.num1 + args.num2
    elif args.operation == 'subtract':
        result = args.num1 - args.num2
    elif args.operation == 'multiply':
        result = args.num1 * args.num2
    elif args.operation == 'divide':
        if args.num2 == 0:
            print("Error: No se puede dividir entre cero.")
            return
        result = args.num1 / args.num2

    # Mostrar el resultado
    print(f'El resultado de {args.operation} entre {args.num1} y {args.num2} es: {result}')

if __name__ == '__main__':
    main()