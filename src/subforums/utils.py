from django.utils import timezone


def calculate_thread_rank(thread):
    if thread.is_pinned:
        return 10
    total_point = 0
    now = timezone.now()
    if thread.comments.exists():
        last_comment = thread.comments.order_by('-created_date').first()
        last_comment_time_diff = now - last_comment.created_date
        total_point += 1 / last_comment_time_diff.total_seconds()
    thread_created_time_diff = now - thread.created_date
    total_point += 1 / thread_created_time_diff.total_seconds()
    return total_point
