import os
from typing import Optional

import boto3

from app.config import settings

class S3Service:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            region_name=settings.AWS_REGION,
        )
        self.bucket = settings.S3_REPORTS_BUCKET
    
    def upload_pdf(
        self,
        file_path: str,
        report_id: str,
    ) -> str:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"PDF file not found: {file_path}")
        
        s3_key = f"reports/{report_id}.pdf"
        
        self.client.upload_file(
            Filename=file_path,
            Bucket=self.bucket,
            Key=s3_key,
            ExtraArgs={
                "ContentType": "application/pdf",
            },
        )
        
        return s3_key
        
        
    def generate_presigned_url(
        self,
        s3_key: Optional[str],
        expires_in: int = 3600,
    ) -> Optional[str]:
        if not s3_key:
            return None

        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket,
                "Key": s3_key,
            },
            ExpiresIn=expires_in,
        )
