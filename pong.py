import pygame
import random

# Inicializar pygame
pygame.init()

# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Pong")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)

# FPS
FPS = 60

# Dimensiones de los objetos
ANCHO_RAQUETA, ALTO_RAQUETA = 10, 100
RADIO_PELOTA = 7

# Fuentes
FUENTE = pygame.font.SysFont("comicsans", 50)

# Velocidad de la pelota inicial
VEL_PELOTA = 7

# Clases
class Raqueta:
    COLOR = BLANCO

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
        pygame.draw.rect(ventana, self.COLOR, self.rect)

    def reset(self):
        self.rect.y = ALTO // 2 - ALTO_RAQUETA // 2

class Pelota:
    COLOR = BLANCO

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
        pygame.draw.ellipse(ventana, self.COLOR, self.rect)

    def reset(self):
        self.rect.center = (ANCHO // 2, ALTO // 2)
        self.vel_x *= random.choice([-1, 1])
        self.vel_y = random.choice([-VEL_PELOTA, VEL_PELOTA])

# Funciones
def dibujar(ventana, raqueta1, raqueta2, pelota, puntuacion1, puntuacion2):
    ventana.fill(NEGRO)
    texto_puntuacion1 = FUENTE.render(f"{puntuacion1}", 1, BLANCO)
    texto_puntuacion2 = FUENTE.render(f"{puntuacion2}", 1, BLANCO)
    ventana.blit(texto_puntuacion1, (ANCHO // 4 - texto_puntuacion1.get_width() // 2, 20))
    ventana.blit(texto_puntuacion2, (ANCHO * 3 // 4 - texto_puntuacion2.get_width() // 2, 20))

    raqueta1.dibujar(ventana)
    raqueta2.dibujar(ventana)
    pelota.dibujar(ventana)

    pygame.display.update()

# Lógica principal
def main():
    reloj = pygame.time.Clock()

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

        if pelota.rect.colliderect(raqueta1.rect) or pelota.rect.colliderect(raqueta2.rect):
            pelota.vel_x *= -1

        if pelota.rect.left <= 0:
            puntuacion2 += 1
            pelota.reset()

        if pelota.rect.right >= ANCHO:
            puntuacion1 += 1
            pelota.reset()

        dibujar(VENTANA, raqueta1, raqueta2, pelota, puntuacion1, puntuacion2)

    pygame.quit()

if __name__ == "__main__":
    main()