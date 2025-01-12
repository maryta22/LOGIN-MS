from flask import request, jsonify


from swagger_server.models.verificar_usuario_request import VerificarUsuarioRequest  # noqa: E501
from swagger_server.models.verificar_usuario_response import VerificarUsuarioResponse  # noqa: E501

from swagger_server.repositories.auth_repository import AuthRepository  # Import repository
from swagger_server import util

auth_repository = AuthRepository()

def verificar_tipo_usuario_post(body):  # noqa: E501
    """Verificar tipo de usuario

    Recibe un correo y devuelve el tipo de usuario asociado. # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: VerificarUsuarioResponse
    """
    if request.is_json:
        try:
            data = request.get_json()
            response = auth_repository.auth_email(data['email'])
            return jsonify(response), 200

        except Exception as e:
            return {"message": f"Error processing request: {str(e)}"}, 500
    else:
        return {"message": "Request body must be JSON."}, 400
