from populate_residential_green_addendum import write_green_addendum_pdf
from pdfrw import PdfWriter
import os
import boto3
import uuid
#lab = label.Label('filetype')
# lab.green_addendum('./out_test.pdf', data_dict)
INPUT_TEMPLATE_PATH = './templates/'
OUTPUT_PATH = './tmp/'


class Label:
    def __init__(self, label_name):
        self.label_name = label_name
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('S3_KEY', ''),
            aws_secret_access_key=os.environ.get('S3_SECRET', '')
            )
        
    def green_addendum(self, data_dict):
        in_file = INPUT_TEMPLATE_PATH + 'ResidentialGreenandEnergyEfficientAddendum.pdf'
        out_file = OUTPUT_PATH+'GreenAddendum.pdf'
        write_green_addendum_pdf(in_file, data_dict, out_file)
        self._write_S3(self, out_file)
        
    def _write_S3(self, file_name):
#        bucket = os.environ.get('S3_BUCKET','')
        bucket = 'certification-label'
        filename = str(uuid.uuid4())+'.pdf'
        self.s3_resource.Object(bucket, filename).upload_file(Filename=file_name)
        os.remove(file_name)
 
