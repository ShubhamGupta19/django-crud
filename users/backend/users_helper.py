import random
import string
from config.helper_functions import paginate
from users.models import UserProfile
from django.db.models import Q


def get_all_users_helper(
    page_number, page_size, sort_by, sort_order, search_text, filters
):

    users = UserProfile.objects.all()

    if search_text:
        users = users.filter(
            Q(user__email__icontains=search_text)
            | Q(mobile_number__icontains=search_text)
            | Q(name__icontains=search_text)
            | Q(surname__icontains=search_text)
        )

    if sort_by == "creation_date":
            users = users.order_by("-user__date_joined")
    elif sort_by == "wallet_balance":
        if sort_order == "asc":
            users = users.order_by("wallet_balance")
        else:
            users = users.order_by("-wallet_balance")
    elif sort_by == "total_rides":
        if sort_order == "asc":
            users = users.order_by("total_rides")
        else:
            users = users.order_by("-total_rides")

    users, total_pages, page_number = paginate(users, page_number, page_size=page_size)

    return {
        "page_number": page_number,
        "total_pages": total_pages,
        "total_count": users.count() if users else 0,
        "data": [user.to_dict() for user in users],
    }


def get_complete_user_details(user_profile):

    user_details = user_profile.to_dict(locations=False)

    user_details.update(
        {
            "rides": [
                ride.to_dict()
                for ride in user_profile.rides.all().order_by("-created_at")
            ],
        }
    )

    user_details.update(
        {
            "wallet_transactions": [
                wallet_transaction.to_dict()
                for wallet_transaction in user_profile.wallet_transactions.all().order_by(
                    "-time"
                )
            ],
        }
    )

    return user_details


