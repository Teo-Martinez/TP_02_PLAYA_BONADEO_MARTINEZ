"""Caja de ahorro que agrega intereses al saldo."""

from cuenta_bancaria import CuentaBancaria


class CajaDeAhorro(CuentaBancaria):
    def __init__(self, titular, numero, saldo_inicial=0, tasa_interes=0.05):
        super().__init__(titular, numero, saldo_inicial)
        self.tasa_interes = self._validar_importe(
            tasa_interes, "valor de la tasa de interés", permitir_cero=True
        )

    def aplicar_interes(self):
        interes = self.saldo * self.tasa_interes
        if interes != 0:
            self.depositar(interes)
