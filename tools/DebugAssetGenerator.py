# tools/DebugAssetGenerator.py
import os
from PIL import Image, ImageDraw, ImageFont

class DebugAssetGenerator:
    def __init__(self, base_dir="debug_assets"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def create_logo(self, size=256):
        """Cria um logo simples com texto 'PATO'"""
        img = Image.new("RGB", (size, size), (30, 30, 50))
        draw = ImageDraw.Draw(img)
        
        # Tenta usar fonte padrão, senão usa default
        try:
            # Em alguns sistemas, essa fonte existe
            font = ImageFont.truetype("arial.ttf", size//4)
        except:
            font = ImageFont.load_default()
        
        text = "PATO"
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x = (size - w) // 2
        y = (size - h) // 2
        draw.text((x, y), text, fill=(100, 200, 255), font=font)
        
        img.save(os.path.join(self.base_dir, "logo.png"))
        print(f"✅ Logo gerado: {size}x{size}")

    def create_button(self, name, color, size=(200, 60)):
        """Cria botão retangular com borda e cor de fundo"""
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Fundo
        draw.rounded_rectangle([0, 0, size[0], size[1]], radius=10, fill=color + (200,))
        # Borda
        draw.rounded_rectangle([0, 0, size[0], size[1]], radius=10, outline=(255, 255, 255, 255), width=2)
        
        img.save(os.path.join(self.base_dir, f"{name}.png"))
        print(f"✅ Botão '{name}' gerado: {size}")

    def create_placeholder_tile(self, name, color, size=64):
        """Cria tile genérico (ex: para fallback de terreno)"""
        img = Image.new("RGB", (size, size), color)
        draw = ImageDraw.Draw(img)
        # Adiciona uma letra para identificação visual
        draw.text((size//4, size//4), name[0].upper(), fill=(255,255,255))
        img.save(os.path.join(self.base_dir, f"{name}.png"))
        print(f"✅ Tile placeholder '{name}' gerado")

    def generate_all(self):
        print("🛠️  Gerando assets de debug...")
        
        # Logo
        self.create_logo(256)
        
        # Botões
        self.create_button("button_normal", (70, 130, 180))      # Steel blue
        self.create_button("button_pressed", (50, 100, 150))     # Darker
        self.create_button("button_exit", (180, 60, 60))         # Vermelho suave
        
        # Tiles de fallback (úteis para evitar crash no carregamento)
        self.create_placeholder_tile("fallback_terrain", (50, 150, 50))
        self.create_placeholder_tile("fallback_water", (50, 100, 200))
        self.create_placeholder_tile("error_tile", (200, 50, 50))
        
        # Font background (opcional)
        bg = Image.new("RGB", (128, 128), (20, 20, 30))
        bg.save(os.path.join(self.base_dir, "font_bg.png"))
        
        print(f"\n✨ Assets de debug prontos em: {self.base_dir}")

if __name__ == "__main__":
    gen = DebugAssetGenerator("debug_assets")
    gen.generate_all()