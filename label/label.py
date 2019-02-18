from populate_residential_green_addendum import write_green_addendum_pdf
from pdfrw import PdfWriter
import os
import os.path
import boto3
import uuid
#lab = label.Label('filetype')
# lab.green_addendum('./out_test.pdf', data_dict)

INPUT_TEMPLATE_PATH = "../templates/"
OUTPUT_PATH = "../tmp/"

class Label:
    def __init__(self):
        self.module_path = os.path.abspath(os.path.dirname(__file__))
        self.in_path = os.path.normpath(os.path.join(self.module_path, INPUT_TEMPLATE_PATH))
        self.out_path = os.path.normpath(os.path.join(self.module_path, OUTPUT_PATH))
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('S3_KEY', ''),
            aws_secret_access_key=os.environ.get('S3_SECRET', '')
            )
        
    def green_addendum(self, data_dict):
        in_file = self.in_path + '/ResidentialGreenandEnergyEfficientAddendum.pdf'
        out_file = self.out_path +'/GreenAddendum.pdf'
        write_green_addendum_pdf(in_file, data_dict, out_file)
        out_filename = self._write_S3(out_file)
        return 'https://s3.amazonaws.com/certification-label/' + out_filename
        
    def _write_S3(self, file_name):
#        bucket = os.environ.get('S3_BUCKET','')
        bucket = 'certification-label'
        filename = str(uuid.uuid4())+'.pdf'
        self.s3_resource.Object(bucket, filename).upload_file(Filename=file_name)
        os.remove(file_name)
        return filename
 
