import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hashlib

def verificar_integridade(row):
    # Formatação exata para bater com o hash gerado no simulador
    f_str = "{:d}|{:.20f}|{:.20f}|{:.20f}".format(
        int(row['frame']), 
        float(row['ruido_vacaum']), 
        float(row['psi_ce_op']), 
        float(row['fidelidade_S'])
    )
    hash_calculado = hashlib.sha256(f_str.encode('utf-8')).hexdigest()
    return hash_calculado == row['hash_id']
    
def analisar_resultados_harpia(filename="harpia_telemetry_secure_2017.parquet"):
    try:
        # 1. Carregamento do arquivo Parquet
        df = pd.read_parquet(filename, engine='pyarrow')
        
        # 2. Resultados da Auditoria (exibição no console)
        print("🚀 INICIANDO AUDITORIA DE CAMPO: SISTEMA HARPIA V2 (PARQUET SECURE)")
        print("🔐 Verificando assinaturas criptográficas...")
        
        # Auditoria de Integridade (verificando os primeiros frames)
        check_frames = df.head(1000).apply(verificar_integridade, axis=1)
        
        if not check_frames.all():
            erro_idx = check_frames[~check_frames].index[0]
            print(f"❌ ALERTA DE SEGURANÇA: Falha de integridade no frame {erro_idx + 1}")
            return

        # 3. Estatísticas
        fidelidade_media = df['fidelidade_S'].mean()
        
        print("✅ Dados validados! Parquet manteve a precisão de 64-bit.")
        print(f"📊 Fidelidade Média: {fidelidade_media:.12f}")
        print(f"🔑 Hash Checksum (Frame 1): {df['hash_id'].iloc[0]}")
        print("-" * 80)

        # 4. Configuração do Gráfico (Layout da Imagem Enviada)
        plt.style.use('seaborn-v0_8-whitegrid') # Estilo mais limpo para artigos
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=False)
        plt.subplots_adjust(hspace=0.4)

        # --- Gráfico Superior: Ruído vs Compensação ---
        # Plotando apenas os primeiros 1000 frames como na imagem
        plot_limit = 1000
        ax1.plot(df['frame'][:plot_limit], df['ruido_vacaum'][:plot_limit], 
                 label='Ruído de Vácuo (Ambiente)', color='gray', alpha=0.5, linewidth=1)
        ax1.plot(df['frame'][:plot_limit], np.abs(df['psi_ce_op'][:plot_limit]), 
                 label=r'Compensação $|\Psi_{CE}|$', color='blue', linestyle='--', linewidth=1)
        
        ax1.set_ylabel('Densidade de Energia (J)')
        ax1.set_title('Sintonização de Impedância de Campo (Harpia V2)')
        ax1.legend(loc='upper right')
        ax1.grid(True, which='both', linestyle='--', alpha=0.5)

        # --- Gráfico Inferior: Fidelidade do Estado ---
        ax2.scatter(df['frame'][:plot_limit], df['fidelidade_S'][:plot_limit], 
                    color='yellow', s=10, label='Fidelidade do Estado (S)', edgecolors='black', linewidths=0.5)
        ax2.axhline(y=0.9999, color='red', linestyle=':', label='Limiar de Coerência Crítica')
        
        ax2.set_ylabel('Fidelidade (0 a 1)')
        ax2.set_xlabel('Frames de Processamento (Tempo)')
        ax2.set_ylim([0.999, 1.0001]) # Foco na alta fidelidade
        ax2.set_title(r'Eficácia da Supressão de Decoerência via $E_{AC}$ Reduzida')
        ax2.legend(loc='lower right')
        ax2.grid(True, which='both', linestyle='--', alpha=0.5)

        # 5. Salvar e Mostrar
        plt.savefig("analise_estabilidade_harpia_final.png", dpi=300)
        print("🖼️ Gráfico salvo como: 'analise_estabilidade_harpia_final.png'")
        plt.show()

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    analisar_resultados_harpia()
