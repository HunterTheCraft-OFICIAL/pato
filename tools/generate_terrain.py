import os
import random
import numpy as np
from PIL import Image, ImageFilter, ImageDraw

class BrazilTerrainFactoryV15:
    def __init__(self, size=512, base_dir="tiles_v15_final"):
        self.size = size
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _generate_texture(self, color, noise_var, current_size):
        r, g, b = color
        noise = np.random.normal(0, noise_var, (current_size, current_size))
        
        # Manchas proporcionais ao tamanho atual
        low_res_val = max(4, int(current_size / 16))
        low_res = np.random.normal(0, 12, (low_res_val, low_res_val))
        stains = np.array(Image.fromarray(low_res).resize((current_size, current_size), resample=Image.BICUBIC))
        
        img_array = np.zeros((current_size, current_size, 3), dtype=np.uint8)
        img_array[...,0] = np.clip(r + noise + stains, 0, 255)
        img_array[...,1] = np.clip(g + noise + stains, 0, 255)
        img_array[...,2] = np.clip(b + noise + stains, 0, 255)
        return Image.fromarray(img_array, "RGB").convert("RGBA")

    def _add_features(self, draw, config, current_size):
        if not config: return
        m_cnt, m_col, p_cnt, c_cnt, v_type, shells = config
        
        # Escala relativa ao padrão de 512px
        scale = current_size / 512.0
        area_s = scale ** 2

        # 1. Vegetação
        for _ in range(int(m_cnt * area_s)):
            x, y = random.randint(0, current_size), random.randint(0, current_size)
            h = (8, 18) if v_type == "capim" else (4, 10)
            draw.line([(x, y), (x + random.randint(int(-4*scale), int(4*scale)), 
                        y - random.randint(int(h[0]*scale), int(h[1]*scale)))], 
                      fill=m_col, width=max(1, int(1.5*scale)))
        
        # 2. Pedras
        for _ in range(int(p_cnt * area_s)):
            x, y = random.randint(0, current_size), random.randint(0, current_size)
            w = random.randint(int(5*scale), int(12*scale))
            s = max(1, int(2*scale))
            draw.ellipse([x+s, y+s, x+w+s, y+int(w*0.8)+s], fill=(0,0,0,60))
            g = random.randint(110, 160)
            draw.ellipse([x, y, x+w, y+int(w*0.8)], fill=(g,g,g,220))
        
        # 3. Conchas e Fissuras
        if shells:
            for _ in range(int(35 * area_s)):
                x, y, w = random.randint(0, current_size), random.randint(0, current_size), random.randint(int(3*scale), int(7*scale))
                draw.arc([x, y, x+w, y+w], start=random.randint(0,180), end=random.randint(200,360), fill=(245,245,230,200), width=max(1, int(2*scale)))
        
        if c_cnt > 0:
            for _ in range(int(c_cnt * area_s)):
                x, y = random.randint(0, current_size), random.randint(0, current_size)
                draw.line([(x, y), (x+int(10*scale), y+int(8*scale))], fill=(0,0,0,40), width=max(1, int(scale)))

    def create_tile(self, name, color, config, target_size, folder, is_ocean=False):
        os.makedirs(os.path.join(self.base_dir, folder), exist_ok=True)
        scale = target_size / 512.0
        
        noise = 8 if is_ocean else 18
        img_rgba = self._generate_texture(color, noise, target_size)
        
        if is_ocean:
            img = img_rgba.filter(ImageFilter.GaussianBlur(radius=2.0 * scale)).convert("RGB")
        else:
            overlay = Image.new("RGBA", (target_size, target_size), (0,0,0,0))
            self._add_features(ImageDraw.Draw(overlay), config, target_size)
            img = Image.alpha_composite(img_rgba, overlay).convert("RGB")
            img = img.filter(ImageFilter.SHARPEN)

        img.save(os.path.join(self.base_dir, folder, f"{name}.png"))

if __name__ == "__main__":
    # CONFIGURAÇÃO DE RESOLUÇÃO (Produção)
    PROD_SIZE = 512 
    factory = BrazilTerrainFactoryV15(size=PROD_SIZE)

    # Database de Biomas
    data = {
        "amazonia": [(25, 80, 40), (140, (15, 45, 15, 160), 10, 0, "mato", False)],
        "cerrado": [(200, 150, 85), (100, (160, 140, 60, 150), 45, 0, "capim", False)],
        "caatinga": [(215, 190, 145), (35, (130, 115, 90, 120), 120, 30, "mato", False)],
        "pampas": [(110, 175, 65), (200, (40, 90, 30, 150), 5, 0, "mato", False)],
        "terra_roxa": [(125, 50, 40), (20, (60, 30, 20, 120), 15, 15, "mato", False)],
        "areia_nordeste": [(245, 235, 205), (0, None, 10, 0, "mato", False)],
        "areia_sudeste": [(220, 200, 160), (0, None, 40, 0, "mato", True)],
        "mar_raso": [(80, 180, 210), None],
        "mar_padrao": [(45, 110, 190), None],
        "mar_profundo": [(20, 40, 100), None]
    }

    # 1. GERAÇÃO PRODUÇÃO (512px ou o definido)
    print(f"🚀 Gerando Ativos de Produção ({PROD_SIZE}px)...")
    for name, params in data.items():
        factory.create_tile(name, params[0], params[1], PROD_SIZE, "producao", is_ocean="mar" in name)

    # 2. GERAÇÃO MVP (64px para Depuração)
    print(f"🧪 Gerando Pasta MVP (64px)...")
    mvp_targets = ["amazonia", "cerrado", "caatinga", "areia_sudeste"]
    for name in mvp_targets:
        params = data[name]
        factory.create_tile(f"debug_{name}", params[0], params[1], 64, "MVP", is_ocean=False)

    print("\n✨ V15 Concluída com Sucesso!")