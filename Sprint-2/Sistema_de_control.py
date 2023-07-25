import sys
import time
import pandas as pd
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QMessageBox, QFormLayout,QVBoxLayout,QInputDialog

class Mesa:
    def __init__(self, numero_mesa, capacidad):
        self.numero_mesa = numero_mesa
        self.capacidad = capacidad
        self.estado = "desocupada"  # Opciones: "ocupada", "desocupada"
        self.tiempo_asignacion = None
        self.tiempo_liberacion = None
        self.comandas = []  # Lista para almacenar las comandas asociadas a esta mesa

    def ocupar_mesa(self):
        self.estado = "ocupada"
        self.tiempo_asignacion = time.time()

    def liberar_mesa(self):
        self.estado = "desocupada"
        self.tiempo_liberacion = time.time()

    def agregar_comanda(self, comanda):
        self.comandas.append(comanda)

class Comanda:
    def __init__(self, numero_comanda, mesa_asociada):
        self.numero_comanda = numero_comanda
        self.mesa_asociada = mesa_asociada
        self.platos = []
        self.bebestibles = []
        self.estado = "en espera"  # Opciones: "en espera", "preparando", "cocinando", "terminado"
        self.tiempo_llegada = time.time()
        self.tiempo_terminacion = None

    def agregar_plato(self, nombre_plato):
        self.platos.append(nombre_plato)

    def agregar_bebestible(self, nombre_bebestible):
        self.bebestibles.append(nombre_bebestible)

    def cambiar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
        if nuevo_estado == "terminado":
            self.tiempo_terminacion = time.time()

class Chef:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad

    def preparar_plato(self, comanda, nombre_plato):
        time.sleep(5)  # Simulamos el tiempo de preparación
        comanda.cambiar_estado("cocinando")

class Bartender:
    def __init__(self, nombre, especialidad):
        self.nombre = nombre
        self.especialidad = especialidad

    def preparar_bebida(self, comanda, nombre_bebestible):
        time.sleep(3)  # Simulamos el tiempo de preparación
        comanda.cambiar_estado("preparando")

class Runner:
    def __init__(self, nombre):
        self.nombre = nombre

    def llevar_comanda_a_mesa(self, comanda):
        time.sleep(2)  # Simulamos el tiempo de entrega
        comanda.cambiar_estado("terminado")

class Restaurant:
    def __init__(self):
        self.mesas = []  # Lista para almacenar las mesas del restaurante
        self.comandas = []  # Lista para almacenar las comandas
        self.chefs = []  # Lista para almacenar los chefs
        self.bartenders = []  # Lista para almacenar los bartenders
        self.runners = []  # Lista para almacenar los runners

    def agregar_mesa(self, numero_mesa, capacidad):
        mesa = Mesa(numero_mesa, capacidad)
        self.mesas.append(mesa)

    def obtener_mesa_por_numero(self, numero_mesa):
        for mesa in self.mesas:
            if mesa.numero_mesa == numero_mesa:
                return mesa
        return None

    def agregar_comanda(self, mesa_asociada, comanda):
        mesa_asociada.agregar_comanda(comanda)
        self.comandas.append(comanda)

    def ocupar_mesa(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                mesa.ocupar_mesa()
                QMessageBox.information(self, "Éxito", f"Mesa {numero_mesa} ocupada.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def liberar_mesa(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                mesa.liberar_mesa()
                QMessageBox.information(self, "Éxito", f"Mesa {numero_mesa} liberada.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def ver_comandas(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                comandas = "\n".join([f"Comanda {c.numero_comanda}: {c.estado}" for c in mesa.comandas])
                QMessageBox.information(self, "Comandas", f"Comandas asociadas a la mesa {numero_mesa}:\n{comandas}")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def asignar_chef(self, nombre_chef, especialidad):
        chef = Chef(nombre_chef, especialidad)
        self.chefs.append(chef)

    def asignar_bartender(self, nombre_bartender, especialidad):
        bartender = Bartender(nombre_bartender, especialidad)
        self.bartenders.append(bartender)

    def asignar_runner(self, nombre_runner):
        runner = Runner(nombre_runner)
        self.runners.append(runner)

    def guardar_mesas_csv(self):
        data = [mesa.__dict__ for mesa in self.mesas]
        df = pd.DataFrame(data)
        df.to_csv("mesas.csv", index=False)

    def cargar_mesas_csv(self):
        try:
            df = pd.read_csv("mesas.csv")
            for _, row in df.iterrows():
                mesa = Mesa(row["numero_mesa"], row["capacidad"])
                mesa.estado = row["estado"]
                mesa.tiempo_asignacion = row["tiempo_asignacion"]
                mesa.tiempo_liberacion = row["tiempo_liberacion"]
                self.mesas.append(mesa)
        except FileNotFoundError:
            pass

    def guardar_comandas_csv(self):
        data = [comanda.__dict__ for comanda in self.comandas]
        df = pd.DataFrame(data)
        df.to_csv("comandas.csv", index=False)

    def cargar_comandas_csv(self):
        try:
            df = pd.read_csv("comandas.csv", encoding="latin-1")
            for _, row in df.iterrows():
                mesa_asociada = self.obtener_mesa_por_numero(row["mesa_asociada"])
                if mesa_asociada:
                    comanda = Comanda(row["numero_comanda"], mesa_asociada)
                    comanda.estado = row["estado"]
                    comanda.platos = [plato.strip() for plato in row["platos"].split(",")]
                    comanda.bebestibles = [bebida.strip() for bebida in row["bebestibles"].split(",")]
                    comanda.tiempo_llegada = row["tiempo_llegada"]
                    comanda.tiempo_terminacion = row["tiempo_terminacion"]
                    self.comandas.append(comanda)
        except FileNotFoundError:
            pass

class RestaurantApp(QWidget):
    def __init__(self, restaurante):
        super().__init__()
        self.restaurante = restaurante
        self.setWindowTitle("Sistema de Control de Restaurante")
        self.init_ui()

    def init_ui(self):
        self.entry_mesa = QLineEdit(self)
        self.button_agregar_comanda = QPushButton("Agregar Comanda", self)
        self.button_ocupar_mesa = QPushButton("Ocupar Mesa", self)
        self.button_liberar_mesa = QPushButton("Liberar Mesa", self)
        self.button_ver_disponibilidad = QPushButton("Ver Disponibilidad", self)  
        self.button_ver_comandas = QPushButton("Ver Comandas", self)
        self.button_cambiar_estado = QPushButton("Cambiar Estado", self)
        self.button_eliminar_comanda = QPushButton("Eliminar Comanda", self)
        # Botones para asignar personal
        self.button_asignar_chef = QPushButton("Asignar Chef", self)
        self.button_asignar_bartender = QPushButton("Asignar Bartender", self)
        self.button_asignar_runner = QPushButton("Asignar Runner", self) 

        self.button_agregar_comanda.clicked.connect(self.agregar_comanda)
        self.button_ocupar_mesa.clicked.connect(self.ocupar_mesa)
        self.button_liberar_mesa.clicked.connect(self.liberar_mesa)
        self.button_ver_disponibilidad.clicked.connect(self.ver_disponibilidad) 
        self.button_ver_comandas.clicked.connect(self.ver_comandas)
        self.button_cambiar_estado.clicked.connect(self.cambiar_estado)
        self.button_eliminar_comanda.clicked.connect(self.eliminar_comanda)
        self.button_asignar_chef.clicked.connect(self.asignar_chef)
        self.button_asignar_bartender.clicked.connect(self.asignar_bartender)
        self.button_asignar_runner.clicked.connect(self.asignar_runner)  



        form_layout = QFormLayout()
        form_layout.addRow("Número de Mesa:", self.entry_mesa)
        form_layout.addRow(self.button_agregar_comanda)
        form_layout.addRow(self.button_ocupar_mesa)
        form_layout.addRow(self.button_liberar_mesa)
        form_layout.addRow(self.button_ver_disponibilidad) 
        form_layout.addRow(self.button_ver_comandas)
        form_layout.addRow(self.button_cambiar_estado)
        form_layout.addRow(self.button_eliminar_comanda) 

        # Elementos para ingresar detalles de la comanda
        self.entry_plato = QLineEdit(self)
        self.entry_bebestible = QLineEdit(self)
        self.button_agregar_plato = QPushButton("Agregar Plato", self)
        self.button_agregar_bebestible = QPushButton("Agregar Bebestible", self)

        self.button_agregar_plato.clicked.connect(self.agregar_plato)
        self.button_agregar_bebestible.clicked.connect(self.agregar_bebestible)

        # Diseño de la interfaz
        vbox = QVBoxLayout()
        vbox.addLayout(form_layout)
        vbox.addWidget(self.entry_plato)
        vbox.addWidget(self.button_agregar_plato)
        vbox.addWidget(self.entry_bebestible)
        vbox.addWidget(self.button_agregar_bebestible)
        vbox.addWidget(self.button_asignar_chef)  # Agregar botón de asignar chef
        vbox.addWidget(self.button_asignar_bartender)  # Agregar botón de asignar bartender
        vbox.addWidget(self.button_asignar_runner)  # Agregar botón de asignar runner

        self.setLayout(vbox)

    def asignar_chef(self):
        nombre_chef, ok = QInputDialog.getText(self, "Asignar Chef", "Ingrese el nombre del Chef:")
        if ok and nombre_chef:
            especialidad, ok = QInputDialog.getText(self, "Asignar Chef", "Ingrese la especialidad del Chef:")
            if ok and especialidad:
                self.restaurante.asignar_chef(nombre_chef, especialidad)
                QMessageBox.information(self, "Éxito", f"Chef '{nombre_chef}' asignado con especialidad '{especialidad}'.")

    def asignar_bartender(self):
        nombre_bartender, ok = QInputDialog.getText(self, "Asignar Bartender", "Ingrese el nombre del Bartender:")
        if ok and nombre_bartender:
            especialidad, ok = QInputDialog.getText(self, "Asignar Bartender", "Ingrese la especialidad del Bartender:")
            if ok and especialidad:
                self.restaurante.asignar_bartender(nombre_bartender, especialidad)
                QMessageBox.information(self, "Éxito", f"Bartender '{nombre_bartender}' asignado con especialidad '{especialidad}'.")

    def asignar_runner(self):
        nombre_runner, ok = QInputDialog.getText(self, "Asignar Runner", "Ingrese el nombre del Runner:")
        if ok and nombre_runner:
            self.restaurante.asignar_runner(nombre_runner)
            QMessageBox.information(self, "Éxito", f"Runner '{nombre_runner}' asignado.")

    def ver_disponibilidad(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                estado = "ocupada" if mesa.estado == "ocupada" else "liberada"
                QMessageBox.information(self, "Disponibilidad", f"La mesa {numero_mesa} está {estado}.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def agregar_comanda(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)  # Usamos self.restaurante
            if mesa:
                comanda = Comanda(len(self.restaurante.comandas) + 1, mesa)  # Usamos self.restaurante
                self.restaurante.agregar_comanda(mesa, comanda)  # Usamos self.restaurante
                QMessageBox.information(self, "Éxito", "Comanda agregada correctamente.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def agregar_plato(self):
        numero_mesa = self.entry_mesa.text()
        plato = self.entry_plato.text()
        if numero_mesa.isdigit() and plato:
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                comanda = mesa.comandas[-1]  # Obtenemos la última comanda agregada a la mesa
                comanda.agregar_plato(plato)
                QMessageBox.information(self, "Éxito", f"Plato '{plato}' agregado a la comanda.")
                self.entry_plato.clear()
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido y el nombre del plato.")

    def agregar_bebestible(self):
        numero_mesa = self.entry_mesa.text()
        bebestible = self.entry_bebestible.text()
        if numero_mesa.isdigit() and bebestible:
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                comanda = mesa.comandas[-1]  # Obtenemos la última comanda agregada a la mesa
                comanda.agregar_bebestible(bebestible)
                QMessageBox.information(self, "Éxito", f"Bebestible '{bebestible}' agregado a la comanda.")
                self.entry_bebestible.clear()
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido y el nombre del bebestible.")

    def ocupar_mesa(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)  # Usamos self.restaurante
            if mesa:
                mesa.ocupar_mesa()
                QMessageBox.information(self, "Éxito", f"Mesa {numero_mesa} ocupada.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def liberar_mesa(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                mesa.liberar_mesa()
                QMessageBox.information(self, "Éxito", f"Mesa {numero_mesa} liberada.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def ver_comandas(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                comandas = ""
                for comanda in mesa.comandas:
                    detalles_comanda = f"Comanda {comanda.numero_comanda}: {comanda.estado}\n"
                    detalles_comanda += "Platos: " + ", ".join(comanda.platos) + "\n"
                    detalles_comanda += "Bebestibles: " + ", ".join(comanda.bebestibles)
                    comandas += detalles_comanda + "\n"
                if comandas:
                    QMessageBox.information(self, "Comandas", f"Comandas asociadas a la mesa {numero_mesa}:\n{comandas}")
                else:
                    QMessageBox.information(self, "Comandas", f"No hay comandas asociadas a la mesa {numero_mesa}.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")
    
    def cambiar_estado(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                comandas_mesa = mesa.comandas
                if comandas_mesa:
                    comanda_ids = [str(comanda.numero_comanda) for comanda in comandas_mesa]  # Convertir a cadena
                    comanda_id, ok = QInputDialog.getItem(
                        self,
                        "Cambiar Estado de Comanda",
                        "Seleccione la comanda para cambiar su estado:",
                        comanda_ids,
                        editable=False
                    )
                    if ok and comanda_id:
                        comanda_id = int(comanda_id)
                        comanda_a_cambiar = next((comanda for comanda in comandas_mesa if comanda.numero_comanda == comanda_id), None)
                        if comanda_a_cambiar:
                            nuevo_estado, ok = QInputDialog.getItem(
                                self,
                                "Nuevo Estado de Comanda",
                                "Seleccione el nuevo estado para la comanda:",
                                ["en espera", "preparando", "cocinando", "terminado"],
                                editable=False
                            )
                            if ok and nuevo_estado:
                                comanda_a_cambiar.cambiar_estado(nuevo_estado)
                                QMessageBox.information(self, "Éxito", f"Comanda {comanda_id} cambió al estado: {nuevo_estado}.")
                        else:
                            QMessageBox.critical(self, "Error", f"No existe la comanda {comanda_id}.")
                else:
                    QMessageBox.critical(self, "Error", "No hay comandas asociadas a la mesa.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def eliminar_comanda(self):
        numero_mesa = self.entry_mesa.text()
        if numero_mesa.isdigit():
            numero_mesa = int(numero_mesa)
            mesa = self.restaurante.obtener_mesa_por_numero(numero_mesa)
            if mesa:
                comandas_mesa = mesa.comandas
                if comandas_mesa:
                    comanda_ids = [str(comanda.numero_comanda) for comanda in comandas_mesa]  # Convertir a cadena
                    comanda_id, ok = QInputDialog.getItem(
                        self,
                        "Eliminar Comanda",
                        "Seleccione la comanda a eliminar:",
                        comanda_ids,
                        editable=False
                    )
                    if ok and comanda_id:
                        comanda_id = int(comanda_id)
                        comanda_a_eliminar = next((comanda for comanda in comandas_mesa if comanda.numero_comanda == comanda_id), None)
                        if comanda_a_eliminar:
                            if comanda_a_eliminar.estado == "en espera" or comanda_a_eliminar.estado == "terminado":
                                mesa.comandas.remove(comanda_a_eliminar)
                                self.restaurante.comandas.remove(comanda_a_eliminar)
                                QMessageBox.information(self, "Éxito", f"Comanda {comanda_id} eliminada.")
                            else:
                                QMessageBox.critical(self, "Error", "Solo se pueden eliminar comandas en espera o terminadas.")
                        else:
                            QMessageBox.critical(self, "Error", f"No existe la comanda {comanda_id}.")
                else:
                    QMessageBox.critical(self, "Error", "No hay comandas asociadas a la mesa.")
            else:
                QMessageBox.critical(self, "Error", f"No existe la mesa {numero_mesa}.")
        else:
            QMessageBox.critical(self, "Error", "Ingrese un número de mesa válido.")

    def guardar_mesas_csv(self):
        data = [mesa.__dict__ for mesa in self.mesas]
        df = pd.DataFrame(data)
        df.to_csv("mesas.csv", index=False)
    

    def cargar_mesas_csv(self):
        try:
            df = pd.read_csv("mesas.csv")
            for _, row in df.iterrows():
                mesa = Mesa(row["numero_mesa"], row["capacidad"])
                mesa.estado = row["estado"]
                mesa.tiempo_asignacion = row["tiempo_asignacion"]
                mesa.tiempo_liberacion = row["tiempo_liberacion"]
                self.mesas.append(mesa)
        except FileNotFoundError:
            pass


    
    
    def guardar_comandas_csv(self):
        data = [comanda.__dict__ for comanda in self.comandas]
        df = pd.DataFrame(data)
        df.to_csv("comandas.csv", index=False)
    

    def cargar_comandas_csv(self):
        try:
            df = pd.read_csv("comandas.csv", encoding="latin-1")
            for _, row in df.iterrows():
                mesa_asociada = self.obtener_mesa_por_numero(row["mesa_asociada"])
                if mesa_asociada:
                    comanda = Comanda(row["numero_comanda"], mesa_asociada)
                    comanda.estado = row["estado"]
                    comanda.platos = [plato.strip() for plato in row["platos"].split(",")]
                    comanda.bebestibles = [bebida.strip() for bebida in row["bebestibles"].split(",")]
                    comanda.tiempo_llegada = row["tiempo_llegada"]
                    comanda.tiempo_terminacion = row["tiempo_terminacion"]
                    self.comandas.append(comanda)
        except FileNotFoundError:
            pass



if __name__ == "__main__":
    restaurante = Restaurant()
    restaurante.agregar_mesa(1, 4)
    restaurante.agregar_mesa(2, 6)

    restaurante.asignar_chef("Juan", "Cocina caliente")
    restaurante.asignar_bartender("Pedro", "Bebidas")
    restaurante.asignar_runner("Ana")

    app = QApplication(sys.argv)
    window = RestaurantApp(restaurante)
    window.show()
    sys.exit(app.exec())