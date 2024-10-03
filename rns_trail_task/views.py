import boto3
from cryptography.fernet import Fernet
from django.conf import settings
from django.http import JsonResponse
from django.views import View

from rns_task.settings import MEDIA_URL
from .models import FileData

from .utilities import encrypt_file, upload_to_s3


# Set up the S3 client
class UploadFileView(View):
    def post(self, request):
        if not request.FILES:
            return JsonResponse({'Error': 'No file provided'}, status=400)
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name
        key = Fernet.generate_key()

        # Encrypt the file content
        encrypted_content = encrypt_file(uploaded_file.read(), key)
        local_path = None
        s3_url = None
        import pdb;pdb.set_trace()
        # Save encrypted file to the local file system or S3
        if settings.STORAGE_TYPE == 'S3':
            # Upload to S3
            s3_url = upload_to_s3(encrypted_content, file_name)
        elif settings.STORAGE_TYPE == 'local':
            # Save to the local file system
            with open(file_name, 'w') as write_file:
                write_file.write(encrypted_content.decode('utf-8'))
            local_path = MEDIA_URL +'/'+ file_name



        # save the file information in the database
        encrypted_file = FileData.objects.create(
            file_name=file_name,
            file_key=key.decode(),  # Store the encryption key as a string
            s3_url=s3_url,
            file_location=local_path
        )

        return JsonResponse(
            {'message': 'File uploaded successfully', 'file_id': encrypted_file.id})

