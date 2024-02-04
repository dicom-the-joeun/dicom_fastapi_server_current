# '''
#     Convert Dicom
#     FTP -> binarydata -> ds -> toJSON
#     Description : FTP에서 받은 binary data -> ds로 JSON 직렬화
#     Author : Okrie, Oh-Kang94
#     Ver : 0.1
#     Site : https://github.com/Okrie/DicomToPng
#     Lisence : MIT
# '''

# from PIL import Image
# import numpy as np
# import pydicom
# import io
# import json
# import cv2


# class ConvertDCM:

#     def dicomToJSON(self, data):
#         info_list = ["Patient ID", "Patient's Name", "Patient's Birth Date", "Series Number", "Study Date", "Study Time", "Image Comments", "Series Description", "Number of Frames",
#                      "Manufacturer", "Manufacturer's Model Name", "Rows", "Columns", "Window Width", "Window Center", "Operator's Name"]
#         ds = pydicom.dcmread(io.BytesIO(data))
#         """
#         ### Front Info for list
#         @Params : fname -> SC 판단 후, Slice Score를 뱉어냄
#         """
#         result = {}
#         for elem in ds:
#             if elem.name in info_list:
#                 if elem.name == "Window Width":
#                     width_value = elem.value if elem.value is not None else 0
#                     result[elem.name] = str(width_value)
#                 elif elem.name == "Window Center" and elem.value is None:
#                     result[elem.name] = str(1)
#                 else:
#                     result[elem.name] = str(elem.value)
#         if "Number of Frames" not in result:
#             result["Number of Frames"] = str(1)
#         if len(ds.pixel_array.shape) == 4:
#             pixel_array_shape = 4
#         elif len(ds.pixel_array.shape) == 3:
#             pixel_array_shape = 3
#         else:
#             pixel_array_shape = 2
#         result['pixel array shape'] = str(pixel_array_shape)
#         return json.dumps(result)

#     def dicomToPNG(self, data, index=0):
#         ds = pydicom.dcmread(io.BytesIO(data))
#         if len(ds.pixel_array.shape) == 4:  # 4차원 배열인 경우
#             new_image = ds.pixel_array.astype(float)
#             new_image = np.reshape(
#                 ds.pixel_array[index, :, :, 0], (-1, ds.pixel_array.shape[2]))
#         elif len(ds.pixel_array.shape) == 3:  # 3차원 배열인 경우
#             new_image = ds.pixel_array[index].astype(float)
#         else:
#             new_image = ds.pixel_array.astype(float)
#         # normalization 작업
#         scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
#         scaled_image = np.uint8(scaled_image)
#         # 흑백 반전 작업
#         # scaled_image = 255 - scaled_image
#         img = Image.fromarray(scaled_image)
#         img_io = io.BytesIO()
#         img.save(img_io, 'PNG', quality=70)
#         img_io.seek(0)  # BytesIO의 커서를 처음으로 이동
#         return img_io

#     ########## 1월 22일 추가 MS
#     def dicomToPNGs_windows(self, data, index=0):
#         ds = pydicom.dcmread(io.BytesIO(data))
#         window_width = ds.WindowWidth

#         start_value = ds.WindowCenter - window_width / 2.0
#         end_value = ds.WindowCenter + window_width / 2.0

#         print(f"minValue = {start_value}")
#         print(f"maxValue = {end_value}")

#         # if len(ds.pixel_array.shape) == 4:
#         #     new_image = ds.pixel_array[index, :, :, 0]
#         # elif len(ds.pixel_array.shape) == 3:
#         #     new_image = ds.pixel_array[index]
#         # else:
#         #     new_image = ds.pixel_array
#         if len(ds.pixel_array.shape) == 4:
#             new_image = ds.pixel_array[index, :, :, 0]
#         elif len(ds.pixel_array.shape) == 3:
#             new_image = ds.pixel_array[index]
#         else:
#             new_image = ds.pixel_array

#         results = []
#         window_centers = []

#         for i in range(10):
#             step =(end_value - start_value) / 9
#             window_center = int(start_value + i * step)
#             converted_image = self.convert_file(new_image, window_center, window_width)
#             results.append(converted_image)
#             print(window_centers)
#             window_centers.append(window_center)
        
#         print(f"window_centers결과 : {window_centers}")    

#         return results, window_centers


#     def convert_file(self, img, window_center, window_width):
#         scaled_image = cv2.convertScaleAbs(
#             img - window_center, alpha=(255.0 / window_width))
#         img_from_scaled = Image.fromarray(scaled_image)
#         img_io = io.BytesIO()
#         img_from_scaled.save(img_io, 'PNG', quality=100)
#         img_io.seek(0)  # BytesIO의 커서를 처음으로 이동
#         return img_io.read()
'''
    Convert Dicom
    FTP -> binarydata -> ds -> toJSON
    Description : FTP에서 받은 binary data -> ds로 JSON 직렬화
    Author : Okrie, Oh-Kang94
    Ver : 0.1
    Site : https://github.com/Okrie/DicomToPng
    Lisence : MIT
'''
import tempfile
from PIL import Image
import numpy as np
import pydicom
import io
import json
import cv2
import os


class ConvertDCM:

    # dcm file의 영상 갯수 확인 함수
    def count_images_in_dicom(file_path):
        #dicomfile로드
        ds = pydicom.dcmread(file_path)
        #image갯수 확인
        if hasattr(ds, 'NumberOfFrames'):
            num_images = ds.NumberOfFrames
            print(f"number of frames: {num_images}")
        else:
            print("number of images : 1(single-frame Dicom)")

    def dicomToJSON(self, data):
        info_list = ["Patient ID", "Patient's Name", "Patient's Birth Date", "Series Number", "Study Date", "Study Time", "Image Comments", "Series Description", "Number of Frames",
                     "Manufacturer", "Manufacturer's Model Name", "Rows", "Columns", "Window Width", "Window Center", "Operator's Name"]
        ds = pydicom.dcmread(io.BytesIO(data))
        
        """
        ### Front Info for list
        @Params : fname -> SC 판단 후, Slice Score를 뱉어냄
        """
        result = {}
        for elem in ds:
            if elem.name in info_list:
                if elem.name == "Window Width":
                    width_value = elem.value if elem.value is not None else 0
                    result[elem.name] = str(width_value)
                elif elem.name == "Window Center" and elem.value is None:
                    result[elem.name] = str(1)
                else:
                    result[elem.name] = str(elem.value)
        if "Number of Frames" not in result:
            result["Number of Frames"] = str(1)
        if len(ds.pixel_array.shape) == 4:
            pixel_array_shape = 4
        elif len(ds.pixel_array.shape) == 3:
            pixel_array_shape = 3
        else:
            pixel_array_shape = 2
        result['pixel array shape'] = str(pixel_array_shape)
        return json.dumps(result)

    def dicomToPNG(self, data, index=0):
        ds = pydicom.dcmread(io.BytesIO(data))
        if len(ds.pixel_array.shape) == 4:  # 4차원 배열인 경우
            new_image = ds.pixel_array.astype(float)
            new_image = np.reshape(
                ds.pixel_array[index, :, :, 0], (-1, ds.pixel_array.shape[2]))
        elif len(ds.pixel_array.shape) == 3:  # 3차원 배열인 경우
            new_image = ds.pixel_array[index].astype(float)
        else:
            new_image = ds.pixel_array.astype(float)
        # normalization 작업
        ###나누기 0 처리
        # k = np.maximum(new_image, 0) 
        # if(k == 0):
        #     k = k+0.01
        ###나누기 0 처리 끝

        # scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        scaled_image = (np.maximum(new_image, 0) / new_image.max()) * 255.0
        
        scaled_image = np.uint8(scaled_image)
        # 흑백 반전 작업
        # scaled_image = 255 - scaled_image
        img = Image.fromarray(scaled_image)
        img_io = io.BytesIO()
        img.save(img_io, 'PNG', quality=100)
        img_io.seek(0)  # BytesIO의 커서를 처음으로 이동
        return img_io

    def dicomToPNGs_windows(self, data, index=0):
        ds = pydicom.dcmread(io.BytesIO(data))
        window_width = ds.WindowWidth 
        '''

        *** window_width의 값이 있을 때, 없을 때 만들어야 함.
        
        '''
        # 'WindowWidth' 속성이 존재하지 않을 경우에 대한 처리
        # if hasattr(ds, 'WindowWidth') and ds.WindowWidth is not None:
        #     window_width = ds.WindowWidth
        # else:
        # # 'WindowWidth'가 없는 경우에 기본값이나 다른 값을 사용
        #     window_width = DEFAULT_WINDOW_WIDTH  # 여기서 DEFAULT_WINDOW_WIDTH는 적절한 기본값으로 설정해야 합니다.
        try:
            window_width = ds.WindowWidth
        except AttributeError:
            window_width = DEFAULT_WINDOW_WIDTH
        
        # print("window_width"+str(window_width) +
        #       "type은 " + str(type(window_width)))

        if isinstance(window_width, pydicom.multival.MultiValue):
            window_width = float(window_width[0])
        if isinstance(ds.WindowCenter, pydicom.multival.MultiValue):
            ds.WindowCenter = float(ds.WindowCenter[0])

        if (ds.WindowCenter == window_width):
            ds.WindowCenter = ds.WindowCenter + 0.01

        start_value = ds.WindowCenter - window_width / 2.0
        end_value = ds.WindowCenter + window_width / 2.0

        if len(ds.pixel_array.shape) == 4:  # 4차원 배열인 경우
            new_image = ds.pixel_array.astype(float)
            new_image = np.reshape(
                ds.pixel_array[index, :, :, 0], (-1, ds.pixel_array.shape[2]))
        elif len(ds.pixel_array.shape) == 3:  # 3차원 배열인 경우
            new_image = ds.pixel_array[index].astype(float)
        else:
            new_image = ds.pixel_array.astype(float)

        results = []
        window_centers = []

        for i in range(10):
            if(end_value == start_value):
                end_value = end_value + 0.01
            step = (end_value - start_value) / 9.0
            window_center = int(start_value + i * step)
            # print("window_center"+str(window_center) +
            #       "type은 " + str(type(window_center)))
            converted_image = self.convert_file(new_image,window_center,window_width)
            results.append(converted_image)
            window_centers.append(window_center)
        return results, window_centers

    ##########  1월 22일 추가 안되면 위에거 살리기
    # def dicomToPNGs_windows(self, data, index=0):
    #     ds = pydicom.dcmread(io.BytesIO(data))
    #     window_width = ds.WindowWidth

    #     start_value = ds.WindowCenter - window_width / 2.0
    #     end_value = ds.WindowCenter + window_width / 2.0

    #     print(f"minValue = {start_value}")
    #     print(f"maxValue = {end_value}")

    #     # if len(ds.pixel_array.shape) == 4:
    #     #     new_image = ds.pixel_array[index, :, :, 0]
    #     # elif len(ds.pixel_array.shape) == 3:
    #     #     new_image = ds.pixel_array[index]
    #     # else:
    #     #     new_image = ds.pixel_array
    #     if len(ds.pixel_array.shape) == 4:
    #         new_image = ds.pixel_array[index, :, :, 0]
    #     elif len(ds.pixel_array.shape) == 3:
    #         new_image = ds.pixel_array[index]
    #     else:
    #         new_image = ds.pixel_array

    #     results = []
    #     window_centers = []

    #     for i in range(10):
    #         step =(end_value - start_value) / 9
    #         window_center = int(start_value + i * step)
    #         converted_image = self.convert_file(new_image, window_center, window_width)
    #         results.append(converted_image)
    #         print(window_centers)
    #         window_centers.append(window_center)
        
    #     print(f"window_centers결과 : {window_centers}")    

    #     return results, window_centers


    def convert_file(self, img, window_center, window_width):
        scaled_image = cv2.convertScaleAbs(

            img - window_center, alpha=(255.0 / window_width))
        img_from_scaled = Image.fromarray(scaled_image)
        img_io = io.BytesIO()
        img_from_scaled.save(img_io, 'PNG', quality=70)
        img_io.seek(0)  # BytesIO의 커서를 처음으로 이동
        return img_io.read()