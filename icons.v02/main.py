import os
from PIL import Image, ImageDraw
from math import pi, sin, cos

class IconGenerator:
    """
    Gerador de ícones vetoriais com coordenadas normalizadas (0..1).
    Canvas virtual sempre 1x1 para o ícone puro; para variantes com fundo,
    o ícone é desenhado centralizado num quadrado de lado = altura do canvas.
    """

    def __init__(self, base_dir="util_icons"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

        # ============== PARÂMETROS GLOBAIS DE ESTILO ==============
        self.style = {
            "stroke_width": 0.04,      # espessura do traço (fração do lado)
            "margin": 0.10,            # margem ao redor do ícone dentro do fundo
            "corner_radius": 0.15,     # raio do arredondamento (fração do lado)
            "bg_fill": (255, 255, 255),# fundo branco
            "bg_outline": (0, 0, 0),   # borda preta
            "outline_width": 0.01,     # espessura da borda do fundo
        }

        # ============== REGISTRO DOS ÍCONES ==============
        # Cada função recebe (draw, canvas_size, color, **kwargs)
        self.icons = {
            "blank": self._draw_blank,
            "pause": self._draw_pause,
            "play": self._draw_play,
            "stop": self._draw_stop,
            "check": self._draw_check,
            "close": self._draw_close,
            "email": self._draw_email,
            "magnifying-glass": self._draw_magnifier,
            "notification": self._draw_notification,
            "chat": self._draw_chat,
            "home": self._draw_home,
            "settings": self._draw_settings,
            "floppy-disk": self._draw_floppy,
            "user": self._draw_user,
            "camera": self._draw_camera,
            "trash": self._draw_trash,
            "download": self._draw_download,
            "upload": self._draw_upload,
            "calendar": self._draw_calendar,
            "clock": self._draw_clock,
        }

    # ------------------------------------------------------------------
    #                       FUNDOS DAS VARIANTES
    # ------------------------------------------------------------------

    def _draw_square_background(self, draw, size):
        """
        Desenha fundo quadrado com bordas arredondadas.
        size: altura/largura do canvas (int)
        """
        margin = size * self.style["margin"]
        rect = [margin, margin, size - margin, size - margin]
        radius = size * self.style["corner_radius"]
        outline_w = max(1, int(size * self.style["outline_width"]))
        draw.rounded_rectangle(rect, radius=radius,
                               fill=self.style["bg_fill"],
                               outline=self.style["bg_outline"],
                               width=outline_w)

    def _draw_rectangle_background(self, draw, canvas_size):
        """
        Desenha fundo retangular 3:1 com bordas arredondadas.
        canvas_size: (largura, altura) – largura = 3 * altura.
        """
        w, h = canvas_size
        margin_x = w * self.style["margin"]
        margin_y = h * self.style["margin"]
        rect = [margin_x, margin_y, w - margin_x, h - margin_y]
        radius = h * self.style["corner_radius"]  # raio proporcional à altura
        outline_w = max(1, int(h * self.style["outline_width"]))
        draw.rounded_rectangle(rect, radius=radius,
                               fill=self.style["bg_fill"],
                               outline=self.style["bg_outline"],
                               width=outline_w)

    # ------------------------------------------------------------------
    #                       DESENHO DOS ÍCONES
    #      (coordenadas normalizadas: 0..1, (0,0) canto superior esquerdo)
    # ------------------------------------------------------------------

    @staticmethod
    def _draw_blank(draw, canvas_size, color, **kwargs):
        """Ícone vazio – não desenha nada."""
        pass

    @staticmethod
    def _draw_pause(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(kwargs.get("stroke_width", 0.12 * w)))
        # duas barras verticais
        bar_w = 0.12 * w
        bar_h = 0.6 * h
        bar_y = (h - bar_h) / 2
        x1 = w * 0.35
        x2 = w * 0.65
        draw.rectangle([x1 - bar_w/2, bar_y, x1 + bar_w/2, bar_y + bar_h], fill=color)
        draw.rectangle([x2 - bar_w/2, bar_y, x2 + bar_w/2, bar_y + bar_h], fill=color)

    @staticmethod
    def _draw_play(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        # triângulo para a direita
        points = [
            (w * 0.3, h * 0.2),
            (w * 0.3, h * 0.8),
            (w * 0.8, h * 0.5)
        ]
        draw.polygon(points, fill=color)

    @staticmethod
    def _draw_stop(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        margin = w * 0.2
        draw.rectangle([margin, margin, w - margin, h - margin],
                       outline=color, width=max(1, int(0.06 * w)))

    @staticmethod
    def _draw_check(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.06 * w))
        points = [(w * 0.2, h * 0.5), (w * 0.45, h * 0.75), (w * 0.8, h * 0.25)]
        draw.line(points, fill=color, width=stroke, joint="curve")

    @staticmethod
    def _draw_close(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.06 * w))
        margin = w * 0.2
        draw.line([(margin, margin), (w - margin, h - margin)], fill=color, width=stroke)
        draw.line([(w - margin, margin), (margin, h - margin)], fill=color, width=stroke)

    @staticmethod
    def _draw_email(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.04 * w))
        # envelope
        x0, y0 = w * 0.2, h * 0.3
        x1, y1 = w * 0.8, h * 0.7
        draw.rectangle([x0, y0, x1, y1], outline=color, width=stroke)
        # aba
        draw.line([(x0, y0), (w*0.5, h*0.55), (x1, y0)], fill=color, width=stroke)

    @staticmethod
    def _draw_magnifier(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.06 * w))
        # lente
        cx, cy = w * 0.35, h * 0.35
        r = w * 0.18
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=stroke)
        # cabo
        draw.line([(w*0.55, h*0.55), (w*0.8, h*0.8)], fill=color, width=stroke)

    @staticmethod
    def _draw_notification(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # sino
        draw.ellipse([w*0.3, h*0.15, w*0.7, h*0.55], outline=color, width=stroke)
        # base
        draw.rectangle([w*0.4, h*0.55, w*0.6, h*0.75], outline=color, width=stroke)
        # alça
        draw.arc([w*0.4, h*0.05, w*0.6, h*0.25], start=0, end=180, fill=color, width=stroke)

    @staticmethod
    def _draw_chat(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # balão
        x0, y0 = w*0.2, h*0.2
        x1, y1 = w*0.8, h*0.65
        draw.rectangle([x0, y0, x1, y1], outline=color, width=stroke)
        # rabinho
        draw.polygon([(w*0.7, h*0.65), (w*0.8, h*0.8), (w*0.8, h*0.65)], fill=color)

    @staticmethod
    def _draw_home(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # telhado
        roof = [(w*0.1, h*0.5), (w*0.5, h*0.1), (w*0.9, h*0.5)]
        draw.polygon(roof, outline=color, width=stroke)
        # corpo
        draw.rectangle([w*0.3, h*0.5, w*0.7, h*0.9], outline=color, width=stroke)
        # porta
        draw.rectangle([w*0.45, h*0.65, w*0.55, h*0.9], outline=color, width=stroke)

    @staticmethod
    def _draw_settings(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        cx, cy = w*0.5, h*0.5
        r_int = w*0.2
        r_ext = w*0.3
        # círculo interno
        draw.ellipse([cx - r_int, cy - r_int, cx + r_int, cy + r_int],
                     outline=color, width=stroke)
        # dentes
        for i in range(8):
            ang = i * 45 * pi / 180
            x1 = cx + r_int * 1.2 * cos(ang)
            y1 = cy + r_int * 1.2 * sin(ang)
            x2 = cx + r_ext * cos(ang)
            y2 = cy + r_ext * sin(ang)
            draw.line([(x1, y1), (x2, y2)], fill=color, width=stroke)

    @staticmethod
    def _draw_floppy(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # corpo
        draw.rectangle([w*0.15, h*0.15, w*0.85, h*0.85],
                       outline=color, width=stroke)
        # disco
        cx, cy = w*0.5, h*0.6
        r = w*0.12
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=color, width=stroke)
        # ranhura
        draw.rectangle([w*0.3, h*0.25, w*0.7, h*0.4],
                       outline=color, width=stroke)

    @staticmethod
    def _draw_user(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # cabeça
        cx, cy = w*0.5, h*0.35
        r = w*0.15
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=color, width=stroke)
        # corpo
        draw.ellipse([w*0.3, h*0.45, w*0.7, h*0.85],
                     outline=color, width=stroke)

    @staticmethod
    def _draw_camera(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # corpo
        draw.rectangle([w*0.1, h*0.3, w*0.9, h*0.7],
                       outline=color, width=stroke)
        # lente
        cx, cy = w*0.5, h*0.5
        r = w*0.15
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=color, width=stroke)
        # flash
        draw.ellipse([w*0.7, h*0.2, w*0.8, h*0.3],
                     outline=color, width=stroke)

    @staticmethod
    def _draw_trash(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        # tampa
        draw.rectangle([w*0.2, h*0.15, w*0.8, h*0.25],
                       outline=color, width=stroke)
        # corpo
        draw.rectangle([w*0.25, h*0.25, w*0.75, h*0.8],
                       outline=color, width=stroke)
        # linhas
        draw.line([(w*0.4, h*0.4), (w*0.4, h*0.65)], fill=color, width=stroke)
        draw.line([(w*0.5, h*0.4), (w*0.5, h*0.65)], fill=color, width=stroke)
        draw.line([(w*0.6, h*0.4), (w*0.6, h*0.65)], fill=color, width=stroke)

    @staticmethod
    def _draw_download(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.06 * w))
        # seta para baixo
        draw.line([(w*0.5, h*0.2), (w*0.5, h*0.7)], fill=color, width=stroke)
        draw.polygon([(w*0.3, h*0.6), (w*0.5, h*0.8), (w*0.7, h*0.6)], fill=color)
        # base
        draw.rectangle([w*0.2, h*0.8, w*0.8, h*0.9], fill=color)

    @staticmethod
    def _draw_upload(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.06 * w))
        # seta para cima
        draw.line([(w*0.5, h*0.8), (w*0.5, h*0.3)], fill=color, width=stroke)
        draw.polygon([(w*0.3, h*0.4), (w*0.5, h*0.2), (w*0.7, h*0.4)], fill=color)
        # base
        draw.rectangle([w*0.2, h*0.8, w*0.8, h*0.9], fill=color)

    @staticmethod
    def _draw_calendar(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.04 * w))
        # corpo
        draw.rectangle([w*0.15, h*0.25, w*0.85, h*0.85],
                       outline=color, width=stroke)
        # argolas
        draw.ellipse([w*0.3, h*0.1, w*0.4, h*0.25], outline=color, width=stroke)
        draw.ellipse([w*0.6, h*0.1, w*0.7, h*0.25], outline=color, width=stroke)
        # linhas
        draw.line([(w*0.15, h*0.45), (w*0.85, h*0.45)], fill=color, width=stroke)
        for i in range(5):
            x = w * (0.2 + i * 0.15)
            draw.line([(x, h*0.55), (x, h*0.75)], fill=color, width=max(1, stroke//2))

    @staticmethod
    def _draw_clock(draw, canvas_size, color, **kwargs):
        w, h = canvas_size
        stroke = max(1, int(0.05 * w))
        cx, cy = w*0.5, h*0.5
        r = w*0.3
        draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                     outline=color, width=stroke)
        # ponteiros
        draw.line([(cx, cy), (cx, cy - r*0.6)], fill=color, width=stroke)
        draw.line([(cx, cy), (cx + r*0.5, cy)], fill=color, width=stroke)

    # ------------------------------------------------------------------
    #                       GERAÇÃO DOS ÍCONES
    # ------------------------------------------------------------------

    def _create_icon_canvas(self, icon_name, canvas_size, color, **kwargs):
        """Cria uma imagem RGBA com o ícone puro (sem fundo)."""
        img = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        icon_func = self.icons[icon_name]
        icon_func(draw, canvas_size, color, **kwargs)
        return img

    def generate_icon_variant(self, icon_name, variant, size, color=(0,0,0), **kwargs):
        """
        Gera uma variante do ícone.
        variant: 'icon', 'square' ou 'rectangle'
        size: altura base (para rectangle, largura = 3*size)
        """
        if icon_name not in self.icons:
            raise ValueError(f"Ícone '{icon_name}' não registrado.")

        color = color + (255,) if len(color) == 3 else color

        # --- Define canvas e fundo ---
        if variant == "icon":
            canvas_size = (size, size)
            img = Image.new("RGBA", canvas_size, (0,0,0,0))
            draw = ImageDraw.Draw(img)
            # desenha o ícone diretamente
            self.icons[icon_name](draw, canvas_size, color, **kwargs)

        elif variant == "square":
            canvas_size = (size, size)
            img = Image.new("RGBA", canvas_size, (0,0,0,0))
            draw = ImageDraw.Draw(img)
            self._draw_square_background(draw, size)
            # área útil: quadrado central com margem reduzida
            inner_size = size * (1 - 2 * self.style["margin"])
            offset = size * self.style["margin"]
            # cria um canvas virtual para o ícone (tamanho inner_size)
            icon_canvas = (inner_size, inner_size)
            icon_img = Image.new("RGBA", (int(inner_size), int(inner_size)), (0,0,0,0))
            icon_draw = ImageDraw.Draw(icon_img)
            self.icons[icon_name](icon_draw, icon_canvas, color, **kwargs)
            # cola no centro do fundo
            img.paste(icon_img, (int(offset), int(offset)), icon_img)

        elif variant == "rectangle":
            canvas_size = (size * 3, size)
            img = Image.new("RGBA", canvas_size, (0,0,0,0))
            draw = ImageDraw.Draw(img)
            self._draw_rectangle_background(draw, canvas_size)
            # área útil: quadrado central de lado = altura * (1 - 2*margin)
            inner_side = size * (1 - 2 * self.style["margin"])
            offset_x = (canvas_size[0] - inner_side) / 2
            offset_y = size * self.style["margin"]
            icon_canvas = (inner_side, inner_side)
            icon_img = Image.new("RGBA", (int(inner_side), int(inner_side)), (0,0,0,0))
            icon_draw = ImageDraw.Draw(icon_img)
            self.icons[icon_name](icon_draw, icon_canvas, color, **kwargs)
            img.paste(icon_img, (int(offset_x), int(offset_y)), icon_img)

        else:
            raise ValueError(f"Variante desconhecida: {variant}")

        return img

    def save_icon(self, icon_name, variant, size, output_subdir=".", color=(0,0,0), **kwargs):
        """Gera e salva o ícone."""
        img = self.generate_icon_variant(icon_name, variant, size, color, **kwargs)
        out_dir = os.path.join(self.base_dir, output_subdir)
        os.makedirs(out_dir, exist_ok=True)
        filename = f"{icon_name}-{variant}.png"
        path = os.path.join(out_dir, filename)
        img.save(path)
        print(f"✅ {filename} ({size}px) salvo")
        return path

    def generate_all_variants(self, icon_name, size, output_subdir, color=(0,0,0)):
        """Gera as três variantes de um ícone."""
        for variant in ["icon", "square", "rectangle"]:
            self.save_icon(icon_name, variant, size, output_subdir, color)

    def generate_full_set(self, size=512, output_subdir="producao"):
        """Gera todos os ícones cadastrados."""
        print(f"🚀 Gerando conjunto completo ({size}px) em '{output_subdir}'...")
        for icon_name in self.icons.keys():
            self.generate_all_variants(icon_name, size, output_subdir)

    def generate_production_set(self, size=512):
        self.generate_full_set(size, "producao")

    def generate_debug_set(self, size=64):
        self.generate_full_set(size, "debug")


# ------------------------------------------------------------------
#                            EXEMPLO DE USO
# ------------------------------------------------------------------
def main():
    generator = IconGenerator()

    # Gera todos os ícones em alta e baixa resolução
    generator.generate_production_set(size=512)
    generator.generate_debug_set(size=64)

    # Gera um ícone avulso com cor personalizada
    generator.generate_all_variants("pause", size=128,
                                   output_subdir="custom_red",
                                   color=(200, 0, 0))

    print("\n✨ Todos os ícones gerados com sucesso!")
    print("📁 Estrutura de arquivos:")
    print("   ├── producao/ (512px)")
    print("   ├── debug/    (64px)")
    print("   └── custom_red/")

if __name__ == "__main__":
    main()