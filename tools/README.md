# 🌿 Gerador de Biomas Brasileiros - Pixel Art

Gerador de texturas pixeladas no estilo Minecraft para os principais biomas brasileiros.

## 📋 Biomas Incluídos

1. **Amazônia** - Floresta tropical úmida
2. **Cerrado** - Campos abertos e savanas
3. **Pantanal** - Áreas alagadas e vida aquática
4. **Caatinga** - Clima semiárido e solo seco
5. **Mata Atlântica** - Floresta tropical costeira
6. **Pampa** - Pradarias e planícies

## 🚀 Como Usar

### Instalação
```bash
pip install -r requirements.txt
```

Geração Completa

```bash
python main.py
```

Testes Rápidos

```bash
python test_single.py
```

Comparar Versões

```bash
python compare_biomes.py
```

Criar Tileset

```bash
python create_tileset.py
```

📁 Estrutura de Arquivos

```
biomas_tiles/
├── producao/          # Tiles de 512px (alta qualidade)
├── debug/             # Tiles de 64px (debug)
├── testes_rapidos/    # Testes individuais
├── tileset_completo.png  # Tileset combinado
└── card_*.png         # Cartões visuais
```

🎨 Características por Bioma

Amazônia

· Tons de verde escuro e médio
· Mato alto denso
· Áreas sombreadas de floresta úmida

Cerrado

· Verde amarelado e marrom claro
· Capim fino
· Pedras cinzas espalhadas

Pantanal

· Verdes médios e azulados
· Capim baixo
· Áreas úmidas e conchas

Caatinga

· Bege, marrom claro e verde seco
· Vegetação rala
· Fissuras no solo e pedras escuras

Mata Atlântica

· Verdes vibrantes e escuros
· Vegetação densa
· Manchas sombreadas úmidas

Pampa

· Verdes claros e médios
· Capim baixo em linhas finas
· Variações sutis de cor

🛠️ Requisitos

· Python 3.7+
· NumPy
· Pillow (PIL)

📄 Licença

Projeto educacional para estudo de biomas brasileiros e geração procedural de texturas.

---
Resumo das Melhorias:

1. ✅ Sistema funcionando: Pelos logs, tudo está gerando corretamente
2. ✅ Texturas específicas: Cada bioma tem características únicas
3. ✅ Duas resoluções: Produção (512px) e Debug (64px)
4. ✅ Novas ferramentas: Adicionei scripts para testes rápidos, comparação e criação de tilesets
5. ✅ Menu interativo: Para facilitar o uso
6. ✅ Documentação: README completo

Como usar as novas ferramentas:

```bash
# Menu interativo
python run_all.py
```

```bash
# Teste rápido
python test_single.py
```

```bash
# Ver estatísticas
python compare_biomes.py
```

```bash
# Criar tileset
python create_tileset.py
```

O sistema está funcionando muito bem! As texturas estão sendo geradas com sucesso e você já tem uma ótima base para trabalhar com biomas brasileiros em estilo pixel art. 🎨