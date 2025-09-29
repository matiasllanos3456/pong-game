import pygame
import random

# Inicializar pygame
pygame.init()
try:
    pygame.mixer.init()
    AUDIO_DISPONIBLE = True
except:
    AUDIO_DISPONIBLE = False

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 150, 255)
VERDE = (0, 255, 150)
GRIS = (128, 128, 128)
AMARILLO = (255, 255, 0)
ROJO = (255, 0, 0)

# FPS
FPS = 60

# Dimensiones de los objetos
ANCHO_RAQUETA, ALTO_RAQUETA = 10, 100
RADIO_PELOTA = 7

# Fuentes
FUENTE = pygame.font.SysFont("comicsans", 50)
FUENTE_MENU = pygame.font.SysFont("arial", 36)
FUENTE_TITULO = pygame.font.SysFont("arial", 72, bold=True)

# Velocidad de la pelota inicial
VEL_PELOTA = 7

# Configuración del juego
PUNTUACION_MAXIMA = 5

# Estados del juego
MENU = 0
JUGANDO = 1
VICTORIA = 2

# Función para crear sonidos simples
def crear_sonido_hit():
    """Crea un sonido de golpe usando pygame"""
    if not AUDIO_DISPONIBLE:
        return None
    try:
        # Crear un sonido de golpe simple
        sound = pygame.mixer.Sound(buffer=b'\x00' * 1000)
        return sound
    except:
        return None

def crear_sonido_punto():
    """Crea un sonido de punto usando pygame"""
    if not AUDIO_DISPONIBLE:
        return None
    try:
        # Crear un sonido de punto simple
        sound = pygame.mixer.Sound(buffer=b'\x00' * 2000)
        return sound
    except:
        return None

# Inicializar sonidos
SONIDO_HIT = crear_sonido_hit()
SONIDO_PUNTO = crear_sonido_punto()

# Clases
class Raqueta:
    COLOR = AZUL

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 5
        self.rect = pygame.Rect(self.x, self.y, ANCHO_RAQUETA, ALTO_RAQUETA)

    def mover(self, arriba=True):
        if arriba:
            self.y -= self.velocidad
        else:
            self.y += self.velocidad
        self.rect.y = self.y

    def dibujar(self, ventana):
        # Dibujar raqueta con borde más moderno
        pygame.draw.rect(ventana, self.COLOR, self.rect)
        pygame.draw.rect(ventana, BLANCO, self.rect, 2)

    def reset(self):
        self.rect.y = ALTO // 2 - ALTO_RAQUETA // 2

class Pelota:
    COLOR = VERDE

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel_x = random.choice([-VEL_PELOTA, VEL_PELOTA])
        self.vel_y = random.choice([-VEL_PELOTA, VEL_PELOTA])
        self.rect = pygame.Rect(self.x, self.y, RADIO_PELOTA * 2, RADIO_PELOTA * 2)

    def mover(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.x = self.x
        self.rect.y = self.y

    def dibujar(self, ventana):
        # Dibujar pelota con efecto brillante
        pygame.draw.ellipse(ventana, self.COLOR, self.rect)
        pygame.draw.ellipse(ventana, BLANCO, self.rect, 2)

    def reset(self):
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.vel_x *= random.choice([-1, 1])
        self.vel_y = random.choice([-VEL_PELOTA, VEL_PELOTA])

# Funciones
def dibujar_linea_central(ventana):
    """Dibuja una línea punteada en el centro de la pantalla"""
    centro_x = ANCHO // 2
    for y in range(0, ALTO, 20):
        pygame.draw.rect(ventana, GRIS, (centro_x - 2, y, 4, 10))

def dibujar_menu(ventana):
    """Dibuja el menú inicial"""
    ventana.fill(NEGRO)
    
    # Título
    titulo = FUENTE_TITULO.render("PONG", 1, AZUL)
    ventana.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 150))
    
    # Opciones del menú
    texto_jugar = FUENTE_MENU.render("Presiona ESPACIO para jugar", 1, BLANCO)
    texto_salir = FUENTE_MENU.render("Presiona ESC para salir", 1, BLANCO)
    
    ventana.blit(texto_jugar, (ANCHO // 2 - texto_jugar.get_width() // 2, 300))
    ventana.blit(texto_salir, (ANCHO // 2 - texto_salir.get_width() // 2, 350))
    
    # Controles
    controles = FUENTE.render("Jugador 1: W/S  |  Jugador 2: ↑/↓", 1, GRIS)
    ventana.blit(controles, (ANCHO // 2 - controles.get_width() // 2, 450))
    
    pygame.display.update()

def dibujar_victoria(ventana, ganador):
    """Dibuja la pantalla de victoria"""
    ventana.fill(NEGRO)
    
    # Mensaje de victoria
    if ganador == 1:
        color_ganador = AZUL
        texto_ganador = "¡JUGADOR 1 GANA!"
    else:
        color_ganador = VERDE
        texto_ganador = "¡JUGADOR 2 GANA!"
    
    titulo_victoria = FUENTE_TITULO.render(texto_ganador, 1, color_ganador)
    ventana.blit(titulo_victoria, (ANCHO // 2 - titulo_victoria.get_width() // 2, 200))
    
    # Opciones
    texto_reiniciar = FUENTE_MENU.render("Presiona R para jugar de nuevo", 1, BLANCO)
    texto_menu = FUENTE_MENU.render("Presiona M para volver al menú", 1, BLANCO)
    
    ventana.blit(texto_reiniciar, (ANCHO // 2 - texto_reiniciar.get_width() // 2, 350))
    ventana.blit(texto_menu, (ANCHO // 2 - texto_menu.get_width() // 2, 400))
    
    pygame.display.update()

def dibujar(ventana, raqueta1, raqueta2, pelota, puntuacion1, puntuacion2):
    ventana.fill(NEGRO)
    
    # Dibujar línea central
    dibujar_linea_central(ventana)
    
    # Marcador mejorado
    texto_puntuacion1 = FUENTE.render(f"{puntuacion1}", 1, AZUL)
    texto_puntuacion2 = FUENTE.render(f"{puntuacion2}", 1, VERDE)
    ventana.blit(texto_puntuacion1, (ANCHO // 4 - texto_puntuacion1.get_width() // 2, 20))
    ventana.blit(texto_puntuacion2, (ANCHO * 3 // 4 - texto_puntuacion2.get_width() // 2, 20))

    raqueta1.dibujar(ventana)
    raqueta2.dibujar(ventana)
    pelota.dibujar(ventana)

    pygame.display.update()

# Lógica principal
def main():
    reloj = pygame.time.Clock()
    estado = MENU
    ganador = 0
    
    raqueta1 = Raqueta(10, ALTO // 2 - ALTO_RAQUETA // 2)
    raqueta2 = Raqueta(ANCHO - 10 - ANCHO_RAQUETA, ALTO // 2 - ALTO_RAQUETA // 2)
    pelota = Pelota(ANCHO // 2, ALTO // 2)
    
    puntuacion1, puntuacion2 = 0, 0

    corriendo = True
    while corriendo:
        reloj.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        teclas = pygame.key.get_pressed()

        if estado == MENU:
            dibujar_menu(VENTANA)
            
            if teclas[pygame.K_SPACE]:
                estado = JUGANDO
                # Reiniciar el juego
                puntuacion1, puntuacion2 = 0, 0
                raqueta1.reset()
                raqueta2.reset()
                pelota.reset()
            elif teclas[pygame.K_ESCAPE]:
                corriendo = False
                
        elif estado == JUGANDO:
            # Controles
            if teclas[pygame.K_w] and raqueta1.rect.top > 0:
                raqueta1.mover(arriba=True)
            if teclas[pygame.K_s] and raqueta1.rect.bottom < ALTO:
                raqueta1.mover(arriba=False)
            if teclas[pygame.K_UP] and raqueta2.rect.top > 0:
                raqueta2.mover(arriba=True)
            if teclas[pygame.K_DOWN] and raqueta2.rect.bottom < ALTO:
                raqueta2.mover(arriba=False)

            # Movimiento de la pelota
            pelota.mover()
            if pelota.rect.top <= 0 or pelota.rect.bottom >= ALTO:
                pelota.vel_y *= -1

            # Colisiones con las raquetas
            if pelota.rect.colliderect(raqueta1.rect) or pelota.rect.colliderect(raqueta2.rect):
                pelota.vel_x *= -1
                # Reproducir sonido de golpe
                if SONIDO_HIT:
                    try:
                        SONIDO_HIT.play()
                    except:
                        pass

            # Puntuación
            if pelota.rect.left <= 0:
                puntuacion2 += 1
                pelota.reset()
                # Reproducir sonido de punto
                if SONIDO_PUNTO:
                    try:
                        SONIDO_PUNTO.play()
                    except:
                        pass

            if pelota.rect.right >= ANCHO:
                puntuacion1 += 1
                pelota.reset()
                # Reproducir sonido de punto
                if SONIDO_PUNTO:
                    try:
                        SONIDO_PUNTO.play()
                    except:
                        pass

            # Verificar condición de victoria
            if puntuacion1 >= PUNTUACION_MAXIMA:
                ganador = 1
                estado = VICTORIA
            elif puntuacion2 >= PUNTUACION_MAXIMA:
                ganador = 2
                estado = VICTORIA

            dibujar(VENTANA, raqueta1, raqueta2, pelota, puntuacion1, puntuacion2)
            
        elif estado == VICTORIA:
            dibujar_victoria(VENTANA, ganador)
            
            if teclas[pygame.K_r]:
                estado = JUGANDO
                # Reiniciar el juego
                puntuacion1, puntuacion2 = 0, 0
                raqueta1.reset()
                raqueta2.reset()
                pelota.reset()
            elif teclas[pygame.K_m]:
                estado = MENU

    pygame.quit()

if __name__ == "__main__":
    main()