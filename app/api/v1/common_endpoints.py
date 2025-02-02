from fastapi import APIRouter, HTTPException
from app.schemas.sample import StatusReq
from app.services.sample_service.sample import Sample1, Sample2


router = APIRouter()


@router.get("/",
            summary="Hello World",
            description="Hello Worldです。疎通確認に使用してください。")
def home_hello_world():
    return {"message": "Hello World"}


@router.get("/sample/1",
            summary="get sample",
            description="servicesのクラスを使用するサンプル")
def sampole_1():
    sample_1 = Sample1()
    return {"message": sample_1.do("test")}


@router.post("/sample/2",
             summary="post sample",
             description="schemasとservicesのクラスとloggerを使用するサンプル")
def sampole_2(request: StatusReq):
    # validation
    if request.user == "a":
        raise HTTPException(status_code=404, detail="User not found")

    # main
    sampleservice = Sample2()
    sampleservice.do(request)

    # respponse
    if sampleservice.result:
        return sampleservice.response
    else:
        raise HTTPException(
            status_code=sampleservice.status_code,
            detail=sampleservice.detail
        )
