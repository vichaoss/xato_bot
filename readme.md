# El xato bot

Es un bot de discord desarrollado para gestionar la xatos league.

## Errores conocidos

* Posible error al promocionar un Challenger o al bajar un Bronce 5, posible perdida de liga

## Funciones por añadir

* Rango unranked
* Comando para flushear la tabla
* Servio para windows
*

## Comandos soportados

cada comando se utiliza con el prefijo "xato!" seguido de la instrucción

* `leaderboard` o `leader`
  * El bot indicará la tabla de rankings
* `promo {@etiqueta}`
  * El bot promocionará a la persona etiquetada 1 liga
* `down {@etiqueta}`
  * El bot bajará a la persona etiquetada 1 liga
* `add {@etiqueta} as {alias} in {liga y división}`
  * El bot agregará a la persona etiquetada a la liga en la división dada esto.

    Ejemplos de sintaxis de liga son: _bronce2_, _challenger_, _dIaMaNtE5_
* `alias [nuevo alias]`
  * El bot modificará el alias de quien haya invocado el comando, siempre y cuanto esté registrado en la liga. En caso
    de no ingresar un [nuevo alias], se asignará su apodo actual.

###### _control de versiones pendiente_

Se considerará la version 1.0.0.0 como la inicial, con el bot _estable_ siguiendo el patrón A.B.C.D donde:

- A: Identificador de gran cambio o implementación mayor.
- B: Implementaciones _normales_ o _menores_, o cambios en la funcionalidad de ellas.
- C: Corrección de errores.
- D: Cambios menores.

* 1.3.0.0
  * Implementados tabla de liderazgo, promoción, descenso y registro.

* 1.0.0.0
  * Primera version _estable_, capaz conectarse y crear su base de datos vacía.
