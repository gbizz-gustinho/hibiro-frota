// utilitarios-hibiro.js

// 1. Configuração de Máscaras Automáticas
document.addEventListener('DOMContentLoaded', () => {
    // Máscara dinâmica CPF/CNPJ
    document.querySelectorAll('.mask-doc').forEach(el => {
        IMask(el, {
            mask: [
                { mask: '000.000.000-00', type: 'CPF' },
                { mask: '00.000.000/0000-00', type: 'CNPJ' }
            ]
        });
    });

    // Máscara de Telefone (Celular e Fixo)
    document.querySelectorAll('.mask-phone').forEach(el => {
        IMask(el, { mask: '(00) 00000-0000' });
    });

    // Máscara de CEP
    document.querySelectorAll('.mask-cep').forEach(el => {
        IMask(el, { mask: '00000-000' });
    });
});

// 2. Rotina ViaCEP
async function buscarCep(cepInput) {
    const cep = cepInput.value.replace(/\D/g, '');
    if (cep.length !== 8) return;

    try {
        const response = await fetch(`https://viacep.com.br/ws/${cep}/json/`);
        const data = await response.json();

        if (!data.erro) {
            // Preenche automaticamente os campos se existirem na página
            document.querySelector('[name="logradouro"]')?.setAttribute('value', data.logradouro);
            document.querySelector('[name="bairro"]')?.setAttribute('value', data.bairro);
            document.querySelector('[name="cidade"]')?.setAttribute('value', data.localidade);
            document.querySelector('[name="estado"]')?.setAttribute('value', data.uf);
            
            // Também tenta pelo ID caso o name falhe
            if(document.getElementById('logradouro')) document.getElementById('logradouro').value = data.logradouro;
            if(document.getElementById('bairro')) document.getElementById('bairro').value = data.bairro;
            if(document.getElementById('cidade')) document.getElementById('cidade').value = data.localidade;
            if(document.getElementById('uf')) document.getElementById('uf').value = data.uf;
            
            document.querySelector('[name="numero"]')?.focus();
        }
    } catch (error) {
        console.error("Erro ao buscar CEP:", error);
    }
}