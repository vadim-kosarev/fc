# fc

1. Create venv
```
python -m venv .venv
```
2. set PATH to venv
```
set PATH=C:\dev\github\vadim-kosarev\fc\.venv\Scripts;%PATH%
```
3. Install numpy
```
python -m pip install numpy --upgrade
```
4. Install pika
```
python -m pip install pika --upgrade
```
```
python -m pip install dlib
```
```
python -m pip install face_recognition
```
```
python -m pip install opencv-python
```
```
python -m pip install minio
```

```
set PATH=C:\Tools\Minio;%PATH%
set MINIO_ROOT_USER=minioAdmin
set MINIO_ROOT_PASSWORD=minioAdminPass
minio server G:\minio

# open http://localhost:9000/ in browser
# create bucket 'jpgdata'

mc alias set local http://127.0.0.1:9000 %MINIO_ROOT_USER% %MINIO_ROOT_PASSWORD%
mc put data/orban_putin.jpg local/jpgdata/HARON/Camera#0/image.jpg

# Create AccessKey
set ACCESS_KEY=PTsZCtt8gGKXo3rUjOXW
set PRIVATE_KEY=hhYU2uZBh3kdwCtxdKQkHw7fFs1CAVh6TwWBwRWl

```
