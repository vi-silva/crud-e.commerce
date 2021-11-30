from fastapi import FastAPI, status
from fastapi.params import Body, Header
from pydantic import BaseModel
from starlette.responses import Response
from fastapi.exceptions import HTTPException


app = FastAPI()

produtos = []
categorias = []
fornecedores = []
compradores = []

class Categoria(BaseModel):
    nome: str
    caracteristicas: str

class Produto(BaseModel):
    nome: str
    categoria:Categoria
    preço: float
    quantidade: int

class Fornecedor(BaseModel):
    nome: str
    cnpj: str
    itens_a_venda: int
    valor_vendido: float

class Comprador(BaseModel):
    nome: str
    cpf: str
    valor_comprado = 0.00
    endereco: str

class CompradorUpdateDTO(BaseModel):
    nome: str
    valor_comprado: float
    endereco: str

@app.post('/compradores', status_code = status.HTTP_201_CREATED)
def cadastrar_compradores(comprador: Comprador = Body(...)):
    compradores.append(comprador)

@app.get('/compradores', status_code = status.HTTP_200_OK)
def busca_compradores():
    return compradores

@app.get('/compradores/{cpf}')
def busca_compradores_cpf(cpf: str):
    resultado = list(filter(lambda a: a.cpf == cpf, compradores))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe comprador com o cpf {cpf}')
    return resultado[0]

@app.delete('/compradores/{cpf}')
def deleta_compradores(cpf: str):
    resultado = list(filter(lambda a: a[1].cpf == cpf, enumerate(compradores)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe comprador com o cpf {cpf}')
    i,*rest = resultado[0]
    del compradores[i]
    
@app.put('/compradores/{cpf}')
def altera_compradores(cpf: str, comprador_update_dto: CompradorUpdateDTO):
    resultado = list(filter(lambda a: a[1].cpf == cpf, enumerate(compradores)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe comprador com o cpf {cpf}')
    i,_ = resultado[0]
    compradores[i].nome = comprador_update_dto.nome
    compradores[i].valor_comprado = comprador_update_dto.valor_comprado
    compradores[i].endereco = comprador_update_dto.endereco
    return compradores[i]
