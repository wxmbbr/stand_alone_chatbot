-- Supabase schema for invite-only chatbot

-- Users
create table if not exists public.users (
  id uuid primary key,
  email text unique not null,
  role text not null default 'member',
  created_at timestamptz default now(),
  last_login_at timestamptz
);

-- Invites
create table if not exists public.invites (
  id uuid primary key,
  email text,
  token text unique not null,
  issued_by uuid references public.users(id),
  expires_at timestamptz,
  used_at timestamptz,
  used_by uuid references public.users(id),
  created_at timestamptz default now()
);

-- Sessions
create table if not exists public.sessions (
  id uuid primary key,
  user_id uuid references public.users(id),
  started_at timestamptz default now(),
  last_active_at timestamptz,
  client_info text
);

-- Messages
create table if not exists public.messages (
  id uuid primary key,
  session_id uuid references public.sessions(id),
  user_id uuid references public.users(id),
  role text not null,
  content text not null,
  created_at timestamptz default now()
);

-- Helpful indexes
create index if not exists idx_messages_session_created_at on public.messages (session_id, created_at);
create index if not exists idx_sessions_user on public.sessions (user_id);

-- RLS policies (examples; adjust as needed)
-- For simplicity, allow service role to bypass RLS; implement finer policies for production.

