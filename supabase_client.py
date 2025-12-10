"""
Supabase helpers for invite-only auth and chat persistence.
Assumes tables exist (see docs/supabase_schema.sql).
"""

import os
import secrets
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from supabase import Client, create_client


def _now() -> datetime:
    return datetime.now(timezone.utc)


def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("Supabase config missing. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY/ANON_KEY.")
    return create_client(url, key)


def get_user_by_email(client: Client, email: str) -> Optional[Dict[str, Any]]:
    res = client.table("users").select("*").eq("email", email).limit(1).execute()
    data = res.data or []
    return data[0] if data else None


def get_user_by_id(client: Client, user_id: str) -> Optional[Dict[str, Any]]:
    res = client.table("users").select("*").eq("id", user_id).limit(1).execute()
    data = res.data or []
    return data[0] if data else None


def count_admins(client: Client) -> int:
    res = client.table("users").select("id", count="exact").eq("role", "admin").execute()
    return res.count or 0


def create_user(client: Client, email: str, role: str = "member") -> Dict[str, Any]:
    payload = {
        "id": str(uuid.uuid4()),
        "email": email,
        "role": role,
        "created_at": _now().isoformat(),
        "last_login_at": _now().isoformat(),
    }
    res = client.table("users").insert(payload).execute()
    return res.data[0]


def touch_last_login(client: Client, user_id: str) -> None:
    client.table("users").update({"last_login_at": _now().isoformat()}).eq("id", user_id).execute()


def get_invite(client: Client, token: str) -> Optional[Dict[str, Any]]:
    res = (
        client.table("invites")
        .select("*")
        .eq("token", token)
        .is_("used_at", None)
        .limit(1)
        .execute()
    )
    data = res.data or []
    invite = data[0] if data else None
    if not invite:
        return None
    expires_at = invite.get("expires_at")
    if expires_at:
        exp_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
        if exp_dt < _now():
            return None
    return invite


def mark_invite_used(client: Client, invite_id: str, user_id: str) -> None:
    client.table("invites").update({"used_at": _now().isoformat(), "used_by": user_id}).eq("id", invite_id).execute()


def create_invite(
    client: Client,
    email: Optional[str],
    days_valid: int,
    issued_by: Optional[str],
) -> Dict[str, Any]:
    token = secrets.token_urlsafe(16)
    payload = {
        "id": str(uuid.uuid4()),
        "email": email,
        "token": token,
        "issued_by": issued_by,
        "expires_at": (_now() + timedelta(days=days_valid)).isoformat(),
    }
    res = client.table("invites").insert(payload).execute()
    return res.data[0]


def list_invites(client: Client, limit: int = 20) -> List[Dict[str, Any]]:
    res = (
        client.table("invites")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return res.data or []


def create_session(client: Client, user_id: str, client_info: Optional[str] = None) -> Dict[str, Any]:
    payload = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "started_at": _now().isoformat(),
        "last_active_at": _now().isoformat(),
        "client_info": client_info,
    }
    res = client.table("sessions").insert(payload).execute()
    return res.data[0]


def touch_session(client: Client, session_id: str) -> None:
    client.table("sessions").update({"last_active_at": _now().isoformat()}).eq("id", session_id).execute()


def get_session(client: Client, session_id: str) -> Optional[Dict[str, Any]]:
    res = client.table("sessions").select("*").eq("id", session_id).limit(1).execute()
    data = res.data or []
    return data[0] if data else None


def save_message(client: Client, session_id: str, user_id: Optional[str], role: str, content: str) -> None:
    payload = {
        "id": str(uuid.uuid4()),
        "session_id": session_id,
        "user_id": user_id,
        "role": role,
        "content": content,
        "created_at": _now().isoformat(),
    }
    client.table("messages").insert(payload).execute()


def fetch_messages(client: Client, session_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    res = (
        client.table("messages")
        .select("*")
        .eq("session_id", session_id)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    data = res.data or []
    return list(reversed(data))

