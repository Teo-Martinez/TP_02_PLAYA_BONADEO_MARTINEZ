"""Cuenta corriente que permite utilizar un descubierto limitado."""

from cuenta_bancaria import CuentaBancaria


class CuentaCorriente(CuentaBancaria):
    def __init__(self, titular, numero, saldo_inicial=0, limite_descubierto=2000):
        super().__init__(titular, numero, saldo_inicial)
        self.limite_descubierto = self._validar_importe(
            limite_descubierto, "límite de descubierto", permitir_cero=True
        )

    def extraer(self, monto):
        """Sobrescribe la extracción para admitir un saldo negativo limitado."""
        monto = self._validar_importe(monto)
        nuevo_saldo = self._saldo - monto
        if nuevo_saldo < -self.limite_descubierto:
            raise ValueError("La extracción supera el límite de descubierto.")
        self._saldo = nuevo_saldo
