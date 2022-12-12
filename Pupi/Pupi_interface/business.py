class Result:
    def __init__(self):
        self._errors = []

    def add_error(self, error):
        self._errors.append(error)

    def is_succesfull(self):
        return len(self._errors) == 0

    def errors(self):
        return self._errors


class SimulatedPupi:
    def enviar_xml(self, client, xml):
        result = Result()
        if len(xml) == 0:
            result.add_error("Root element is missing.")
        return result


class Cliente:
    def __init__(self, cliente, sucursal, token):
        pass


