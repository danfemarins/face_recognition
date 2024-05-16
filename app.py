import cv2
import numpy as np
import time
import os
import threading
import tkinter as tk
from tkinter import messagebox, Menu, filedialog
from PIL import Image, ImageTk

# Carregar o classificador pré-treinado para detecção de rostos
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Diretório para armazenar as imagens de pessoas cadastradas
registered_faces_dir = 'static/uploads'  # Alterado para o diretório onde as fotos das pessoas cadastradas são armazenadas
# Diretório para armazenar as fotos dos rostos detectados
fotos_dir = 'fotos'

# Verificar se os diretórios existem, caso contrário, crie-os
if not os.path.exists(registered_faces_dir):
    os.makedirs(registered_faces_dir)

if not os.path.exists(fotos_dir):
    os.makedirs(fotos_dir)

# Lista para armazenar os nomes das pessoas cadastradas
registered_people = []

# Carregar os nomes das pessoas cadastradas
def load_registered_people():
    global registered_people
    registered_people = [filename.split('.')[0] for filename in os.listdir(registered_faces_dir)]

# Inicializar a lista de pessoas cadastradas
load_registered_people()

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        
        self.username_label = tk.Label(root, text="Usuário:")
        self.username_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.username_entry = tk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.password_label = tk.Label(root, text="Senha:")
        self.password_label.grid(row=1, column=0, padx=10, pady=5)
        
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)
        
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # Adicione a lógica de validação do usuário e senha aqui
        if username == "admin" and password == "admin":
            self.root.destroy()
            root = tk.Tk()
            app = FaceDetectionApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos")

class CadastroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro")
        self.nome = None
        self.fotos_tiradas = 0
        self.fotos = []

        self.camera = cv2.VideoCapture(0)
        self.camera_thread = threading.Thread(target=self.mostrar_camera, daemon=True)
        self.camera_thread.start()

        self.camera_label = tk.Label(root)
        self.camera_label.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

        self.nome_label = tk.Label(root, text="Nome:")
        self.nome_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.nome_entry = tk.Entry(root)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=5)
        
        self.tirar_foto_button = tk.Button(root, text="Tirar Foto", command=self.tirar_foto)
        self.tirar_foto_button.grid(row=1, column=0, columnspan=2, padx=10, pady=5)
        
        self.cadastrar_button = tk.Button(root, text="Finalizar Cadastro", command=self.finalizar_cadastro, state=tk.DISABLED)
        self.cadastrar_button.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def mostrar_camera(self):
        while True:
            ret, frame = self.camera.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)

                self.camera_label.config(image=img)
                self.camera_label.image = img
            time.sleep(0.03)

    def tirar_foto(self):
        if self.nome is None:
            self.nome = self.nome_entry.get()
            self.nome_entry.config(state=tk.DISABLED)

        ret, frame = self.camera.read()
        if ret:
            filename = f"{self.nome}_{self.fotos_tiradas + 1}.jpg"
            cv2.imwrite(os.path.join(fotos_dir, filename), frame)
            self.fotos.append(filename)
            
            self.fotos_tiradas += 1
            if self.fotos_tiradas == 5:
                self.cadastrar_button.config(state=tk.NORMAL)

    def finalizar_cadastro(self):
        # Adicione a lógica para salvar o nome e as fotos no diretório de cadastrados
        messagebox.showinfo("Cadastro", "Cadastro finalizado com sucesso")
        self.camera.release()
        self.root.destroy()

class FaceDetectionApp:
    def __init__(self, root, video_source=0):
        self.root = root
        self.root.title("Face Detection")
        
        # Menu Superior
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        menubar.add_command(label="Iniciar", command=self.start_camera)
        menubar.add_command(label="Cadastro", command=self.open_cadastro)
        menubar.add_command(label="Banco de Dados")
        menubar.add_command(label="Fotos")
        menubar.add_command(label="Sobre")
        menubar.add_command(label="Sair", command=self.root.quit)  # Modificado para fechar o aplicativo

        self.video_source = video_source
        self.cap = None

        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()

    def start_camera(self):
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(self.video_source)
            self.delay = 10
            self.update()
        
    def update(self):
        if self.cap is not None and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = self.detect_faces(frame)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.root.after(self.delay, self.update)

    def detect_faces(self, frame):
        # Converter o frame para escala de cinza para melhor detecção de rostos
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detectar rostos no frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Desenhar retângulos ao redor dos rostos detectados e realizar reconhecimento facial
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Realizar reconhecimento facial
            name = self.recognize_face(frame[y:y+h, x:x+w])
            cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

        return frame

    def recognize_face(self, face_img):
        # Procurar correspondência do rosto enviado com as imagens das pessoas cadastradas
        for filename in os.listdir(registered_faces_dir):
            registered_face = cv2.imread(os.path.join(registered_faces_dir, filename))
            
            # Comparar as características faciais
            if registered_face is not None:
                registered_face_gray = cv2.cvtColor(registered_face, cv2.COLOR_BGR2GRAY)
                if cv2.equalizeHist(face_img).shape == cv2.equalizeHist(registered_face_gray).shape:
                    res = cv2.matchTemplate(cv2.equalizeHist(registered_face_gray), cv2.equalizeHist(face_img), cv2.TM_CCOEFF_NORMED)
                    threshold = 0.8
                    loc = np.where(res >= threshold)
                    if loc[0].shape[0] > 0:
                        return filename.split('_')[0]  # Retorna o nome da pessoa
        return "Desconhecido"

    def open_cadastro(self):
        cadastro_window = tk.Toplevel(self.root)
        app = CadastroApp(cadastro_window)

if __name__ == '__main__':
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
