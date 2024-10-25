from BD import DatabaseManager
from neo_config import uri, user, password

class CRUDOperations:
    def _init_(self):
        self.db_manager = DatabaseManager(uri, user, password)

    def create_profesor(self, nombre, apellido, direccion, telefono, email, registro, carreras):
        self.db_manager.create_profesor(nombre, apellido, direccion, telefono, email, registro, carreras)
        print(f"Profesor {nombre} {apellido} creado exitosamente.")

    def get_profesores(self):
        with self.db_manager.driver.session() as session:
            result = session.run("MATCH (p:Profesor) RETURN p.nombre AS nombre, p.apellido AS apellido")
            print("Profesores:")
            for record in result:
                print(f"{record['nombre']} {record['apellido']}")

    def update_profesor(self, registro, nombre=None, apellido=None, direccion=None, telefono=None, email=None):
        with self.db_manager.driver.session() as session:
            session.run(
                "MATCH (p:Profesor {registro: $registro}) "
                "SET p.nombre = COALESCE($nombre, p.nombre), "
                "p.apellido = COALESCE($apellido, p.apellido), "
                "p.direccion = COALESCE($direccion, p.direccion), "
                "p.telefono = COALESCE($telefono, p.telefono), "
                "p.email = COALESCE($email, p.email)",
                registro=registro,
                nombre=nombre,
                apellido=apellido,
                direccion=direccion,
                telefono=telefono,
                email=email
            )
            print(f"Profesor con registro {registro} actualizado.")

    def delete_profesor(self, registro):
        with self.db_manager.driver.session() as session:
            session.run("MATCH (p:Profesor {registro: $registro}) DELETE p", registro=registro)
            print(f"Profesor con registro {registro} eliminado.")

    def close(self):
        self.db_manager.close()