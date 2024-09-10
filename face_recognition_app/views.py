import boto3
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .face_recognition import process_video  # Your face recognition processing function

# Initialize the boto3 S3 client with the AWS credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_S3_REGION_NAME
)

def index(request):
    return render(request, 'index.html')

def process_video_view(request):
    if request.method == 'POST' and request.FILES['video']:
        try:
            # Get the uploaded video
            video_file = request.FILES['video']
            temp_file_name = f'temp_videos/{video_file.name}'
            
            # Save the uploaded video temporarily for processing
            temp_file_path = default_storage.save(temp_file_name, ContentFile(video_file.read()))

            # Process the video locally (this should return the path of the processed video)
            local_processed_video_path = process_video(default_storage.path(temp_file_path))

            if not local_processed_video_path:
                return render(request, 'process_error.html')

            # Define the S3 object name for the processed video
            processed_video_name_on_s3 = f'processed_videos/{os.path.basename(local_processed_video_path)}'

            try:
                # Upload the processed video to S3 using boto3 (without ACL)
                s3_client.upload_file(
                    local_processed_video_path,  # Local path to the processed video
                    settings.AWS_STORAGE_BUCKET_NAME,  # S3 Bucket name
                    processed_video_name_on_s3,  # S3 Object name (path in the bucket)
            
                )
            except Exception as upload_error:
                print(f"Error uploading processed video to S3: {upload_error}")
                return render(request, 'process_error.html')

            # Generate the S3 URL of the processed video
            processed_video_url = f"https://{settings.AWS_S3_CUSTOM_DOMAIN}/{processed_video_name_on_s3}"

            # Clean up the local temporary files if needed
            if os.path.exists(local_processed_video_path):
                os.remove(local_processed_video_path)
            if os.path.exists(default_storage.path(temp_file_name)):
                default_storage.delete(temp_file_name)

            # Render success template with the URL of the processed video
            return render(request, 'process_success.html', {'video_url': processed_video_url})

        except Exception as e:
            print(f"Error during video processing or upload: {e}")
            return render(request, 'process_error.html')

    return redirect('index')
