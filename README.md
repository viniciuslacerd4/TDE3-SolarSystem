## 🌌 SolarSystem - Animação do Sistema Solar

Bem-vindo ao projeto **SolarSystem** — uma animação em Pygame que simula o Sistema Solar de forma visual, com órbitas proporcionais, rotações (compressas para visual), estrelas de fundo, meteoros, cometas e até pequenas "naves ET" para dar vida ao cenário. Este README explica como executar o projeto, a lógica por trás de cada elemento e como ajustar parâmetros.

Índice
- Como rodar (rápido)
- Usando um venv (recomendado)
- Dependências
- Estrutura e lógica dos elementos
  - Planetas
  - Órbitas e velocidades orbitais
  - Rotação própria (chevron indicando rotação)
  - Lua
  - Estrelas de fundo
  - Meteoros (shooting stars)
  - Cometas
  - ETs (pequenas naves)
- Parâmetros principais e onde alterá-los
- Dicas e resolução de problemas
- Próximos passos / ideias

---

Como rodar (rápido)

    # (opcional) ativar venv se você já tiver um funcional
    # source .venv/bin/activate

    # instalar pygame (se necessário)
    python3 -m pip install --user pygame

    # executar o script
    python3 ./SolarSystem.py

Usando um venv (recomendado)

    # criar e ativar um venv
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install pygame
    python3 ./SolarSystem.py

Observação: em Debian/Ubuntu, se ao criar o venv ocorrer erro sobre `ensurepip` instale: sudo apt install python3-venv.

Dependências
- Python 3.8+ (o projeto foi editado/testado em 3.12)
- pygame

---

Lógica dos elementos (explicado)

Planetas 🪐
- Os planetas estão definidos em `SolarSystem.py` na lista `PLANETAS` como dicionários contendo campos:
  - `nome`: nome do planeta (string)
  - `raio_orbita`: raio visual da órbita (pixels)
  - `raio_planeta`: raio visual do planeta (pixels)
  - `periodo_real`: período orbital real em dias (usado para manter proporção orbital)
  - `rotacao_real_days`: período de rotação real em dias (usado para mapa das rotações próprias)
  - `cor`: cor RGB do planeta

Órbitas e velocidades orbitais ☄️
- Proporção orbital: o código define `MERCURIO_GAME_PERIOD = 5.0` segundos (no jogo) para a volta completa de Mercúrio. Os demais planetas têm seu período de jogo proporcional ao período real de Mercúrio:

    game_period = (periodo_real / MERCURIO_REAL_DAYS) * MERCURIO_GAME_PERIOD

    e a velocidade angular é calculada como `vel_orbital = 2*pi / game_period` (rad/s).

Rotação própria — chevron indicando rotação ↻
- Para dar vida, cada planeta tem uma rotação própria calculada a partir do período real (`rotacao_real_days`) mas compressa para o jogo:

    periodo_rotacao_jogo = rotacao_real_days * EARTH_GAME_DAY
    vel_rotacao = 2*pi / periodo_rotacao_jogo

- `EARTH_GAME_DAY` (em segundos) define quanto tempo a Terra demora para completar 1 dia no jogo. Por padrão está em `2.0` (ou seja, Terra completa uma rotação a cada 2 segundos). Os outros planetas seguem a proporção real em relação ao dia da Terra; assim preservamos as razões reais mas em uma escala reduzida.
- A indicação visual da rotação foi trocada por um chevron (pequeno triângulo branco) posicionado um pouco fora da borda do planeta e que gira conforme `angulo_rotacao`. Vênus usa rotacao negativa (retrógrada) então o chevron gira no sentido oposto.

Lua 🌕
- A Lua é desenhada apenas para a Terra e possui parâmetros simples em `LUA` (distância, raio, velocidade). A órbita é desenhada em torno da posição atual da Terra.

Estrelas de fundo ✨
- `STAR_COUNT` define quantas estrelas fixes existem no fundo. Cada estrela tem brilho levemente oscilante para dar dinamismo.

Meteoros (shooting stars) 💫
- Meteoros surgem aleatoriamente com probabilidade `SHOOTING_STAR_CHANCE_PER_SEC` por segundo, atravessam a tela com velocidade alta e possuem uma vida curta com um traço (tail).

Cometas ☄️
- Cometas surgem raramente (`COMET_CHANCE_PER_SEC`) e têm um trail (rastro) armazenado como uma lista de posições que é desenhada com degradê para efeito visual.

ETs (pequenas naves) 👽
- Pequenas entidades que aparecem aleatoriamente (`ET_CHANCE_PER_SEC`) e se movem suavemente pelo espaço — apenas para dar vida. São desenhadas como elipses com uma luz inferior.

Parâmetros principais e onde alterá-los
- `MERCURIO_GAME_PERIOD` — define quanto tempo Mercúrio demora a completar uma volta (segundos). Padrão: 5.0
- `EARTH_GAME_DAY` — define quantos segundos no jogo correspondem a 1 dia terrestre (afeta todas as rotações próprias). Padrão: 2.0
- `STAR_COUNT` — número de estrelas fixas no fundo.
- `SHOOTING_STAR_CHANCE_PER_SEC`, `COMET_CHANCE_PER_SEC`, `ET_CHANCE_PER_SEC` — controlam frequência de meteoros/cometas/ets.
- `PLANETAS` — ajustar `raio_orbita` e `raio_planeta` muda o visual. Ex.: aumentar `raio_planeta` de Marte deixa-o mais redondo.

Dicas rápidas de ajuste
- Se planetas muito pequenos parecerem irregulares, aumente `raio_planeta` em 1–3 pixels e/ou mantenha `borda` (o script já desenha um contorno preto uma vez).
- Para rotações mais realistas (e muito lentas), aumente `EARTH_GAME_DAY` (ex.: 5.0 ou 10.0) — isso estende todos os tempos de rotação proporcionalmente.
- Para ver rotações mais rápidas, reduza `EARTH_GAME_DAY`.

Resolução de problemas comuns
- Erro ao criar venv / `ensurepip is not available`: em Debian/Ubuntu, instale o pacote de sistema:

    sudo apt update
    sudo apt install python3-venv

- `pygame` não instalado: instale com `python3 -m pip install --user pygame` ou dentro do venv `pip install pygame`.
- Se o jogo não abrir (em servidores sem display), rode em uma máquina com GUI ou use um ambiente com suporte a display (X11).

Próximos passos / ideias
- Melhorar sprites de planetas (texturas) e adicionar iluminação dinâmica.
- Adicionar controles de velocidade do tempo (teclas + / -) ou UI para ajustar `EARTH_GAME_DAY` em runtime.
- Sons para meteoros/cometas/ets.

---

Se quiser, posso:
- ajustar o valor de `EARTH_GAME_DAY` (ex.: 3.0 ou 5.0) e mostrar os novos períodos calculados;
- aumentar a densidade de estrelas ou frequências de cometas/ets;
- criar um `.gitignore` com `.venv/` e outros arquivos gerados.

Divirta-se explorando o Sistema Solar! 🚀🌟👽
