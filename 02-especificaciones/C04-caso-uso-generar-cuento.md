---
id: C04
nombre: Caso de Uso Generar Cuento
tipo: Servicio
modulo: M2
mvp: true
historias: [HU-02, HU-04, HU-05, HU-06]
---

# Especificación del Componente: Caso de Uso Generar Cuento

**Tipo:** Servicio (cliente)
**Historias de usuario relacionadas:** HU-02, HU-04, HU-05, HU-06

## Propósito
Orquestar la generación de un cuento: pedirlo al backend, guardar el dibujo **solo en el
dispositivo**, persistir el cuento e incrementar el contador gratuito, sin que la UI conozca
esos detalles.

## Entradas
- `drawingPng` (bytes de la imagen exportada por C03).

## Salidas
- `StoryEntity` con la ruta local del dibujo (`drawingLocalPath`).
- Excepción de dominio (`StoryGenerationException`) si la generación falla.

## Reglas de negocio
- El dibujo se guarda en almacenamiento privado del dispositivo (`/drawings/{id}.png`), **nunca** en la nube.
- El contador de cuentos gratuitos se incrementa **solo tras una generación exitosa**.
- Si ya se alcanzó el límite gratuito (3), no debe iniciarse la generación.

## Flujo principal (máx. 5 pasos)
1. Recibe el PNG del dibujo.
2. Llama al repositorio (→ C06 → C11) para generar el cuento.
3. Guarda el dibujo del niño en disco local.
4. Persiste el cuento en el Almacenamiento Local (C10).
5. Incrementa el contador y devuelve el cuento.

## Requisitos no funcionales (RNF)
- **Rendimiento:** operación asíncrona; no bloquea la UI durante la espera.
- **Seguridad:** aísla el dibujo del niño en almacenamiento privado de la app.
- **Fiabilidad:** ante un fallo, no se persiste ni se cuenta nada (operación atómica de éxito).

## Criterios de aceptación
- **Dado** un PNG válido, **cuando** la generación tiene éxito, **entonces** el cuento queda guardado y el contador de cuentos gratuitos aumenta en 1.
- **Dado** un fallo del backend, **cuando** se lanza la excepción, **entonces** el contador NO cambia y no se persiste ningún cuento.
- **Dado** un cuento generado con éxito, **cuando** se inspecciona el dispositivo, **entonces** el dibujo está en almacenamiento local y no fue subido a la nube.
