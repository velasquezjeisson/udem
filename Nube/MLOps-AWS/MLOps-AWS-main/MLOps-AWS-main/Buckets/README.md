# Pasos para usar ec2 con s3

## 1- Crear una instancia con las siguientes configuraciones:



* Istancia tipo Linux/UNIX

* Creas unas keys nuevas para conectarnos desde local o lo hace directamente desde la consola

* Permitir el tráfico HTTP desde internet
* Ir a User y crear credenciales son keys

## 2- Crear una instancia con las siguientes configuraciones:2- ### Crear una instancia con las siguientes configuraciones:

* Usar `aws configure`
* Para crear un bucket desde la CLI hacer`RANDOM_ID=$(aws secretsmanager get-random-password --exclude-punctuation --exclude-uppercase --password-length 6 --require-each-included-type --output text --query RandomPassword)`
* Ejecutar en la terminal `aws s3api help`
* `aws s3api list-buckets` para listar obetos
* `aws s3api list-objects --bucket feature-engineering-bank` para ver al interior de un bucket en concreto

## 3 - Create s3 bucket

* `echo "$RANDOM_ID"` para ver que hay al interior de `RANDOM_ID`
* `aws s3api create-bucket --bucket awsml-$RANDOM_ID`
* Guardar una imagen random en la UI

## 4- Clean up

* `aws s3api delete-bucket --bucket awsml-$RANDOM_ID`

## Actividad 1 - 10%

- Generar un script en Python para la carga automática de datos en un bucket.
- El script deberá contener también una función o método para eliminar objetos dentro de un bucket.

A tener en cuenta:

* Deberán identificar key y access token de tu user en AWS.
* Las credenciales de acceso no se deben de compartir con nadie, es de uso privado y no se deben exponer. (Usa import o variables de entorno.)
* Plazo máximo domingo 30 de marzo a media noche.
