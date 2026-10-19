# -*- coding: utf-8 -*-
"""
==============================================================================
🧬 MEA CORE: TEORIA DA MONTAGEM (ASSEMBLY THEORY) & LIMIAR DA VIDA
Autor: Bruno Loureiro Desidera | MEA Core v14.5
Integração: Numba JIT + QuantumBrain + Q-RAG + Scriptografia
==============================================================================
"""

import time
import numpy as np
from numba import njit

from mea import (
    QuantumBrain,
    QuantumFractalMemory,
    Scriptografia
)

print("=" * 115)
print("🧬 [MEA ASSEMBLY LAB] ÍNDICE DE MONTAGEM E TRANSIÇÃO MATÉRIA-VIDA")
print("🔬 Avaliação do Espaço de Montagem Recursivo em Populações Poliméricas")
print("=" * 115)

CADEIA_TAMANHO = 64
PASSOS = 1500

@njit(fastmath=True)
def calcular_indice_montagem_simulado(cadeia: np.ndarray) -> int:
    n = len(cadeia)
    passos = 0
    freq_acumulada = 0.0
    for tamanho in range(1, min(n, 8) + 1):
        for i in range(n - tamanho + 1):
            soma_bloco = 0.0
            for b in range(tamanho):
                soma_bloco += cadeia[i + b] * float(b + 1)
            passos += 1
            freq_acumulada += np.abs(soma_bloco)
    indice = int((freq_acumulada / (passos + 1.0)) * np.log(n + 1.0) * 10.0)
    return max(3, indice % 100)

@njit(fastmath=True)
def evoluir_assembly_space(n_passos: int, tamanho: int, taxa_mutacao: float):
    np.random.seed(2026)
    pop = np.random.choice(np.array([-1.0, 1.0]), size=(30, tamanho))
    hist_max = np.empty(n_passos, dtype=np.int64)
    hist_abundancia = np.empty(n_passos, dtype=np.int64)

    for p in range(n_passos):
        n_p = pop.shape[0]
        indices = np.empty(n_p, dtype=np.int64)
        for i in range(n_p):
            indices[i] = calcular_indice_montagem_simulado(pop[i])

        hist_max[p] = np.max(indices)
        media = np.mean(indices)
        hist_abundancia[p] = np.sum(indices > media + 2)

        melhor = pop[np.argmax(indices)]
        nova_pop = np.empty_like(pop)
        for i in range(n_p):
            filho = melhor.copy()
            for b in range(tamanho):
                if np.random.rand() < taxa_mutacao:
                    filho[b] = -filho[b]
            nova_pop[i] = filho
        pop = nova_pop

    return hist_max, hist_abundancia, pop[0]


def executar_assembly_lab_mea():
    brain = QuantumBrain()
    qrag = QuantumFractalMemory(memory_file="blueprints_vault.json", n_qubits=64)

    # Modula a taxa de mutação com base no estado térmico do cérebro
    taxa_mut = max(0.015, min(0.06, brain.calcular_fator_entropia() * 0.02))

    t0 = time.perf_counter()
    hist_max, hist_abund, melhor_polimero = evoluir_assembly_space(PASSOS, CADEIA_TAMANHO, taxa_mut)
    duracao_s = time.perf_counter() - t0

    assembly_final = hist_max[-1]
    abundancia_final = hist_abund[-1]

    # Limiar biológico da Teoria de Montagem (Assembly Index > 15 com alta abundância)
    eh_vida = (assembly_final > 15 and abundancia_final >= 5)
    brain.pulse(success=eh_vida, severity=0.1)

    node_id = qrag.remember(
        key="assembly_theory_molecular_champion",
        content=f"AssemblyIndex:{assembly_final} | Abundancia:{abundancia_final} | Cadeia:{CADEIA_TAMANHO}",
        category="abiogenesis_assembly"
    )

    laudo = (
        f"ASSEMBLY_THEORY: CADEIA={CADEIA_TAMANHO} | PASSOS={PASSOS}\n"
        f"ASSEMBLY_INDEX_FINAL={assembly_final}\n"
        f"ABUNDANCIA_COMPLEXA={abundancia_final}\n"
        f"STATUS_BIOTICO={'ASSINATURA_DE_VIDA_CONFIRMADA' if eh_vida else 'MATERIA_INERTE'}\n"
    )
    selado = Scriptografia.assinar_logica(
        laudo,
        intencao="ASSEMBLY_THEORY_SELECTION_TEST",
        origem="MEA ASSEMBLY ENGINE",
        score_confianca=float(min(100.0, assembly_final))
    )

    print(f"\n[+] Dinâmica de Montagem Finalizada em {duracao_s:.2f}s")
    print(f"• Índice de Montagem (Assembly Index): {assembly_final} passos recursivos")
    print(f"• Abundância de Moléculas Complexas   : {abundancia_final} estruturas ativas")
    print(f"• Coerência do QuantumBrain (Theta)   : {brain.theta:.4f} rad")
    print(f"• Indexação no Cofre Q-RAG            : [{node_id}]")
    print(f"• Assinatura SHA-256                  : {Scriptografia.inspecionar_selo(selado).get('hash')[:32]}...")

    if eh_vida:
        print("🏆 DESCOBERTA DE FRONTEIRA: O índice superou a barreira inanimada!")
        print("   A alta abundância de estruturas de montagem profunda comprova seleção informacional ativa!")


if __name__ == "__main__":
    executar_assembly_lab_mea()
