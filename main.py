from typing import List
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
    id: str
    nome: str
    caracteristicas: str

class CategoriaUpdateDTO(BaseModel):
    nome:str
    caracteristicas: str

class Produto(BaseModel):
    nome: str
    categoria:Categoria
    preço: float
    quantidade: int

class Fornecedor(BaseModel):
    nome: str
    cnpj: str
    itens_a_venda: List[Produto]
    valor_vendido: float

class FornecedorUpdateDTO(BaseModel):
    nome:str
    itens_a_venda: List[Produto]
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

@app.post('/fornecedores', status_code=status.HTTP_201_CREATED)
def cadastras_fornecedores(fornecedor: Fornecedor = Body(...)):
    fornecedores.append(fornecedor)

@app.get('/fornecedores')
def busca_fornecedores():
    return fornecedores

@app.get('/fornecedores/{cnpj}')
def busca_fornecedores_cnpj(cnpj:str):
    resultado = list(filter(lambda a: a.cnpj == cnpj, fornecedores))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe fornecedor com o cnpj {cnpj}')
    return resultado[0]

@app.delete('/fornecedores/{cnpj}')
def deleta_compradores(cnpj: str):
    resultado = list(filter(lambda a: a[1].cnpj == cnpj, enumerate(compradores)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe fornecedor com o cnpj {cnpj}')
    i, _ = resultado[0]
    del fornecedores[i]

@app.put('/fonecedores/{cnpj}')
def altera_fornecedores(cnpj: str, fornecedor_update_dto: FornecedorUpdateDTO = Body(...)):
    resultado = list(filter(lambda a: a[1].cnpj == cnpj, enumerate(fornecedores)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe fornecedor com o cnpj {cnpj}')
    i, _ = resultado[0]
    fornecedores[i].nome = fornecedor_update_dto.nome
    fornecedores[i].itens_a_venda = fornecedor_update_dto.itens_a_venda
    fornecedores[i].valor_vendido = fornecedor_update_dto.valor_vendido
    return fornecedores[i]

@app.get('/categorias')
def busca_categorias():
    return categorias

@app.post('/categoria')
def cadastrar_categoria(categoria: Categoria = Body(...)):
    categorias.append(categoria)

@app.get('/categorias/{id}')
def busca_categorias(id: str):
    resultado = list(filter(lambda a:a.id == id, categorias))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe categoria com o id {id}')
    return resultado[0]

@app.delete('/categorias/{id}')
def deleta_categorias(id: str):
    resultado = list(filter(lambda a:a[1].id == id, enumerate(categorias)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe categoria com o id {id}')
    i,_ = resultado[0]
    del categorias[i]

@app.put('/categorias/{id}')
def altera_categoria(id: str, categoria_update_dto : CategoriaUpdateDTO = Body(...)):
    resultado = list(filter(lambda a:a[1].id == id, enumerate(categorias)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não existe categoria com o id {id}')
    i,_ = resultado[0]
    categorias[i].nome = categoria_update_dto.nome
    categorias[i].caracteristicas = categoria_update_dto.caracteristicas
    return categorias[i]
    
        