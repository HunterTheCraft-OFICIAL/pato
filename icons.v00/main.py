import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

class IconGenerator:
    """
    Gerador procedural de ícones com múltiplos estilos e características.
    """
    def __init__(self, base_dir="icons"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

        # ============== Definição dos estilos de ícone ==============
        self.styles = {
            # Planeta inspirado no SVG
            "planet": {
                "shape": self._draw_planet_shape,
                "base_color": (70, 130, 200),      # azul médio
                "features": [self._add_craters, self._add_highlight_dot],
                "noise_variance": 12,
            },
            # Estrela dourada
            "star": {
                "shape": self._draw_star_shape,
                "base_color": (255, 215, 0),       # ouro
                "features": [self._add_sparkles],
                "noise_variance": 8,
            },
            # Montanha com neve
            "mountain": {
                "shape": self._draw_mountain_shape,
                "base_color": (100, 120, 100),     # verde musgo
                "features": [self._add_snow_cap],
                "noise_variance": 15,
            },
            # Árvore simples
            "tree": {
                "shape": self._draw_tree_shape,
                "base_color": (34, 139, 34),       # verde floresta
                "features": [self._add_fruits],
                "noise_variance": 10,
            },
            # Diamante / losango
            "diamond": {
                "shape": self._draw_diamond_shape,
                "base_color": (200, 180, 255),     # lavanda
                "features": [self._add_facet_highlight],
                "noise_variance": 5,
            }
        }

    # ------------------------------------------------------------------
    #                       MÉTODOS DE DESENHO (FORMAS)
    # ------------------------------------------------------------------

    def _draw_planet_shape(self, draw, size, color, noise_variance):
        """Desenha o formato do planeta (SVG adaptado) com ruído."""
        # Coordenadas normalizadas para base 16x16 (escala de 0 a 16)
        # Polígono externo (casca)
        outer = [
            (5.5,0), (5,0.5), (4.5,1), (3.5,1), (3,1.5), (2.5,2), (2,2.5), (1.5,3),
            (1,3.5), (1,4.5), (0.5,5), (0,5.5), (0,6.5), (0,7.5), (0,8.5), (0,9.5),
            (0,10.5), (0.5,11), (1,11.5), (1,12.5), (1.5,13), (2,13.5), (2.5,14),
            (3,14.5), (3.5,15), (4.5,15), (5,15.5), (5.5,16), (6.5,16), (7.5,16),
            (8.5,16), (9.5,16), (10.5,16), (11,15.5), (11.5,15), (12.5,15),
            (13,14.5), (13.5,14), (14,13.5), (14.5,13), (15,12.5), (15,11.5),
            (15.5,11), (16,10.5), (16,9.5), (16,8.5), (16,7.5), (16,6.5),
            (16,5.5), (15.5,5), (15,4.5), (15,3.5), (14.5,3), (14,2.5),
            (13.5,2), (13,1.5), (12.5,1), (11.5,1), (11,0.5), (10.5,0),
            (9.5,0), (8.5,0), (7.5,0), (6.5,0), (5.5,0)
        ]
        # Polígono interno ("continente")
        inner = [
            (6.5,1), (7,1.5), (7.5,2), (8.5,2), (9,2.5), (9,3.5), (9.5,4),
            (10,4.5), (10.5,5), (11,5.5), (11.5,6), (12.5,6), (13.5,6),
            (14.5,6), (15,6.5), (15,7.5), (15,8.5), (15,9.5), (14.5,10),
            (14,10.5), (14,11.5), (13.5,12), (13,12.5), (12.5,13), (12,13.5),
            (11.5,14), (10.5,14), (10,14.5), (9.5,15), (8.5,15), (8,14.5),
            (7.5,14), (7,13.5), (7,12.5), (7.5,12), (8,11.5), (8.5,11),
            (9,10.5), (9,9.5), (9,8.5), (8.5,8), (8,7.5), (7.5,7), (6.5,7),
            (5.5,7), (4.5,7), (4,7.5), (3.5,8), (3,8.5), (2.5,9), (2,9.5),
            (1.5,10), (1,9.5), (1,8.5), (1,7.5), (1,6.5), (1.5,6), (2,5.5),
            (2,4.5), (2.5,4), (3,3.5), (3.5,3), (4,2.5), (4.5,2), (5.5,2),
            (6,1.5), (6.5,1)
        ]

        scale = size / 16.0
        # Escala e desenha o polígono externo
        scaled_outer = [(int(x*scale), int(y*scale)) for x,y in outer]
        draw.polygon(scaled_outer, fill=color)
        # Escala e desenha o polígono interno (cor um pouco mais escura)
        scaled_inner = [(int(x*scale), int(y*scale)) for x,y in inner]
        darker = tuple(max(0, c-30) for c in color[:3])
        draw.polygon(scaled_inner, fill=darker + (255,))

    def _draw_star_shape(self, draw, size, color, noise_variance):
        """Desenha uma estrela de 5 pontas."""
        cx, cy = size//2, size//2
        points = []
        for i in range(10):
            angle = i * 36 - 90  # 36° entre pontas, começa no topo
            radius = size//2 if i%2==0 else size//4
            x = cx + radius * np.cos(np.radians(angle))
            y = cy + radius * np.sin(np.radians(angle))
            points.append((x, y))
        draw.polygon(points, fill=color)

    def _draw_mountain_shape(self, draw, size, color, noise_variance):
        """Desenha uma montanha (triângulo com base irregular)."""
        w, h = size, size
        points = [
            (0, h),                     # base esquerda
            (w//4, h//3),              # primeira elevação
            (w//2, h//2),             # vale
            (3*w//4, h//4),           # segunda elevação
            (w, h)                    # base direita
        ]
        draw.polygon(points, fill=color)

    def _draw_tree_shape(self, draw, size, color, noise_variance):
        """Desenha uma árvore: tronco marrom + copa verde."""
        w, h = size, size
        # Tronco
        trunk_w = max(2, w//6)
        trunk_x = w//2 - trunk_w//2
        draw.rectangle([trunk_x, 3*h//4, trunk_x+trunk_w, h], fill=(101, 67, 33))
        # Copa (triângulos sobrepostos)
        crown_color = color
        draw.polygon([(w//2, h//8), (w//4, 3*h//4), (3*w//4, 3*h//4)], fill=crown_color)
        draw.polygon([(w//2, h//6), (w//3, 2*h//3), (2*w//3, 2*h//3)], fill=crown_color)

    def _draw_diamond_shape(self, draw, size, color, noise_variance):
        """Desenha um losango."""
        w, h = size, size
        points = [(w//2, 0), (w, h//2), (w//2, h), (0, h//2)]
        draw.polygon(points, fill=color)

    # ------------------------------------------------------------------
    #                    CARACTERÍSTICAS (FEATURES)
    # ------------------------------------------------------------------

    @staticmethod
    def _add_craters(draw, size):
        """Adiciona pequenas crateras ao ícone (planeta)."""
        scale = size / 16.0
        for _ in range(int(6 * scale)):
            x = random.randint(int(2*scale), size-int(2*scale))
            y = random.randint(int(2*scale), size-int(2*scale))
            r = random.randint(int(2*scale), int(4*scale))
            draw.ellipse([x-r, y-r, x+r, y+r], fill=(0,0,0,40), outline=(0,0,0,80))

    @staticmethod
    def _add_highlight_dot(draw, size):
        """Ponto de brilho (como no SVG)."""
        scale = size / 16.0
        # coordenadas normalizadas do SVG
        x, y = 11.5, 9
        w = 2
        draw.ellipse([x*scale, y*scale, (x+w)*scale, (y+w)*scale], fill=(255,255,255,200))

    @staticmethod
    def _add_sparkles(draw, size):
        """Brilhos ao redor da estrela."""
        scale = size / 16.0
        for _ in range(int(10 * scale)):
            x = random.randint(0, size)
            y = random.randint(0, size)
            draw.point((x, y), fill=(255,255,200,150))

    @staticmethod
    def _add_snow_cap(draw, size):
        """Neve no topo da montanha."""
        w = size
        snow_color = (255,255,255,220)
        draw.polygon([(w//4, size//3), (w//2, size//4), (3*w//4, size//3)], fill=snow_color)

    @staticmethod
    def _add_fruits(draw, size):
        """Frutos na árvore."""
        scale = size / 16.0
        for _ in range(int(4 * scale)):
            x = random.randint(size//3, 2*size//3)
            y = random.randint(size//4, size//2)
            r = max(1, int(1.5*scale))
            draw.ellipse([x-r, y-r, x+r, y+r], fill=(255,0,0,200))

    @staticmethod
    def _add_facet_highlight(draw, size):
        """Brilho nas facetas do diamante."""
        w = size
        draw.polygon([(w//2, w//6), (5*w//6, w//2), (w//2, w//2)], fill=(255,255,255,80))

    # ------------------------------------------------------------------
    #              MÉTODOS DE GERAÇÃO DE TEXTURA E COMPOSIÇÃO
    # ------------------------------------------------------------------

    def _generate_base_texture(self, shape_func, color, noise_variance, size):
        """
        Gera a textura base: aplica a forma e adiciona ruído.
        """
        # Cria uma imagem RGBA transparente
        img = Image.new("RGBA", (size, size), (0,0,0,0))
        draw = ImageDraw.Draw(img)

        # Desenha a forma principal
        shape_func(draw, size, color, noise_variance)

        # Adiciona ruído gaussiano (variação de cor)
        noise = np.random.normal(0, noise_variance, (size, size, 3))
        img_array = np.array(img)
        if img_array.shape[2] == 4:
            rgb = img_array[:,:,:3].astype(np.int16)
            alpha = img_array[:,:,3]
            rgb_noisy = np.clip(rgb + noise, 0, 255).astype(np.uint8)
            img_array = np.dstack((rgb_noisy, alpha))
        else:
            img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

        return Image.fromarray(img_array, "RGBA")

    def generate_icon(self, style_name, size, output_subdir="."):
        """
        Gera um ícone com o estilo e tamanho especificados.
        """
        if style_name not in self.styles:
            print(f"⚠️  Estilo '{style_name}' não encontrado!")
            return

        style = self.styles[style_name]
        color = style["base_color"]
        # Se a cor for uma função, executa; senão usa a tupla
        if callable(color):
            color = color()
        # Garante que a cor tenha canal alpha (255 opaco)
        if len(color) == 3:
            color = color + (255,)

        # 1. Gera textura base
        base = self._generate_base_texture(
            shape_func=style["shape"],
            color=color,
            noise_variance=style.get("noise_variance", 10),
            size=size
        )

        # 2. Cria overlay para as características
        overlay = Image.new("RGBA", (size, size), (0,0,0,0))
        draw_overlay = ImageDraw.Draw(overlay)
        for feature in style["features"]:
            feature(draw_overlay, size)

        # 3. Combina as camadas
        final = Image.alpha_composite(base, overlay).convert("RGB")
        final = final.filter(ImageFilter.SHARPEN)

        # 4. Salva
        output_dir = os.path.join(self.base_dir, output_subdir)
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"{style_name}.png")
        final.save(path)
        print(f"✅ {style_name} ({size}px) salvo em: {path}")
        return final

    def generate_production_icons(self, size=512):
        """Gera ícones em alta resolução."""
        print(f"🚀 Gerando ícones de produção ({size}px)...")
        for style in self.styles.keys():
            self.generate_icon(style, size, "producao")

    def generate_debug_icons(self, size=64):
        """Gera ícones em baixa resolução para testes."""
        print(f"🧪 Gerando ícones de debug ({size}px)...")
        for style in self.styles.keys():
            self.generate_icon(style, size, "debug")


# ------------------------------------------------------------------
#                            EXEMPLO DE USO
# ------------------------------------------------------------------
def main():
    generator = IconGenerator()

    # Gera todos os estilos em dois tamanhos
    generator.generate_production_icons(size=512)
    generator.generate_debug_icons(size=64)

    # Gera um ícone avulso com cor personalizada (sobrescrevendo)
    generator.styles["planet"]["base_color"] = (180, 100, 80)  # vermelho
    generator.generate_icon("planet", 128, "variacoes")

    print("\n✨ Todos os ícones gerados com sucesso!")
    print("📁 Estrutura de arquivos criada:")
    print("   ├── producao/")
    print("   ├── debug/")
    print("   └── variacoes/")
    print("\n📋 Estilos disponíveis:")
    for style in generator.styles.keys():
        print(f"   • {style.title()}")

if __name__ == "__main__":
    main()