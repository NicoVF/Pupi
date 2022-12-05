class PreownedCar:
    def __init__(self, marca, cliente):
        self._marca = marca
        self._cliente = cliente

    def brand(self):
        return self._marca
