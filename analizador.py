import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def analisar_resultados_harpia(filename="harpia_telemetry_2017_rev.csv"):
    try:
        # 1. Carregamento dos Dados de Telemetria
        df = pd.read_csv(filename)
        print(f"📊 Analisando {len(df)} frames de dados do Sistema Harpia...")

        # 2. Configuração Estética do Gráfico (Estilo Científico)
        plt.style.use('seaborn-v0_8-muted')
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)
        plt.subplots_adjust(hspace=0.3)

        # --- GRÁFICO 1: RUÍDO VS COMPENSAÇÃO (Equilíbrio de Fase) ---
        ax1.plot(df['frame'][:1000], df['ruido_vacaum'][:1000], label='Ruído de Vácuo (Ambiente)', color='gray', alpha=0.5)
        ax1.plot(df['frame'][:1000], np.abs(df['psi_ce_op'][:1000]), label=r'Compensação $|\Psi_{CE}|$', color='blue', linestyle='--')
        ax1.set_ylabel('Densidade de Energia (J)')
        ax1.set_title('Sintonização de Impedância de Campo (Harpia V2)')
        ax1.legend(loc='upper right')
        ax1.grid(True, which='both', linestyle='--', alpha=0.5)

        # --- GRÁFICO 2: ESTABILIDADE DA FIDELIDADE (Manutenção do Qubit) ---
        ax2.scatter(df['frame'][:1000], df['fidelidade_S'][:1000], c=df['fidelidade_S'][:1000], 
                    cmap='viridis', s=10, label='Fidelidade do Estado (S)')
        ax2.axhline(y=0.9999, color='red', linestyle=':', label='Limiar de Coerência Crítica')
        ax2.set_ylabel('Fidelidade (0 a 1)')
        ax2.set_xlabel('Frames de Processamento (Tempo)')
        ax2.set_ylim([0.999, 1.0001]) # Foco na alta fidelidade
        ax2.set_title(r'Eficácia da Supressão de Decoerência via $E_{AC}$ Reduzida')
        ax2.legend(loc='lower right')
        ax2.grid(True, which='both', linestyle='--', alpha=0.5)

        # 3. Análise Estatística para o Texto do Artigo
        fidelidade_media = df['fidelidade_S'].mean()
        desvio_padrao = df['fidelidade_S'].std()
        
        print(f"\n--- RELATÓRIO DE COERÊNCIA SPHY ---")
        print(f"🔹 Fidelidade Média: {fidelidade_media:.12f}")
        print(f"🔹 Estabilidade (Sigma): {desvio_padrao:.12e}")
        print(f"🔹 Status do Sistema: {'✅ OPERAÇÃO COERENTE ATIVA' if fidelidade_media > 0.99 else '⚠️ DISSIPAÇÃO DETECTADA'}")
        
        # Salvar o gráfico para o artigo
        plt.savefig("analise_estabilidade_harpia.png", dpi=300)
        print("\n🖼️ Gráfico científico salvo como: 'analise_estabilidade_harpia.png'")
        plt.show()

    except FileNotFoundError:
        print("❌ Erro: O arquivo de telemetria não foi encontrado. Rode o simulador primeiro!")

if __name__ == "__main__":
    analisar_resultados_harpia()
