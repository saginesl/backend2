from fastapi import APIRouter,Query, Depends

router=APIRouter()


def check_name(name:str=Query(None)):
    if name:
        return name
    else:
        return 'Параметр отсутствует'

@router.get('/get_check')
async def check(name_p:str=Depends(check_name)):
    return {"name":name_p}