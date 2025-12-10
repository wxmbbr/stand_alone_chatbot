# Stand-alone Chatbot App Specification

## Scope
- Build a standalone chatbot (Streamlit-based) reusing current BBR styling (dark blue palette) with improved responsive layout for desktop and mobile.
- Add invite-only user management with roles (admin/member) and basic admin console.
- Persist auth, sessions, and chat messages in Supabase.
- Keep existing OpenAI Assistant/API configuration (keys pulled from environment).

## Tech Stack
- Frontend: Streamlit (Python) with responsive CSS; optional lightweight JS for scroll/viewport fixes.
- Backend: Streamlit server for UI + OpenAI calls; Supabase for auth/data; Python HTTP requests for OpenAI Assistants v2.
- Dependencies to add: `supabase` (supabase-py), `python-dotenv` (already), `pydantic` (for request/response models if needed).

## Environment & Config
- `.env` keys: `OPENAI_API_KEY`, `OPENAI_ASSISTANT_ID`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`.
- `config.py` should only read from env (no hardcoded secrets).
- Service role key used server-side only (never exposed to browser).

## User Management (Invite-Only)
- Roles: `admin`, `member`.
- Invite flow:
  - Admin creates invite (token, email, expiry, single-use).
  - User signs up with email + invite token (magic link or password-based login).
  - On success, invite marked used; user created with `member` role by default.
- Admin console:
  - Create/revoke invites, view invite status.
  - View users (email, role, created, last login), promote/demote roles.

## Data Model (Supabase)
- `users`: id (uuid), email (unique), role (text), created_at, last_login_at.
- `invites`: id (uuid), email, token, issued_by (uuid), expires_at, used_at, used_by (uuid).
- `sessions`: id (uuid), user_id (uuid), started_at, last_active_at, client_info.
- `messages`: id (uuid), session_id (uuid), user_id (uuid, nullable for assistant), role (user/assistant/system), content (text), created_at.

## Application Flow
1) User hits app:
   - If not authenticated, show welcome + login/signup with invite code.
   - Validate invite; create account; login.
2) Authenticated user enters chat:
   - Load or start session row; stream messages to/from OpenAI Assistant.
   - Persist messages to Supabase after each exchange.
3) Admin panel (if role=admin):
   - Manage invites; view users; revoke access.

## UI/UX Requirements
- Preserve dark blue palette; refine spacing/typography; consistent avatars.
- Desktop: wide chat area with fixed header and floating input; scrolling stable.
- Mobile: full-height view, sticky input, collapsible header, larger touch targets.
- Empty states and error toasts for auth and network errors.
- Accessibility: focus states, readable contrast, keyboard navigation for inputs.

## Security & Privacy
- Secrets only in env; never in client bundle.
- Rate limiting per user/session for outbound OpenAI calls.
- Validate invite tokens server-side; expire and single-use enforcement.
- Minimal PII (email only); log auth events (success/failure) to Supabase.

## Rollout Plan
1) Dependencies/config: add Supabase client; update env sample; keep OpenAI config.
2) Auth layer: Supabase auth + invite validation; login/signup screens.
3) Data layer: create tables; wire persistence for sessions/messages.
4) UI refactor: responsive layout for chat; keep branding; mobile polish.
5) Admin console: invite management, user list/roles.
6) QA: manual auth flows, chat persistence, mobile/desktop smoke.

## Cleanup Notes (proposed)
- Remove hardcoded secrets from repo (done via env-based config).
- Keep branding assets in `images/`; archive old HTML demos if not needed during build.


