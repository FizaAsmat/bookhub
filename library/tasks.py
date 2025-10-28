from celery import shared_task
from .models import Borrow

@shared_task
def send_due_reminder():
    """
    Sends reminder to all users who have borrowed books and not returned them yet.
    """
    borrows_to_remind = Borrow.objects.filter(is_returned=False)  # fixed typo

    if not borrows_to_remind.exists():
        print("No borrowed books found. No reminders to send.")
        return

    for borrow in borrows_to_remind:
        print(
            f"Reminder: {borrow.user.username}, please return the book '{borrow.book.title}'."
        )
