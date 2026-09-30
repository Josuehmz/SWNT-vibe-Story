---
id: C12
nombre: Pipeline de IA
tipo: Servicio
modulo: M5
mvp: true
historias: [HU-02, HU-03, HU-05]
---

# Especificación del Componente: Pipeline de IA

**Tipo:** Servicio (backend)
**Historias de usuario relacionadas:** HU-02, HU-03, HU-05

## Propósito
Transformar el dibujo en un cuento ilustrado y narrado, orquestando en orden:
visión → guion → (ilustración ∥ voz) → almacenamiento en la nube.

## Entradas
- `image_bytes`: dibujo en memoria (recibido de la API).

## Salidas
- `StoryResponse` con 3 páginas; cada página incluye texto, `image_url` y `audio_url` (o `null`).

## Reglas de negocio
- El dibujo se usa **solo** en el paso de visión y no se persiste en ninguna parte.
- Ilustraciones y audios se generan **en paralelo** para caber dentro del límite de tiempo.
- Las imágenes se **re-hospedan** en la nube porque las URLs de origen expiran (~1 h); si la
  subida falla, se usa una imagen *placeholder* en lugar de romper el cuento.
- **Degradación elegante:** si el servicio de voz no está configurado, `audio_url = null` y el
  cuento se entrega igual (solo texto e imagen).

## Flujo principal (máx. 5 pasos)
1. El servicio de visión describe el dibujo.
2. El servicio de guion crea un cuento de 3 páginas.
3. En paralelo: se generan las 3 ilustraciones y los 3 audios.
4. Se suben los assets a la nube y se obtienen URLs públicas.
5. Se arma y devuelve `StoryResponse`.

## Requisitos no funcionales (RNF)
- **Rendimiento:** la paralelización debe permitir completar en < 85 s.
- **Seguridad:** las claves de los proveedores de IA viven solo en variables de entorno del backend, nunca en el cliente.
- **Fiabilidad:** el fallo de una imagen o un audio individual no debe tumbar la generación completa del cuento.

## Criterios de aceptación
- **Dado** un dibujo interpretable, **cuando** corre el pipeline, **entonces** devuelve exactamente 3 páginas con texto no vacío.
- **Dada** una subida de imagen fallida, **cuando** se arma la página, **entonces** se usa el placeholder y no se lanza error.
- **Dado** un servicio de voz deshabilitado, **cuando** el pipeline termina, **entonces** cada página tiene `audio_url = null` y el cuento se entrega de todos modos.
