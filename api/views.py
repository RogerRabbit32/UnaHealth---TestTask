import csv
from io import StringIO

from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.utils.dateformat import format as date_format
import openpyxl
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import GlucoseLevelFilter
from .models import GlucoseLevel
from .serializers import GlucoseLevelSerializer, UploadCSVSerializer
from .utils import parse_glucose_data


class GlucoseLevelViewSet(viewsets.ModelViewSet):
    queryset = GlucoseLevel.objects.all()
    serializer_class = GlucoseLevelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = GlucoseLevelFilter
    ordering_fields = ['id', 'timestamp']

    @action(detail=False, methods=['post'], url_path='upload')
    def upload_csv(self, request):
        serializer = UploadCSVSerializer(data=request.data)

        if serializer.is_valid():
            file = serializer.validated_data['file']
            user_id = serializer.validated_data['user_id']

            decoded_file = file.read().decode('utf-8')
            io_string = StringIO(decoded_file)
            reader = csv.reader(io_string)

            try:
                parse_glucose_data(reader, user_id)
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        user_id = request.query_params.get('user_id', None)

        queryset = self.filter_queryset(self.get_queryset())
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)

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
                date_format(obj.timestamp, 'd-m-Y H:m'),
                obj.glucose_value
            ]
            ws.append(row)

        # Prepare response with Excel file for download
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=glucose_levels.xlsx'
        wb.save(response)

        return response
