"""Cuenta bancaria base: saldo protegido y operaciones validadas."""

from math import isfinite


class CuentaBancaria:
    def __init__(self, titular, numero, saldo_inicial=0):
        self.titular = titular
        self.numero = numero
        self._saldo = self._validar_importe(
            saldo_inicial, "saldo inicial", permitir_cero=True
        )

    @staticmethod
    def _validar_importe(valor, nombre="monto", permitir_cero=False):
        """Valida un número finito y devuelve su representación como float."""
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError(f"El {nombre} debe ser un número.")
        try:
            valor = float(valor)
        except OverflowError as error:
            raise ValueError(f"El {nombre} está fuera de rango.") from error
        if not isfinite(valor):
            raise ValueError(f"El {nombre} debe ser finito.")
        if valor < 0 or (valor == 0 and not permitir_cero):
            condicion = "mayor o igual a cero" if permitir_cero else "mayor a cero"
            raise ValueError(f"El {nombre} debe ser {condicion}.")
        return valor

    @property
    def saldo(self):
        """Permite consultar el saldo sin modificarlo desde afuera."""
        return self._saldo

    def depositar(self, monto):
        monto = self._validar_importe(monto)
        nuevo_saldo = self._saldo + monto
        if not isfinite(nuevo_saldo):
            raise ValueError("El depósito produce un saldo fuera de rango.")
        self._saldo = nuevo_saldo

    def extraer(self, monto):
        monto = self._validar_importe(monto)
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente para realizar la extracción.")
        self._saldo -= monto

    def __str__(self):
        return f"Cuenta {self.numero} - {self.titular} - Saldo: ${self.saldo:.2f}"
