---
id: C01
nombre: Lienzo de Dibujo
tipo: UI
modulo: M1
mvp: true
historias: [HU-01]
---

# Especificación del Componente: Lienzo de Dibujo

**Tipo:** UI
**Historias de usuario relacionadas:** HU-01

## Propósito
Permitir al niño dibujar libremente con trazos suaves, cambiar color y grosor y borrar, sin
depender de un adulto y sin necesidad de leer.

## Entradas
- Gestos táctiles (secuencia de puntos con presión).
- Color y grosor seleccionados en la barra de herramientas.
- Acciones de borrar / deshacer.

## Salidas
- Estructura de trazos en memoria (para render en tiempo real).
- Al confirmar: imagen `PNG` (bytes) exportada, entregada al Caso de Uso Generar Cuento (C04).

## Reglas de negocio
- El botón "crear cuento" se habilita **solo** si el lienzo tiene al menos un trazo.
- La exportación usa `pixelRatio = 2.0` (≈ 2048 px en pantallas grandes) para calidad de visión.
- El dibujo no se envía a ninguna red salvo por la acción explícita del niño.

## Flujo principal (máx. 5 pasos)
1. El niño elige color y grosor.
2. Traza sobre el lienzo (render inmediato).
3. Puede borrar o deshacer trazos.
4. Pulsa "crear cuento".
5. El lienzo se exporta a PNG y se entrega a C04.

## Requisitos no funcionales (RNF)
- **Rendimiento:** trazo fluido a ≥ 60 fps, sin lag perceptible al dibujar.
- **Seguridad:** el dibujo permanece en el dispositivo hasta la petición explícita.
- **Accesibilidad:** botones grandes (≥ 48 dp); la operación no requiere leer texto.

## Criterios de aceptación
- **Dado** un lienzo vacío, **cuando** el niño no ha trazado nada, **entonces** el botón "crear cuento" está deshabilitado.
- **Dado** un color y grosor elegidos, **cuando** el niño levanta el dedo tras trazar, **entonces** el trazo queda dibujado con ese color y grosor.
- **Dado** un lienzo con al menos un trazo, **cuando** pulsa "crear cuento", **entonces** se exporta un PNG no vacío y se navega a la Pantalla Mágica.
