from label.populate_residential_green_addendum import write_green_addendum_pdf
from label.populate_vermont_energy_profile import write_vermont_energy_profile_pdf
from label.populate_massachusetts_home_scorecard import create_pdf
from label.generic_energy_profile import write_generic_energy_profile_pdf
import os
import os.path
import boto3
import uuid
# lab = label.Label('filetype')
# lab.green_addendum(data_dict)

INPUT_TEMPLATE_PATH = "./templates/"
OUTPUT_PATH = "./tmp/"


class Label:
    def __init__(self, aws_key='', aws_secret=''):
        self.module_path = os.path.abspath(os.path.dirname(__file__))
        self.in_path = os.path.normpath(os.path.join(self.module_path, INPUT_TEMPLATE_PATH))
        self.out_path = os.path.normpath(os.path.join(self.module_path, OUTPUT_PATH))
        self.s3_resource = boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('S3_KEY', aws_key),
            aws_secret_access_key=os.environ.get('S3_SECRET', aws_secret)
            )

    def green_addendum(self, data_dict, aws_bucket=''):
        in_file = self.in_path + '/ResidentialGreenandEnergyEfficientAddendum.pdf'
        out_file = self.out_path + '/GreenAddendum.pdf'
        write_green_addendum_pdf(in_file, data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def energy_first_mortgaga(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/GreenAddendum.pdf'
        write_energy_first_mortgage_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def vermont_energy_profile(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/VTLabel.pdf'
        write_vermont_energy_profile_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def generic_energy_profile(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/EnergyLabel.pdf'
        write_generic_energy_profile_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def massachusetts_energy_scorecard(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/MAScorecard.pdf'
        create_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def _write_S3(self, file_name, aws_bucket = ''):
        bucket = os.environ.get('S3_BUCKET', aws_bucket)
        filename = 'labels/' + str(uuid.uuid4())+'.pdf'
        self.s3_resource.Object(bucket, filename).upload_file(Filename=file_name, ExtraArgs={'ContentType': 'application/pdf', 'ACL': 'public-read'})
        os.remove(file_name)
        return filename

    def remove_label(self, filename, aws_bucket=''):
        bucket = os.environ.get('S3_BUCKET', aws_bucket)
        ret = self.s3_resource.Object(bucket, 'labels/' + filename).delete()
        if ret['ResponseMetadata']['HTTPStatusCode'] == 204:
            return True
        else:
            return False
