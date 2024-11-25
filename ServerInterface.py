import io
import cv2
import json
import os.path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse

app = FastAPI()


@app.get('/ShoppingItemsGet')
async def getShoppingItems() -> JSONResponse:
    with open(r'resources/ShoppingContentData/ShoppingItemsStorage.json', 'r', encoding='utf') as jsonFile:
        jsonResponse = json.load(jsonFile)
    return JSONResponse(content=jsonResponse)


@app.get('/CoverImageGet')
async def getCoverImage(cover: str) -> FileResponse:
    cover_image_path = fr'resources/ShoppingContentData/ShoppingContentResource/{cover}'
    default_cover_image_path = rf'resources/ShoppingContentData/ShoppingContentResource/wuthering_wave_tsubaki.jpg'
    response = FileResponse(cover_image_path if os.path.exists(cover_image_path) else default_cover_image_path,
                            media_type='image/jpeg')
    return response


@app.get('/ShoppingGameDataGet')
async def getShoppingGameData(code) -> JSONResponse:
    with open(r'resources/ShoppingContentData/ShoppingContentData.json', 'r', encoding='utf') as jsonFile:
        jsonResponse = json.load(jsonFile)
    jsonResponse = jsonResponse.get(code)
    return JSONResponse(content=jsonResponse)


@app.get('/GameMediaListGet')
async def getGameMediaList(code) -> JSONResponse:
    video_list = list()
    image_list = list()
    # {'name': media name, 'type': media type(video, image)}
    for item in os.listdir(fr'resources/ShoppingContentData/ShoppingGameDataResource/{code}'):
        file_name, file_extension = os.path.splitext(item)
        if file_extension in ['.jpg', '.jpeg', '.png', '.webp']:
            image_list.append({'name': item, 'type': 'image'})
        elif file_extension in ['.mp4', '.avi', '.mkv', '.mpeg', '.webm']:
            video_list.append({'name': item, 'type': 'video'})
    image_list.extend(video_list)
    return JSONResponse(content=image_list)


@app.get('/GameMediaGet')
async def getGameMedia(code, media_type, name) -> FileResponse:
    cover_image_path = fr'resources/ShoppingContentData/ShoppingGameDataResource/{code}/{name}'
    if not os.path.exists(cover_image_path):
        cover_image_path = rf'resources/ShoppingContentData/ShoppingContentResource/wuthering_wave_tsubaki.jpg'
        media_type = 'image/jpeg'
    else:
        media_type = 'video/mp4' if media_type == 'video' else 'image/jpeg'
    return FileResponse(cover_image_path, media_type=media_type)


@app.get('/GameVideoCoverGet')
async def getGameVideoCover(code: str, name: str) -> StreamingResponse:
    video_path = fr'resources/ShoppingContentData/ShoppingGameDataResource/{code}/{name}'
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        video_path = rf'resources/ShoppingContentData/ShoppingContentResource/wuthering_wave_tsubaki.jpg'
        return FileResponse(video_path, media_type='image/jpeg')
    else:
        video_capture = cv2.VideoCapture(video_path)
        # 设置当前帧的位置
        frame_number = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT) * 0.02)
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        # 读取帧
        success, frame = video_capture.read()
        # 释放视频捕获对象
        video_capture.release()
        if success:
            # 将帧转换为字节流
            success, encoded_image = cv2.imencode('.jpeg', frame)
            if success:
                bytes_data = encoded_image.tobytes()
                return StreamingResponse(io.BytesIO(bytes_data), media_type='image/jpeg')
    return {"error": "未能提取帧"}
