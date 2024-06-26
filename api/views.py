from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import GlucoseLevelFilter
from .models import GlucoseLevel
from .serializers import ExportCSVSerializer, GlucoseLevelSerializer, UploadCSVSerializer
from .utils import export_glucose_data, parse_glucose_data


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

            try:
                parse_glucose_data(file, user_id)
                return Response({"status": "success"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='export')
    def export_excel(self, request):
        serializer = ExportCSVSerializer(data=request.query_params)
        if serializer.is_valid():
            user_id = serializer.validated_data['user_id']
            queryset = self.filter_queryset(self.get_queryset()).filter(user__id=user_id)
            response = export_glucose_data(queryset)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
