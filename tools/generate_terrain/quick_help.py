"""
Ajuda rápida para o sistema
"""

HELP_TEXT = """
🌿 GERADOR DE BIOMAS BRASILEIROS - AJUDA RÁPIDA
==================================================

📋 COMANDOS DISPONÍVEIS:

1. 🚀 Geração completa:
   python main.py

2. 🎮 Menu interativo:
   python run_all.py

3. 🧪 Teste rápido:
   python simple_test.py

4. 🔍 Diagnóstico:
   python fix_imports.py

5. 🧹 Limpeza:
   python cleanup.py

6. 📊 Comparação (sem gráficos):
   python compare_biomes.py

7. 🎨 Tileset:
   python create_tileset.py

📁 ESTRUTURA DE ARQUIVOS:

bioma_*.py     - Classes de cada bioma
biome_base.py  - Classe base comum
main.py        - Geração principal
run_all.py     - Menu interativo

📚 TUTORIAL RÁPIDO:

1. Primeira execução:
   python fix_imports.py  # Verifique problemas
   python main.py         # Gere todos os biomas

2. Para testes:
   python simple_test.py  # Teste básico
   python run_all.py      # Use o menu

3. Para limpar:
   python cleanup.py      # Libere espaço

⚠️  SOLUÇÃO DE PROBLEMAS:

❌ "ModuleNotFoundError":
   - Execute: pip install numpy Pillow
   - Ou use: python fix_imports.py

❌ Arquivos faltando:
   - Verifique se todos os biome_*.py estão presentes

❌ Erro na geração:
   - Tente: python simple_test.py
   - Verifique permissões de escrita

📞 SUPORTE:
   - Verifique README.md para detalhes
   - Execute diagnósticos com fix_imports.py
"""

if __name__ == "__main__":
    print(HELP_TEXT)