// Sistema de Gestão Make It Real 3D - JavaScript

// Variáveis globais
let currentTab = 'materias-primas';

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    loadMateriasPrimas();
    loadEquipamentos();
    loadInsumos();
    setupEventListeners();
});

// Event Listeners
function setupEventListeners() {
    document.getElementById('form-materia-prima').addEventListener('submit', handleMateriaPrimaSubmit);
    document.getElementById('form-equipamento').addEventListener('submit', handleEquipamentoSubmit);
    document.getElementById('form-insumo').addEventListener('submit', handleInsumoSubmit);
    document.getElementById('form-custos').addEventListener('submit', handleCustosSubmit);
}

// Navegação entre abas
function showTab(tabName) {
    // Esconder todas as abas
    document.querySelectorAll('.content').forEach(content => {
        content.classList.add('hidden');
    });
    
    // Remover classe active de todas as abas
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Mostrar aba selecionada
    document.getElementById(tabName).classList.remove('hidden');
    event.target.classList.add('active');
    
    currentTab = tabName;
    
    // Carregar dados se necessário
    if (tabName === 'custos') {
        loadSelectOptions();
    }
}

// Funções de API
async function apiCall(url, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(url, options);
        const result = await response.json();
        
        if (!response.ok) {
            throw new Error(result.error || 'Erro na requisição');
        }
        
        return result;
    } catch (error) {
        showAlert('Erro: ' + error.message, 'error');
        throw error;
    }
}

// Matérias-Primas
async function loadMateriasPrimas() {
    try {
        const materias = await apiCall('/api/materias-primas');
        const tbody = document.querySelector('#table-materias-primas tbody');
        tbody.innerHTML = '';
        
        materias.forEach(mp => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${mp.nome}</td>
                <td>${mp.tipo}</td>
                <td>${mp.marca}</td>
                <td>${mp.qualidade}</td>
                <td>${mp.quantidade}</td>
                <td>R$ ${mp.preco.toFixed(2)}</td>
            `;
        });
    } catch (error) {
        console.error('Erro ao carregar matérias-primas:', error);
    }
}

async function handleMateriaPrimaSubmit(event) {
    event.preventDefault();
    
    const data = {
        nome: document.getElementById('mp-nome').value,
        tipo: document.getElementById('mp-tipo').value,
        marca: document.getElementById('mp-marca').value,
        qualidade: document.getElementById('mp-qualidade').value,
        quantidade: parseFloat(document.getElementById('mp-quantidade').value),
        preco: parseFloat(document.getElementById('mp-preco').value)
    };
    
    try {
        await apiCall('/api/materias-primas', 'POST', data);
        showAlert('Matéria-prima adicionada com sucesso!', 'success');
        document.getElementById('form-materia-prima').reset();
        loadMateriasPrimas();
    } catch (error) {
        console.error('Erro ao adicionar matéria-prima:', error);
    }
}

// Equipamentos
async function loadEquipamentos() {
    try {
        const equipamentos = await apiCall('/api/equipamentos');
        const tbody = document.querySelector('#table-equipamentos tbody');
        tbody.innerHTML = '';
        
        equipamentos.forEach(eq => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${eq.nome}</td>
                <td>${eq.potencia}W</td>
                <td>R$ ${eq.preco.toFixed(2)}</td>
                <td>${eq.vida_util}h</td>
            `;
        });
    } catch (error) {
        console.error('Erro ao carregar equipamentos:', error);
    }
}

async function handleEquipamentoSubmit(event) {
    event.preventDefault();
    
    const data = {
        nome: document.getElementById('eq-nome').value,
        potencia: parseFloat(document.getElementById('eq-potencia').value),
        preco: parseFloat(document.getElementById('eq-preco').value),
        valor_inicial: parseFloat(document.getElementById('eq-valor-inicial').value),
        vida_util: parseFloat(document.getElementById('eq-vida-util').value)
    };
    
    try {
        await apiCall('/api/equipamentos', 'POST', data);
        showAlert('Equipamento adicionado com sucesso!', 'success');
        document.getElementById('form-equipamento').reset();
        loadEquipamentos();
    } catch (error) {
        console.error('Erro ao adicionar equipamento:', error);
    }
}

// Insumos
async function loadInsumos() {
    try {
        const insumos = await apiCall('/api/insumos');
        const tbody = document.querySelector('#table-insumos tbody');
        tbody.innerHTML = '';
        
        insumos.forEach(insumo => {
            const row = tbody.insertRow();
            row.innerHTML = `
                <td>${insumo.nome}</td>
                <td>${insumo.quantidade}</td>
                <td>${insumo.unidade}</td>
                <td>R$ ${insumo.preco.toFixed(2)}</td>
            `;
        });
    } catch (error) {
        console.error('Erro ao carregar insumos:', error);
    }
}

async function handleInsumoSubmit(event) {
    event.preventDefault();
    
    const data = {
        nome: document.getElementById('in-nome').value,
        quantidade: parseFloat(document.getElementById('in-quantidade').value),
        unidade: document.getElementById('in-unidade').value,
        preco: parseFloat(document.getElementById('in-preco').value)
    };
    
    try {
        await apiCall('/api/insumos', 'POST', data);
        showAlert('Insumo adicionado com sucesso!', 'success');
        document.getElementById('form-insumo').reset();
        loadInsumos();
    } catch (error) {
        console.error('Erro ao adicionar insumo:', error);
    }
}

// Custos
async function loadSelectOptions() {
    try {
        const [equipamentos, materias] = await Promise.all([
            apiCall('/api/equipamentos'),
            apiCall('/api/materias-primas')
        ]);
        
        const selectEq = document.getElementById('custo-equipamento');
        const selectMp = document.getElementById('custo-materia-prima');
        
        selectEq.innerHTML = '<option value="">Selecione...</option>';
        selectMp.innerHTML = '<option value="">Selecione...</option>';
        
        equipamentos.forEach(eq => {
            selectEq.innerHTML += `<option value="${eq.id}">${eq.nome}</option>`;
        });
        
        materias.forEach(mp => {
            selectMp.innerHTML += `<option value="${mp.id}">${mp.nome}</option>`;
        });
    } catch (error) {
        console.error('Erro ao carregar opções:', error);
    }
}

async function handleCustosSubmit(event) {
    event.preventDefault();
    
    const data = {
        equipamento_id: parseInt(document.getElementById('custo-equipamento').value),
        materia_prima_id: parseInt(document.getElementById('custo-materia-prima').value),
        quantidade_utilizada: parseFloat(document.getElementById('custo-quantidade').value),
        tempo_impressao: parseFloat(document.getElementById('custo-tempo').value)
    };
    
    try {
        const resultado = await apiCall('/api/calcular-custos', 'POST', data);
        
        document.getElementById('custo-mp').textContent = resultado.custo_materia_prima.toFixed(2);
        document.getElementById('custo-energia').textContent = resultado.custo_energia.toFixed(2);
        document.getElementById('custo-total').textContent = resultado.custo_total.toFixed(2);
        
        document.getElementById('resultado-custos').classList.remove('hidden');
        showAlert('Custos calculados com sucesso!', 'success');
    } catch (error) {
        console.error('Erro ao calcular custos:', error);
    }
}

// Utilitários
function showAlert(message, type) {
    const container = document.getElementById('alert-container');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.textContent = message;
    
    container.innerHTML = '';
    container.appendChild(alert);
    
    setTimeout(() => {
        alert.remove();
    }, 5000);
}
