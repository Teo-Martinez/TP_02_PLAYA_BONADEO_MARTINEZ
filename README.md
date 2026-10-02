# TP POO - Banco Digital

Trabajo práctico grupal de Programación Orientada a Objetos: **Banco Digital POO**.
Resolución de las Partes 1 a 4 y preparación de los archivos de entrega de la
Parte 5 de la consigna `TP_Grupal_POO_Banco.ipynb`.

**Grupo:** 1. **Repositorio:** `tp-poo-banco-grupo1`.

## Integrantes

- Teo Martinez
- Tomas Playa
- Gonzalo Bonadeo

## Cómo ejecutarlo

Requiere Python 3. No utiliza paquetes externos.
Desde la carpeta del proyecto:

```bash
python main.py
```

La ejecución muestra la demostración y realiza las pruebas automáticas. La salida
esperada es:

```text
Cuenta 001 - Ana - Saldo: $1700.00
Cuenta 002 - Luis - Saldo: $-500.00
Total en el banco: 1200.0
¡Todas las pruebas pasaron!
```

Ejecutar sin la opción `-O`, porque las pruebas de la consigna usan `assert`.

## Estructura de la entrega

```text
tp-poo-banco-grupo1/
├── .gitignore
├── README.md
├── cuenta_bancaria.py
├── caja_de_ahorro.py
├── cuenta_corriente.py
├── banco.py
└── main.py
```

Cada clase está en su propio archivo. El notebook original se conserva localmente
como consigna y se excluye de Git, tal como exige la Parte 5. El borrador vacío
`tp.py` también se excluye.

## Requisitos implementados

| Parte | Implementación |
| --- | --- |
| 1. Cuenta bancaria | `titular` y `numero` como `str`; `_saldo` como `float`, saldo inicial cero por defecto, propiedad `saldo`, depósitos, extracciones y `__str__` con dos decimales. |
| 2. Herencia | `CajaDeAhorro` y `CuentaCorriente` heredan de `CuentaBancaria` y reutilizan su constructor con `super()`. |
| 2. Interés | `aplicar_interes()` suma al saldo el interés calculado con `tasa_interes`. |
| 2. Polimorfismo | `CuentaCorriente.extraer()` permite un saldo negativo hasta `-limite_descubierto`, inclusive. |
| 3. Banco | Diccionario protegido de cuentas; alta sin números repetidos; búsqueda con `None` si no existe; transferencias por número; total y listado. |
| 4. Pruebas | `main.py` incluye todas las pruebas originales y pruebas adicionales de límites, errores y conservación de saldos. |
| 5. Entrega | Una clase por archivo, programa principal independiente, README con integrantes y al menos tres commits locales. |

## Validaciones y decisiones

- Depósitos y extracciones requieren montos numéricos, finitos y mayores a cero.
- El saldo inicial, la tasa de interés y el límite de descubierto deben ser
  finitos y no negativos. Una tasa de `0.05` representa un 5 %.
- Una cuenta base o caja de ahorro no permite extraer más que su saldo.
- El interés se aplica sobre el saldo actual; una tasa o saldo cero no lo cambia.
- Una transferencia requiere dos cuentas existentes y distintas. El destino se
  valida antes de extraer del origen. Los casos rechazados conservan los saldos.
- `total_depositado()` suma los saldos actuales, incluidos los negativos de las
  cuentas corrientes, como indica la consigna.
- Se utilizan `float` según lo solicitado; las comparaciones de resultados
  decimales en las pruebas emplean tolerancia cuando corresponde.

## Conceptos de POO

1. **Encapsulamiento:** `_saldo` indica un atributo protegido por convención.
   Se consulta mediante la propiedad `saldo` y se modifica a través de los métodos
   que aplican las validaciones. La propiedad no tiene setter.
2. **Herencia y `super()`:** las clases hijas reutilizan la inicialización de la
   clase base, evitando repetir la gestión del titular, número y saldo inicial.
3. **Polimorfismo:** `Banco.transferir()` llama a `origen.extraer(monto)`.
   Python utiliza la implementación de la cuenta concreta, por lo que una cuenta
   corriente puede usar descubierto y una caja de ahorro no puede hacerlo.
4. **Agregación:** el banco mantiene referencias a objetos cuenta en `_cuentas`;
   las cuentas se crean de forma independiente y luego se agregan al banco.

## Publicación en GitHub

Para completar la Parte 5, falta publicar el repositorio, agregar a los
colaboradores y entregar su enlace. La consigna propone crear el README en GitHub;
en esta carpeta el README ya está creado y guardado en el historial local.

1. Crear un repositorio **público** llamado `tp-poo-banco-grupo1`.
   Como esta carpeta ya tiene README y commits,
   crear el repositorio remoto vacío, sin agregar README, licencia ni `.gitignore`.
2. Desde esta carpeta, conectar el repositorio y subir la rama `main`:

   ```bash
   git remote add origin https://github.com/USUARIO/tp-poo-banco-grupo1.git
   git push -u origin main
   ```

   Reemplazar `USUARIO` por el usuario de GitHub que cree el repositorio.

3. Agregar a los demás integrantes como colaboradores del repositorio.
4. Verificar que los archivos estén publicados y que se vean al menos tres
   commits. Se puede comprobar el historial local con `git log --oneline`.
5. Entregar el enlace del repositorio en el aula virtual o formulario indicado
   por el docente.

Subir mediante Git conserva los commits locales que exige la consigna.
