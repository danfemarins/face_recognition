# Reconhecimento Facial com Cadastro e Detecção de Rostos

Este é um projeto que utiliza reconhecimento facial para cadastrar pessoas e detectar rostos em tempo real usando a webcam. Ele permite o cadastro de pessoas, a detecção de rostos e o reconhecimento facial comparando os rostos detectados com as pessoas cadastradas.

## Funcionalidades

1. **Login de Usuário:**
   - Permite que o usuário faça login utilizando um nome de usuário e senha.

2. **Cadastro de Pessoas:**
   - Permite o cadastro de novas pessoas, capturando fotos de seus rostos em tempo real.

3. **Detecção de Rostos:**
   - Utiliza a webcam para detectar rostos em tempo real e exibir retângulos ao redor dos rostos detectados.

4. **Reconhecimento Facial:**
   - Realiza o reconhecimento facial comparando os rostos detectados com as pessoas cadastradas, exibindo o nome da pessoa se for reconhecida.

## Requisitos

- Python 3
- Bibliotecas Python:
  - OpenCV (cv2)
  - NumPy
  - tkinter
  - Pillow (PIL)

## Como Usar

1. **Configuração do Ambiente:**
   - Certifique-se de ter Python 3 e as bibliotecas Python listadas acima instaladas no seu ambiente.

2. **Execução do Código:**
   - Execute o arquivo Python `main.py` para iniciar o aplicativo.
   - Será exibida uma janela de login onde você pode entrar com um usuário e senha.
   - Após o login bem-sucedido, você será redirecionado para a página principal do aplicativo, onde poderá iniciar a câmera para detecção de rostos.

3. **Cadastro de Pessoas:**
   - Na página principal do aplicativo, selecione a opção "Cadastro" no menu superior.
   - Digite o nome da pessoa a ser cadastrada e clique no botão "Tirar Foto" para capturar fotos do rosto da pessoa.
   - Após tirar 5 fotos, o cadastro será finalizado automaticamente.

4. **Detecção de Rostos:**
   - Na página principal do aplicativo, selecione a opção "Iniciar" no menu superior para iniciar a detecção de rostos.
   - A webcam será ativada e você verá retângulos ao redor dos rostos detectados em tempo real.

## Observações

- Este é um projeto de exemplo e pode ser estendido ou personalizado conforme necessário.
- Certifique-se de ter uma webcam funcional para usar as funcionalidades de detecção de rostos em tempo real.

Para qualquer dúvida ou problema, sinta-se à vontade para entrar em contato.

