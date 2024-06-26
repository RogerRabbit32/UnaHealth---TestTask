import csv

import openpyxl
from datetime import datetime
from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from django.utils.dateformat import format as date_format
from io import StringIO

from .models import GlucoseLevel


@transaction.atomic
def parse_glucose_data(csv_file, user_id):
    """ This function reads the csv file data
    (previously converted into binary format)
    and parses the file columns, with relation
    to the GlucoseLevel model """

    # Read and convert the file into binary
    decoded_file = csv_file.read().decode('utf-8')
    io_string = StringIO(decoded_file)
    csv_file_data = csv.reader(io_string)

    # Retrieve the user by id and make sure we
    # upload glucose data for an existing user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        raise KeyError("User with this id does not exist")

    # Skip lines until we find the header (column titles)
    header = None
    for row in csv_file_data:
        if row[:2] == ['Gerät', 'Seriennummer']:
            header = row
            break

    if not header:
        raise AttributeError("CSV file does not contain the expected header")

    # Now read the actual data (assuming header matches the fields)
    data = list(csv_file_data)
    for row in data:
        if not row:  # skip empty rows
            continue

        if row[3] == '0':
            parsed_glucose_value = int(row[4])
        elif row[3] == '1':
            parsed_glucose_value = int(row[5])
        else:
            parsed_glucose_value = None

        date_str = row[2]
        date_obj = datetime.strptime(date_str, '%d-%m-%Y %H:%M')
        # Format datetime object to YYYY-MM-DD HH:MM
        django_formatted_datetime = date_obj.strftime('%Y-%m-%d %H:%M')

        GlucoseLevel.objects.create(
            user=user,
            device_name=row[0],
            device_serial_number=row[1],
            timestamp=django_formatted_datetime,
            recording_type=row[3],
            glucose_value=parsed_glucose_value,
        )


def export_glucose_data(queryset):
    """ This function creates an Excel file and
     fills it with GlucoseLevel objects data. The
    queryset is filtered by user_id by the viewset """

    # Create Excel workbook and sheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Glucose Levels'

    # Define headers for the Excel sheet
    headers = ['ID', 'Timestamp', 'Glucose Level']
    ws.append(headers)

    # Add data rows from queryset to Excel sheet
    for obj in queryset:
        row = [
            obj.id,
            date_format(obj.timestamp, 'd-m-Y H:i'),
            obj.glucose_value
        ]
        ws.append(row)

    # Prepare response with Excel file for download
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=glucose_levels.xlsx'
    wb.save(response)

    return response
