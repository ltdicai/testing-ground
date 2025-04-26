from abc import ABC

class Vehiculo(ABC):
    def __init__(self, marca, modelo, marca_radio, potencia_radio):
        self._marca = marca
        self._modelo = modelo
        self._radio = Radio(marca_radio, potencia_radio, self)

    def __repr__(self):
        return f"{type(self).__name__} (marca: {self._marca}, modelo: {self._modelo}, radio: {self._radio})"
        


class AutoNuevo(Vehiculo):
    def __init__(self, marca, modelo, marca_radio, potencia_radio):
        super().__init__(marca, modelo, marca_radio, potencia_radio)

    def asignar_radio(self, radio):
        if not radio.esta_conectada():
            if self._radio:
                self._desconectar_radio()
            self._conectar_radio(radio)
        else:
            print("Radio ya conectada a otro vehiculo")

    def _desconectar_radio(self):
        self._radio._desconectar_vehiculo()
        self._radio = None

    def _conectar_radio(self, radio):
        radio._conectar_vehiculo(self)
        self._radio = radio
            


class Radio:
    def __init__(self, marca, potencia, vehiculo):
        self._marca = marca
        self._potencia = potencia
        self._vehiculo = vehiculo

    def esta_conectada(self):
        return self._vehiculo is not None

    def _desconectar_vehiculo(self):
        self._vehiculo = None

    def _conectar_vehiculo(self, vehiculo):
        self._vehiculo = vehiculo

    def __repr__(self):
        return f"{type(self).__name__} (marca: {self._marca}, potencia: {self._potencia}, vehiculo: {self._vehiculo and self._vehiculo._marca})"
        

def main():
    auto1 = AutoNuevo("aaa", "bbb", "sony", 20)
    radio1 = auto1._radio

    auto2 = AutoNuevo("ccc", "ddd", "hitachi", 15)
    radio2 = auto2._radio

    print(auto1)
    print(auto2)

    auto2.asignar_radio(auto1._radio)

    print(auto1)
    print(auto2)

    radio3 = Radio("Samsung", 300, None)

    auto2.asignar_radio(radio3)

    print(auto1)
    print(auto2)
    print(radio1)
    print(radio2)
    print(radio3)