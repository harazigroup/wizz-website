-- Wizz referral programme. Safe to run more than once.
-- Anyone signs up for a code; new clients get RM 100 off orders of RM 1,000+ (applied in netlify/functions/checkout.mjs);
-- referrers earn 10% of the amount paid, approved by an admin after the service is completed.
create table if not exists public.referrers (
  id uuid primary key default gen_random_uuid(),
  code text not null unique check (code ~ '^[A-Z0-9]{4,16}$'),
  name text not null, email text not null, phone text, country text,
  payout_method text, payout_details text,
  status text not null default 'active' check (status in ('active','paused')),
  lang text not null default 'en', notes text,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now()
);
create unique index if not exists referrers_email_uq on public.referrers (lower(email));

create table if not exists public.referral_commissions (
  id uuid primary key default gen_random_uuid(),
  code text not null references public.referrers(code) on update cascade,
  source text not null check (source in ('order','manual')),
  source_ref text not null,
  client_name text,
  sale_amount numeric not null check (sale_amount >= 0),
  currency text not null default 'MYR',
  rate numeric not null default 0.10,
  commission numeric not null,
  status text not null default 'pending' check (status in ('pending','approved','paid','void')),
  approved_at timestamptz, paid_at timestamptz, note text,
  created_at timestamptz not null default now(), updated_at timestamptz not null default now(),
  unique (source, source_ref)
);

alter table public.leads  add column if not exists ref_code text;
alter table public.orders add column if not exists ref_code text;
alter table public.orders add column if not exists discount numeric;
alter table public.quotes add column if not exists ref_code text;

alter table public.referrers enable row level security;
alter table public.referral_commissions enable row level security;
drop policy if exists referrers_admin on public.referrers;
create policy referrers_admin on public.referrers for all to authenticated using (public.is_admin()) with check (public.is_admin());
drop policy if exists refcom_admin on public.referral_commissions;
create policy refcom_admin on public.referral_commissions for all to authenticated using (public.is_admin()) with check (public.is_admin());

drop trigger if exists referrers_touch on public.referrers;
create trigger referrers_touch before update on public.referrers for each row execute function public.touch_updated_at();
drop trigger if exists refcom_touch on public.referral_commissions;
create trigger refcom_touch before update on public.referral_commissions for each row execute function public.touch_updated_at();

create or replace function public.refcom_status_times() returns trigger language plpgsql set search_path to '' as $$
begin
  if new.status = 'approved' and new.approved_at is null then new.approved_at := now(); end if;
  if new.status = 'paid' then
    if new.approved_at is null then new.approved_at := now(); end if;
    if new.paid_at is null then new.paid_at := now(); end if;
  end if;
  return new;
end $$;
drop trigger if exists refcom_times on public.referral_commissions;
create trigger refcom_times before insert or update on public.referral_commissions for each row execute function public.refcom_status_times();

-- Public: is this code valid? No personal data returned.
create or replace function public.public_check_ref(p_code text) returns boolean
language sql security definer set search_path to '' stable as $$
  select exists (select 1 from public.referrers where code = upper(trim(p_code)) and status = 'active');
$$;
revoke all on function public.public_check_ref(text) from public;
grant execute on function public.public_check_ref(text) to anon, authenticated;

-- Server: sign up. Returns 'new|CODE' or 'exists|CODE'. The server emails the code; an existing code is never shown in the browser.
create or replace function public.server_referral_signup(p_secret text, p_data jsonb) returns text
language plpgsql security definer set search_path to '' as $$
declare v_code text; v_base text; v_email text := lower(trim(p_data->>'email')); v_try int := 0;
begin
  if p_secret is null or p_secret <> (select value from private.settings where name = 'server_secret') then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  if v_email !~ '^[^@\s]+@[^@\s]+\.[^@\s]{2,}$' or coalesce(trim(p_data->>'name'),'') = '' then
    raise exception 'missing fields' using errcode = '22023';
  end if;
  select code into v_code from public.referrers where lower(email) = v_email;
  if v_code is not null then return 'exists|' || v_code; end if;
  v_base := left(regexp_replace(upper(split_part(trim(p_data->>'name'), ' ', 1)), '[^A-Z]', '', 'g'), 8);
  if length(v_base) < 3 then v_base := 'WIZZ'; end if;
  loop
    v_try := v_try + 1;
    v_code := v_base || lpad((floor(random() * 90) + 10)::int::text, 2, '0');
    exit when not exists (select 1 from public.referrers where code = v_code);
    if v_try > 30 then v_code := v_base || (floor(random() * 9000) + 1000)::int::text; exit; end if;
  end loop;
  insert into public.referrers (code, name, email, phone, country, payout_method, payout_details, lang)
  values (v_code, left(trim(p_data->>'name'),120), v_email, nullif(left(p_data->>'phone',60),''), nullif(left(p_data->>'country',80),''),
          nullif(left(p_data->>'payout_method',40),''), nullif(left(p_data->>'payout_details',300),''), coalesce(nullif(p_data->>'lang',''),'en'));
  return 'new|' || v_code;
end $$;

-- Server: a referrer's own summary, only when code and email match.
create or replace function public.server_referral_stats(p_secret text, p_code text, p_email text) returns jsonb
language plpgsql security definer set search_path to '' stable as $$
declare r public.referrers; v jsonb;
begin
  if p_secret is null or p_secret <> (select value from private.settings where name = 'server_secret') then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  select * into r from public.referrers where code = upper(trim(p_code)) and lower(email) = lower(trim(p_email));
  if r.id is null then return null; end if;
  select jsonb_build_object(
    'code', r.code, 'name', r.name,
    'enquiries', (select count(*) from public.leads where ref_code = r.code),
    'orders', (select count(*) from public.orders where ref_code = r.code),
    'commissions', coalesce((select jsonb_agg(jsonb_build_object('currency', currency, 'status', status, 'amount', amt, 'count', n))
       from (select currency, status, sum(commission) amt, count(*) n from public.referral_commissions where code = r.code and status <> 'void' group by 1,2) s), '[]'::jsonb)
  ) into v;
  return v;
end $$;

-- Leads keep a valid referral code.
create or replace function public.server_add_lead(p_secret text, p_lead jsonb)
 returns text language plpgsql security definer set search_path to '' as $function$
declare v_id uuid; v_ref text; v_score int := 0; v_pri text; v_code text;
begin
  if p_secret is null or p_secret <> (select value from private.settings where name = 'server_secret') then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  if coalesce(p_lead->>'phone','') <> '' then v_score := v_score + 20; end if;
  if coalesce(p_lead->>'mkt','') not in ('', 'Not sure yet', 'Other / not sure yet') then v_score := v_score + 20; end if;
  if length(coalesce(p_lead->>'act','')) > 25 then v_score := v_score + 15; end if;
  if coalesce(p_lead->>'services','') ~* '(formation|company|acquisition|banking|amazon|saudi|mm2h)' then v_score := v_score + 25; end if;
  if length(coalesce(p_lead->>'msg','')) > 40 then v_score := v_score + 10; end if;
  if coalesce(p_lead->>'brand','') <> '' then v_score := v_score + 10; end if;
  select code into v_code from public.referrers where code = upper(trim(coalesce(p_lead->>'ref',''))) and status = 'active';
  if v_code is not null then v_score := v_score + 10; end if;
  v_pri := case when v_score >= 70 then 'hot' when v_score >= 40 then 'warm' else 'cold' end;
  insert into public.leads (source, name, email, phone, nationality, residence, market, activity, services, owners, brand, message, lang, score, priority, next_follow_up, ref_code)
  values ('website', left(p_lead->>'name',200), lower(left(p_lead->>'email',200)), nullif(left(p_lead->>'phone',60),''),
          nullif(left(p_lead->>'nat',100),''), nullif(left(p_lead->>'res',100),''), nullif(left(p_lead->>'mkt',100),''),
          nullif(left(p_lead->>'act',300),''), nullif(left(p_lead->>'services',300),''), nullif(left(p_lead->>'own',100),''),
          nullif(left(p_lead->>'brand',100),''), nullif(left(p_lead->>'msg',4000),''), coalesce(nullif(p_lead->>'lang',''),'en'),
          v_score, v_pri, current_date, v_code)
  returning id, ref into v_id, v_ref;
  insert into public.lead_events (lead_id, kind, note, created_by)
  values (v_id, 'created', 'Website enquiry' || coalesce(' · referral ' || v_code, ''), 'website');
  return v_ref || '|' || v_pri || '|' || v_score;
end; $function$;

-- Orders keep the code and discount, and open a pending 10% commission on the amount paid (not for self-referrals).
create or replace function public.server_record_order(p_secret text, p_order jsonb)
 returns uuid language plpgsql security definer set search_path to '' as $function$
declare v_id uuid; v_code text; v_amt numeric;
begin
  if p_secret is null or p_secret <> (select value from private.settings where name = 'server_secret') then
    raise exception 'not allowed' using errcode = '42501';
  end if;
  select code into v_code from public.referrers where code = upper(trim(coalesce(p_order->>'ref_code',''))) and status = 'active';
  v_amt := (p_order->>'amount')::numeric;
  insert into public.orders (order_ref, stripe_session_id, email, customer_name, phone, package, items, amount, currency, ref_code, discount)
  values (p_order->>'order_ref', p_order->>'stripe_session_id', lower(p_order->>'email'), p_order->>'customer_name', p_order->>'phone',
          coalesce(p_order->>'package',''), coalesce(p_order->'items','[]'::jsonb), v_amt, upper(p_order->>'currency'),
          v_code, nullif(p_order->>'discount','')::numeric)
  on conflict (order_ref) do update set
    stripe_session_id = coalesce(excluded.stripe_session_id, public.orders.stripe_session_id),
    customer_name = coalesce(public.orders.customer_name, excluded.customer_name),
    phone = coalesce(public.orders.phone, excluded.phone),
    ref_code = coalesce(public.orders.ref_code, excluded.ref_code),
    discount = coalesce(public.orders.discount, excluded.discount)
  returning id into v_id;
  insert into public.order_events (order_id, status, note, created_by)
  select v_id, 'paid', 'Payment received' || coalesce(' · referral ' || v_code, ''), 'system'
  where not exists (select 1 from public.order_events e where e.order_id = v_id and e.status = 'paid');
  if v_code is not null and not exists (select 1 from public.referrers where code = v_code and lower(email) = lower(p_order->>'email')) then
    insert into public.referral_commissions (code, source, source_ref, client_name, sale_amount, currency, rate, commission, note)
    values (v_code, 'order', p_order->>'order_ref', p_order->>'customer_name', v_amt, upper(p_order->>'currency'), 0.10, round(v_amt * 0.10, 2),
            'Approve when the service is completed')
    on conflict (source, source_ref) do nothing;
  end if;
  return v_id;
end; $function$;
