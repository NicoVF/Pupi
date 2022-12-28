

class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        marca_elements = ""
        for row in rows:
            marca_element = self._convert_row_to_xml(row)
            marca_elements += marca_element
        converted_xml = f"<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
{marca_elements}\
            </marcas>\
        "
        return converted_xml

    def _convert_row_to_xml(self, row):
        fields = row.split(',')
        marca = fields[0]
        modelo_elemento = ""
        if len(fields) > 1:
            modelo = fields[1]
            modelo_elemento = f"                    <modelo display='{modelo}' estado='activo'>" + \
                              "                    </modelo>"

        return f"                <marca nombre='{marca}' estado='activo'>\
{modelo_elemento}\
                </marca>"