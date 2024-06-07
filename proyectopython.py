import serial
import pygame
import os

class ControladorDeServos:
    def init(self, puerto='COM3', tasa_baudios=9600):
        pygame.init()
        self.pantalla = pygame.display.set_mode((800, 400))
        pygame.display.set_caption("Control de Servos del Brazo Robótico")
        
        self.BLANCO = (255, 255, 255)
        self.NEGRO = (0, 0, 0)
        self.ROJO = (255, 0, 0)
        self.GRIS = (200, 200, 200)

        self.arduino = None
        try:
            self.arduino = serial.Serial(port=puerto, baudrate=tasa_baudios, timeout=.1)
        except Exception as e:
            print(f"Error al abrir el puerto serie: {e}")
            exit()

        self.angulos = {'base': 90, 'hombro': 90, 'codo': 90}
        self.desplazamientos = {'base': 0, 'hombro': 0, 'codo': 0}
        self.cargar_angulos()

    def cargar_angulos(self):
        if os.path.exists("angulos_guardados.txt"):
            with open("angulos_guardados.txt", "r") as archivo:
                contenido = archivo.read().strip()
                if contenido:
                    try:
                        self.angulos = eval(contenido)
                    except:
                        self.angulos = {'base': 90, 'hombro': 90, 'codo': 90}

    def enviar_comando(self):
        comando = f"{self.angulos['base']},{self.angulos['hombro']},{self.angulos['codo']}\n"
        try:
            self.arduino.write(comando.encode('utf-8'))
        except Exception as e:
            print(f"Error al enviar comando: {e}")

    def dibujar_controles(self):
        self.pantalla.fill(self.GRIS)

        # Dibujar las bases de los joysticks
        pygame.draw.rect(self.pantalla, self.NEGRO, (100, 90, 200, 20))
        pygame.draw.rect(self.pantalla, self.NEGRO, (100, 190, 200, 20))
        pygame.draw.rect(self.pantalla, self.NEGRO, (100, 290, 200, 20))

        # Limitar los desplazamientos dentro de los límites de las barras
        self.desplazamientos['base'] = max(-100, min(100, self.desplazamientos['base']))
        self.desplazamientos['hombro'] = max(-100, min(100, self.desplazamientos['hombro']))
        self.desplazamientos['codo'] = max(-100, min(100, self.desplazamientos['codo']))

        # Dibujar los sticks y puntos rojos
        pygame.draw.circle(self.pantalla, self.NEGRO, (200 + self.desplazamientos['base'], 100), 15)
        pygame.draw.circle(self.pantalla, self.ROJO, (200 + self.desplazamientos['base'], 100), 10)
        pygame.draw.circle(self.pantalla, self.NEGRO, (200 + self.desplazamientos['hombro'], 200), 15)
        pygame.draw.circle(self.pantalla, self.ROJO, (200 + self.desplazamientos['hombro'], 200), 10)
        pygame.draw.circle(self.pantalla, self.NEGRO, (200 + self.desplazamientos['codo'], 300), 15)
        pygame.draw.circle(self.pantalla, self.ROJO, (200 + self.desplazamientos['codo'], 300), 10)

        # Dibujar etiquetas
        fuente = pygame.font.Font(None, 36)
        etiqueta_base = fuente.render("Base", True, self.NEGRO)
        etiqueta_hombro = fuente.render("Hombro", True, self.NEGRO)
        etiqueta_codo = fuente.render("Codo", True, self.NEGRO)
        self.pantalla.blit(etiqueta_base, (10, 90))
        self.pantalla.blit(etiqueta_hombro, (10, 190))
        self.pantalla.blit(etiqueta_codo, (10, 290))

    def main(self):
        ejecutando = True
        arrastrando = {'base': False, 'hombro': False, 'codo': False}

        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        if pygame.Rect(200 + self.desplazamientos['base'] - 15, 85, 30, 30).collidepoint(evento.pos):
                            arrastrando['base'] = True
                        elif pygame.Rect(200 + self.desplazamientos['hombro'] - 15, 185, 30, 30).collidepoint(evento.pos):
                            arrastrando['hombro'] = True
                        elif pygame.Rect(200 + self.desplazamientos['codo'] - 15, 285, 30, 30).collidepoint(evento.pos):
                            arrastrando['codo'] = True
                elif evento.type == pygame.MOUSEBUTTONUP:
                    if evento.button == 1:
                        arrastrando = {'base': False, 'hombro': False, 'codo': False}

            for parte in arrastrando:
                if arrastrando[parte]:
                    mouse_x, _ = pygame.mouse.get_pos()
                    # Calcular el nuevo desplazamiento asegurándose de que esté dentro de los límites
                    nuevo_desplazamiento = mouse_x - 200
                    nuevo_desplazamiento = max(-100, min(100, nuevo_desplazamiento))
                    self.desplazamientos[parte] = nuevo_desplazamiento
                    self.angulos[parte] = int((nuevo_desplazamiento + 100) / 200 * 180)

            self.dibujar_controles()
            self.enviar_comando()

            pygame.display.flip()

        self.guardar_angulos()
        pygame.quit()
        if self.arduino:
            self.arduino.close()

    def guardar_angulos(self):
        with open("angulos_guardados.txt", "w") as archivo:
            archivo.write(str(self.angulos))

if name == "main":
    controlador = ControladorDeServos()
    controlador.main()
