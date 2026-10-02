"""Demostración y pruebas automáticas del trabajo práctico Banco Digital POO."""

from math import isclose

from cuenta_bancaria import CuentaBancaria
from caja_de_ahorro import CajaDeAhorro
from cuenta_corriente import CuentaCorriente
from banco import Banco


def probar(condicion, mensaje):
    assert condicion, mensaje


def ejecutar_pruebas():
    """Ejecuta todas las pruebas originales de la Parte 4 del notebook."""
    # --- CuentaBancaria ---
    c = CuentaBancaria("Test", "T1", 100)
    probar(c.saldo == 100, "El saldo inicial no es correcto")
    c.depositar(50)
    probar(c.saldo == 150, "depositar no suma bien")
    c.extraer(30)
    probar(c.saldo == 120, "extraer no resta bien")
    for malo in (lambda: c.depositar(-10), lambda: c.extraer(0), lambda: c.extraer(10_000)):
        try:
            malo()
            probar(False, "Falta validar montos inválidos o saldo insuficiente")
        except ValueError:
            pass
    probar("T1" in str(c) and "Test" in str(c), "__str__ debe mostrar número y titular")

    # --- CajaDeAhorro ---
    a = CajaDeAhorro("Test", "T2", 1000, 0.10)
    probar(isinstance(a, CuentaBancaria), "CajaDeAhorro debe heredar de CuentaBancaria")
    a.aplicar_interes()
    probar(abs(a.saldo - 1100) < 0.01, "aplicar_interes no calcula bien")

    # --- CuentaCorriente ---
    cc = CuentaCorriente("Test", "T3", 500, 2000)
    cc.extraer(2500)
    probar(cc.saldo == -2000, "CuentaCorriente debe permitir descubierto hasta el límite")
    try:
        cc.extraer(1)
        probar(False, "CuentaCorriente no debe superar el límite de descubierto")
    except ValueError:
        pass

    # --- Banco ---
    b = Banco("Test")
    b.agregar_cuenta(CajaDeAhorro("A", "X1", 1000))
    b.agregar_cuenta(CuentaCorriente("B", "X2", 0, 500))
    try:
        b.agregar_cuenta(CuentaBancaria("C", "X1"))
        probar(False, "No se deben permitir números de cuenta repetidos")
    except ValueError:
        pass
    probar(b.buscar_cuenta("NOEXISTE") is None, "buscar_cuenta debe devolver None si no existe")
    b.transferir("X2", "X1", 300)
    probar(b.buscar_cuenta("X1").saldo == 1300, "transferir no deposita bien en el destino")
    probar(b.buscar_cuenta("X2").saldo == -300, "transferir no extrae bien del origen")
    probar(b.total_depositado() == 1000, "total_depositado no suma bien")

    print("¡Todas las pruebas pasaron!")


def esperar_value_error(operacion):
    """Comprueba que una operación inválida lance la excepción esperada."""
    try:
        operacion()
    except ValueError:
        return
    raise AssertionError("La operación debía lanzar ValueError")


def ejecutar_pruebas_adicionales():
    """Comprueba límites y que los errores no alteren los saldos."""
    for clase in (CuentaBancaria, CajaDeAhorro, CuentaCorriente):
        cuenta = clase("Prueba", "P1", 100)
        for monto in (0, -1, float("nan"), float("inf"), "10", None, True):
            for operacion in (cuenta.depositar, cuenta.extraer):
                esperar_value_error(lambda: operacion(monto))
                probar(cuenta.saldo == 100, "Una operación inválida modificó el saldo")
        probar(isinstance(cuenta.saldo, float), "El saldo debe ser float")
        try:
            cuenta.saldo = 0
        except AttributeError:
            pass
        else:
            raise AssertionError("saldo debe ser una propiedad de solo lectura")

    cuenta = CuentaBancaria("Ana", "001", 1000)
    cuenta.depositar(500)
    probar(str(cuenta) == "Cuenta 001 - Ana - Saldo: $1500.00", "Formato incorrecto de __str__")
    cuenta.extraer(1500)
    probar(cuenta.saldo == 0, "Debe permitir extraer el saldo exacto")
    esperar_value_error(lambda: cuenta.extraer(1))

    for clase in (CuentaBancaria, CajaDeAhorro, CuentaCorriente):
        probar(clase("Prueba", "P0").saldo == 0, "El saldo inicial predeterminado debe ser cero")
        for saldo in (-1, float("nan"), float("inf")):
            esperar_value_error(lambda: clase("Prueba", "P0", saldo))
    esperar_value_error(lambda: CajaDeAhorro("Prueba", "P0", tasa_interes=-0.1))
    esperar_value_error(lambda: CuentaCorriente("Prueba", "P0", limite_descubierto=-1))

    for ahorro in (CajaDeAhorro("Prueba", "A0"), CajaDeAhorro("Prueba", "A1", 100, 0)):
        saldo_anterior = ahorro.saldo
        ahorro.aplicar_interes()
        probar(ahorro.saldo == saldo_anterior, "El interés cero debe conservar el saldo")
    ahorro = CajaDeAhorro("Prueba", "A2", 1000, 0.10)
    ahorro.aplicar_interes()
    ahorro.aplicar_interes()
    probar(isclose(ahorro.saldo, 1210), "El interés debe aplicarse sobre el saldo actualizado")

    corriente = CuentaCorriente("Prueba", "C1", 500, 2000)
    corriente.extraer(2500)
    esperar_value_error(lambda: corriente.extraer(1))
    probar(corriente.saldo == -2000, "El rechazo debe conservar el saldo en el límite")
    corriente.depositar(2000)
    probar(corriente.saldo == 0, "El depósito debe cancelar el descubierto")
    sin_descubierto = CuentaCorriente("Prueba", "C0", limite_descubierto=0)
    esperar_value_error(lambda: sin_descubierto.extraer(1))

    banco = Banco("Pruebas adicionales")
    probar(banco.total_depositado() == 0, "Un banco vacío debe tener total cero")
    cuentas = (
        CuentaBancaria("Base", "B", 100),
        CajaDeAhorro("Ahorro", "A", 100),
        CuentaCorriente("Corriente", "C", 0, 100),
    )
    for cuenta in cuentas:
        banco.agregar_cuenta(cuenta)
        probar(banco.buscar_cuenta(cuenta.numero) is cuenta, "El banco debe guardar el objeto recibido")
    esperar_value_error(lambda: banco.agregar_cuenta(CuentaBancaria("Duplicada", "B", 999)))
    probar(banco.buscar_cuenta("B") is cuentas[0], "Un duplicado no debe reemplazar la cuenta original")
    esperar_value_error(lambda: banco.agregar_cuenta(object()))

    transferencias_invalidas = [
        ("NOEXISTE", "A", 10), ("B", "NOEXISTE", 10),
        ("B", "B", 10), ("B", "A", 101), ("C", "A", 101),
    ]
    transferencias_invalidas.extend(
        ("B", "A", monto) for monto in (0, -1, float("nan"), float("inf"), "10", None, True)
    )
    for origen, destino, monto in transferencias_invalidas:
        saldos_antes = tuple(cuenta.saldo for cuenta in cuentas)
        esperar_value_error(lambda: banco.transferir(origen, destino, monto))
        probar(tuple(cuenta.saldo for cuenta in cuentas) == saldos_antes, "Una transferencia rechazada modificó los saldos")

    total_antes = banco.total_depositado()
    banco.transferir("B", "A", 25.50)
    banco.transferir("A", "B", 10.25)
    banco.transferir("C", "A", 100)
    probar(cuentas[0].saldo == 84.75, "Transferencia incorrecta desde la cuenta base")
    probar(cuentas[1].saldo == 215.25, "Transferencia incorrecta desde la caja de ahorro")
    probar(cuentas[2].saldo == -100, "Debe transferir hasta el límite de descubierto")
    probar(isclose(banco.total_depositado(), total_antes), "Las transferencias deben conservar el total")

    banco_grande = Banco("Límites numéricos")
    origen = CuentaBancaria("Origen", "O", 1e308)
    destino = CuentaBancaria("Destino", "D", 1e308)
    banco_grande.agregar_cuenta(origen)
    banco_grande.agregar_cuenta(destino)
    esperar_value_error(lambda: destino.depositar(1e308))
    esperar_value_error(lambda: banco_grande.transferir("O", "D", 1e308))
    probar(origen.saldo == destino.saldo == 1e308, "Un saldo fuera de rango no debe modificar las cuentas")


def main():
    banco = Banco("Banco POO")
    banco.agregar_cuenta(CajaDeAhorro("Ana", "001", 1000))
    banco.agregar_cuenta(CuentaCorriente("Luis", "002", 200, 1000))
    banco.transferir("002", "001", 700)
    banco.listar_cuentas()
    print("Total en el banco:", banco.total_depositado())

    ejecutar_pruebas_adicionales()
    ejecutar_pruebas()


if __name__ == "__main__":
    main()
