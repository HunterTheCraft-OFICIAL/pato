from PIL import Image

# Definições: (nome, cor em RGB)
tiles = [
    ("plain", (144, 238, 144)),      # verde claro
    ("forest", (34, 139, 34)),        # verde escuro
    ("mountain", (128, 128, 128)),    # cinza
    ("water", (30, 144, 255)),        # azul
    ("ruins", (139, 69, 19))          # marrom
]

for name, color in tiles:
    img = Image.new("RGB", (64, 64), color)
    img.save(f"{name}.png")
    print(f"Criado: {name}.png")
