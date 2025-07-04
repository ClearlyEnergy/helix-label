from django.core.files.storage import default_storage
from label.generic_energy_profile import write_generic_energy_profile_pdf
from label.populate_beam_profile import write_beam_profile_pdf
from label.populate_residential_green_addendum import write_green_addendum_pdf
from label.populate_vermont_energy_profile import write_vermont_energy_profile_pdf
from label.populate_massachusetts_home_scorecard import create_pdf
from label.populate_energy_first_mortgage import write_energy_first_mortgage_pdf
from label.populate_beam_ann_arbor import write_ann_arbor_profile_pdf
from label.populate_beam_ann_arbor_2030 import write_ann_arbor_2030_profile_pdf
from label.populate_beam_cambridge import write_cambridge_profile_pdf
from label.populate_beam_columbia import write_columbia_profile_pdf
from label.populate_beam_core import write_core_profile_pdf
from label.populate_beam_detroit_2030 import write_detroit_2030_profile_pdf
from label.populate_beam_grand_rapids import write_grand_rapids_profile_pdf
from label.populate_beam_indianapolis import write_indianapolis_profile_pdf
from label.populate_beam_lexington import write_lexington_profile_pdf
from label.populate_beam_madison import write_madison_profile_pdf
from label.populate_beam_new_jersey import write_new_jersey_profile_pdf
from label.populate_beam_portland import write_portland_profile_pdf
from label.populate_beam_philadelphia import write_philadelphia_profile_pdf
from label.populate_beam_oak_park import write_oak_park_profile_pdf
from label.populate_beam_orlando import write_orlando_profile_pdf
from label.populate_beam_providence import write_providence_profile_pdf
from label.populate_beam_reno import write_reno_profile_pdf
from label.populate_beam_san_diego import write_san_diego_profile_pdf
from label.populate_beam_south_portland import write_south_portland_profile_pdf
from label.populate_remotely_ipc import write_remotely_ipc_pdf
from label.utils.utils import validate_data_dict

import io
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

    def energy_first_mortgage(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/ProjectSummary.pdf'
        write_energy_first_mortgage_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def vermont_energy_profile(self, data_dict, aws_bucket=''):
        out_file = io.BytesIO()
        write_vermont_energy_profile_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def generic_energy_profile(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/EnergyLabel.pdf'
        write_generic_energy_profile_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename

    def beam_profile(self, data_dict, object_id, out_path='', out_file='', organization_name='', aws_bucket=None):
        org_pdf_mapping = {'City of Ann Arbor': write_ann_arbor_profile_pdf,
                           'Ann Arbor and Washtenaw 2030 District': write_ann_arbor_2030_profile_pdf,
                           'City of Cambridge': write_cambridge_profile_pdf,
                           'City of Columbia': write_columbia_profile_pdf,
                           'CORE': write_core_profile_pdf,
                           'Detroit 2030 District': write_detroit_2030_profile_pdf,
                           'Grand Rapids 2030': write_grand_rapids_profile_pdf,
                           'City of Indianapolis': write_indianapolis_profile_pdf,
                           'Town of Lexington MA': write_lexington_profile_pdf,
                           'New Jersey BPU': write_new_jersey_profile_pdf,
                           'Village of Oak Park': write_oak_park_profile_pdf,
                           'City of Orlando': write_orlando_profile_pdf,
                           'City of Portland': write_portland_profile_pdf,
                           'City of Philadelphia': write_philadelphia_profile_pdf,
                           'City of Providence': write_providence_profile_pdf,
                           'City of San Diego': write_san_diego_profile_pdf,
                           'City of Reno': write_reno_profile_pdf,
                           'City of South Portland': write_south_portland_profile_pdf,
                           }
        fn = org_pdf_mapping.get(organization_name, write_beam_profile_pdf)

        out_path = out_path if out_path else self.out_path
        out_file = out_file if out_file else f'{object_id}_profile.pdf'

        full_path = out_path + '/' + out_file

        is_data_valid, msg, data_dict = validate_data_dict(data_dict)

        if is_data_valid:
            try:
                fn(data_dict, full_path)
                return full_path, ''
            except FileNotFoundError:
                with default_storage.open(full_path, 'wb') as file:
                    fn(data_dict, file)
                return full_path, ''
        else:
            return '', f'Errors for {object_id}: ' + msg

    def massachusetts_energy_scorecard(self, data_dict, aws_bucket=''):
        out_file = self.out_path + '/MAScorecard.pdf'
        create_pdf(data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        return out_filename
    

    def remotely_ipc_pdf(self, data_dict, aws_bucket):
        """
        Produce a PDF report for IPC's SMARTE-Loan programs.
        
        Question/answers will be placed into groups based on the question_group value.
        Question/answers are added in the same order they are defined.
        
        :param dict data_dict: The data required to construct the IPC PDF.
        :param str aws_bucket: The destination S3 bucket for the resultant PDF file.
        :return str out_filename: The destination on S3 where resultant file was saved.
        """

        if 'ce_api_id' not in data_dict:
            raise ValueError('ce_api_id required in data_dict in order to write result file.')

        out_file = io.BytesIO()
        write_remotely_ipc_pdf(self.s3_resource, data_dict, out_file)
        out_filename = self._write_S3(out_file, aws_bucket)
        bucket = os.environ.get('S3_BUCKET', aws_bucket)
        url = f"https://{bucket}.s3.amazonaws.com/{out_filename}"
        return url

    def _write_S3(self, file_name, aws_bucket = ''):
        bucket = os.environ.get('S3_BUCKET', aws_bucket)
        filename = 'labels/' + str(uuid.uuid4())+'.pdf'
        args = {'ContentType': 'application/pdf', 'ACL': 'public-read'}
        if isinstance(file_name, str):
            self.s3_resource.Object(bucket, filename).upload_file(Filename=file_name, ExtraArgs=args)
            os.remove(file_name)
        elif hasattr(file_name, 'read') and hasattr(file_name, 'seek'):
            file_name.seek(0)
            self.s3_resource.Object(bucket, filename).upload_fileobj(file_name, ExtraArgs=args)
        
        return filename

    def remove_label(self, filename, aws_bucket=''):
        bucket = os.environ.get('S3_BUCKET', aws_bucket)
        ret = self.s3_resource.Object(bucket, 'labels/' + filename).delete()
        if ret['ResponseMetadata']['HTTPStatusCode'] == 204:
            return True
        else:
            return False
