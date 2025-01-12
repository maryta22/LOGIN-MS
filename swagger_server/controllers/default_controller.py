from flask import request, jsonify


from swagger_server.models.verificar_usuario_request import VerificarUsuarioRequest  # noqa: E501
from swagger_server.models.verificar_usuario_response import VerificarUsuarioResponse  # noqa: E501
from swagger_server import util


def verificar_tipo_usuario_post(body):  # noqa: E501
    """Verificar tipo de usuario

    Recibe un correo y devuelve el tipo de usuario asociado. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: VerificarUsuarioResponse
    """
    if request.is_json:
        body = VerificarUsuarioRequest.from_dict(request.get_json())  # noqa: E501
    return 'do some magic!'
