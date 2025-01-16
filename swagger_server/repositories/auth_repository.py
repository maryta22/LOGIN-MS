import datetime
import logging
from datetime import datetime

from flask import jsonify
from sqlalchemy.orm import sessionmaker, joinedload
from sqlalchemy import create_engine
from swagger_server.database_models.models import User, SalesAdvisor, Administrator
from dotenv import load_dotenv
import os

from sqlalchemy.orm import aliased

load_dotenv()

class AuthRepository:
    def __init__(self):
        db_password = os.getenv('DB_PASSWORD')
        self.engine = create_engine(f'mysql+pymysql://root:{db_password}@localhost:3306/espae_prospections')
        self.Session = sessionmaker(bind=self.engine)

    def auth_email(self, email):
        session = self.Session()
        try:
            print("Iniciando auth_email")

            if not email:
                print("No se proporcionó un correo")
                return {
                    "error": "No se proporcionó un correo",
                    "role": "invalid",
                    "user_data": None
                }

            print(f"Buscando usuario con email: {email}")
            user = session.query(User).filter(User.email == email).first()

            if not user:
                print("No se encontró el usuario en la base de datos")
                return {
                    "error": "No registrado como usuario activo. Contáctese con el Administrador",
                    "role": "invalid",
                    "user_data": None
                }

            print(f"Usuario encontrado: {user.to_dict()}")

            print("Verificando si el usuario es administrador")
            admin = session.query(Administrator).filter(
                Administrator.id_user == user.id,
                Administrator.state == 1
            ).first()

            if admin:
                print(f"Usuario es administrador: {admin}")
                return {
                    "role": "admin",
                    "user_data": {
                        **user.to_dict(),
                        "additional_info": {
                            "creation_date": admin.creation_date.strftime('%Y-%m-%d') if admin.creation_date else None,
                            "modification_date": admin.modification_date.strftime('%Y-%m-%d') if admin.modification_date else None
                        }
                    }
                }

            print("Verificando si el usuario es vendedor")
            sales_advisor = session.query(SalesAdvisor).filter(
                SalesAdvisor.id_user == user.id,
                SalesAdvisor.state == 1
            ).first()

            if sales_advisor:
                print(f"Usuario es vendedor: {sales_advisor}")
                return {
                    "role": "user",
                    "user_data": {
                        **user.to_dict(),
                        "additional_info": {
                            "sales_advisor_id": sales_advisor.id
                        }
                    }
                }

            print("Usuario no activo")
            return {
                "error": "Usuario no se encuentra activo. Contáctese con el Administrador",
                "role": "invalid",
                "user_data": None
            }

        except Exception as e:
            print(f"Error en auth_email: {str(e)}")
            logging.error(f"Error en auth_email: {str(e)}")
            return {
                "error": f"Error directo: {str(e)}",
                "role": "invalid",
                "user_data": None
            }
        finally:
            print("Cerrando sesión de base de datos")
            session.close()


