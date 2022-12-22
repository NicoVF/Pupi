class Result:
    def __init__(self):
        self._errors = []

    def add_error(self, error):
        self._errors.append(error)

    def is_succesfull(self):
        return len(self._errors) == 0

    def errors(self):
        return self._errors


class Cliente:
    def __init__(self, cliente, sucursal, token):
        self._client_name = cliente
        self._sucursal = sucursal
        self._token = token

    def client_name(self):
        return self._client_name

    def sucursal(self):
        return self._sucursal

    def token(self):
        return self._token
