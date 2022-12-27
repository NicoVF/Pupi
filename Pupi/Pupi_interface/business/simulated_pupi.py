from Pupi_interface.business import Result


class SimulatedPupi:
    def send_xml(self, client, xml):
        result = Result()
        if len(xml) == 0:
            result.add_error("status code: 400\n" + \
                             "content: <errors xmlns=\"http://chat.soybot.com/catalogo/V1\"><error>Root element is " \
                             "missing.</error></errors>")
        return result

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


