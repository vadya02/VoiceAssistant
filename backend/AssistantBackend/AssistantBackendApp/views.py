import io
import os

import ffmpeg
import pydub
import speech_recognition as sr
from pydub import AudioSegment
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.Parse_w2v_text import ParseKeywords

# from utils.parse_w2v import ParseKeywords
from utils.ParseText import ParseText

from AssistantBackendApp.serializers import AudioFileSerializer

from .models import RequestHistory
from .serializers import RequestHistorySerializer

# Получаем путь к текущему файлу (этот файл views.py)
current_file_path = os.path.abspath(__file__)

# Получаем путь к папке views
views_folder_path = os.path.dirname(current_file_path)

# Получаем путь к корневой папке проекта (предполагая, что ваш файл .exe находится в папке executables)
project_root_path = os.path.dirname(os.path.dirname(views_folder_path))

# Строим путь к файлу .exe
exe_file_path = os.path.join(
    project_root_path, "ffmpeg-2023-11-22-git-0008e1c5d5-essentials_build", "ffmpeg.exe"
)

# pydub.AudioSegment.converter = exe_file_path
class AudioUploadViewMp3(generics.ListAPIView):
    try:
        serializer_class = RequestHistorySerializer

        def post(self, request, *args, **kwargs):
            print(self.request.user)
            print(self.request.user.is_authenticated)
            url = "http://213.171.10.37:8088/superset/dashboard/12/?native_filters_key=jq9pf2aXz9sgIwMI4e93RLk20IGHu5DI5-Q30RvvwuMqUI4aa00PjdbJvzOkwzNv"

            serializer = AudioFileSerializer(data=request.data)
            print(serializer)
            try:
                if serializer.is_valid():
                    audio_file = serializer.validated_data["audio_file"]
                    print(audio_file)
                    
                    audio = AudioSegment.from_mp3(audio_file)
                    print(f"audio {audio}")
                    wav_data = audio.set_frame_rate(16000).raw_data
                    wav_file = AudioSegment(
                        wav_data, frame_rate=16000, sample_width=2, channels=1
                    )
                    print(wav_file)
                    wav_filename = f"{audio_file.name.split('.')[0]}.wav"
                    wav_file.export(wav_filename, format="wav")

                    filename = f"{wav_filename}"
                    file_path = os.path.join(
                        os.path.dirname(os.path.abspath(__file__)), "..", f"{filename}"
                    )
                    with open(file_path, "rb") as file:
                        # Здесь вы можете что-то сделать с содержимым файла, например, прочитать его или отправить клиенту
                        file_content = file.read()
                        print(file)

                    print(type(audio_file))
                    r = sr.Recognizer()
                    harvard = sr.AudioFile(f"{filename}")
                    print(harvard)
                    with harvard as source:
                        audio = r.record(source)

                    print(f"audio: {audio}")
                    msg = r.recognize_google(audio, language="ru-RU")
                    # url = ParseText(msg) #получаем url
                    print(f"Распознанный текст: {msg}")
                    url = ParseKeywords(msg)
                    print(f"url после нахождения ключевых слов: {url}")
                    print(f"url: {url}")

                    print(url)
                    print(f"Тип URL: {type(url)} \n")
                    try:
                        if url != None:
                            obj, created = RequestHistory.objects.get_or_create(
                                user=self.request.user,
                                url=url,
                                text=msg,
                            )
                            print(url)
                            return Response(
                                {
                                    "message": "File uploaded successfully.",
                                    "url": url,
                                    "text": msg,
                                }
                            )
                        else:
                            return Response({"url": "null"})
                    except Exception as e:
                        print(f"message_error: {e}")
                        return Response({"message_error": {e}})
                else:
                    return Response({"message": "Invalid request."}, status=400)
            except Exception as e:
                return Response({"message_error": {e}})
    except Exception as e:
        print(f"message_error: {e}")


class AudioUploadViewMp3V2(generics.ListAPIView):
    try:
        serializer_class = RequestHistorySerializer

        def post(self, request, *args, **kwargs):
            print(f'Путь до ffmpeg: {exe_file_path}')
            print(self.request.user)
            print(self.request.user.is_authenticated)

            serializer = AudioFileSerializer(data=request.data)
            print(serializer)
            try:
                if serializer.is_valid():
                    audio_file = serializer.validated_data["audio_file"]
                    print(type(audio_file))
                    print("Имя файла:", audio_file.name)
                    print("Размер файла:", audio_file.size)

                    audio_stream = io.BytesIO(audio_file.read())

                    # Перемещаем указатель в начало потока после чтения
                    audio_stream.seek(0)

                    audio = AudioSegment.from_file(audio_stream)
                    audio = audio.set_channels(
                        1)  # Установить один канал (моно)
                    audio.export("audio.wav", format="wav")
                    # Распознать речь
                    recognizer = sr.Recognizer()
                    with sr.AudioFile("audio.wav") as source:
                        audio_data = recognizer.record(source)
                        text = recognizer.recognize_google(audio_data,
                                                           language="ru-RU")

                    print(f"Распознанный текст: {text}")

                    url = ParseKeywords(text)
                    print(f"url после нахождения ключевых слов: {url}")
                    print(f"url: {url}")
                    print(url)
                    print(f"Тип URL: {type(url)} \n")
                    try:
                        if url != None:
                            obj, created = RequestHistory.objects.get_or_create(
                                user=self.request.user,
                                url=url,
                                text=text,
                            )
                            print(url)
                            return Response({
                                "message": "File uploaded successfully.",
                                "url": url,
                                "text": text,
                            })
                        else:
                            return Response({"url": "null", "text": text})
                    except Exception as e:
                        print(f"message_error: {e}")
                        return Response({"message_error": {e}})
                else:
                    return Response({"message": "Invalid request."},
                                    status=400)
            except Exception as e:
                print(f"message_error: {e}")
                return Response({"message_error": {e}})
    except Exception as e:
        print(f"message_error: {e}")


class RequestHistoryList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = RequestHistory.objects.all()
    serializer_class = RequestHistorySerializer

    def get_queryset(self):
        # Получаем историю запросов текущего пользователя
        return RequestHistory.objects.filter(user=self.request.user)


class AudioUploadViewText(generics.ListAPIView):
    serializer_class = RequestHistorySerializer

    def post(self, request, *args, **kwargs):
        print(self.request.user)
        print(self.request.user.is_authenticated)

        text = self.request.data.get("textRequest", "")
        print(f"Присланный текст: {text}")
        url = ParseText(text)
        url = "http://213.171.10.37:8088/superset/dashboard/12/?native_filters_key=jq9pf2aXz9sgIwMI4e93RLk20IGHu5DI5-Q30RvvwuMqUI4aa00PjdbJvzOkwzNv12345"
        print(url)
        if url != None:
            obj, created = RequestHistory.objects.get_or_create(
                user=self.request.user,
                url=url,
                text=text,
            )
            return Response(
                {"message": "File uploaded successfully.", "url": url, "text": text}
            )
        else:
            return Response({"url": "null"})


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # request.user содержит информацию о текущем пользователе
        user_data = {
            "username": request.user.username,
            "email": request.user.email,
            # Другие поля, которые вы хотите включить
        }
        return Response(user_data, status=status.HTTP_200_OK)
