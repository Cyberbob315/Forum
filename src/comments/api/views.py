from rest_framework.generics import ListAPIView
from comments.models import Comment
from threads.api.pagination import UserThreadCommentPagination
from .serializers import CommentSerializer


class UserCommentAPIView(ListAPIView):
    pagination_class = UserThreadCommentPagination
    serializer_class = CommentSerializer

    def get_queryset(self):
        student_id = self.request.GET.get('student_id','')
        queryset = Comment.objects.filter(author__student_id=student_id)
        return queryset
