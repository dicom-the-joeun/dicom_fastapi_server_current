# import json
# import os
# import io
# import shutil
# import tempfile
# import zipfile

# from fastapi import BackgroundTasks
# from fastapi.responses import FileResponse
# from app.conf.ftp_config import FTPConfig
# from app.models.api_model import SelectSereies, SelectThumbnail
# from app.models.db_model import ImageViewTab, SeriesTab
# from app.util.dcm_gen import ConvertDCM
# from typing import List
# ftp = FTPConfig()
# #1월 17일 추가
# # from app.services.dcm_service import DcmService


# class DcmService:
#     @staticmethod
#     def get_dcm_json(filepath, filename):
#         conv = ConvertDCM()
#         try:
#             ftp.connect()
#             data = ftp.getdata(filepath=filepath, filename=filename)
#         except Exception as e:
#             print(f'문제는 {e}')
#         finally:
#             ftp.disconnect()
#             return conv.dicomToJSON(data)

#     @staticmethod
#     def get_dcm_img(filepath, filename, index=0):
#         conv = ConvertDCM()
#         try:
#             ftp.connect()
#             data = ftp.getdata(filepath=filepath, filename=filename)
#         except Exception as e:
#             print(f'문제는 {e}')
#         finally:
#             ftp.disconnect()
#             return conv.dicomToPNG(data, index)

#     @staticmethod
#     async def get_dcm_img_compressed(studykey, serieskey, db): 
#         '''
#             이미지들을 반환해야함.
#             @return : images `list`

#             TODO: 3차원 4차원 예외 처리 필요!
#         '''
#         conv = ConvertDCM()
#         images = []
#         result = await DcmService.get_seriestab_one(studykey, serieskey, db)
#         json_data =  json.loads(DcmService.get_dcm_json(filepath=result[0].PATH,
#                                       filename=result[0].FNAME))
#         print("jsondata", json_data)
#         print(json_data["pixel array shape"])
#         if json_data["pixel array shape"] == "2":
#             try:
#                 ftp.connect()
#                 for one_result in result:
#                     data = ftp.getdata(one_result.PATH, one_result.FNAME)
#                     images.append(conv.dicomToPNG(data, 0))
#             except Exception as e:
#                 print(f'문제는 {e}')
#             finally:
#                 ftp.disconnect()
#             return images

#     @staticmethod
#     def get_dcm_images_windowCenter(filepath, filename, index=0):
#         conv = ConvertDCM()
#         images = []
#         try:
#             ftp.connect()
#             data = ftp.getdata(filepath=filepath, filename=filename)
#             images = conv.dicomToPNGs_windows(data, index)
#         except Exception as e:
#             print(f'문제는 {e}')
#         finally:
#             ftp.disconnect()
#         return images

#     @staticmethod
#     async def get_seriestab_all_studykey(studykey, db) -> List[SelectThumbnail]:
#         thumbnails = db.query(SeriesTab).filter(
#             SeriesTab.STUDYKEY == studykey).all()
#         return thumbnails

#     @staticmethod
#     async def get_seriestab_one(studykey, serieskey, db) -> List[SelectSereies]:
#         image_fname_all = db.query(ImageViewTab.IMAGEKEY, ImageViewTab.PATH, ImageViewTab.FNAME).filter(
#             ImageViewTab.STUDYKEY == studykey, ImageViewTab.SERIESKEY == serieskey).all()
#         return [SelectSereies(IMAGEKEY=row.IMAGEKEY, PATH=row.PATH, FNAME=row.FNAME) for row in image_fname_all]

#     # # studykey별 압축 ##############################
#     # @staticmethod
#     # async def get_dcm_studykeyimages_zip(studykey, db) -> bytes:
#     #     conv = ConvertDCM()
#     #     images = []
#     #     result = await DcmService.get_seriestab_all_studykey(studykey, db)

#     #     try:
#     #         ftp.connect()

#     #         # 고유임시디렉토리 생성
#     #         temp_dir = tempfile.mkdtemp()

#     #         for one_result in result:
#     #             series_images = await DcmService.get_seriestab_one(studykey, one_result.SERIESKEY, db)
#     #             print(f"studykey = {studykey}")

#     #             # #별 의미 없는 작업 수정필요
#     #             # series_images.sort(key=lambda x: x.IMAGEKEY)

#     #             for image_info in series_images:
#     #                 print(f"serieskey = {one_result.SERIESKEY}")
#     #                 data = ftp.getdata(image_info.PATH, image_info.FNAME)
#     #                 # img_data = conv.dicomToPNG(data, 0)
                    
#     #                 i=0
#     #                 for img_data, window_center in zip(*conv.dicomToPNGs_windows(data,0)):
#     #                     i = i+1
#     #                     image_key = image_info.IMAGEKEY
#     #                     filename = f"{studykey}_{one_result.SERIESKEY}_{image_key}_{i}_{window_center}.png"

#     #                     # 이미지를 임시 디렉토리에 저장
#     #                     with open(os.path.join(temp_dir, filename), 'wb') as f:
#     #                         f.write(img_data)

#     #         # zip 파일명 설정
#     #         zip_filename = os.path.join(temp_dir, f"{studykey}_images.zip")

#     #         # zip파일 생성 
#     #         zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
#     #         for root, dirs, files in os.walk(temp_dir):
#     #             for file in files:
#     #                 if file != f'{studykey}_images.zip':
#     #                     zipf.write(os.path.join(root, file), arcname=file)
#     #         zip.close()

#     #         # zip파일 데이터 읽기
#     #         with open(zip_filename, 'rb') as zip_file:
#     #             zip_data = zip_file.read()

#     #         return zip_data

#     #     except Exception as e:
#     #         print(f"발생한 문제 :{e}")
#     #     finally:
#     #         ftp.disconnect()
#     #         shutil.rmtree(temp_dir)
# # 1월 18일 생성
#     @staticmethod
#     async def get_study_images_zip(studykey, db) -> bytes:
#         conv = ConvertDCM()
#         images = []
#         result = await DcmService.get_seriestab_all_studykey(studykey, db)

#         try:
#             ftp.connect()

#             # 고유한 임시 디렉토리 생성
#             temp_dir = tempfile.mkdtemp()

#             for one_result in result:
#                 series_images = await DcmService.get_seriestab_one(studykey, one_result.SERIESKEY, db)
#                 print(f"studykey = {studykey}")

#                 for image_info in series_images:
#                     print(f"serieskey = {one_result.SERIESKEY}")
#                     data = ftp.getdata(image_info.PATH, image_info.FNAME)

#                     i = 0
#                     for img_data, window_center in zip(*conv.dicomToPNGs_windows(data, 0)):
#                         i = i+1
#                         image_key = image_info.IMAGEKEY
#                         filename = f"{studykey}_{one_result.SERIESKEY}_{image_key}_{i}_{window_center}.png"


#                         # 이미지를 임시 디렉토리에 저장
#                         with open(os.path.join(temp_dir, filename), 'wb') as f:
#                             f.write(img_data)  # BytesIO에서 데이터를 가져와야 합니다.

#             # zip 파일명을 고유하게 설정
#             zip_filename = os.path.join(temp_dir, f'{studykey}_images.zip')

#             # zip 파일 생성
#             zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
#             for root, dirs, files in os.walk(temp_dir):
#                 for file in files:
#                     if file != f'{studykey}_images.zip':  # 'filename.zip' 파일은 제외하고 압축
#                         # arcname을 추가하여 상대 경로만 압축에 포함
#                         zipf.write(os.path.join(root, file), arcname=file)
#             zipf.close()

#             # zip 파일 데이터 읽기
#             with open(zip_filename, 'rb') as zip_file:
#                 zip_data = zip_file.read()

#             return zip_data

#         except Exception as e:
#             print(f'문제는 {e}')
#         finally:
#             ftp.disconnect()
#             shutil.rmtree(temp_dir)

import json
import os
import io
import shutil
import tempfile
import zipfile
from fastapi import BackgroundTasks

from fastapi.responses import FileResponse
from app.conf.ftp_config import FTPConfig
from app.models.api_model import SelectSereies, SelectThumbnail
from app.models.db_model import ImageViewTab, SeriesTab
from app.util.dcm_gen import ConvertDCM
from typing import List
ftp = FTPConfig()

class DcmService:
    @staticmethod
    def get_dcm_json(filepath, filename):
        conv = ConvertDCM()
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            return conv.dicomToJSON(data)

    @staticmethod
    def get_dcm_img(filepath, filename, index=0):
        conv = ConvertDCM()
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            return conv.dicomToPNG(data, index)

    @staticmethod
    async def get_dcm_img_compressed(studykey, serieskey, db): 
        '''
            이미지들을 반환해야함.
            @return : images `list`

            TODO: 3차원 4차원 예외 처리 필요!
        '''
        conv = ConvertDCM()
        images = []
        result = await DcmService.get_seriestab_one(studykey, serieskey, db)
        json_data =  json.loads(DcmService.get_dcm_json(filepath=result[0].PATH,
                                      filename=result[0].FNAME))
        print("jsondata", json_data)
        print(json_data["pixel array shape"])
        if json_data["pixel array shape"] == "2":
            try:
                ftp.connect()
                for one_result in result:
                    data = ftp.getdata(one_result.PATH, one_result.FNAME)
                    images.append(conv.dicomToPNG(data, 0))
            except Exception as e:
                print(f'문제는 {e}')
            finally:
                ftp.disconnect()
            return images
    '''
        이미지들을 반환할 때 IMAGEKEY를 추가하여 반환하도록 하는 함수를 만들어서 get_dcm_img_compressed함수를 대체해야함.
    '''
    # # 0116_2004 get_dcm_img_compressed_STUDYKEY함수 만들기 시작
    # @staticmethod
    # async def get_dcm_img_compressed_STUDYKEY(studykey, db):
    #     conv = ConvertDCM()
    #     images_by_study = (list)
    #     # get all series for study
    #     series_for_study = db.query(SeriesTab.STUDYKEY == studykey).all()

    #     for series in series_for_study:
    #         result = await DcmService.get_seriestab_one(studykey, series.STUDYKEY, db)
    #         #imagekey를 기준으로 정렬
    #         result.sort(key = lambda x : x.IMAGEKEY)

    #         for one_result in result:
    #             try:
    #                 ftp.connect()
    #                 data = ftp.getdata(one_result.PATH, one_result.FNAME)
    #                 images_by_study[studykey].append((one_result.IMAGEKEY, conv.dicomToPNG(data,0)))
    #             except Exception as e:
    #                 print(f"발생한 문제: {e}")
    #             finally:
    #                 ftp.disconnect()
    #     # image를 저장할 임시 디렉토리 생성
    #     temp_dir = tempfile.mkdtemp()

    #     # image를 temp_dir에 저장
    #     for study, images in images_by_study.items():
    #         for imagekey, img in images:
    #             img_data = img.getvalue() if isinstance(img, io.BytesIO) else img
    #             image_filename = f"{study}_{imagekey}.png"
    #             with open(os.path.join(temp_dir, image_filename),'wb') as f:
    #                 f.write(img_data)

    #     # zip 파일명 설정
    #     zip_filename = os.path.join(temp_dir, f'{studykey}_test.zip') #test빼면된다.
        
    #     # zip 파일 생성
    #     zipf = zipfile.ZipFile(zip_filename,'w',zipfile.ZIP_DEFLATED)
    #     for root, dirs, files in os.walk(temp_dir):
    #         for file in files:
    #             zipf.write(os.path.join(root.file), arcname = file)
    #     zipf.close()

    #     # 파일 전송이 완료된 후에 호출될 콜백 함수 정의
    #     def delete_temp_dir():
    #         shutil.rmtree(temp_dir)

    #     # 파일스트림 반환, 파일 전송 완료 후 콜백함수 호출
    #     return FileResponse(
    #         zip_filename,
    #         media_type = 'application/zip',
    #         headers = {
    #             "Content-Disposition": f"attachment;filename={studykey}.zip"
    #             },
    #             filename = "images.zip",
    #             background = BackgroundTasks().add_task(delete_temp_dir,temp_dir)    
            
    #     )


    ### get_dcm_img_compressed_STUDYKEY함수 END

    @staticmethod
    def get_dcm_images_windowCenter(filepath, filename, index=0):
        conv = ConvertDCM()
        images = []
        try:
            ftp.connect()
            data = ftp.getdata(filepath=filepath, filename=filename)
            images = conv.dicomToPNGs_windows(data, index)
        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
        return images

    @staticmethod
    async def get_seriestab_all_studykey(studykey, db) -> List[SelectThumbnail]:
        thumbnails = db.query(SeriesTab).filter(
            SeriesTab.STUDYKEY == studykey).all()
        return thumbnails

    @staticmethod
    async def get_seriestab_one(studykey, serieskey, db) -> List[SelectSereies]:
        image_fname_all = db.query(ImageViewTab.IMAGEKEY, ImageViewTab.PATH, ImageViewTab.FNAME).filter(
            ImageViewTab.STUDYKEY == studykey, ImageViewTab.SERIESKEY == serieskey).all()
        return [SelectSereies(IMAGEKEY=row.IMAGEKEY, PATH=row.PATH, FNAME=row.FNAME) for row in image_fname_all]
    


# 1월 18일 생성
    @staticmethod
    async def get_study_images_zip(studykey, db) -> bytes:
        conv = ConvertDCM()
        images = []
        result = await DcmService.get_seriestab_all_studykey(studykey, db)

        try:
            ftp.connect()

            # 고유한 임시 디렉토리 생성
            temp_dir = tempfile.mkdtemp()

            for one_result in result:
                series_images = await DcmService.get_seriestab_one(studykey, one_result.SERIESKEY, db)
                print(f"studykey = {studykey}")
                # image_info.IMAGEKEY를 기준으로 정렬
                # series_images.sort(key=lambda x: x.IMAGEKEY)

                for image_info in series_images:
                    # print(f"serieskey = {one_result.SERIESKEY}")
                    data = ftp.getdata(image_info.PATH, image_info.FNAME)


                    # img_data = conv.dicomToPNGs_windows(data, 0)


                    # for i, (img_data, window_center) in enumerate(conv.dicomToPNGs_windows(data,0)):
                    #     image_key = image_info.IMAGEKEY
                    #     filename = f"{studykey}_{one_result.SERIESKEY}_{image_key}_{i}.png"
                    # for i, img_data in enumerate(conv.dicomToPNGs_windows(data, 0)[0]):
                    #     window_center = conv.dicomToPNGs_windows(data, 0)[1][i]
                    #     image_key = image_info.IMAGEKEY
                    #     filename = f"{studykey}_{one_result.SERIESKEY}_{image_key}_{window_center}.png"
                    i = 0
                    for img_data, window_center in zip(*conv.dicomToPNGs_windows(data, 0)):
                        i = i+1
                        image_key = image_info.IMAGEKEY
                        filename = f"{studykey}_{one_result.SERIESKEY}_{image_key}_{i}.png"


                        # 이미지를 임시 디렉토리에 저장
                        with open(os.path.join(temp_dir, filename), 'wb') as f:
                            f.write(img_data)  # BytesIO에서 데이터를 가져와야 합니다.

            # zip 파일명을 고유하게 설정
            zip_filename = os.path.join(temp_dir, f'{studykey}_images.zip')

            # zip 파일 생성
            zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file != f'{studykey}_images.zip':  # 'filename.zip' 파일은 제외하고 압축
                        # arcname을 추가하여 상대 경로만 압축에 포함
                        zipf.write(os.path.join(root, file), arcname=file)
            zipf.close()

            # zip 파일 데이터 읽기
            with open(zip_filename, 'rb') as zip_file:
                zip_data = zip_file.read()

            return zip_data

        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
            shutil.rmtree(temp_dir)


# 0125
# All Study Key in dataTable : 1,2,3,4,5,6,8,9,12,14,15,16,17,18,19,20,21,24
    @staticmethod
    async def get_study_images_zip_twentyFive(studykey, db, zip_dir="./images/studykey_images_for_client") -> bytes:
        conv = ConvertDCM()
        images = []
        result = await DcmService.get_seriestab_all_studykey(studykey, db)

        try:
            ftp.connect()

            # 고유한 임시 디렉토리 생성
            temp_dir = tempfile.mkdtemp()

            for one_result in result:
                series_images = await DcmService.get_seriestab_one(studykey, one_result.SERIESKEY, db)
                print(f"studykey = {studykey}")
                # image_info.IMAGEKEY를 기준으로 정렬
                # series_images.sort(key=lambda x: x.IMAGEKEY)

                for image_info in series_images:
                    print(f"serieskey = {one_result.SERIESKEY}")
                    data = ftp.getdata(image_info.PATH, image_info.FNAME)
                    i = 0
                    for img_data, window_center in zip(*conv.dicomToPNGs_windows(data, 0)):
                        i = i+1
                        image_key = image_info.IMAGEKEY
                        filename = f"{studykey}_{one_result.SERIESKEY}_{image_key}_{i}.png"

                        # 이미지를 임시 디렉토리에 저장
                        with open(os.path.join(temp_dir, filename), 'wb') as f:
                            f.write(img_data)  # BytesIO에서 데이터를 가져와야 합니다.

            # zip 파일명을 고유하게 설정
            zip_filename = os.path.join(temp_dir, f'{studykey}_images.zip')

            # zip 파일 생성
            zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file != f'{studykey}_images.zip':  # 'filename.zip' 파일은 제외하고 압축
                        # arcname을 추가하여 상대 경로만 압축에 포함
                        zipf.write(os.path.join(root, file), arcname=file)
            zipf.close()

            # zip 파일 데이터 읽기
            with open(zip_filename, 'rb') as zip_file:
                zip_data = zip_file.read()

            return zip_data

        except Exception as e:
            print(f'문제는 {e}')
        finally:
            ftp.disconnect()
