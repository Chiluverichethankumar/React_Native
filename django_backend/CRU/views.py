from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from google.cloud import storage
from django.conf import settings
from .models import CallRecording
from .serializers import CallRecordingSerializer

class UploadCallRecording(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        file = request.data['file']
        storage_client = storage.Client()
        bucket = storage_client.bucket(settings.GCP_BUCKET_NAME)
        # 👇 Store under "recordings/" folder inside GCP bucket
        blob_path = f"recordings/{file.name}"
        blob = bucket.blob(blob_path)
        # blob = bucket.blob(file.name)
        blob.upload_from_file(file)
        # Save metadata to DB
        record = CallRecording.objects.create(filename=file.name)
        serializer = CallRecordingSerializer(record)
        return Response(serializer.data)
