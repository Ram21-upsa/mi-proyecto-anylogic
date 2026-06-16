# TODO: Movimiento visual de autos en AnyLogic

## Estado actual

- Modelo vigente: `EstacionamientoV1.original.alp`.
- Imagen de fondo ya agregada como recurso: `fondos_parqueo_upsa.png`.
- La imagen esta colocada en `Main`, aprox. en `X=0`, `Y=1000`, `Width=1672`, `Height=941`.
- Ya existen estos `PointNode`:
  - `nEntradaGeneral`
  - `nEntradaExterno`
  - `nSalidaGeneral`
  - `nEntradaCentral`
  - `nEntradaPolideportivo`
- Ya existe un `MoveTo` creado manualmente desde AnyLogic:
  - `moverEntradaExterno`
- Tambien aparecen creados, pero aparentemente sin configurar completamente:
  - `moverParqueoExterno`
  - `moverSalidaExterno`

## Backup

Antes de tocar el XML hice una copia:

```text
EstacionamientoV1.original.alp.bak-before-moveto
```

## Hallazgos importantes

- `moverEntradaExterno` esta configurado como `MoveTo` hacia `nEntradaExterno`.
- AnyLogic cambio conectores alrededor de la rama Externo, pero el flujo quedo sospechoso:
  - `Filainext -> moverEntradaExterno`
  - `moverEntradaExterno -> Desicion1`
- Lo esperado conceptualmente era mover despues de `Desicion1` hacia la entrada del externo, no necesariamente volver a `Desicion1`. Revisar visualmente en AnyLogic antes de seguir.
- Hay una inconsistencia menor en graficos:
  - `EstIng` tiene capacidad `91`.
  - Dos expresiones aun usan `92 - EstIng.idle()`.
  - Cambiar esas expresiones a `91 - EstIng.idle()`.

## Objetivo final

Que los autos se vean moviendose sobre el fondo:

```text
llegada -> decision -> entrada parqueo -> punto/zona parqueo -> salida general -> sink
```

La logica de ocupacion debe seguir controlada por:

- `EstExterno = 100`
- `EstCentral = 73`
- `EstIng = 91`

## Recomendacion para retomar

Como el XML de `MoveTo` es delicado, retomar desde AnyLogic para evitar romper el modelo.

### 1. Corregir rama Externo primero

El flujo recomendado para Externo es:

```text
Desicion1 -> moverEntradaExterno -> Filainext -> Entradaext -> Espaciosext -> moverParqueoExterno -> Estacionando -> Universidad1 -> Libreext -> moverSalidaExterno -> Saliendoext -> Filaoutext -> Salidaext -> Estacionadoext
```

Configurar:

- `moverEntradaExterno`
  - Destination: `Network / GIS node`
  - Node: `nEntradaExterno`
- `moverParqueoExterno`
  - Opcion segura: crear `PointNode` llamado `nParqueoExterno` dentro del estacionamiento Externo y mover hacia ese nodo.
  - Opcion mejor: usar coordenadas aleatorias dentro del area del parqueo externo.
- `moverSalidaExterno`
  - Destination: `Network / GIS node`
  - Node: `nSalidaGeneral`

### 2. Crear nodos de parqueo

Crear estos `PointNode` sobre la imagen:

- `nParqueoCentral`: dentro del parqueo Central.
- `nParqueoExterno`: dentro del parqueo Externo.
- `nParqueoPolideportivo`: dentro del parqueo Polideportivo.

Esto es mas simple que coordenadas aleatorias y evita errores de configuracion.

### 3. Replicar para Central

Crear bloques:

- `moverEntradaCentral`
- `moverParqueoCentral`
- `moverSalidaCentral`

Flujo recomendado:

```text
Desicion2 -> moverEntradaCentral -> Filaincent -> Entradacent -> Espacioscent -> moverParqueoCentral -> Estacionandocent -> Universidad2 -> Librecent -> moverSalidaCentral -> Saliendocent -> Filaoutcent -> Salidacent -> Estacionadocent
```

Configurar:

- `moverEntradaCentral` -> `nEntradaCentral`
- `moverParqueoCentral` -> `nParqueoCentral`
- `moverSalidaCentral` -> `nSalidaGeneral`

### 4. Replicar para Polideportivo

Crear bloques:

- `moverEntradaPolideportivo`
- `moverParqueoPolideportivo`
- `moverSalidaPolideportivo`

Flujo recomendado:

```text
Desicion3 -> moverEntradaPolideportivo -> FilainIng -> EntradaIng -> EspaciosIng -> moverParqueoPolideportivo -> EstacionandoIng -> Universidad3 -> LibreIng -> moverSalidaPolideportivo -> SaliendoIng -> FilaoutIng -> SalidaIng -> EstacionadoIng
```

Configurar:

- `moverEntradaPolideportivo` -> `nEntradaPolideportivo`
- `moverParqueoPolideportivo` -> `nParqueoPolideportivo`
- `moverSalidaPolideportivo` -> `nSalidaGeneral`

## Si se quiere usar coordenadas aleatorias luego

Solo despues de que la version con nodos funcione, cambiar los `moverParqueo...` a coordenadas aleatorias aproximadas.

Rangos tentativos segun imagen:

```java
// Central
X: uniform(150, 650)
Y: uniform(1100, 1450)

// Externo
X: uniform(900, 1500)
Y: uniform(1100, 1450)

// Polideportivo
X: uniform(300, 1200)
Y: uniform(1600, 1850)
```

Ajustar visualmente si los autos caen fuera de los parqueos.

## Verificacion

1. Correr el modelo solo con Externo arreglado.
2. Verificar que los autos se vean moviendose sobre la imagen.
3. Verificar que ocupacion/rechazos sigan funcionando.
4. Luego replicar Central y Polideportivo.

## Pendientes concretos

- [ ] Revisar en AnyLogic si `moverEntradaExterno` esta conectado en el lugar correcto.
- [ ] Crear `nParqueoExterno`, `nParqueoCentral`, `nParqueoPolideportivo`.
- [ ] Configurar `moverParqueoExterno` y `moverSalidaExterno`.
- [ ] Replicar `MoveTo` para Central.
- [ ] Replicar `MoveTo` para Polideportivo.
- [ ] Corregir `92 - EstIng.idle()` a `91 - EstIng.idle()`.
- [ ] Probar simulacion.
