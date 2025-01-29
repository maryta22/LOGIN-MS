from connexion import FlaskApp

from swagger_server import encoder


def main():
    app = FlaskApp(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'LOGIN-MS'}, pythonic_params=True)
    app.run(host='0.0.0.0', port=2045)


if __name__ == '__main__':
    main()
