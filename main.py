from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from typing import List
from pydantic import BaseModel
import sqlite3
import uvicorn
import os

app = FastAPI()

# Configurar CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar o diretório de arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")


class Tarefa(BaseModel):
    id: int
    titulo: str
    descricao: str
    data_hora_inicio: str
    data_hora_fim: str
    situacao: str


# Criar conexão e tabela no banco de dados
def create_table():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY,
            titulo TEXT NOT NULL,
            descricao TEXT NOT NULL,
            data_hora_inicio TEXT NOT NULL,
            data_hora_fim TEXT NOT NULL,
            situacao TEXT NOT NULL
        );
    """
    )

    conn.commit()
    conn.close()


create_table()

# Servir a página inicial
@app.get("/", include_in_schema=False)
async def root():
    with open(os.path.join("static", "index.html"), mode="r", encoding="utf-8") as f:
        content = f.read()
    return Response(content, media_type="text/html")


# Listar tarefas
@app.get("/tarefas", response_model=List[Tarefa])
def listar_tarefas():
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tarefas")

    tarefas = cursor.fetchall()
    conn.close()

    return [
        {
            "id": t[0],
            "titulo": t[1],
            "descricao": t[2],
            "data_hora_inicio": t[3],
            "data_hora_fim": t[4],
            "situacao": t[5],
        }
        for t in tarefas
    ]


# Obter Tarefa
@app.get("/tarefas/{tarefa_id}", response_model=Tarefa)
def obter_tarefa(tarefa_id: int):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tarefas WHERE id = ?", (tarefa_id,))

    t = cursor.fetchone()
    conn.close()
    tarefa = {
        "id": t[0],
        "titulo": t[1],
        "descricao": t[2],
        "data_hora_inicio": t[3],
        "data_hora_fim": t[4],
        "situacao": t[5],
    }
    return tarefa
    

# Inserir tarefa
@app.post("/tarefas", response_model=Tarefa)
def inserir_tarefa(tarefa: Tarefa):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tarefas (titulo, descricao, data_hora_inicio, data_hora_fim, situacao) VALUES (?, ?, ?, ?, ?)
    """,
        (
            tarefa.titulo,
            tarefa.descricao,
            tarefa.data_hora_inicio,
            tarefa.data_hora_fim,
            tarefa.situacao,
        ),
    )

    conn.commit()
    tarefa.id = cursor.lastrowid
    conn.close()

    return tarefa


# Alterar tarefa
@app.put("/tarefas/{tarefa_id}", response_model=Tarefa)
def alterar_tarefa(tarefa_id: int, tarefa: Tarefa):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE tarefas SET titulo = ?, descricao = ?, data_hora_inicio = ?, data_hora_fim = ?, situacao = ? WHERE id = ?
    """,
        (
            tarefa.titulo,
            tarefa.descricao,
            tarefa.data_hora_inicio,
            tarefa.data_hora_fim,
            tarefa.situacao,
            tarefa_id,
        ),
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return tarefa


# Excluir tarefa
@app.delete("/tarefas/{tarefa_id}")
def excluir_tarefa(tarefa_id: int):
    conn = sqlite3.connect("tarefas.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id = ?", (tarefa_id,))

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")

    return {"message": "Tarefa excluída com sucesso"}


uvicorn.run(app, host="127.0.0.1", port=8000)
