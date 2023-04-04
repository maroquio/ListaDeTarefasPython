const apiUrl = 'http://localhost:8000/tarefas';

const tarefaForm = document.getElementById('tarefa-form');
const tarefaId = document.getElementById('tarefa-id');
const titulo = document.getElementById('titulo');
const descricao = document.getElementById('descricao');
const data_hora_inicio = document.getElementById('data_hora_inicio');
const data_hora_fim = document.getElementById('data_hora_fim');
const situacao = document.getElementById('situacao');
const tarefasDiv = document.getElementById('tarefas');

tarefaForm.addEventListener('submit', (e) => {
    e.preventDefault();

    if (tarefaId.value === '') {
        axios.post(apiUrl, {
            id: 0,
            titulo: titulo.value,
            descricao: descricao.value,
            data_hora_inicio: data_hora_inicio.value,
            data_hora_fim: data_hora_fim.value,
            situacao: situacao.value
        }).then(() => {
            listarTarefas();
            tarefaForm.reset();
        });
    } else {
        axios.put(`${apiUrl}/${tarefaId.value}`, {
            id: tarefaId.value,
            titulo: titulo.value,
            descricao: descricao.value,
            data_hora_inicio: data_hora_inicio.value,
            data_hora_fim: data_hora_fim.value,
            situacao: situacao.value
        }).then(() => {
            listarTarefas();
            tarefaForm.reset();
            tarefaId.value = '';
        });
    }
});

function listarTarefas() {
    axios.get(apiUrl).then((response) => {
        const tarefas = response.data;
        tarefasDiv.innerHTML = '';

        for (const tarefa of tarefas) {
            const tarefaElement = document.createElement('div');
            tarefaElement.classList.add('tarefa');
            tarefaElement.innerHTML = `
                <h3>${tarefa.titulo}</h3>
                <p>${tarefa.descricao}</p>
                <p>Início: ${tarefa.data_hora_inicio}</p>
                <p>Fim: ${tarefa.data_hora_fim}</p>
                <p>Situação: ${tarefa.situacao}</p>
                <button onclick="editarTarefa(${tarefa.id})">Editar</button>
                <button onclick="excluirTarefa(${tarefa.id})">Excluir</button>
            `;
            tarefasDiv.appendChild(tarefaElement);
        }
    });
}

function editarTarefa(id) {
    axios.get(`${apiUrl}/${id}`).then((response) => {
        const tarefa = response.data;
        tarefaId.value = tarefa.id;
        titulo.value = tarefa.titulo;
        descricao.value = tarefa.descricao;
        data_hora_inicio.value = tarefa.data_hora_inicio;
        data_hora_fim.value = tarefa.data_hora_fim;
        situacao.value = tarefa.situacao;
    });
}

function excluirTarefa(id) {
    axios.delete(`${apiUrl}/${id}`).then(() => {
        listarTarefas();
    });
}

listarTarefas();

