# TODO: Parking Lots Visuales en AnyLogic

Este documento resume el estado actual del modelo `EstacionamientoV1.original.alp` y lo que falta para completar la animacion visual de autos sobre el fondo `fondos_parqueo_upsa.png`.

## Objetivo

Mostrar autos moviendose sobre la imagen de fondo sin cambiar la logica estadistica del modelo.

La logica de capacidad sigue estando en los `ResourcePool`:

- `EstExterno`: 100 espacios
- `EstCentral`: 73 espacios
- `EstIng`: 91 espacios

La imagen, los nodos y los `MoveTo` son solo capa visual.

## Estado actual encontrado

### Imagen de fondo

El fondo ya esta agregado en `Main`:

- Archivo: `fondos_parqueo_upsa.png`
- Posicion aproximada: `X=0`, `Y=1000`
- Tamano aproximado: `Width=1672`, `Height=941`

### Nodos ya existentes

Ya existen estos nodos visuales:

| Nodo | Proposito | Coordenadas aproximadas |
| --- | --- | --- |
| `nEntradaGeneral` | Entrada principal desde la izquierda | `X=20`, `Y=1520` |
| `nEntradaExterno` | Entrada al parqueo externo | `X=900`, `Y=1480` |
| `nSalidaGeneral` | Salida hacia la derecha | `X=1640`, `Y=1520` |
| `nEntradaCentral` | Entrada al parqueo central | `X=650`, `Y=1490` |
| `nEntradaPolideportivo` | Entrada al parqueo polideportivo | `X=1230`, `Y=1670` |

### Zona visual ya existente

Ya existe una zona rectangular para el parqueo externo:

- Nombre: `rParqueoExterno`
- Tipo: `RectangleNode`
- Posicion: `X=870`, `Y=1080`
- Tamano: `Width=730`, `Height=380`
- Tiene muchos `Attractor` generados automaticamente.
- El `MoveTo` `moverParqueoExterno` apunta a `rParqueoExterno`.

Esto indica que se empezo a usar una estrategia mejor que un solo `PointNode`: mover autos hacia una zona con atractores. Mantener ese enfoque para Central y Polideportivo.

### MoveTo ya existentes

Ya existen tres bloques `MoveTo` para Externo:

| Bloque | Destino configurado |
| --- | --- |
| `moverEntradaExterno` | `nEntradaExterno` |
| `moverParqueoExterno` | `rParqueoExterno` |
| `moverSalidaExterno` | `nSalidaGeneral` |

## Advertencia sobre conexiones actuales

Revisar visualmente la rama Externo antes de copiar el patron.

En el XML actual aparecen conexiones que sugieren que algunos `MoveTo` pudieron quedar insertados en sentido no ideal:

- `Filainext -> moverEntradaExterno`
- `moverEntradaExterno -> Desicion1`
- `Estacionando -> moverParqueoExterno`
- `moverParqueoExterno -> Espaciosext`
- `Saliendoext -> moverSalidaExterno`
- `moverSalidaExterno -> Libreext`

Conceptualmente, lo esperado seria:

```text
Desicion1 -> moverEntradaExterno -> Filainext -> Entradaext -> Espaciosext -> moverParqueoExterno -> Estacionando -> Universidad1 -> Libreext -> moverSalidaExterno -> Saliendoext -> Filaoutext -> Salidaext -> Estacionadoext
```

Si la simulacion compila pero el movimiento se ve raro, corregir primero el orden de Externo desde la interfaz de AnyLogic, no desde XML.

## Nodos/zonas que falta agregar

Faltan las zonas rectangulares equivalentes para Central y Polideportivo.

### 1. Crear `rParqueoCentral`

En AnyLogic:

1. Ir a `Palette > Space Markup`.
2. Arrastrar `Rectangular Node` sobre el estacionamiento Central de la imagen.
3. Renombrarlo a `rParqueoCentral`.
4. Ubicarlo cubriendo el area gris del parqueo Central, no la calle principal.
5. Usar un tamano aproximado inicial:

```text
X ~= 120
Y ~= 1080
Width ~= 560
Height ~= 380
```

6. Si AnyLogic permite agregar atractores automaticamente, usar layout aleatorio o crear varios attractors dentro del rectangulo.
7. No usar la capacidad real aqui como logica principal; la capacidad real sigue en `EstCentral = 73`.

### 2. Crear `rParqueoPolideportivo`

En AnyLogic:

1. Ir a `Palette > Space Markup`.
2. Arrastrar `Rectangular Node` sobre el estacionamiento inferior.
3. Renombrarlo a `rParqueoPolideportivo`.
4. Ubicarlo cubriendo el area gris del parqueo Polideportivo.
5. Usar un tamano aproximado inicial:

```text
X ~= 300
Y ~= 1580
Width ~= 930
Height ~= 300
```

6. Agregar attractors o dejar layout aleatorio si AnyLogic lo genera.
7. La capacidad real sigue en `EstIng = 91`.

## MoveTo que falta crear

Faltan seis bloques `MoveTo`:

### Para Central

- `moverEntradaCentral`
- `moverParqueoCentral`
- `moverSalidaCentral`

Configuracion:

| Bloque | Destination | Node/Zona |
| --- | --- | --- |
| `moverEntradaCentral` | `Network / GIS node` | `nEntradaCentral` |
| `moverParqueoCentral` | `Network / GIS node` | `rParqueoCentral` |
| `moverSalidaCentral` | `Network / GIS node` | `nSalidaGeneral` |

Flujo recomendado:

```text
Desicion2 -> moverEntradaCentral -> Filaincent -> Entradacent -> Espacioscent -> moverParqueoCentral -> Estacionandocent -> Universidad2 -> Librecent -> moverSalidaCentral -> Saliendocent -> Filaoutcent -> Salidacent -> Estacionadocent
```

### Para Polideportivo

- `moverEntradaPolideportivo`
- `moverParqueoPolideportivo`
- `moverSalidaPolideportivo`

Configuracion:

| Bloque | Destination | Node/Zona |
| --- | --- | --- |
| `moverEntradaPolideportivo` | `Network / GIS node` | `nEntradaPolideportivo` |
| `moverParqueoPolideportivo` | `Network / GIS node` | `rParqueoPolideportivo` |
| `moverSalidaPolideportivo` | `Network / GIS node` | `nSalidaGeneral` |

Flujo recomendado:

```text
Desicion3 -> moverEntradaPolideportivo -> FilainIng -> EntradaIng -> EspaciosIng -> moverParqueoPolideportivo -> EstacionandoIng -> Universidad3 -> LibreIng -> moverSalidaPolideportivo -> SaliendoIng -> FilaoutIng -> SalidaIng -> EstacionadoIng
```

## Como configurar cada MoveTo

En propiedades del bloque `MoveTo`:

- `Agent`: seleccionar `moves to`.
- `Destination`: seleccionar `Network / GIS node`.
- `Node`: seleccionar el nodo o zona correspondiente.
- `Movement is defined by`: dejar `Distance / speed`.
- `Set agent's speed`: opcional. Si los autos se mueven muy lento o muy rapido, activar y usar una velocidad visual razonable.

Configuracion ejemplo para `moverEntradaCentral`:

```text
Agent: moves to
Destination: Network / GIS node
Node: nEntradaCentral
Movement is defined by: Distance / speed
```

Configuracion ejemplo para `moverParqueoCentral`:

```text
Agent: moves to
Destination: Network / GIS node
Node: rParqueoCentral
Movement is defined by: Distance / speed
```

## Recomendacion de orden de trabajo

1. Abrir el modelo en AnyLogic.
2. Revisar que Externo compile y que los conectores esten en el orden esperado.
3. Si Externo esta mal conectado, corregirlo manualmente primero.
4. Crear `rParqueoCentral`.
5. Crear `rParqueoPolideportivo`.
6. Crear y configurar los 3 `MoveTo` de Central.
7. Probar simulacion.
8. Crear y configurar los 3 `MoveTo` de Polideportivo.
9. Probar simulacion completa.

## Validaciones esperadas

Despues de agregar los movimientos visuales:

- Los autos deben seguir siendo agentes `Autos` creados por `llegada`.
- Los `ResourcePool` deben seguir controlando la ocupacion.
- Los conteos de ocupacion, rechazos y saturacion no deberian cambiar salvo por pequenos tiempos extra si los `MoveTo` agregan duracion significativa.
- Si se desea que los tiempos estadisticos no cambien demasiado, mantener velocidades altas o tiempos visuales cortos en los `MoveTo`.

## Pendiente menor de datos

Hay una expresion de ocupacion total que aun usa `92 - EstIng.idle()` aunque `EstIng` tiene capacidad `91`.

Buscar y corregir:

```java
(100 - EstExterno.idle()) + (73 - EstCentral.idle()) + (92 - EstIng.idle())
```

por:

```java
(100 - EstExterno.idle()) + (73 - EstCentral.idle()) + (91 - EstIng.idle())
```

La mayoria de los otros graficos ya usan `91` correctamente.
