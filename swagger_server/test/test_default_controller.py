# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.verificar_usuario_request import VerificarUsuarioRequest  # noqa: E501
from swagger_server.models.verificar_usuario_response import VerificarUsuarioResponse  # noqa: E501
from swagger_server.test import BaseTestCase


class TestDefaultController(BaseTestCase):
    """DefaultController integration test stubs"""

    def test_verificar_tipo_usuario_post(self):
        """Test case for verificar_tipo_usuario_post

        Verificar tipo de usuario
        """
        body = VerificarUsuarioRequest()
        response = self.client.open(
            '/api/v1/verificar-tipo-usuario',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
