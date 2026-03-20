/**
 * Hibiro 2026 - Utilitários de Front-end
 * Centraliza Máscaras, ViaCEP e UI Helpers
 */

const HibiroUtils = {
 // Adicione dentro do seu objeto HibiroUtils.initMasks
initMasks: function() {
    // ... máscaras anteriores (CPF, CNPJ, CEP) ...

    // Moeda (R$)
    document.querySelectorAll('.mask-money').forEach(el => {
        IMask(el, {
            mask: 'R$ num',
            blocks: {
                num: {
                    mask: Number,
                    thousandsSeparator: '.',
                    padFractionalZeros: true,
                    radix: ',',
                    mapToRadix: ['.']
                }
            }
        });
    });

    // Taxa / Porcentagem (%)
    document.querySelectorAll('.mask-percent').forEach(el => {
        IMask(el, {
            mask: 'num%',
            blocks: {
                num: {
                    mask: Number,
                    radix: ',',
                    mapToRadix: ['.'],
                    scale: 2 // Duas casas decimais
                }
            }
        });
    });

    // Data (DD/MM/AAAA)
    document.querySelectorAll('.mask-date').forEach(el => {
        IMask(el, { mask: '00/00/0000' });
    });
}

        // 1. Máscara Dinâmica CPF/CNPJ
        document.querySelectorAll('.mask-doc').forEach(el => {
            IMask(el, {
                mask: [
                    { mask: '000.000.000-00', type: 'CPF' },
                    { mask: '00.000.000/0000-00', type: 'CNPJ' }
                ]
            });
        });

        // 2. Telefone (Celular e Fixo)
        document.querySelectorAll('.mask-phone').forEach(el => {
            IMask(el, { mask: '(00) 00000-0000' });
        });

        // 3. CEP
        document.querySelectorAll('.mask-cep').forEach(el => {
            IMask(el, { mask: '00000-000' });
        });
    },

    /**
     * Consulta API ViaCEP e preenche campos de endereço
     */
    buscarCep: async function(input) {
        const cep = input.value.replace(/\D/g, '');
        if (cep.length !== 8) return;

        // Feedback visual
        input.classList.add('animate-pulse', 'border-blue-500', 'ring-2', 'ring-blue-500/20');

        try {
            const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
            const data = await response.json();

            if (!data.erro) {
                // Mapeamento: Chave do ViaCEP -> Atributo 'name' ou 'id' no HTML
                this._fillField('logradouro', data.logradouro);
                this._fillField('bairro', data.bairro);
                this._fillField('cidade', data.localidade);
                this._fillField('estado', data.uf);
                this._fillField('uf', data.uf); // Algumas tabelas usam 'uf' em vez de 'estado'

                // Move o foco para o número se ele existir
                const numField = document.querySelector('[name="numero"]') || document.getElementById('numero');
                if (numField) numField.focus();
            } else {
                console.warn("CEP não encontrado.");
            }
        } catch (e) {
            console.error("Erro ao consultar ViaCEP:", e);
        } finally {
            input.classList.remove('animate-pulse', 'border-blue-500', 'ring-2', 'ring-blue-500/20');
        }
    },

    /**
     * Helper interno para preenchimento de campos
     */
    _fillField: function(nameOrId, value) {
        const el = document.querySelector(`[name="${nameOrId}"]`) || document.getElementById(nameOrId);
        if (el) {
            el.value = value.toUpperCase();
            // Dispara eventos para garantir que o navegador perceba a mudança
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
        }
    }
};

// Inicializa ao carregar o DOM
document.addEventListener('DOMContentLoaded', () => {
    HibiroUtils.initMasks();
});