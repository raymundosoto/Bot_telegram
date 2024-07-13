import telebot

bot = telebot.TeleBot("API_Token", parse_mode=None)  # Reemplaza con tu clave de API

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Qué haces?")

# Handler para el comando /numero
@bot.message_handler(commands=['numero'])
def send_multiplication_table(message):
    try:
        # Extrae el número del mensaje
        num_str = message.text.split()[1]
        num = int(num_str)

        # Genera la tabla de multiplicar
        table = "\n".join([f"{num} x {i} = {num * i}" for i in range(1, 11)])

        # Envía la tabla de multiplicar al usuario
        bot.reply_to(message, f"Tabla de multiplicar del {num}:\n{table}")
    except (IndexError, ValueError):
        bot.reply_to(message, "Por favor, proporciona un número válido después del comando /numero. Ejemplo: /numero 5")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def handle_text_doc(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    text = downloaded_file.decode('utf-8')  # Decodificar el contenido del archivo a texto
    bot.reply_to(message, text)

# Maneja todas las imágenes enviadas
@bot.message_handler(content_types=['photo'])
def handle_images(message):
    handle_photo(message)

def handle_photo(message):
    file_id = message.photo[-1].file_id  # Obtiene la mejor calidad de imagen (última en la lista)
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    # Puedes responder al usuario o realizar alguna operación con la imagen aquí
    bot.reply_to(message, "Has enviado una imagen.")

# Maneja todos los documentos PDF enviados
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    if message.document.mime_type == 'application/pdf':
        handle_pdf(message)
    else:
        bot.reply_to(message, "Por favor, envía un documento PDF.")

def handle_pdf(message):
    try:
        bot.reply_to(message, "Recibí un documento PDF. Procesando...")
        print("Recibí un documento PDF. Procesando...")  # Mensaje de depuración

        file_info = bot.get_file(message.document.file_id)
        print(f"File info: {file_info}")  # Mensaje de depuración

        downloaded_file = bot.download_file(file_info.file_path)
        print("Archivo PDF descargado")  # Mensaje de depuración
        
        # Responder al usuario con un mensaje de confirmación
        bot.reply_to(message, "Has enviado un documento PDF.")
        
        # Opcionalmente, guarda el archivo PDF localmente
        with open(f"{message.document.file_name}", 'wb') as new_file:
            new_file.write(downloaded_file)
        
        print("Archivo PDF guardado localmente")  # Mensaje de depuración
        bot.reply_to(message, "El documento PDF se ha guardado correctamente.")
    except Exception as e:
        print(f"Hubo un error: {e}")  # Mensaje de depuración
        bot.reply_to(message, f"Hubo un error al procesar el documento PDF: {e}")

# Ejemplo de comando que envía una imagen al usuario
@bot.message_handler(commands=['sendimage'])
def send_image(message):
    chat_id = message.chat.id
    print(chat_id)
    with open(r'ruta/archivo.extension', 'rb') as photo:
        bot.send_photo(chat_id, photo, caption="Aquí tienes una imagen")

bot.infinity_polling()
