---
id: C10
nombre: Almacenamiento Local
tipo: Datos
modulo: M4
mvp: true
historias: [HU-04, HU-06]
---

# Especificación del Componente: Almacenamiento Local

**Tipo:** Datos (cliente)
**Historias de usuario relacionadas:** HU-04, HU-06

## Propósito
Guardar los cuentos en el dispositivo, listarlos, aplicar un límite de almacenamiento y llevar
el contador de cuentos gratuitos.

## Entradas
- `StoryEntity` a guardar; identificador de cuento a borrar.
- Consultas de lista de cuentos y de contador.

## Salidas
- Lista de cuentos (más recientes primero).
- `storiesGeneratedCount` (entero) y `hasReachedFreeLimit` (booleano).

## Reglas de negocio
- Los cuentos se guardan en base local (Hive); el contador en preferencias (SharedPreferences).
- Máximo 20 cuentos almacenados: al superarlo, se borran automáticamente los más antiguos.
- El límite gratuito se considera alcanzado cuando el contador es ≥ 3.

## Flujo principal (máx. 5 pasos)
1. Guarda el cuento recibido.
2. Aplica el límite de 20 (poda los más antiguos si es necesario).
3. Al solicitar la lista, ordena por fecha de creación descendente.
4. Expone el contador de cuentos generados.
5. Expone la bandera de límite gratuito alcanzado.

## Requisitos no funcionales (RNF)
- **Rendimiento:** lectura de la galería instantánea (acceso local, sin red).
- **Seguridad:** datos en almacenamiento privado de la app.
- **Accesibilidad / Fiabilidad:** funciona sin conexión a internet.

## Criterios de aceptación
- **Dado** que hay 20 cuentos guardados, **cuando** se guarda el cuento nº 21, **entonces** se elimina el más antiguo y quedan 20.
- **Dado** que se han generado 3 cuentos, **cuando** se consulta `hasReachedFreeLimit`, **entonces** devuelve `true`.
- **Dados** varios cuentos guardados, **cuando** se solicita la lista, **entonces** aparecen del más reciente al más antiguo.
