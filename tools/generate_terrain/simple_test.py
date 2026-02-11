"""
Teste super simples para verificar se o sistema funciona
"""

import os

print("🧪 TESTE SUPER SIMPLES DO GERADOR")
print("=" * 50)

# 1. Verificar estrutura básica
print("\n1. 📁 Verificando estrutura...")
required = ["biome_base.py", "main.py"]
for file in required:
    if os.path.exists(file):
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} faltando")

# 2. Testar importação básica
print("\n2. 🔧 Testando importação...")
try:
    from biome_amazonia import AmazoniaBiome
    print("   ✅ Importação de AmazoniaBiome OK")
except ImportError as e:
    print(f"   ❌ Erro na importação: {e}")

# 3. Testar geração de um único bioma
print("\n3. 🎨 Testando geração de Amazônia...")
try:
    amazonia = AmazoniaBiome("teste_simples")
    # Tamanho pequeno para teste rápido
    result = amazonia.generate_biome(128, "teste", 8)
    print(f"   ✅ Amazônia gerada: {result}")
except Exception as e:
    print(f"   ❌ Erro na geração: {e}")

print("\n" + "=" * 50)
print("✨ Teste concluído!")