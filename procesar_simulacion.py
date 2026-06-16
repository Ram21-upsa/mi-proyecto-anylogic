#!/usr/bin/env python3
"""
Procesa el CSV de eventos generado por AnyLogic y genera una tabla resumen por hora.

Uso:
    python procesar_simulacion.py simulacion_eventos.csv [salida.csv] [--inicio YYYY-MM-DD]

Si no se especifica fecha de inicio, usa 2026-05-21 (fecha del InitialDate en el modelo).
Si no se especifica archivo de salida, genera: resumen_horario.csv
"""

import csv
import sys
from datetime import datetime, timedelta
from collections import defaultdict


DIAS_ES = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]


def hora_a_fecha(hora_sim, fecha_inicio):
    """Convierte hora de simulación a fecha/hora legible."""
    dt = fecha_inicio + timedelta(hours=hora_sim)
    return dt


def formato_rango(dt):
    """Devuelve '07:00 - 08:00' para un datetime."""
    inicio = dt.strftime("%H:%M")
    fin = (dt + timedelta(hours=1)).strftime("%H:%M")
    return f"{inicio} - {fin}"


def formato_dia(dt):
    """Devuelve 'Jueves 21' para un datetime."""
    nombre = DIAS_ES[dt.weekday()]
    return f"{nombre} {dt.day}"


def procesar(archivo_entrada, archivo_salida, fecha_inicio):
    horas = defaultdict(lambda: {
        "ent_ext": 0, "sal_ext": 0, "ocup_ext": 0,
        "ent_cent": 0, "sal_cent": 0, "ocup_cent": 0,
        "ent_poli": 0, "sal_poli": 0, "ocup_poli": 0,
        "rechazados": 0,
    })

    with open(archivo_entrada, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            hora = int(float(row["hora"]))
            evento = row["evento"]
            parqueo = row["parqueo"]
            ocup_ext = int(float(row["ocup_externo"]))
            ocup_cent = int(float(row["ocup_central"]))
            ocup_poli = int(float(row["ocup_polideportivo"]))
            rechazados = int(float(row["rechazados"]))

            h = horas[hora]
            h["ocup_ext"] = ocup_ext
            h["ocup_cent"] = ocup_cent
            h["ocup_poli"] = ocup_poli
            h["rechazados"] = rechazados

            if evento == "entrada":
                if parqueo == "Externo":
                    h["ent_ext"] += 1
                elif parqueo == "Central":
                    h["ent_cent"] += 1
                elif parqueo == "Polideportivo":
                    h["ent_poli"] += 1
            elif evento == "salida":
                if parqueo == "Externo":
                    h["sal_ext"] += 1
                elif parqueo == "Central":
                    h["sal_cent"] += 1
                elif parqueo == "Polideportivo":
                    h["sal_poli"] += 1

    filas = []
    for hora in sorted(horas.keys()):
        h = horas[hora]
        ent_total = h["ent_ext"] + h["ent_cent"] + h["ent_poli"]
        sal_total = h["sal_ext"] + h["sal_cent"] + h["sal_poli"]
        ocup_total = h["ocup_ext"] + h["ocup_cent"] + h["ocup_poli"]
        dt = hora_a_fecha(hora, fecha_inicio)
        filas.append({
            "hora_sim": hora,
            "fecha": dt,
            "rango": formato_rango(dt),
            "ent_ext": h["ent_ext"], "sal_ext": h["sal_ext"], "ocup_ext": h["ocup_ext"],
            "ent_cent": h["ent_cent"], "sal_cent": h["sal_cent"], "ocup_cent": h["ocup_cent"],
            "ent_poli": h["ent_poli"], "sal_poli": h["sal_poli"], "ocup_poli": h["ocup_poli"],
            "ent_total": ent_total, "sal_total": sal_total, "ocup_total": ocup_total,
            "rechazados": h["rechazados"],
        })

    # CSV
    header = [
        "Dia", "Hora",
        "EntExt", "SalExt", "OcupExt",
        "EntCent", "SalCent", "OcupCent",
        "EntPoli", "SalPoli", "OcupPoli",
        "EntTotal", "SalTotal", "OcupTotal",
        "Rechazados",
    ]

    with open(archivo_salida, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for fila in filas:
            writer.writerow([
                formato_dia(fila["fecha"]), fila["rango"],
                fila["ent_ext"], fila["sal_ext"], fila["ocup_ext"],
                fila["ent_cent"], fila["sal_cent"], fila["ocup_cent"],
                fila["ent_poli"], fila["sal_poli"], fila["ocup_poli"],
                fila["ent_total"], fila["sal_total"], fila["ocup_total"],
                fila["rechazados"],
            ])

    # Consola
    print(f"Resumen generado: {archivo_salida}")
    print(f"Fecha inicio: {fecha_inicio.strftime('%A %d %m %Y')}")
    print(f"Horas con datos: {len(filas)}")
    print()

    dia_actual = None
    for fila in filas:
        dt = fila["fecha"]
        dia_str = formato_dia(dt)

        if dia_str != dia_actual:
            if dia_actual is not None:
                print()
            print(f"  {dia_str}")
            print(f"  {'Hora':^21} | {'Externo':^17} | {'Central':^17} | {'Polideportivo':^17} | {'Total':^15} | {'Rech'}")
            print(f"  {'':21} | {'Ent':>5} {'Sal':>5} {'Ocu':>5} | {'Ent':>5} {'Sal':>5} {'Ocu':>5} | {'Ent':>5} {'Sal':>5} {'Ocu':>5} | {'Ent':>5} {'Sal':>5} {'Ocu':>5} | {'':>5}")
            print(f"  {'-' * 21}-+-{'-' * 17}-+-{'-' * 17}-+-{'-' * 17}-+-{'-' * 15}-+-{'-' * 5}")
            dia_actual = dia_str

        print(f"  {fila['rango']:>21} | {fila['ent_ext']:>5} {fila['sal_ext']:>5} {fila['ocup_ext']:>5} | {fila['ent_cent']:>5} {fila['sal_cent']:>5} {fila['ocup_cent']:>5} | {fila['ent_poli']:>5} {fila['sal_poli']:>5} {fila['ocup_poli']:>5} | {fila['ent_total']:>5} {fila['sal_total']:>5} {fila['ocup_total']:>5} | {fila['rechazados']:>5}")

    total_ent = sum(f["ent_total"] for f in filas)
    total_sal = sum(f["sal_total"] for f in filas)
    total_rech = sum(f["rechazados"] for f in filas)
    print(f"  {'-' * 21}-+-{'-' * 17}-+-{'-' * 17}-+-{'-' * 17}-+-{'-' * 15}-+-{'-' * 5}")
    print(f"  {'TOTAL':>21} | {'':>5} {'':>5} {'':>5} | {'':>5} {'':>5} {'':>5} | {'':>5} {'':>5} {'':>5} | {total_ent:>5} {total_sal:>5} {'':>5} | {total_rech:>5}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    archivo = sys.argv[1]
    salida = "resumen_horario.csv"
    fecha_inicio = datetime(2026, 5, 21, 7, 0)  # InitialDate del modelo

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--inicio" and i + 1 < len(args):
            fecha_inicio = datetime.strptime(args[i + 1], "%Y-%m-%d").replace(hour=7)
            i += 2
        else:
            salida = args[i]
            i += 1

    procesar(archivo, salida, fecha_inicio)
