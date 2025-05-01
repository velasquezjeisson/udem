# Análisis de Multicolinealidad con VIF (Variance Inflation Factor)

Este documento describe el análisis de multicolinealidad realizado utilizando el VIF (Variance Inflation Factor).

## ¿Qué es el VIF?

El Variance Inflation Factor (VIF) es una métrica utilizada para detectar multicolinealidad en modelos de regresión múltiple.  La multicolinealidad ocurre cuando dos o más variables predictoras en un modelo están altamente correlacionadas entre sí.  Esto puede causar problemas en la interpretación de los coeficientes del modelo, ya que puede inflar la varianza de los coeficientes estimados y hacer que parezca que una variable es estadísticamente significativa cuando en realidad no lo es (o viceversa).

## ¿Para qué sirve el VIF?

El VIF sirve para:

* **Identificar la presencia de multicolinealidad:**  Ayuda a determinar si las variables predictoras de un modelo están altamente correlacionadas.
* **Evaluar el impacto de la multicolinealidad:** Permite evaluar la gravedad de la multicolinealidad y su posible impacto en los resultados del modelo.
* **Guiar la selección de variables:** Facilita la selección de un subconjunto de variables predictoras que sean menos correlacionadas entre sí, mejorando la estabilidad y la interpretabilidad del modelo.

## ¿Cómo funciona el VIF?

El VIF para una variable predictora específica se calcula de la siguiente manera:

1. **Regresión Auxiliar:** Se realiza una regresión lineal donde la variable predictora en cuestión es la variable dependiente, y todas las demás variables predictoras del modelo original son las variables independientes.
2. **Cálculo del R cuadrado:** Se calcula el R cuadrado (R²) de esta regresión auxiliar.  El R² representa la proporción de la varianza de la variable predictora que puede ser explicada por las otras variables predictoras.
3. **Cálculo del VIF:** El VIF se calcula como:

   ```
   VIF = 1 / (1 - R²)
   ```

   Un R² cercano a 1 indica que la variable predictora está altamente correlacionada con las otras variables predictoras, lo que resulta en un VIF alto.

## ¿Cómo se interpreta el VIF?

La interpretación del VIF se basa en la magnitud del valor obtenido:

* **VIF = 1:** No hay multicolinealidad detectada. La variable predictora no está correlacionada con las otras variables predictoras.
* **1 < VIF < 5:** Multicolinealidad moderada.  Puede haber cierta correlación entre la variable predictora y las otras variables predictoras, pero generalmente no se considera un problema grave.
* **VIF >= 5 (o 10):** Alta multicolinealidad. La variable predictora está altamente correlacionada con las otras variables predictoras, lo que puede causar problemas en la interpretación de los resultados del modelo. El umbral de 5 o 10 es una guía, y la decisión de tomar medidas correctivas puede depender del contexto del problema.

En general, se recomienda tomar medidas para abordar la multicolinealidad si el VIF de alguna variable es significativamente mayor que 5 o 10.

## Resultados del VIF

Los siguientes son los valores de VIF obtenidos para cada variable:


| Variable            | VIF      |
| ------------------- | -------- |
| euribor3m           | 1.194015 |
| no_previous_contact | 1.151436 |
| not_working         | 1.093422 |
| age                 | 1.059205 |
| campaign            | 1.027740 |

## Interpretación (Específica para este conjunto de datos)

En general, los valores de VIF son bastante bajos.  Según las reglas generales descritas anteriormente, ninguno de los valores se acerca a umbrales problemáticos.

**Conclusión:**

No hay evidencia de multicolinealidad problemática en este conjunto de datos, al menos entre las variables incluidas en el cálculo del VIF.  Esto implica que se puede confiar en los coeficientes de un modelo (si se está utilizando uno) sin preocuparse de que estén inflados o distorsionados debido a la multicolinealidad.

## Puntos a Tener en Cuenta

* **Variables Omitidas:** El VIF solo evalúa la multicolinealidad entre las variables *incluidas* en el modelo/cálculo del VIF.  Si existen otras variables en el conjunto de datos que no se han incluido, podrían potencialmente causar multicolinealidad con las variables que sí se incluyeron.
* **Transformaciones:** Si se planea agregar términos de interacción o términos polinómicos (por ejemplo, `age^2`), la multicolinealidad podría convertirse en un problema. En ese caso, se podría considerar centrar o estandarizar las variables originales antes de crear los términos de interacción o polinómicos.
