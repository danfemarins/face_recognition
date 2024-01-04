import cv2
import face_recognition

# Carregando uma imagem de referência (pode ser sua própria imagem)
reference_image = face_recognition.load_image_file("assets/eu.jpeg")
reference_encoding = face_recognition.face_encodings(reference_image)[0]

# Inicializando a captura de vídeo
video_capture = cv2.VideoCapture(0)

while True:
    # Capturando um quadro de vídeo
    ret, frame = video_capture.read()

    # Encontrando todas as faces no quadro
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Comparando com a imagem de referência
        matches = face_recognition.compare_faces([reference_encoding], face_encoding)

        name = "Desconhecido"
        if matches[0]:
            name = "Pessoa Conhecida"

        # Desenhando o retângulo e o nome na imagem
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

    # Exibindo o resultado
    cv2.imshow('Video', frame)

    # Sair do loop se a tecla 'q' for pressionada
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberando os recursos
video_capture.release()
cv2.destroyAllWindows()
