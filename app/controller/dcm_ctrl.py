# import io
# import json
# import os
# import shutil
# import tempfile
# from typing import List
# import zipfile
# from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
# from sqlalchemy.orm import Session
# from starlette import status
# from app.conf.db_config import DBConfig
# from app.controller.auth_ctrl import verify_user
# from app.models.api_model import SelectThumbnail
# from app.services.dcm_service import DcmService


# router = APIRouter()
# db = DBConfig()


# @router.get("/image", description="이미지를 가져오는 라우트")
# async def get_dcm_image(filepath: str, filename: str, index: int = 0, _=Depends(verify_user)):
#     '''
#         Depends는 Decorator
#     '''
#     image = DcmService.get_dcm_img(filepath, filename, index)
#     if not image:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Patients not found"
#         )
#     return StreamingResponse(image, media_type="image/png", status_code=status.HTTP_200_OK)


# @router.get("/image/compressed", description="이미지를 압축해서 가져오는 라우트")
# async def get_dcm_image(studykey: str, serieskey: str, db: Session = Depends(db.get_db),  _=Depends(verify_user)):
#     '''
    
#     '''
#     images = await DcmService.get_dcm_img_compressed(studykey, serieskey, db)
#     if not images:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="images not found"
#         )
#     # 고유한 임시 디렉토리 생성
#     temp_dir = tempfile.mkdtemp()
#     print(temp_dir)

#     # 이미지를 임시 디렉토리에 저장
#     for i, img in enumerate(images):
#         img_data = img.getvalue() if isinstance(img, io.BytesIO) else img
#         ### 1월 15일   ||   f"image_{i}.png") =>  f"{STUDYKEY}_{SERIESKEY}_{IMAGEKEY}.png" 로 수정
#         ### EX) 1_1_1.png, 1_1_2.png ....
#         with open(os.path.join(temp_dir, f"{studykey}_{serieskey}_{i}.png"), 'wb') as f: 
#             f.write(img_data)
#             # print(IMAGEKEY)

#             ### 1월 15일 || f"image_{i}.png") =>  f"{STUDYKEY}_{SERIESKEY}_{IMAGEKEY}.png" 로 수정시 서버에서 잘못된 인자로 파일을 던져주는 것을 확인
#             ### IMAGEKEY를 참조하도록 만들어야 하는데 그게 현재 안되는 상황.

#     # zip 파일명을 고유하게 설정
#     zip_filename = os.path.join(temp_dir, f'{studykey}.{serieskey}.zip')

#     # zip 파일 생성
#     zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
#     for root, dirs, files in os.walk(temp_dir):
#         for file in files:
#             if file != f'{studykey}.{serieskey}.zip':  # 'filename.zip' 파일은 제외하고 압축
#                 # arcname을 추가하여 상대 경로만 압축에 포함
#                 zipf.write(os.path.join(root, file), arcname=file)
#     zipf.close()

#     # 파일 전송이 완료된 후에 호출될 콜백 함수 정의
#     def delete_temp_dir():
#         shutil.rmtree(temp_dir)

#     # 파일 스트림을 반환하고, 파일 전송이 완료된 후에 콜백 함수 호출
#     return FileResponse(
#         zip_filename,
#         media_type="application/zip",
#         headers={
#             "Content-Disposition": f"attachment;filename={studykey}.{serieskey}.zip"},
#         filename="images.zip",
#         background=BackgroundTasks().add_task(delete_temp_dir)
#     )


# @router.get("/image/windows", description="윈도우 조정된 이미지들을 가져오는 라우트")
# async def get_dcm_image(filepath: str, filename: str, index: int = 0, _=Depends(verify_user)):
#     images = DcmService.get_dcm_images_windowCenter(filepath, filename, index)
#     if not images:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Patients not found"
#         )
#     # 고유한 임시 디렉토리 생성
#     temp_dir = tempfile.mkdtemp()

#     # 이미지를 임시 디렉토리에 저장
#     for i, img in enumerate(images):
#         with open(os.path.join(temp_dir, f"image_{i}.png"), 'wb') as f:
#             f.write(img)

#     # zip 파일명을 고유하게 설정
#     zip_filename = os.path.join(temp_dir, f'{filename}.{index}.zip')

#     # zip 파일 생성
#     zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
#     for root, dirs, files in os.walk(temp_dir):
#         for file in files:
#             if file != f'{filename}.{index}.zip':  # 'filename.zip' 파일은 제외하고 압축
#                 # arcname을 추가하여 상대 경로만 압축에 포함
#                 zipf.write(os.path.join(root, file), arcname=file)
#     zipf.close()

#     # 파일 전송이 완료된 후에 호출될 콜백 함수 정의
#     def delete_temp_dir():
#         shutil.rmtree(temp_dir)

#     # 파일 스트림을 반환하고, 파일 전송이 완료된 후에 콜백 함수 호출
#     return FileResponse(
#         zip_filename,
#         media_type="application/zip",
#         headers={
#             "Content-Disposition": f"attachment;filename={filename}.{index}.zip"},
#         filename="images.zip",
#         background=BackgroundTasks().add_task(delete_temp_dir)
#     )


# @router.get("/thumbnails", response_model=List[SelectThumbnail], description="썸네일을 위한 라우트")
# async def get_thumbnail(studykey: int, db: Session = Depends(db.get_db), _=Depends(verify_user)):
#     results = []
#     thumbnails = await DcmService.get_seriestab_all_studykey(studykey, db)
#     if not thumbnails:
#         raise HTTPException(status_code=404, detail="Can't find thumbnail")
#     for thumbnail in thumbnails:
#         jsondata = DcmService.get_dcm_json(filepath=thumbnail.PATH,
#                                            filename=thumbnail.FNAME)
#         json_dcm = json.loads(jsondata)
#         if "Image Comments" in json_dcm:
#             SCORE = json_dcm["Image Comments"]
#         else:
#             SCORE = None
#         result_by_one = SelectThumbnail(
#             SERIESKEY=thumbnail.SERIESKEY,
#             SERIESDESC=thumbnail.SERIESDESC,
#             SCORE=SCORE,
#             IMAGECNT=thumbnail.IMAGECNT,
#             PATH=thumbnail.PATH,
#             FNAME=thumbnail.FNAME,
#             HEADERS=json.dumps(json_dcm)
#         ).dict()
#         results.append(result_by_one)
#     return JSONResponse(content=results, status_code=status.HTTP_200_OK)


# @router.get("/details", description="시리즈에서 이미지랑 모든 Header가져오기")
# async def get_details(studykey: int, serieskey: int, db: Session = Depends(db.get_db), _=Depends(verify_user)):
#     result = await DcmService.get_seriestab_one(studykey=studykey, serieskey=serieskey, db=db)
#     json_data = DcmService.get_dcm_json(filepath=result[0].PATH,
#                                         filename=result[0].FNAME)
#     result_json = json.loads(json_data)
#     result = jsonable_encoder(result)
#     result_json['result'] = result
#     return JSONResponse(content=result_json, status_code=status.HTTP_200_OK)


# #### STUDYKEY별 압축 ####
# @router.get("/image/zip", description="StudyKey별 이미지들을 압축후 zip파일로 반환")
# async def get_dcm_studykeyimages_zip(studykey: int, db: Session=Depends(db.get_db), _=Depends(verify_user)):
#     try:
#         zip_data = await DcmService.get_study_images_zip(studykey,db)
#         return StreamingResponse(io.BytesIO(zip_data), 
#                                 media_type="application/zip", 
#                                 headers={"Content-Disposition":f"attachment; filename={studykey}_images.zip"})
#     except Exception as e:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error:{e}")

import io
import json
import os
import shutil
import tempfile
from typing import List, Tuple
import zipfile
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from sqlalchemy.orm import Session
from starlette import status
from app.conf.db_config import DBConfig
from app.controller.auth_ctrl import verify_user
from app.models.api_model import SelectThumbnail
from app.services.dcm_service import DcmService
from app.util.dcm_gen import ConvertDCM
from pathlib import Path
from fastapi.responses import FileResponse


router = APIRouter()
db = DBConfig()


@router.get("/image", description="이미지를 가져오는 라우트")
async def get_dcm_image(filepath: str, filename: str, index: int = 0, _=Depends(verify_user)):
    '''
        Depends는 Decorator
    '''
    image = DcmService.get_dcm_img(filepath, filename, index)
    # count_images_in_dicom(image.filename)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patients not found"
        )
    return StreamingResponse(image, media_type="image/png", status_code=status.HTTP_200_OK)


@router.get("/image/compressed", description="이미지를 압축해서 가져오는 라우트")
async def get_dcm_image(studykey: str, serieskey: str, db: Session = Depends(db.get_db),  _=Depends(verify_user)):
    '''
    
    '''
    images = await DcmService.get_dcm_img_compressed(studykey, serieskey, db)
    if not images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="images not found"
        )
    # 고유한 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()
    print(temp_dir)

    # 이미지를 임시 디렉토리에 저장
    for i, img in enumerate(images):
        img_data = img.getvalue() if isinstance(img, io.BytesIO) else img
        ### 1월 15일   ||   f"image_{i}.png") =>  f"{STUDYKEY}_{SERIESKEY}_{IMAGEKEY}.png" 로 수정
        ### EX) 1_1_1.png, 1_1_2.png ....
        with open(os.path.join(temp_dir, f"{studykey}_{serieskey}_{i}.png"), 'wb') as f: 
            f.write(img_data)
            # print(IMAGEKEY)

            ### 1월 15일 || f"image_{i}.png") =>  f"{STUDYKEY}_{SERIESKEY}_{IMAGEKEY}.png" 로 수정시 서버에서 잘못된 인자로 파일을 던져주는 것을 확인
            ### IMAGEKEY를 참조하도록 만들어야 하는데 그게 현재 안되는 상황.

    # zip 파일명을 고유하게 설정
    zip_filename = os.path.join(temp_dir, f'{studykey}.{serieskey}.zip')

    # zip 파일 생성
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file != f'{studykey}.{serieskey}.zip':  # 'filename.zip' 파일은 제외하고 압축
                # arcname을 추가하여 상대 경로만 압축에 포함
                zipf.write(os.path.join(root, file), arcname=file)
    zipf.close()

    # 파일 전송이 완료된 후에 호출될 콜백 함수 정의
    def delete_temp_dir():
        shutil.rmtree(temp_dir)

    # 파일 스트림을 반환하고, 파일 전송이 완료된 후에 콜백 함수 호출
    return FileResponse(
        zip_filename,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment;filename={studykey}.{serieskey}.zip"},
        filename="images.zip",
        background=BackgroundTasks().add_task(delete_temp_dir)
    )
# '''
#     0116_2004 get_dcm_img_compressed_STUDYKEY함수 라우터
#     0117에 router만들어서 TEST필요.
# '''
# @router.get("/image/compressed/study/{studykey}", description="STUDYKEY별로 압축해서 이미지를 가져오는 route")
# async def get_dcm_image_compressed_STUDYKEY(studykey: int, db:Session = Depends(db.get_db)):
#     try: 
#         return await DcmService.get_dcm_img_compressed_STUDYKEY(studykey,db)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Internal Server Error:{str(e)}")


@router.get("/image/windows", description="윈도우 조정된 이미지들을 가져오는 라우트")
async def get_dcm_image(filepath: str, filename: str, index: int = 0, _=Depends(verify_user)):
    images = DcmService.get_dcm_images_windowCenter(filepath, filename, index)
    if not images:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patients not found"
        )
    # 고유한 임시 디렉토리 생성
    temp_dir = tempfile.mkdtemp()

    # 이미지를 임시 디렉토리에 저장
    for i, img in enumerate(images):
        with open(os.path.join(temp_dir, f"image_{i}.png"), 'wb') as f:
            f.write(img)

    # zip 파일명을 고유하게 설정
    zip_filename = os.path.join(temp_dir, f'{filename}.{index}.zip')

    # zip 파일 생성
    zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(temp_dir):
        for file in files:
            if file != f'{filename}.{index}.zip':  # 'filename.zip' 파일은 제외하고 압축
                # arcname을 추가하여 상대 경로만 압축에 포함
                zipf.write(os.path.join(root, file), arcname=file)
    zipf.close()

    # 파일 전송이 완료된 후에 호출될 콜백 함수 정의
    def delete_temp_dir():
        shutil.rmtree(temp_dir)

    # 파일 스트림을 반환하고, 파일 전송이 완료된 후에 콜백 함수 호출
    return FileResponse(
        zip_filename,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment;filename={filename}.{index}.zip"},
        filename="images.zip",
        background=BackgroundTasks().add_task(delete_temp_dir)
    )





@router.get("/thumbnails", response_model=List[SelectThumbnail], description="썸네일을 위한 라우트")
async def get_thumbnail(studykey: int, db: Session = Depends(db.get_db), _=Depends(verify_user)):
    results = []
    thumbnails = await DcmService.get_seriestab_all_studykey(studykey, db)
    if not thumbnails:
        raise HTTPException(status_code=404, detail="Can't find thumbnail")
    for thumbnail in thumbnails:
        jsondata = DcmService.get_dcm_json(filepath=thumbnail.PATH,
                                           filename=thumbnail.FNAME)
        json_dcm = json.loads(jsondata)
        if "Image Comments" in json_dcm:
            SCORE = json_dcm["Image Comments"]
        else:
            SCORE = None
        result_by_one = SelectThumbnail(
            SERIESKEY=thumbnail.SERIESKEY,
            SERIESDESC=thumbnail.SERIESDESC,
            SCORE=SCORE,
            IMAGECNT=thumbnail.IMAGECNT,
            PATH=thumbnail.PATH,
            FNAME=thumbnail.FNAME,
            HEADERS=json.dumps(json_dcm)
        ).dict()
        results.append(result_by_one)
    return JSONResponse(content=results, status_code=status.HTTP_200_OK)


@router.get("/details", description="시리즈에서 이미지랑 모든 Header가져오기")
async def get_details(studykey: int, serieskey: int, db: Session = Depends(db.get_db), _=Depends(verify_user)):
    result = await DcmService.get_seriestab_one(studykey=studykey, serieskey=serieskey, db=db)
    json_data = DcmService.get_dcm_json(filepath=result[0].PATH,
                                        filename=result[0].FNAME)
    result_json = json.loads(json_data)
    result = jsonable_encoder(result)
    result_json['result'] = result
    return JSONResponse(content=result_json, status_code=status.HTTP_200_OK)


#1월 18일 추가
@router.get("/images/return", description="StudyKey 별 이미지들을 압축한 후 zip 파일로 반환")
async def get_study_images_zip(studykey: int, db: Session = Depends(db.get_db), _=Depends(verify_user)):
    try:
        zip_data = await DcmService.get_study_images_zip(studykey, db)
        return StreamingResponse(io.BytesIO(zip_data), media_type="application/zip", headers={"Content-Disposition": f"attachment; filename={studykey}_images.zip"})
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")


#1월 25일 추가
@router.get("/images/study", description="Studykey1개. StudyKey 별 이미지들을 압축한 후 zip 파일로 server에 저장.")
async def get_study_images_zip(studykey: int, db: Session = Depends(db.get_db), _=Depends(verify_user)):
    try:
        # 디렉토리 경로 설정
        zip_dir = "./app/images/studykeyZips"
        print(zip_dir)
        os.makedirs(zip_dir, exist_ok=True)
        # zip 파일 경로 설정
        zip_filename = f"{studykey}_images.zip"
        zip_path = os.path.join(zip_dir, zip_filename)

        if os.path.exists(zip_path):
            return {"zip_path": zip_path}
        # zip 파일 생성
        zip_data = await DcmService.get_study_images_zip_twentyFive(studykey, db, zip_dir=zip_dir)
        # zip 파일을 서버에 저장
        with open(zip_path, "wb") as zip_file:
            zip_file.write(zip_data)
        # 클라이언트에게는 파일의 경로를 반환
        return {"zip_path": zip_path}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")

@router.get("/images/save", description="Studykey전부. StudyKey 별 이미지들을 압축한 후 zip 파일로 server에 저장")
async def get_study_images_zip_all(db: Session = Depends(db.get_db), _=Depends(verify_user)):
    try:
        # 디렉토리 경로 설정
        zip_dir = "./app/images/studykeyZips"
        os.makedirs(zip_dir, exist_ok=True)

        # StudyKey 전체 리스트
        all_studykeys = [1, 2, 3, 4, 5, 6, 8, 9, 12, 14, 15, 16, 17, 18, 19, 20, 21, 24]

        # 각 StudyKey에 대해 처리
        for studykey in all_studykeys:
            # zip 파일 경로 설정
            zip_filename = f"{studykey}_images.zip"
            zip_path = os.path.join(zip_dir, zip_filename)

            # 이미 zip 파일이 존재하는지 확인
            if os.path.exists(zip_path):
                # 이미 존재하는 경우 기존 파일의 경로를 반환
                print(f"Zip file for StudyKey {studykey} already exists.")
            else:
                # zip 파일 생성
                zip_data = await DcmService.get_study_images_zip_twentyFive(studykey, db, zip_dir=zip_dir)

                # zip 파일을 서버에 저장
                with open(zip_path, "wb") as zip_file:
                    zip_file.write(zip_data)
                
                print(f"Zip file for StudyKey {studykey} created and saved at {zip_path}")

        # 클라이언트에게는 파일의 경로를 반환
        return {"message": "Zip files for all StudyKeys created and saved."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Internal Server Error: {e}")

#1월 25일 추가
@router.get("/images/{studykey}",
    description="특정 StudyKey에 대한 zip 파일을 클라이언트에게 반환\n[1,2,3,4,6,8,12,14,15,18,19,24만 가능]")
async def retrieve_study_zip(studykey: str, db: Session = Depends(db.get_db), _=Depends(verify_user)):
    try:
        # 저장된 디렉토리 설정
        zip_dir = "./app/images/studykeyZips"
        # 파일 경로 설정
        zip_path = Path(zip_dir)/f"{studykey}_images.zip"
        print(f"zip_path = {zip_path}")
        # 파일이 존재하는지 확인
        if not zip_path.exists() or not zip_path.is_file():
            raise HTTPException(status_code=404, detail="Zip file not found.")
        # 클라이언트에게 zip 파일을 반환
        return FileResponse(zip_path, media_type="application/zip", filename = f"{studykey}_images.zip")
    except Exception as e:
        print(f"Error : {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# #1월 26일 추가
# @router.get("/images/onlyZip_{studykey}", description="특정스터디키에 대한 ZIP 반환")
# async def retrieve_zip_for_studykey(studykey: str):
#     try:
#         zip_dir = ".\images\studykey"
#     except:


'''
trouble1 : (16,17,20,21)
     =문제는 'FileDataset' object has no attribute 'WindowWidth'

trouble2 : (5, 9)
     =문제는 image가 정상적으로 출력되지 않는 문제. 가운데 화면이 뻥뚫림.
solution : ipynb에서 테스트로 해당 dcm을 정상적으로 출력할 수 있도록 해보자.
touble5 =문제는 배열?

toruble3 : studykey 16번 진행시 divide 0 발생.
나누기 0이 뜨는 곳?

trouble4 : studykey별 이미지 압축을 하는 동안 다른 작업을 하지 못한다. 압축하는동안 다른 작업도 되게 하려면 async를 붙이면 되는줄 알았는데 아닌가? => 비동기 처리에 대해 더 알아보자.
all_studykeys = [1, 2, 3, 4, 5, 6, 8, 9, 12, 14, 15, 16, 17, 18, 19, 20, 21, 24]
                [1, 2, 3, 4, 6, 8, 12 ,14, 15 ,18 ,19, 24만 가능]

'''
