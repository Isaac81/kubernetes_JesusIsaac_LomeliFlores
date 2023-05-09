from fastapi import APIRouter, HTTPException
from schemas import LibroResponseModel
from data.datos import retornoDatos

router = APIRouter(
    prefix = "/libros",
    tags = ['libros']
)

@router.get('/')
async def obtener_libros():
    return retornoDatos()


@router.get('/{id}')
async def obtener_libro(id: int):
    lista = retornoDatos()
    return lista[id - 1]


@router.get('/unidades/{unidades}')
async def obtener_libro(unidades: float):
    lista = retornoDatos()
    coincidentes = []
    for i in lista:
        if i["unidades"] <= unidades:
            coincidentes.append(i)
    return coincidentes

