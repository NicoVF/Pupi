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
        fields = csv.split(',')
        marca = fields[0]
        modelo_elemento = ""
        if len(fields) > 1:
            modelo = fields[1]
            modelo_elemento = f"                    <modelo display='{modelo}' estado='activo'>" + \
                              "                    </modelo>"

        converted_xml = f"<?xml version='1.0' encoding='utf-8'?>\
            <marcas xmlns='http://chat.soybot.com/catalogo/V1'>\
                <marca nombre='{marca}' estado='activo'>\
{modelo_elemento}\
                </marca>\
            </marcas>\
        "

        return converted_xml
