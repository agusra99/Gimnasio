from datetime import datetime
from modelos.socio import Socio
from modelos.pago import Pago

def obtener_socios_deudores():
    hoy = datetime.today()
    if hoy.day <= 10:
        return []

    periodo_actual = hoy.strftime("%Y-%m")
    socios = Socio.obtener_todos()
    deudores = []

    for socio in socios:
        socio_id = socio[0]
        ultimo_pago = Pago.obtener_ultimo_periodo_pagado(socio_id)
        if ultimo_pago != periodo_actual:
            deudores.append({
                "nombre": f"{socio[1]} {socio[2]}",
                "telefono": socio[4],
                "deuda": periodo_actual
            })

    return deudores