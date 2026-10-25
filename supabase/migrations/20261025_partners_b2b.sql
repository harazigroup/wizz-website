-- B2B partner offices (wholesale). Wizz adds each office after KYC (Admin → Partners); the office then creates its login at account.html
-- with the same email and uses partner.html: partner price list, orders per end client, documents, invoices and statements.
-- Payment is by invoice (bank transfer or USDT). Run once in Supabase → SQL Editor.

create table if not exists public.partners (
  id uuid primary key default gen_random_uuid(),
  code text not null unique default ('P-' || upper(substr(md5(random()::text), 1, 5))),
  company text not null,
  contact_name text,
  email text not null unique check (email = lower(email)),
  phone text,
  country text,
  city text,
  cr_number text,
  kyc_date date,
  status text not null default 'active' check (status in ('active','suspended')),
  notes text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists public.partner_prices (
  id uuid primary key default gen_random_uuid(),
  sku text not null unique,
  category text not null default 'formation',
  name_en text not null,
  name_ar text,
  retail_myr numeric,
  price numeric check (price is null or price >= 0),
  currency text not null default 'MYR',
  active boolean not null default false,
  sort int not null default 100,
  note_en text,
  note_ar text,
  updated_at timestamptz not null default now()
);

create table if not exists public.partner_orders (
  id uuid primary key default gen_random_uuid(),
  ref text not null unique default ('PO-' || to_char(now(), 'YYMM') || '-' || upper(substr(md5(random()::text), 1, 4))),
  partner_id uuid not null references public.partners(id),
  client_name text not null,
  client_nationality text,
  client_country text,
  client_notes text,
  items jsonb not null default '[]'::jsonb,
  total numeric not null default 0,
  currency text not null default 'MYR',
  pay_method text not null default 'bank' check (pay_method in ('bank','usdt')),
  status text not null default 'submitted' check (status in ('submitted','invoiced','paid','in_progress','completed','cancelled')),
  invoice_no text unique,
  invoiced_at timestamptz,
  paid_at timestamptz,
  completed_at timestamptz,
  note_to_partner text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists partner_orders_partner on public.partner_orders(partner_id, created_at desc);

create table if not exists public.partner_order_docs (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.partner_orders(id) on delete cascade,
  side text not null check (side in ('partner','wizz')),
  path text not null unique,
  name text not null,
  size int,
  created_at timestamptz not null default now()
);

-- who is signed in
create or replace function public.my_partner_id() returns uuid
language sql stable security definer set search_path to '' as $$
  select p.id from public.partners p where p.email = lower(coalesce(auth.jwt() ->> 'email', '')) and p.status = 'active';
$$;
create or replace function public.owns_partner_order(p_order uuid) returns boolean
language sql stable security definer set search_path to '' as $$
  select exists (select 1 from public.partner_orders o where o.id = p_order and o.partner_id = public.my_partner_id());
$$;
create or replace function public.owns_partner_path(p_folder text) returns boolean
language plpgsql stable security definer set search_path to '' as $$
begin
  return public.owns_partner_order(p_folder::uuid);
exception when others then return false;
end $$;
grant execute on function public.owns_partner_path(text) to authenticated;
grant execute on function public.my_partner_id() to authenticated;
grant execute on function public.owns_partner_order(uuid) to authenticated;

-- prices and totals always come from the price list, never from the browser
create or replace function public.partner_order_before_insert() returns trigger
language plpgsql security definer set search_path to '' as $$
declare it jsonb; p public.partner_prices; q int; out_items jsonb := '[]'::jsonb; tot numeric := 0; cur text;
begin
  if not public.is_admin() then
    new.partner_id := public.my_partner_id();
    if new.partner_id is null then raise exception 'not an active partner' using errcode = '42501'; end if;
    new.status := 'submitted'; new.invoice_no := null; new.note_to_partner := null;
  end if;
  if coalesce(trim(new.client_name), '') = '' then raise exception 'client name required' using errcode = '22023'; end if;
  for it in select * from jsonb_array_elements(coalesce(new.items, '[]'::jsonb)) loop
    select * into p from public.partner_prices where sku = it->>'sku' and active and price is not null;
    if not found then raise exception 'unknown or inactive service: %', it->>'sku' using errcode = '22023'; end if;
    q := greatest(1, least(50, coalesce((it->>'qty')::int, 1)));
    if cur is not null and cur <> p.currency then raise exception 'one currency per order' using errcode = '22023'; end if;
    cur := p.currency;
    out_items := out_items || jsonb_build_object('sku', p.sku, 'name_en', p.name_en, 'name_ar', p.name_ar, 'qty', q, 'unit', p.price);
    tot := tot + q * p.price;
  end loop;
  if jsonb_array_length(out_items) = 0 then raise exception 'choose at least one service' using errcode = '22023'; end if;
  new.items := out_items; new.total := tot; new.currency := coalesce(cur, 'MYR');
  return new;
end $$;
drop trigger if exists partner_order_bi on public.partner_orders;
create trigger partner_order_bi before insert on public.partner_orders for each row execute function public.partner_order_before_insert();

-- status dates and invoice numbers
create or replace function public.partner_order_status_times() returns trigger
language plpgsql set search_path to '' as $$
begin
  if new.status is distinct from old.status then
    if new.status = 'invoiced' and new.invoiced_at is null then new.invoiced_at := now(); end if;
    if new.status = 'paid' and new.paid_at is null then new.paid_at := now(); end if;
    if new.status = 'completed' and new.completed_at is null then new.completed_at := now(); end if;
  end if;
  if new.status in ('invoiced','paid','in_progress','completed') and new.invoice_no is null then
    new.invoice_no := 'INV-' || to_char(now(), 'YYMM') || '-' || upper(substr(md5(random()::text), 1, 5));
    new.invoiced_at := coalesce(new.invoiced_at, now());
  end if;
  return new;
end $$;
drop trigger if exists partner_order_bu on public.partner_orders;
create trigger partner_order_bu before update on public.partner_orders for each row execute function public.partner_order_status_times();
drop trigger if exists partner_orders_touch on public.partner_orders;
create trigger partner_orders_touch before update on public.partner_orders for each row execute function public.touch_updated_at();
drop trigger if exists partners_touch on public.partners;
create trigger partners_touch before update on public.partners for each row execute function public.touch_updated_at();
drop trigger if exists partner_prices_touch on public.partner_prices;
create trigger partner_prices_touch before update on public.partner_prices for each row execute function public.touch_updated_at();

-- row-level security
alter table public.partners enable row level security;
alter table public.partner_prices enable row level security;
alter table public.partner_orders enable row level security;
alter table public.partner_order_docs enable row level security;

drop policy if exists partners_read on public.partners;
create policy partners_read on public.partners for select to authenticated
  using (email = lower(coalesce((select auth.jwt()) ->> 'email', '')) or (select public.is_admin()));
drop policy if exists partners_admin on public.partners;
create policy partners_admin on public.partners for all to authenticated using ((select public.is_admin())) with check ((select public.is_admin()));

drop policy if exists partner_prices_read on public.partner_prices;
create policy partner_prices_read on public.partner_prices for select to authenticated
  using ((active and price is not null and (select public.my_partner_id()) is not null) or (select public.is_admin()));
drop policy if exists partner_prices_admin on public.partner_prices;
create policy partner_prices_admin on public.partner_prices for all to authenticated using ((select public.is_admin())) with check ((select public.is_admin()));

drop policy if exists partner_orders_read on public.partner_orders;
create policy partner_orders_read on public.partner_orders for select to authenticated
  using (partner_id = (select public.my_partner_id()) or (select public.is_admin()));
drop policy if exists partner_orders_insert on public.partner_orders;
create policy partner_orders_insert on public.partner_orders for insert to authenticated
  with check ((select public.my_partner_id()) is not null or (select public.is_admin()));
drop policy if exists partner_orders_admin on public.partner_orders;
create policy partner_orders_admin on public.partner_orders for update to authenticated using ((select public.is_admin())) with check ((select public.is_admin()));

drop policy if exists partner_docs_read on public.partner_order_docs;
create policy partner_docs_read on public.partner_order_docs for select to authenticated
  using ((select public.is_admin()) or public.owns_partner_order(order_id));
drop policy if exists partner_docs_insert on public.partner_order_docs;
create policy partner_docs_insert on public.partner_order_docs for insert to authenticated
  with check ((select public.is_admin()) or (side = 'partner' and public.owns_partner_order(order_id)));
drop policy if exists partner_docs_delete on public.partner_order_docs;
create policy partner_docs_delete on public.partner_order_docs for delete to authenticated
  using ((select public.is_admin()) or (side = 'partner' and public.owns_partner_order(order_id)));

-- private file storage: partner-docs/<order id>/<partner|wizz>/<file>
insert into storage.buckets (id, name, public, file_size_limit)
values ('partner-docs', 'partner-docs', false, 10485760) on conflict (id) do nothing;
drop policy if exists "partner docs read" on storage.objects;
create policy "partner docs read" on storage.objects for select to authenticated
  using (bucket_id = 'partner-docs' and ((select public.is_admin()) or public.owns_partner_path((storage.foldername(name))[1])));
drop policy if exists "partner docs upload" on storage.objects;
create policy "partner docs upload" on storage.objects for insert to authenticated
  with check (bucket_id = 'partner-docs' and ((select public.is_admin()) or ((storage.foldername(name))[2] = 'partner' and public.owns_partner_path((storage.foldername(name))[1]))));
drop policy if exists "partner docs delete" on storage.objects;
create policy "partner docs delete" on storage.objects for delete to authenticated
  using (bucket_id = 'partner-docs' and ((select public.is_admin()) or ((storage.foldername(name))[2] = 'partner' and public.owns_partner_path((storage.foldername(name))[1]))));

-- starting price list: every service, hidden until you enter a partner price and switch it on in Admin → Partners → Price list
insert into public.partner_prices (sku, category, name_en, name_ar, retail_myr, sort) values
('us-starter','formation','United States - Starter','الولايات المتحدة - الأساسية',1199,10),
('us-business','formation','United States - Business','الولايات المتحدة - الأعمال',7899,20),
('us-complete','formation','United States - Complete','الولايات المتحدة - الشاملة',12099,30),
('uk-starter','formation','United Kingdom - Starter','المملكة المتحدة - الأساسية',1299,40),
('uk-business','formation','United Kingdom - Business','المملكة المتحدة - الأعمال',2499,50),
('uk-complete','formation','United Kingdom - Complete','المملكة المتحدة - الشاملة',5399,60),
('ca-starter','formation','Canada - Starter','كندا - الأساسية',3099,70),
('ca-business','formation','Canada - Business','كندا - الأعمال',4999,80),
('ee-starter','formation','Estonia - Starter','إستونيا - الأساسية',3099,90),
('ee-business','formation','Estonia - Business','إستونيا - الأعمال',7500,100),
('pl-standard','formation','Poland - Standard','بولندا - القياسية',7099,110),
('pl-full-setup','formation','Poland - Full setup','بولندا - الإعداد الكامل',10399,120),
('fr-starter','formation','France - Starter','فرنسا - الأساسية',3499,130),
('fr-business','formation','France - Business','فرنسا - الأعمال',5799,140),
('nl-starter','formation','Netherlands - Starter','هولندا - الأساسية',10399,150),
('nl-business','formation','Netherlands - Business','هولندا - الأعمال',14499,160),
('ae-deposit','formation','UAE - Free zone, no visa','الإمارات - منطقة حرة بدون تأشيرة',10399,170),
('ae-deposit-visa','formation','UAE - Free zone + 1 visa','الإمارات - منطقة حرة + تأشيرة واحدة',20799,180),
('sa-assessment','formation','Saudi Arabia - Market-entry assessment','السعودية - تقييم دخول السوق',500,190),
('sa-company-setup','formation','Saudi Arabia - Company setup','السعودية - تأسيس الشركة',12999,200),
('om-company-setup','formation','Oman - Company setup','سلطنة عُمان - تأسيس الشركة',3500,210),
('om-setup-investor-visa','formation','Oman - Setup + investor visa','سلطنة عُمان - التأسيس + تأشيرة مستثمر',7500,220),
('my-starter','formation','Malaysia - Starter','ماليزيا - الأساسية',4099,230),
('my-business','formation','Malaysia - Business','ماليزيا - الأعمال',7499,240),
('th-company-setup','formation','Thailand - Company setup','تايلاند - تأسيس الشركة',6199,250),
('th-setup-compliance','formation','Thailand - Setup + compliance','تايلاند - التأسيس + الامتثال',10399,260),
('th-work-permit-2-years','formation','Thailand - Work permit, 2 years','تايلاند - تصريح عمل لمدة سنتين',18000,270),
('pk-starter','formation','Pakistan - Starter','باكستان - الأساسية',3299,280),
('pk-business','formation','Pakistan - Business','باكستان - الأعمال',5799,290),
('acq-pk','established','Established company - Pakistan','شركة قائمة - باكستان',7999,300),
('acq-eg','established','Established company - Egypt','شركة قائمة - مصر',9999,310),
('acq-my','established','Established company - Malaysia','شركة قائمة - ماليزيا',11999,320),
('acq-uk','established','Established company - United Kingdom','شركة قائمة - المملكة المتحدة',13999,330),
('addon-amazon','addon','Amazon seller account application support','دعم طلب حساب بائع أمازون',1999,340),
('addon-marketplace','addon','Marketplace onboarding: Noon, TikTok Shop, Shopee, Lazada and others','تسجيل في المنصات: نون وتيك توك شوب وشوبي ولازادا وغيرها',300,350)
on conflict (sku) do nothing;
