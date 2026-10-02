"""Banco que agrupa cuentas y realiza transferencias entre ellas."""

from math import isfinite

from cuenta_bancaria import CuentaBancaria


class Banco:
    def __init__(self, nombre):
        self.nombre = nombre
        self._cuentas = {}

    def agregar_cuenta(self, cuenta):
        if not isinstance(cuenta, CuentaBancaria):
            raise ValueError("Solo se pueden agregar cuentas bancarias.")
        if cuenta.numero in self._cuentas:
            raise ValueError(f"Ya existe una cuenta con el número {cuenta.numero}.")
        self._cuentas[cuenta.numero] = cuenta

    def buscar_cuenta(self, numero):
        return self._cuentas.get(numero)

    def transferir(self, numero_origen, numero_destino, monto):
        origen = self.buscar_cuenta(numero_origen)
        destino = self.buscar_cuenta(numero_destino)
        if origen is None or destino is None:
            raise ValueError("Las cuentas de origen y destino deben existir.")
        if origen is destino:
            raise ValueError("Las cuentas de origen y destino deben ser distintas.")
        monto = CuentaBancaria._validar_importe(monto)
        # Validar el destino antes de extraer evita debitar una transferencia
        # que luego no podría acreditarse por exceder el rango numérico.
        if not isfinite(destino.saldo + monto):
            raise ValueError("La transferencia produce un saldo fuera de rango.")
        # Cada cuenta decide cómo extraer: aquí se aplica el polimorfismo.
        origen.extraer(monto)
        destino.depositar(monto)

    def total_depositado(self):
        return sum((cuenta.saldo for cuenta in self._cuentas.values()), 0.0)

    def listar_cuentas(self):
        for cuenta in self._cuentas.values():
            print(cuenta)
