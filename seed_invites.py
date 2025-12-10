"""
Seed initial admin/member users and invite tokens for quick login.
Run locally with your .env loaded (contains Supabase keys).

Usage:
    python seed_invites.py

It will create:
  - admin email: adm_bbr
  - member email: bbru1
and output invite tokens for both.
"""

import os
from dotenv import load_dotenv

from supabase_client import (
    get_client,
    get_user_by_email,
    create_user,
    count_admins,
    create_invite,
)


def main():
    load_dotenv()
    client = get_client()

    targets = [
        ("adm_bbr", "admin"),
        ("bbru1", "member"),
    ]

    for email, desired_role in targets:
        user = get_user_by_email(client, email)
        if not user:
            role = desired_role
            # ensure at least one admin exists
            if role != "admin" and count_admins(client) == 0:
                role = "admin"
            user = create_user(client, email=email, role=role)
            print(f"Created user {email} with role {role}")
        else:
            print(f"User {email} already exists with role {user.get('role')}")

        invite = create_invite(client, email=email, days_valid=30, issued_by=None)
        print(f"Invite token for {email}: {invite['token']}")


if __name__ == "__main__":
    main()

