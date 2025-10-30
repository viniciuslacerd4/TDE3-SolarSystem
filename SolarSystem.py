import pygame
import math
import sys
import random

pygame.init()

# Janela
LARGURA, ALTURA = 1000, 800
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Animação do Sistema Solar")

# Cores
PRETO = (0, 0, 0)
AMARELO = (255, 215, 0)
AZUL = (0, 100, 255)
VERMELHO = (220, 20, 60)
LARANJA = (255, 140, 0)
VERDE = (50, 205, 50)
CINZA = (169, 169, 169)
BRANCO = (255, 255, 255)

# Centro e relógio
CENTRO_X, CENTRO_Y = LARGURA // 2, ALTURA // 2
RELOGIO = pygame.time.Clock()

# CENÁRIO: estrelas, meteoros, cometas e "ETs"
STAR_COUNT = 120
SHOOTING_STAR_CHANCE_PER_SEC = 0.02
COMET_CHANCE_PER_SEC = 0.01
ET_CHANCE_PER_SEC = 0.008

def gerar_estrelas(n):
    stars = []
    for _ in range(n):
        x = random.randint(0, LARGURA)
        y = random.randint(0, ALTURA)
        r = random.choice([1, 1, 2])
        b = random.randint(120, 255)
        stars.append((x, y, r, b))
    return stars

def spawn_shooting_star():
    # começa em uma borda superior/lat e atravessa a tela
    side = random.choice(['top', 'left', 'right'])
    if side == 'top':
        x = random.uniform(0, LARGURA)
        y = -5
        vx = random.uniform(-300, 300)
        vy = random.uniform(200, 500)
    elif side == 'left':
        x = -5
        y = random.uniform(0, ALTURA/2)
        vx = random.uniform(200, 500)
        vy = random.uniform(-50, 150)
    else:
        x = LARGURA + 5
        y = random.uniform(0, ALTURA/2)
        vx = random.uniform(-500, -200)
        vy = random.uniform(-50, 150)
    life = random.uniform(0.6, 1.6)
    return {'x': x, 'y': y, 'vx': vx, 'vy': vy, 'life': life, 'age': 0.0}

def spawn_comet():
    # cometa cruza do topo esquerdo para baixo direito com cauda
    x = random.uniform(-100, -20)
    y = random.uniform(0, ALTURA/3)
    vx = random.uniform(80, 180)
    vy = random.uniform(10, 60)
    return {'x': x, 'y': y, 'vx': vx, 'vy': vy, 'trail': []}

def spawn_et():
    # pequena "nave" que aparece perto das órbitas fazendo curva
    angle = random.uniform(0, 2*math.pi)
    dist = random.uniform(80, 380)
    cx = CENTRO_X + dist * math.cos(angle)
    cy = CENTRO_Y + dist * math.sin(angle)
    vx = random.uniform(-80, 80)
    vy = random.uniform(-60, 60)
    return {'x': cx, 'y': cy, 'vx': vx, 'vy': vy, 't': 0.0}

# Planetas (valores visuais e períodos reais)
MERCURIO_GAME_PERIOD = 5.0
MERCURIO_REAL_DAYS = 88.0

# Lista de planetas com períodos reais aproximados (dias)
PLANETAS = [
    {"nome": "Mercúrio", "raio_orbita": 70,  "raio_planeta": 5,  "periodo_real": 88.0,   "rotacao_real_days": 58.6,  "cor": LARANJA},
    # Observação: Vênus tem rotação retrógrada (gira em sentido oposto) -> usamos valor negativo
    {"nome": "Vênus",    "raio_orbita": 100, "raio_planeta": 7,  "periodo_real": 225.0,  "rotacao_real_days": -243.0, "cor": VERDE},
    {"nome": "Terra",    "raio_orbita": 140, "raio_planeta": 9,  "periodo_real": 365.0,  "rotacao_real_days": 1.0,   "cor": AZUL},
    {"nome": "Marte",    "raio_orbita": 180, "raio_planeta": 7,  "periodo_real": 687.0,  "rotacao_real_days": 1.03,  "cor": VERMELHO},
    {"nome": "Júpiter",  "raio_orbita": 240, "raio_planeta": 20, "periodo_real": 4333.0, "rotacao_real_days": 0.41,  "cor": (200,150,100)},
    {"nome": "Saturno",  "raio_orbita": 290, "raio_planeta": 17, "periodo_real": 10759.0,"rotacao_real_days": 0.45,  "cor": (210,180,140)},
    {"nome": "Urano",    "raio_orbita": 340, "raio_planeta": 12, "periodo_real": 30687.0,"rotacao_real_days": 0.72,  "cor": (150,220,220)},
    {"nome": "Netuno",   "raio_orbita": 390, "raio_planeta": 12, "periodo_real": 60190.0,"rotacao_real_days": 0.67,  "cor": (100,120,255)},
]

# Velocidades orbitais e rotações
for p in PLANETAS:
    game_period = (p["periodo_real"] / MERCURIO_REAL_DAYS) * MERCURIO_GAME_PERIOD
    p["vel_orbital"] = 2 * math.pi / game_period

EARTH_GAME_DAY = 2.0
MIN_ROT_VEL = 0.01
MAX_ROT_VEL = 20.0
for p in PLANETAS:
    rot_days_raw = p.get("rotacao_real_days", 1.0)
    sign = -1.0 if rot_days_raw < 0 else 1.0
    rot_days = max(0.01, abs(rot_days_raw))
    periodo_rotacao_jogo = rot_days * EARTH_GAME_DAY
    vel = sign * (2 * math.pi) / periodo_rotacao_jogo
    vel_mag = max(MIN_ROT_VEL, min(abs(vel), MAX_ROT_VEL))
    p["vel_rotacao"] = math.copysign(vel_mag, vel)

# Lua (órbita em torno da Terra)
LUA = {
    "distancia_terra": 25,
    "raio": 3,
    "velocidade": 0.1,
    "cor": CINZA
}

# Função para desenhar planeta com rotação própria (textura simples com mancha)
def desenhar_planeta_com_rotacao(superficie, cor, raio, centro, angulo_rotacao):
    pygame.draw.circle(superficie, (0, 0, 0), centro, raio + 1)
    pygame.draw.circle(superficie, cor, centro, raio)
    ux = math.cos(angulo_rotacao)
    uy = math.sin(angulo_rotacao)
    chevron_dist = raio * 1.15
    ponta_x = centro[0] + chevron_dist * ux
    ponta_y = centro[1] + chevron_dist * uy
    chevron_len = max(3, int(raio * 0.45))
    chevron_w = max(2, int(raio * 0.3))
    base_center_x = ponta_x - chevron_len * ux
    base_center_y = ponta_y - chevron_len * uy
    perp_x = -uy
    perp_y = ux
    left_x = base_center_x + chevron_w * perp_x
    left_y = base_center_y + chevron_w * perp_y
    right_x = base_center_x - chevron_w * perp_x
    right_y = base_center_y - chevron_w * perp_y
    pygame.draw.polygon(
        superficie,
        (255, 255, 255),
        [
            (int(ponta_x), int(ponta_y)),
            (int(left_x), int(left_y)),
            (int(right_x), int(right_y)),
        ],
    )

# Loop principal
def main():
    tempo = 0
    rodando = True

    # inicializa cenário dinâmico
    stars = gerar_estrelas(STAR_COUNT)
    shooting_stars = []
    comets = []
    ets = []

    while rodando:
        dt = RELOGIO.tick(60)  # 60 FPS
        tempo += dt / 1000  # Tempo em segundos

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

        # Limpar tela
        TELA.fill(PRETO)

        # Desenhar estrelas de fundo (fixas)
        for sx, sy, sr, sb in stars:
            # brilho levemente piscante
            br = int(sb * (0.85 + 0.15 * math.sin(tempo * 0.5 + (sx+sy) % 7)))
            color = (br, br, br)
            pygame.draw.circle(TELA, color, (sx, sy), sr)

        # Spawn aleatório de shooting stars/cometas/ets com base em dt
        # chance baseada em tempo real (dt em segundos)
        if random.random() < SHOOTING_STAR_CHANCE_PER_SEC * (dt/1000.0):
            shooting_stars.append(spawn_shooting_star())
        if random.random() < COMET_CHANCE_PER_SEC * (dt/1000.0):
            comets.append(spawn_comet())
        if random.random() < ET_CHANCE_PER_SEC * (dt/1000.0):
            ets.append(spawn_et())

        # Atualizar e desenhar shooting stars
        for ss in shooting_stars[:]:
            ss['age'] += dt/1000.0
            ss['x'] += ss['vx'] * (dt/1000.0)
            ss['y'] += ss['vy'] * (dt/1000.0)
            alpha = max(0, 255 * (1 - ss['age']/ss['life']))
            start_pos = (int(ss['x']), int(ss['y']))
            tail_pos = (int(ss['x'] - ss['vx'] * 0.05), int(ss['y'] - ss['vy'] * 0.05))
            color = (255, 255, 200)
            pygame.draw.line(TELA, color, start_pos, tail_pos, 2)
            if ss['age'] >= ss['life'] or ss['x'] < -50 or ss['x'] > LARGURA+50 or ss['y'] > ALTURA+50:
                shooting_stars.remove(ss)

        # Atualizar e desenhar cometas (com rastro)
        for c in comets[:]:
            c['x'] += c['vx'] * (dt/1000.0)
            c['y'] += c['vy'] * (dt/1000.0)
            # registrar trail
            c['trail'].insert(0, (c['x'], c['y']))
            if len(c['trail']) > 20:
                c['trail'].pop()
            # desenhar rastro degradê
            for i, (tx, ty) in enumerate(c['trail']):
                alpha = int(255 * (1 - i/len(c['trail'])))
                w = max(1, 4 - i//5)
                pygame.draw.circle(TELA, (200,200,220), (int(tx), int(ty)), w)
            # desenhar núcleo do cometa
            pygame.draw.circle(TELA, (240,240,200), (int(c['x']), int(c['y'])), 4)
            if c['x'] > LARGURA + 100 or c['y'] > ALTURA + 100:
                comets.remove(c)

        # Atualizar e desenhar ETs (pequenas naves)
        for e in ets[:]:
            e['t'] += dt/1000.0
            # movimento suave
            e['x'] += e['vx'] * (dt/1000.0)
            e['y'] += e['vy'] * (dt/1000.0) + 10 * math.sin(e['t'] * 2)
            # desenhar "nave" simples
            ex, ey = int(e['x']), int(e['y'])
            pygame.draw.ellipse(TELA, (180,180,255), (ex-10, ey-5, 20, 8))
            pygame.draw.ellipse(TELA, (220,220,255), (ex-6, ey-7, 12, 6))
            # luz inferior
            pygame.draw.circle(TELA, (255,200,80), (ex, ey+6), 3)
            if e['x'] < -50 or e['x'] > LARGURA+50 or e['y'] < -50 or e['y'] > ALTURA+50:
                ets.remove(e)

        # --- Desenhar Sol (com escala e brilho) ---
        sol_raio_base = 30
        # Escala pulsante (efeito de brilho)
        escala_sol = 1 + 0.1 * math.sin(tempo * 3)
        sol_raio = int(sol_raio_base * escala_sol)
        pygame.draw.circle(TELA, AMARELO, (CENTRO_X, CENTRO_Y), sol_raio)
        # Núcleo mais claro
        pygame.draw.circle(TELA, (255, 255, 150), (CENTRO_X, CENTRO_Y), sol_raio_base)

        # --- Desenhar órbitas (linhas tracejadas) ---
        for planeta in PLANETAS:
            raio_orbita = planeta["raio_orbita"]
            pygame.draw.circle(TELA, (50, 50, 50), (CENTRO_X, CENTRO_Y), raio_orbita, 1)

        # --- Desenhar planetas com translação e rotação ---
        for p in PLANETAS:
            nome = p["nome"]
            raio_orbita = p["raio_orbita"]
            raio_planeta = p["raio_planeta"]
            vel_orbital = p["vel_orbital"]
            vel_rotacao = p.get("vel_rotacao", 0.1)
            cor = p["cor"]

            # Ângulo orbital (translação ao redor do Sol)
            angulo_orbital = tempo * vel_orbital

            # Posição do planeta (translação)
            planeta_x = CENTRO_X + raio_orbita * math.cos(angulo_orbital)
            planeta_y = CENTRO_Y + raio_orbita * math.sin(angulo_orbital)
            centro_planeta = (int(planeta_x), int(planeta_y))

            # Ângulo de rotação própria (usamos vel_rotacao em rad/s)
            angulo_rotacao = tempo * vel_rotacao

            # Desenhar planeta com rotação
            desenhar_planeta_com_rotacao(TELA, cor, raio_planeta, centro_planeta, angulo_rotacao)

            # --- Desenhar Lua (apenas para a Terra) ---
            if nome == "Terra":
                # Posição relativa da Lua em torno da Terra
                angulo_lua = tempo * LUA["velocidade"]
                lua_x = planeta_x + LUA["distancia_terra"] * math.cos(angulo_lua)
                lua_y = planeta_y + LUA["distancia_terra"] * math.sin(angulo_lua)
                lua_centro = (int(lua_x), int(lua_y))

                # Órbita da Lua
                pygame.draw.circle(TELA, (40, 40, 40), centro_planeta, LUA["distancia_terra"], 1)
                # Lua
                pygame.draw.circle(TELA, LUA["cor"], lua_centro, LUA["raio"])

            # Nome do planeta
            fonte = pygame.font.SysFont("Arial", 14)
            texto = fonte.render(nome, True, BRANCO)
            TELA.blit(texto, (planeta_x - 15, planeta_y + raio_planeta + 5))

        # Atualizar tela
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()