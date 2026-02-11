"""
Atualiza o requirements.txt para versão mínima
"""

REQUIREMENTS = """numpy>=1.21.0
Pillow>=9.0.0
# Matplotlib removido para compatibilidade com Android
# matplotlib>=3.5.0  # Opcional, para gráficos
"""

print("📦 ATUALIZANDO REQUIREMENTS.TXT")
print("=" * 60)

with open("requirements.txt", "w") as f:
    f.write(REQUIREMENTS)

print("✅ requirements.txt atualizado!")
print("\n📋 Conteúdo:")
print("-" * 30)
print(REQUIREMENTS)
print("-" * 30)
print("\n🎯 Versão mínima para funcionamento no Android")