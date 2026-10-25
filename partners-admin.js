// Team admin: Partners (B2B offices). Add an office after KYC, send its invite, manage partner orders and the partner price list.
(function(){
  const $=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const money=(n,c)=>{try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c||'MYR',currencyDisplay:'code',maximumFractionDigits:2}).format(n)}catch(e){return (c||'')+' '+n}};
  const fmt=d=>d?new Date(d).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'}):'';
  const ST={submitted:'Received',invoiced:'Invoiced (unpaid)',paid:'Paid',in_progress:'In progress',completed:'Completed',cancelled:'Cancelled'};
  const CLS={submitted:'s-docs_needed',invoiced:'s-review',paid:'s-paid',in_progress:'s-filed',completed:'s-delivered',cancelled:'s-cancelled'};
  const CAT={formation:'Company formation',established:'Established companies',addon:'Add-on services',visa:'Visas & permits',other:'Other services'};
  let sb=null,view='orders',partners=[],orders=[],prices=[],docs={},openId=null,fP='',fS='open';
  const flash=(m,bad)=>{const x=$('adMsg');x.hidden=false;x.textContent=m;x.className='ac-msg'+(bad?' bad':'');clearTimeout(flash.t);flash.t=setTimeout(()=>x.hidden=true,4500);};
  const token=async()=>(await sb.auth.getSession()).data.session.access_token;
  const fn=async body=>{const r=await fetch('/.netlify/functions/partner',{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+await token()},body:JSON.stringify(body)});const j=await r.json().catch(()=>({}));if(!r.ok)throw new Error(j.error||('Error '+r.status));return j;};

  async function load(){
    const [p,o,pr]=await Promise.all([sb.from('partners').select('*').order('company'),sb.from('partner_orders').select('*').order('created_at',{ascending:false}).limit(1000),sb.from('partner_prices').select('*').order('sort')]);
    if(p.error){$('ptBody').innerHTML='<p class="ac-none">Partners aren\'t set up in the database yet. Run supabase/migrations/20261025_partners_b2b.sql in Supabase, then reload.</p>';return;}
    partners=p.data||[];orders=o.data||[];prices=pr.data||[];render();
  }
  async function loadDocs(id){const {data}=await sb.from('partner_order_docs').select('*').eq('order_id',id).order('created_at');docs[id]=data||[];render();}
  const pname=id=>{const p=partners.find(x=>x.id===id);return p?p.company:'?';};

  function render(){
    const due=orders.filter(o=>o.status==='invoiced').length,newO=orders.filter(o=>o.status==='submitted').length;
    $('ptBody').innerHTML='<div class="ld-stats rf-st"><div class="ld-stat"><b>'+partners.filter(p=>p.status==='active').length+'</b><span>Active partners</span></div><div class="ld-stat"><b>'+newO+'</b><span>New orders to invoice</span></div><div class="ld-stat"><b>'+due+'</b><span>Invoices unpaid</span></div><div class="ld-stat"><b>'+prices.filter(p=>p.active&&p.price!=null).length+' / '+prices.length+'</b><span>Services on the price list</span></div></div>'+
      '<div class="ad-tabs pt-sub">'+[['orders','Orders'],['partners','Partner offices'],['prices','Price list']].map(([k,v])=>'<button type="button" data-v="'+k+'" aria-selected="'+(view===k)+'">'+v+'</button>').join('')+'</div>'+({orders:vOrders,partners:vPartners,prices:vPrices}[view])();
  }
  function vPartners(){
    return '<details class="ad-new"'+(partners.length?'':' open')+'><summary>Add a partner office (after KYC)</summary><form id="ptAdd" class="ad-form"><input name="company" required placeholder="Company name"><input name="contact_name" placeholder="Contact person"><input name="email" type="email" required placeholder="Login email"><input name="phone" placeholder="WhatsApp"><input name="country" placeholder="Country"><input name="city" placeholder="City"><input name="cr_number" placeholder="Commercial registration no."><input name="kyc_date" type="date" title="KYC completed on"><input name="notes" placeholder="Notes (internal)"><button class="btn solid small" type="submit">Add partner</button></form><p class="ld-hint">After adding, press <b>Send invite</b>. The office creates its login at account.html with this email and lands in its partner portal.</p></details>'+
      (partners.length?'<div class="rf-table"><table><thead><tr><th>Office</th><th>Contact</th><th>KYC</th><th>Orders</th><th>Unpaid</th><th></th></tr></thead><tbody>'+partners.map(p=>{const os=orders.filter(o=>o.partner_id===p.id);const un=os.filter(o=>o.status==='invoiced');
        return '<tr class="'+(p.status!=='active'?'rf-paused':'')+'"><td><b>'+esc(p.company)+'</b><br><small class="ltr">'+esc(p.code)+'</small> · <small>'+esc([p.city,p.country].filter(Boolean).join(', '))+'</small>'+(p.cr_number?'<br><small>CR '+esc(p.cr_number)+'</small>':'')+'</td><td>'+esc(p.contact_name||'')+'<br><a href="mailto:'+esc(p.email)+'">'+esc(p.email)+'</a>'+(p.phone?'<br><a target="_blank" rel="noopener" href="https://wa.me/'+String(p.phone).replace(/\D/g,'')+'">'+esc(p.phone)+'</a>':'')+'</td><td>'+(p.kyc_date?fmt(p.kyc_date):'<span class="ac-badge s-docs_needed">Missing</span>')+'</td><td>'+os.length+'</td><td class="ltr">'+(un.length?money(un.reduce((t,o)=>t+Number(o.total),0),un[0].currency):'–')+'</td><td><div class="rf-acts"><button class="btn solid small" data-invite="'+p.id+'">Send invite</button><a class="ac-link" target="_blank" href="invoice.html?statement=1&p='+p.id+'">Statement</a><button class="ac-link'+(p.status==='active'?' danger':'')+'" data-pstat="'+p.id+'">'+(p.status==='active'?'Suspend':'Activate')+'</button></div></td></tr>';}).join('')+'</tbody></table></div>':'<p class="ac-none">No partner offices yet.</p>');
  }
  function vOrders(){
    const list=orders.filter(o=>(!fP||o.partner_id===fP)&&(fS==='open'?!['completed','cancelled'].includes(o.status):(!fS||o.status===fS)));
    return '<div class="ad-filter"><select id="ptFP"><option value="">All partners</option>'+partners.map(p=>'<option value="'+p.id+'"'+(p.id===fP?' selected':'')+'>'+esc(p.company)+'</option>').join('')+'</select><select id="ptFS"><option value="open"'+(fS==='open'?' selected':'')+'>Open orders</option>'+Object.entries(ST).map(([k,v])=>'<option value="'+k+'"'+(k===fS?' selected':'')+'>'+v+'</option>').join('')+'<option value=""'+(fS===''?' selected':'')+'>Everything</option></select></div>'+
      (list.length?'<div class="ac-orders">'+list.map(o=>{const open=o.id===openId;
        const head='<button type="button" class="ac-head" data-open="'+o.id+'" aria-expanded="'+open+'"><span class="ac-ref ltr">'+esc(o.ref)+'</span><span class="ac-pkg">'+esc(pname(o.partner_id))+' → '+esc(o.client_name)+'<small>'+esc((o.items||[]).map(i=>i.qty+'× '+i.name_en).join(' · '))+'</small></span><span class="ac-meta">'+fmt(o.created_at)+' · <span class="ltr">'+money(o.total,o.currency)+'</span> · '+(o.pay_method==='usdt'?'USDT':'Bank')+'</span><span class="ac-badge '+CLS[o.status]+'">'+ST[o.status]+'</span></button>';
        if(!open)return '<article class="ac-order">'+head+'</article>';
        const dl=side=>{const L=(docs[o.id]||[]).filter(d=>d.side===side);return L.length?'<ul class="ac-docs">'+L.map(d=>'<li><span class="ac-file">'+esc(d.name)+'<small>'+fmt(d.created_at)+'</small></span><button type="button" class="ac-link" data-dl="'+esc(d.path)+'">Download</button>'+(side==='wizz'?'<button type="button" class="ac-link danger" data-del="'+d.id+'">Delete</button>':'')+'</li>').join('')+'</ul>':'<p class="ac-none">None yet.</p>';};
        return '<article class="ac-order open">'+head+'<div class="ac-body"><div class="ad-form pt-oform"><label>Status <select data-st="'+o.id+'">'+Object.entries(ST).map(([k,v])=>'<option value="'+k+'"'+(k===o.status?' selected':'')+'>'+v+'</option>').join('')+'</select></label><label class="pt-wide">Message to the partner (they see it) <textarea data-note="'+o.id+'" rows="2" maxlength="1000">'+esc(o.note_to_partner||'')+'</textarea></label><label class="pt-chk"><input type="checkbox" id="ptMail" checked> Email the partner about this change</label><button class="btn solid small" data-save="'+o.id+'">Save</button></div>'+
          '<p class="ld-hint">Set to <b>Invoiced</b> to issue the invoice number. Set to <b>Paid</b> when the money arrives. Client: <b>'+esc(o.client_name)+'</b>'+esc([o.client_nationality,o.client_country].filter(Boolean).map(x=>' · '+x).join(''))+(o.client_notes?'<br>Notes: '+esc(o.client_notes):'')+'</p>'+
          '<div class="ac-row"><a class="btn ghost small" target="_blank" href="invoice.html?o='+o.id+'">'+(o.invoice_no?'Invoice '+esc(o.invoice_no):'Order confirmation')+'</a></div>'+
          '<div class="ac-cols"><section><h3>From the partner</h3>'+dl('partner')+'</section><section><h3>Delivered by Wizz</h3>'+dl('wizz')+'<label class="btn ghost ac-up"><input type="file" multiple data-up="'+o.id+'" hidden>Upload company documents</label><p class="ac-upmsg" id="pup-'+o.id+'" hidden></p></section></div></div></article>';}).join('')+'</div>':'<p class="ac-none">No orders here.</p>');
  }
  function vPrices(){
    const groups={};prices.forEach(p=>(groups[p.category]=groups[p.category]||[]).push(p));
    return '<p class="ld-hint">Partners only see services that are <b>On</b> and have a partner price. Retail is the website price, for reference. Prices are per client; government fees follow your usual rules.</p>'+
      Object.entries(groups).map(([c,L])=>'<section class="ad-box"><h3>'+esc(CAT[c]||c)+'</h3><div class="rf-table"><table class="pt-ptable"><thead><tr><th>Service</th><th>Retail (RM)</th><th>Partner price</th><th>Currency</th><th>On</th><th></th></tr></thead><tbody>'+L.map(p=>'<tr data-row="'+p.id+'"><td><input class="pt-n" data-f="name_en" value="'+esc(p.name_en)+'"><input class="pt-n ar" dir="rtl" data-f="name_ar" value="'+esc(p.name_ar||'')+'" placeholder="Arabic name"></td><td class="ltr">'+(p.retail_myr!=null?Number(p.retail_myr).toLocaleString('en-US'):'–')+'</td><td><input type="number" min="0" step="0.01" data-f="price" value="'+(p.price??'')+'" placeholder="Set price"></td><td><select data-f="currency">'+['MYR','USD','SAR','OMR','AED'].map(c=>'<option'+(c===p.currency?' selected':'')+'>'+c+'</option>').join('')+'</select></td><td><input type="checkbox" data-f="active"'+(p.active?' checked':'')+'></td><td><button class="btn solid small" data-psave="'+p.id+'">Save</button></td></tr>').join('')+'</tbody></table></div></section>').join('')+
      '<details class="ad-new"><summary>Add a service to the partner price list</summary><form id="ptNewSvc" class="ad-form"><input name="name_en" required placeholder="Service name (English)"><input name="name_ar" dir="rtl" placeholder="اسم الخدمة"><select name="category">'+Object.entries(CAT).map(([k,v])=>'<option value="'+k+'">'+v+'</option>').join('')+'</select><input name="price" type="number" step="0.01" min="0" required placeholder="Partner price"><select name="currency"><option>MYR</option><option>USD</option><option>SAR</option><option>OMR</option><option>AED</option></select><button class="btn solid small" type="submit">Add service</button></form></details>';
  }

  document.addEventListener('click',async e=>{
    const root=$('tabPartners');if(!root||!root.contains(e.target))return;
    const v=e.target.closest('[data-v]');if(v){view=v.dataset.v;render();return;}
    const o=e.target.closest('[data-open]');if(o){openId=openId===o.dataset.open?null:o.dataset.open;render();if(openId)loadDocs(openId);return;}
    const inv=e.target.closest('[data-invite]');if(inv){const p=partners.find(x=>x.id===inv.dataset.invite);if(!confirm('Email the sign-in instructions to '+p.email+'?'))return;inv.disabled=true;try{await fn({action:'invite',partner_id:p.id});flash('Invite sent to '+p.email+'.');}catch(err){flash('Invite failed: '+err.message,true);}inv.disabled=false;return;}
    const ps=e.target.closest('[data-pstat]');if(ps){const p=partners.find(x=>x.id===ps.dataset.pstat);const st=p.status==='active'?'suspended':'active';if(st==='suspended'&&!confirm('Suspend '+p.company+'? They lose access to the portal and prices.'))return;const {error}=await sb.from('partners').update({status:st}).eq('id',p.id);if(error)return flash(error.message,true);load();return;}
    const sv=e.target.closest('[data-save]');if(sv){const id=sv.dataset.save;const st=root.querySelector('[data-st="'+id+'"]').value,note=root.querySelector('[data-note="'+id+'"]').value.trim(),mail=$('ptMail').checked;
      sv.disabled=true;const {error}=await sb.from('partner_orders').update({status:st,note_to_partner:note||null}).eq('id',id);
      if(error){sv.disabled=false;return flash(error.message,true);}
      if(mail){try{await fn({action:'order_update',order_id:id});flash('Saved and emailed the partner.');}catch(err){flash('Saved, but the email failed: '+err.message,true);}}else flash('Saved.');
      load();return;}
    const pv=e.target.closest('[data-psave]');if(pv){const tr=root.querySelector('[data-row="'+pv.dataset.psave+'"]');const g=f=>tr.querySelector('[data-f="'+f+'"]');
      const price=g('price').value===''?null:Number(g('price').value);const active=g('active').checked;
      if(active&&price==null)return flash('Enter a partner price before switching the service on.',true);
      const {error}=await sb.from('partner_prices').update({name_en:g('name_en').value.trim(),name_ar:g('name_ar').value.trim()||null,price,currency:g('currency').value,active}).eq('id',pv.dataset.psave);
      if(error)return flash(error.message,true);flash('Price saved.');load();return;}
    const dl=e.target.closest('[data-dl]');if(dl){const w=window.open('','_blank');const {data,error}=await sb.storage.from('partner-docs').createSignedUrl(dl.dataset.dl,60);if(error||!data){if(w)w.close();return flash(error?error.message:'Error',true);}if(w)w.location=data.signedUrl;else location.href=data.signedUrl;return;}
    const del=e.target.closest('[data-del]');if(del){if(!confirm('Delete this file?'))return;const d=(docs[openId]||[]).find(x=>x.id===del.dataset.del);await sb.storage.from('partner-docs').remove([d.path]);await sb.from('partner_order_docs').delete().eq('id',d.id);loadDocs(openId);}
  });
  document.addEventListener('change',async e=>{
    if(e.target.id==='ptFP'){fP=e.target.value;render();return;}
    if(e.target.id==='ptFS'){fS=e.target.value;render();return;}
    const inp=e.target.closest&&e.target.closest('#tabPartners [data-up]');if(!inp)return;const id=inp.dataset.up;
    const files=[...inp.files];inp.value='';let ok=0,bad=[];
    for(const f of files){if(f.size>10*1024*1024){bad.push(f.name);continue;}const path=id+'/wizz/'+crypto.randomUUID()+'-'+f.name.replace(/[^\w.\-]+/g,'_').slice(-80);
      const up=await sb.storage.from('partner-docs').upload(path,f,{contentType:f.type||undefined});if(up.error){bad.push(f.name);continue;}
      const ins=await sb.from('partner_order_docs').insert({order_id:id,side:'wizz',path,name:f.name.slice(0,200),size:f.size});if(ins.error){await sb.storage.from('partner-docs').remove([path]);bad.push(f.name);continue;}ok++;}
    flash((ok?ok+' file(s) uploaded. ':'')+(bad.length?'Not uploaded: '+bad.join(', '):''),bad.length>0);loadDocs(id);
  });
  document.addEventListener('submit',async e=>{
    if(e.target.id==='ptAdd'){e.preventDefault();const d=Object.fromEntries(new FormData(e.target));const row={};for(const[k,v]of Object.entries(d))if(String(v).trim())row[k]=String(v).trim();row.email=(row.email||'').toLowerCase();
      const {error}=await sb.from('partners').insert(row);if(error)return flash(error.message.includes('duplicate')?'A partner with this email already exists.':error.message,true);flash(row.company+' added. Now press Send invite.');view='partners';load();return;}
    if(e.target.id==='ptNewSvc'){e.preventDefault();const d=Object.fromEntries(new FormData(e.target));
      const sku='p-'+d.name_en.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40)+'-'+Math.random().toString(36).slice(2,6);
      const {error}=await sb.from('partner_prices').insert({sku,name_en:d.name_en.trim(),name_ar:d.name_ar.trim()||null,category:d.category,price:Number(d.price),currency:d.currency,active:true,sort:900});
      if(error)return flash(error.message,true);flash('Service added and switched on.');load();}
  });
  function start(d){sb=d.sb;load();}
  if(window.wizzAdmin)start(window.wizzAdmin);else document.addEventListener('wizz:admin-ready',e=>start(e.detail));
})();
