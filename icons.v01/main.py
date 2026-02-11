import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

class UtilityIconGenerator:
    """
    Gerador de ícones utilitários com três variações:
    - icon       : apenas o desenho, fundo transparente
    - rectangle  : ícone dentro de um retângulo arredondado (como botão)
    - square     : ícone dentro de um quadrado (pode ser arredondado)
    """
    def __init__(self, base_dir="util_icons"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

        # ============== DEFINIÇÃO DOS ÍCONES ==============
        # Cada ícone é uma função que desenha em coordenadas normalizadas (0-16)
        self.icons = {
            "blank":       self._draw_blank,
            "chat":        self._draw_chat,
            "check":       self._draw_check,
            "close":       self._draw_close,
            "email":       self._draw_email,
            "floppy-disk": self._draw_floppy,
            "home":        self._draw_home,
            "magnifying-glass": self._draw_magnifier,
            "notification": self._draw_notification,
            "pause":       self._draw_pause,
            "play":        self._draw_play,
            "settings":    self._draw_settings,
            "stop":        self._draw_stop,
        }

        # Cores padrão (podem ser alteradas por ícone individualmente)
        self.default_primary_color = (60, 60, 60)      # cinza escuro
        self.default_secondary_color = (100, 100, 100) # cinza médio
        self.default_accent_color = (0, 120, 212)      # azul

    # ------------------------------------------------------------------
    #                    FUNÇÕES DE DESENHO DOS ÍCONES
    #           (coordenadas normalizadas em grid 0-16)
    # ------------------------------------------------------------------

    @staticmethod
    def _draw_blank(draw, size, color, **kwargs):
        """Ícone vazio – não desenha nada."""
        pass

    @staticmethod
    def _draw_check(draw, size, color, **kwargs):
        """Ícone de visto (checkmark)."""
        scale = size / 16.0
        # Coordenadas normalizadas (aprox. 4,8 -> 12,12)
        points = [(4*scale, 8*scale), (7*scale, 11*scale), (12*scale, 4*scale)]
        draw.line(points, fill=color, width=max(1, int(1.5*scale)))

    @staticmethod
    def _draw_close(draw, size, color, **kwargs):
        """Ícone de fechar (X)."""
        scale = size / 16.0
        pad = 3 * scale
        draw.line([(pad, pad), (size-pad, size-pad)], fill=color, width=max(1, int(1.5*scale)))
        draw.line([(size-pad, pad), (pad, size-pad)], fill=color, width=max(1, int(1.5*scale)))

    @staticmethod
    def _draw_chat(draw, size, color, **kwargs):
        """Balão de conversa."""
        scale = size / 16.0
        # Retângulo principal
        x0, y0 = 3*scale, 3*scale
        x1, y1 = 13*scale, 11*scale
        draw.rectangle([x0, y0, x1, y1], outline=color, width=max(1, int(scale)))
        # Rabinho do balão
        tail = [(11*scale, 11*scale), (13*scale, 13*scale), (13*scale, 11*scale)]
        draw.polygon(tail, fill=color)

    @staticmethod
    def _draw_email(draw, size, color, **kwargs):
        """Envelope de email."""
        scale = size / 16.0
        # Corpo do envelope
        x0, y0 = 2*scale, 4*scale
        x1, y1 = 14*scale, 12*scale
        draw.rectangle([x0, y0, x1, y1], outline=color, width=max(1, int(scale)))
        # Aba triangular
        draw.line([(x0, y0), (size//2, 8*scale), (x1, y0)], fill=color, width=max(1, int(scale)))

    @staticmethod
    def _draw_floppy(draw, size, color, **kwargs):
        """Disquete."""
        scale = size / 16.0
        # Corpo
        x0, y0 = 2*scale, 2*scale
        x1, y1 = 14*scale, 14*scale
        draw.rectangle([x0, y0, x1, y1], outline=color, width=max(1, int(1.2*scale)))
        # Detalhe do disco
        cx, cy = 8*scale, 10*scale
        r = 2.5*scale
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=max(1, int(scale)))
        # Ranhura
        draw.rectangle([5*scale, 4*scale, 11*scale, 6*scale], outline=color, width=max(1, int(scale)))

    @staticmethod
    def _draw_home(draw, size, color, **kwargs):
        """Casa."""
        scale = size / 16.0
        # Telhado
        roof = [(1*scale, 8*scale), (8*scale, 1*scale), (15*scale, 8*scale)]
        draw.polygon(roof, outline=color, fill=None, width=max(1, int(1.2*scale)))
        # Corpo
        draw.rectangle([4*scale, 8*scale, 12*scale, 14*scale], outline=color, width=max(1, int(scale)))
        # Porta
        draw.rectangle([7*scale, 10*scale, 9*scale, 14*scale], outline=color, width=max(1, int(scale)))

    @staticmethod
    def _draw_magnifier(draw, size, color, **kwargs):
        """Lupa."""
        scale = size / 16.0
        # Círculo da lente
        cx, cy = 6*scale, 6*scale
        r = 4*scale
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], outline=color, width=max(1, int(1.5*scale)))
        # Cabo
        draw.line([(10*scale, 10*scale), (14*scale, 14*scale)], fill=color, width=max(1, int(1.5*scale)))

    @staticmethod
    def _draw_notification(draw, size, color, **kwargs):
        """Sino de notificação."""
        scale = size / 16.0
        # Corpo do sino
        draw.ellipse([5*scale, 3*scale, 11*scale, 9*scale], outline=color, width=max(1, int(scale)))
        # Base
        draw.rectangle([6*scale, 9*scale, 10*scale, 12*scale], outline=color, width=max(1, int(scale)))
        # Alça
        draw.arc([7*scale, 1*scale, 9*scale, 3*scale], start=0, end=180, fill=color, width=max(1, int(scale)))

    @staticmethod
    def _draw_pause(draw, size, color, **kwargs):
        """Pause (duas barras verticais)."""
        scale = size / 16.0
        w = 2 * scale
        draw.rectangle([4*scale, 4*scale, 4*scale+w, 12*scale], fill=color)
        draw.rectangle([10*scale, 4*scale, 10*scale+w, 12*scale], fill=color)

    @staticmethod
    def _draw_play(draw, size, color, **kwargs):
        """Play (triângulo para a direita)."""
        scale = size / 16.0
        points = [(5*scale, 4*scale), (5*scale, 12*scale), (12*scale, 8*scale)]
        draw.polygon(points, fill=color)

    @staticmethod
    def _draw_settings(draw, size, color, **kwargs):
        """Engrenagem (círculo com dentes)."""
        scale = size / 16.0
        cx, cy = 8*scale, 8*scale
        r_int = 4*scale
        r_ext = 5.5*scale
        # Círculo interno
        draw.ellipse([cx-r_int, cy-r_int, cx+r_int, cy+r_int], outline=color, width=max(1, int(scale)))
        # Dentes (8 pequenas linhas)
        for i in range(8):
            angle = i * 45
            x1 = cx + r_ext * np.cos(np.radians(angle))
            y1 = cy + r_ext * np.sin(np.radians(angle))
            x2 = cx + (r_ext+1.5*scale) * np.cos(np.radians(angle))
            y2 = cy + (r_ext+1.5*scale) * np.sin(np.radians(angle))
            draw.line([(x1, y1), (x2, y2)], fill=color, width=max(1, int(1.2*scale)))

    @staticmethod
    def _draw_stop(draw, size, color, **kwargs):
        """Stop (quadrado)."""
        scale = size / 16.0
        pad = 4*scale
        draw.rectangle([pad, pad, size-pad, size-pad], outline=color, width=max(1, int(1.5*scale)))

    # ------------------------------------------------------------------
    #                    DESENHO DAS VARIANTES
    # ------------------------------------------------------------------

    def _draw_icon_only(self, draw, size, icon_func, color):
        """Apenas o ícone, fundo transparente."""
        icon_func(draw, size, color)

    def _draw_with_rectangle(self, draw, size, icon_func, color):
        """Fundo retangular arredondado + ícone centralizado."""
        # Fundo
        margin = size * 0.1  # 10% de margem
        rect = [margin, margin, size-margin, size-margin]
        draw.rounded_rectangle(rect, radius=size*0.15, fill=(240,240,240), outline=(200,200,200), width=1)
        # Ícone (centralizado)
        icon_func(draw, size, color)

    def _draw_with_square(self, draw, size, icon_func, color):
        """Fundo quadrado (pode ser arredondado) + ícone."""
        margin = size * 0.1
        square = [margin, margin, size-margin, size-margin]
        draw.rounded_rectangle(square, radius=size*0.05, fill=(240,240,240), outline=(200,200,200), width=1)
        icon_func(draw, size, color)

    # ------------------------------------------------------------------
    #                    GERAÇÃO DO ÍCONE
    # ------------------------------------------------------------------

    def generate_icon(self, icon_name, variant, size, output_subdir, custom_color=None):
        """
        Gera um ícone específico.
        variant: 'icon', 'rectangle', 'square'
        """
        if icon_name not in self.icons:
            print(f"⚠️  Ícone '{icon_name}' não encontrado!")
            return

        icon_func = self.icons[icon_name]
        color = custom_color or self.default_primary_color
        if len(color) == 3:
            color = color + (255,)  # alpha opaco

        # Cria imagem RGBA
        img = Image.new("RGBA", (size, size), (0,0,0,0))
        draw = ImageDraw.Draw(img)

        # Escolhe o método de desenho conforme a variante
        if variant == "icon":
            self._draw_icon_only(draw, size, icon_func, color)
        elif variant == "rectangle":
            self._draw_with_rectangle(draw, size, icon_func, color)
        elif variant == "square":
            self._draw_with_square(draw, size, icon_func, color)
        else:
            print(f"❌ Variante desconhecida: {variant}")
            return

        # Pós-processamento: suavização
        img = img.filter(ImageFilter.SMOOTH)

        # Salva
        out_dir = os.path.join(self.base_dir, output_subdir)
        os.makedirs(out_dir, exist_ok=True)
        filename = f"{icon_name}-{variant}.png"
        path = os.path.join(out_dir, filename)
        img.save(path)
        print(f"✅ {filename} ({size}px) salvo")
        return img

    def generate_all_variants(self, icon_name, size, output_subdir, custom_color=None):
        """Gera as três variantes de um ícone."""
        for variant in ["icon", "rectangle", "square"]:
            self.generate_icon(icon_name, variant, size, output_subdir, custom_color)

    def generate_full_set(self, size=512, output_subdir="producao"):
        """Gera todos os ícones em todas as variantes."""
        print(f"🚀 Gerando conjunto completo de ícones ({size}px) em '{output_subdir}'...")
        for icon_name in self.icons.keys():
            self.generate_all_variants(icon_name, size, output_subdir)

    # ------------------------------------------------------------------
    #                    MÉTODOS DE ALTA / BAIXA RESOLUÇÃO
    # ------------------------------------------------------------------

    def generate_production_set(self, size=512):
        """Gera ícones em alta resolução (pasta producao)."""
        self.generate_full_set(size, "producao")

    def generate_debug_set(self, size=64):
        """Gera ícones em baixa resolução (pasta debug)."""
        self.generate_full_set(size, "debug")


# ------------------------------------------------------------------
#                            EXEMPLO DE USO
# ------------------------------------------------------------------
def main():
    generator = UtilityIconGenerator(base_dir="util_icons")

    # 1. Gera todos os ícones em 512px (produção) e 64px (debug)
    generator.generate_production_set(size=512)
    generator.generate_debug_set(size=64)

    # 2. Gera um ícone avulso com cor personalizada
    generator.generate_all_variants("chat", size=128, output_subdir="custom_blue",
                                   custom_color=(0, 160, 210))

    print("\n✨ Todos os ícones gerados com sucesso!")
    print("📁 Estrutura de arquivos criada:")
    print("   ├── producao/")
    print("   │   ├── blank-icon.png, blank-rectangle.png, blank-square.png")
    print("   │   ├── chat-icon.png, chat-rectangle.png, chat-square.png")
    print("   │   └── ...")
    print("   ├── debug/")
    print("   └── custom_blue/")

if __name__ == "__main__":
    main()