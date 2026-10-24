-- Careers: job applications from careers.html (netlify/functions/careers.mjs). CVs go to info@ as email attachments; only the file name is stored here.
create table if not exists public.job_applications (
  id uuid primary key default gen_random_uuid(),
  ref text not null unique default ('J-' || upper(substr(md5(random()::text), 1, 6))),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  role text not null,
  name text not null,
  email text not null,
  phone text,
  country text,
  setup text,
  languages text,
  link text,
  cv_name text,
  message text,
  lang text not null default 'en',
  status text not null default 'new' check (status in ('new','shortlisted','interview','hired','rejected')),
  notes text
);
alter table public.job_applications enable row level security;
drop policy if exists job_applications_admin on public.job_applications;
create policy job_applications_admin on public.job_applications for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop trigger if exists job_applications_touch on public.job_applications;
create trigger job_applications_touch before update on public.job_applications for each row execute function public.touch_updated_at();

create or replace function public.server_add_application(p_secret text, p_data jsonb) returns text
language plpgsql security definer set search_path to '' as $$
declare v_ref text;
begin
  if p_secret is null or p_secret <> (select value from private.settings where name = 'server_secret') then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  if coalesce(trim(p_data->>'name'),'') = '' or coalesce(trim(p_data->>'role'),'') = '' or (p_data->>'email') !~ '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$' then
    raise exception 'missing fields' using errcode = '22023';
  end if;
  insert into public.job_applications (role, name, email, phone, country, setup, languages, link, cv_name, message, lang)
  values (left(p_data->>'role',80), left(trim(p_data->>'name'),120), lower(trim(p_data->>'email')), nullif(left(p_data->>'phone',60),''),
          nullif(left(p_data->>'country',80),''), nullif(left(p_data->>'setup',60),''), nullif(left(p_data->>'languages',200),''),
          nullif(left(p_data->>'link',300),''), nullif(left(p_data->>'cv_name',200),''), nullif(left(p_data->>'message',3000),''),
          coalesce(nullif(p_data->>'lang',''),'en'))
  returning ref into v_ref;
  return v_ref;
end $$;
revoke all on function public.server_add_application(text, jsonb) from public;
grant execute on function public.server_add_application(text, jsonb) to anon, authenticated;
