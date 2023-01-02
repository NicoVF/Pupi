

class Pupi:

    def send_xml(self):
        raise NotImplementedError('Subclass responsibility')

    def convert_to_xml(self, csv):
        rows = csv.splitlines()
        marca_elements = ""
        last_row = ""
        for row in rows:
            marca_element = self._convert_row_to_xml(row, last_row)
            marca_elements += marca_element
            last_row = row
        converted_xml = f"<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
{marca_elements}\
            </marcas>\
        "
        return converted_xml

    def _convert_row_to_xml(self, row, previous_row):
        fields = row.split(',')
        previous_fields = previous_row.split(',')
        current_brand = fields[0]
        previous_brand = previous_fields[0]
        if previous_brand == current_brand:
            return ""
        modelo_elemento = ""
        if len(fields) > 1:
            modelo = fields[1]
            modelo_elemento = f"                    <modelo display='{modelo}' estado='activo'>" + \
                              "                    </modelo>"

        return f"                <marca nombre='{current_brand}' estado='activo'>\
{modelo_elemento}\
                </marca>"