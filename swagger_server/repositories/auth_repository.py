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
            if not email:
                return {
                    "error": "No se proporcionó un correo",
                    "role": "invalid",
                    "user_data": None
                }

            # Buscar el usuario por email
            user = session.query(User).filter(User.email == email).first()

            if not user:
                return {
                    "error": "No registrado como usuario activo. Contáctese con el Administrador",
                    "role": "invalid",
                    "user_data": None
                }

            # Verificar si es administrador
            admin = session.query(Administrator).filter(
                Administrator.id_user == user.id,
                Administrator.state == 1
            ).first()

            if admin:
                return {
                    "role": "admin",
                    "user_data": {
                        **user.to_dict(),
                        "additional_info": {
                            "creation_date": admin.creation_date.strftime('%Y-%m-%d'),
                            "modification_date": admin.modification_date.strftime(
                                '%Y-%m-%d') if admin.modification_date else None
                        }
                    }
                }

            # Verificar si es vendedor
            sales_advisor = session.query(SalesAdvisor).filter(
                SalesAdvisor.id_user == user.id,
                SalesAdvisor.state == 1
            ).first()

            if sales_advisor:
                return {
                    "role": "user",
                    "user_data": {
                        **user.to_dict(),
                        "additional_info": {
                            "sales_advisor_id": sales_advisor.id
                        }
                    }
                }

            return {
                "error": "Usuario no se encuentra activo. Contáctese con el Administrador",
                "role": "invalid",
                "user_data": None
            }

        except Exception as e:
            logging.error(f"Error en auth_email: {str(e)}")
            return {
                "error": f"Error directo: {str(e)}",
                "role": "invalid",
                "user_data": None
            }
        finally:
            session.close()

