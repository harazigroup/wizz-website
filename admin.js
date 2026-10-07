(function(){
  const SB_URL='https://mzkkhotipmgqczavrfqy.supabase.co';
  const SB_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16a2tob3RpcG1ncWN6YXZyZnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTEzNjA5OTEsImV4cCI6MjEwNjkzNjk5MX0.-RX74vfMP8qedH2F7XvBN4OGj_dL8yEX96VlXO8ONA0';
  const $=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const ST={paid:'Paid',docs_needed:'Documents needed',review:'Under review',filed:'Filed',registered:'Company registered',delivered:'Delivered',on_hold:'On hold',cancelled:'Cancelled'};
  const fmtMoney=(n,c)=>{try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c,currencyDisplay:'narrowSymbol'}).format(n)}catch(e){return c+' '+n}};
  const fmtDate=d=>new Date(d).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'});
  const FIELDS=[['full_name','Full name'],['email','Email'],['whatsapp','WhatsApp'],['nationality','Nationality'],['residential_address','Residential address'],['national_id_number','National ID number'],['passport_number','Passport number'],['company_names','Proposed company names'],['business_activity','Business activity'],['owners','Owners'],['brand_model','If selling online'],['notes','Notes']];
  if(!window.supabase){$('adMsg').hidden=false;$('adMsg').textContent='Supabase could not load.';return;}
  const sb=window.supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:true,detectSessionInUrl:true,flowType:'implicit'}});
  let me=null,orders=[],cur=null,docs=[],events=[],rems=[];

  async function gate(){
    const {data:{session}}=await sb.auth.getSession();
    if(!session){$('adGate').hidden=false;$('adGate').innerHTML='<p>Sign in on the <a href="account.html">account page</a> with a team email first, then come back here.</p>';return;}
    me=session.user;
    const {data}=await sb.from('admins').select('email').limit(1);
    if(!data||!data.length){$('adGate').hidden=false;$('adGate').innerHTML='<p><b>'+esc(me.email)+'</b> is not on the team list. Ask an admin to add it.</p>';return;}
    $('adApp').hidden=false;$('adWho').textContent=me.email;loadOrders();
  }
  async function loadOrders(){
    const {data,error}=await sb.from('orders').select('*').order('created_at',{ascending:false}).limit(500);
    if(error)return flash(error.message,true);orders=data||[];renderList();
  }
  function renderList(){
    const q=$('adQ').value.trim().toLowerCase(),f=$('adF').value;
    const L=orders.filter(o=>(!f||o.status===f)&&(!q||[o.order_ref,o.email,o.customer_name,o.package].join(' ').toLowerCase().includes(q)));
    $('adCount').textContent=L.length+' order'+(L.length===1?'':'s');
    $('adList').innerHTML=L.map(o=>'<button type="button" class="ad-row'+(cur&&cur.id===o.id?' on':'')+'" data-id="'+o.id+'"><b class="ltr">'+esc(o.order_ref)+'</b><span>'+esc(o.customer_name||o.email)+'</span><span class="ad-pk">'+esc(o.package)+'</span><span class="ac-badge s-'+o.status+'">'+esc(ST[o.status]||o.status)+'</span><small>'+fmtDate(o.created_at)+' · '+fmtMoney(o.amount,o.currency)+(o.onboarding_at?'':' · no onboarding')+'</small></button>').join('')||'<p class="ac-none">No orders.</p>';
  }
  async function openOrder(id){
    cur=orders.find(o=>o.id===id);if(!cur)return;renderList();
    const [d,e,r]=await Promise.all([sb.from('documents').select('*').eq('order_id',id).order('created_at'),sb.from('order_events').select('*').eq('order_id',id).order('created_at',{ascending:false}),sb.from('reminders').select('*').eq('order_id',id).order('due_date')]);
    docs=d.data||[];events=e.data||[];rems=r.data||[];renderOrder();
  }
  function docRows(side){const L=docs.filter(x=>x.side===side);return L.length?'<ul class="ac-docs">'+L.map(x=>'<li><span class="ac-file">'+esc(x.label?x.label+' · ':'')+esc(x.name)+'<small>'+fmtDate(x.created_at)+' · '+esc(x.uploaded_by||'')+'</small></span><button type="button" class="ac-link" data-dl="'+esc(x.path)+'">Download</button><button type="button" class="ac-link danger" data-del="'+x.id+'">Delete</button></li>').join('')+'</ul>':'<p class="ac-none">None.</p>';}
  function renderOrder(){
    const o=cur,ob=o.onboarding||{};
    $('adDetail').innerHTML='<div class="ad-top"><div><h2 class="ltr">'+esc(o.order_ref)+'</h2><p>'+esc(o.package)+'</p><p class="ad-sub">'+esc(o.customer_name||'')+' · <a href="mailto:'+esc(o.email)+'">'+esc(o.email)+'</a>'+(o.phone?' · <a href="https://wa.me/'+esc(o.phone.replace(/\D/g,''))+'" target="_blank" rel="noopener">'+esc(o.phone)+'</a>':'')+'</p></div><div class="ad-amt">'+fmtMoney(o.amount,o.currency)+'<small>'+fmtDate(o.created_at)+'</small></div></div>'+
      '<section class="ad-box"><h3>Status</h3><div class="ad-form"><select id="adSt">'+Object.keys(ST).map(k=>'<option value="'+k+'"'+(k===o.status?' selected':'')+'>'+ST[k]+'</option>').join('')+'</select><input id="adNote" placeholder="Note for the client\'s history (optional)"><button class="btn solid small" id="adSave" type="button">Update</button></div>'+
      '<label class="ad-lbl">Message shown on the client\'s order<textarea id="adCN" rows="2">'+esc(o.client_note||'')+'</textarea></label><button class="btn ghost small" id="adCNs" type="button">Save message</button></section>'+
      '<section class="ad-box"><h3>Documents from client</h3>'+docRows('client')+'</section>'+
      '<section class="ad-box"><h3>Documents for client</h3>'+docRows('team')+'<div class="ad-form"><input id="adLabel" placeholder="Label, e.g. Certificate of incorporation"><label class="btn ghost small"><input type="file" id="adFile" multiple hidden>Upload</label></div></section>'+
      '<section class="ad-box"><h3>Deadlines</h3>'+(rems.length?'<ul class="ad-rems">'+rems.map(r=>'<li><label><input type="checkbox" data-rem="'+r.id+'"'+(r.done?' checked':'')+'> '+esc(r.title)+' · '+fmtDate(r.due_date)+'</label></li>').join('')+'</ul>':'<p class="ac-none">None.</p>')+'<div class="ad-form"><input id="adRT" placeholder="e.g. Annual report due"><input id="adRD" type="date"><button class="btn ghost small" id="adRA" type="button">Add</button></div></section>'+
      '<section class="ad-box"><h3>Onboarding details</h3>'+(o.onboarding?'<dl class="ad-dl">'+FIELDS.filter(([k])=>ob[k]).map(([k,l])=>'<dt>'+l+'</dt><dd>'+esc(ob[k])+'</dd>').join('')+'</dl>':'<p class="ac-none">Not received yet.</p>')+'</section>'+
      '<section class="ad-box"><h3>History</h3><ul class="ad-ev">'+events.map(e=>'<li><b>'+esc(ST[e.status]||e.status||'Note')+'</b>'+(e.note?' · '+esc(e.note):'')+'<small>'+fmtDate(e.created_at)+' · '+esc(e.created_by||'')+'</small></li>').join('')+'</ul></section>';
  }
  function flash(m,bad){const x=$('adMsg');x.hidden=false;x.className='ac-msg '+(bad?'bad':'good');x.textContent=m;clearTimeout(flash.t);flash.t=setTimeout(()=>x.hidden=true,4000);}

  $('adQ').addEventListener('input',renderList);$('adF').addEventListener('change',renderList);
  $('adList').addEventListener('click',e=>{const b=e.target.closest('[data-id]');if(b)openOrder(b.dataset.id);});
  $('adDetail').addEventListener('click',async e=>{
    if(e.target.id==='adSave'){const st=$('adSt').value,note=$('adNote').value.trim();
      const u=await sb.from('orders').update({status:st}).eq('id',cur.id);if(u.error)return flash(u.error.message,true);
      await sb.from('order_events').insert({order_id:cur.id,status:st,note:note||null,created_by:me.email});cur.status=st;flash('Status updated.');loadOrders();openOrder(cur.id);}
    if(e.target.id==='adCNs'){const v=$('adCN').value.trim();const u=await sb.from('orders').update({client_note:v||null}).eq('id',cur.id);if(u.error)return flash(u.error.message,true);cur.client_note=v;flash('Message saved.');}
    if(e.target.id==='adRA'){const t=$('adRT').value.trim(),d=$('adRD').value;if(!t||!d)return flash('Add a title and a date.',true);const u=await sb.from('reminders').insert({order_id:cur.id,title:t,due_date:d});if(u.error)return flash(u.error.message,true);openOrder(cur.id);}
    const dl=e.target.closest('[data-dl]');if(dl){const w=window.open('','_blank');const {data,error}=await sb.storage.from('docs').createSignedUrl(dl.dataset.dl,60);if(error){if(w)w.close();return flash(error.message,true);}if(w)w.location=data.signedUrl;}
    const del=e.target.closest('[data-del]');if(del){if(!confirm('Delete this file for everyone?'))return;const d=docs.find(x=>x.id===del.dataset.del);await sb.storage.from('docs').remove([d.path]);await sb.from('documents').delete().eq('id',d.id);openOrder(cur.id);}
  });
  $('adDetail').addEventListener('change',async e=>{
    if(e.target.id==='adFile'){const label=$('adLabel').value.trim();let n=0;
      for(const f of e.target.files){const path=cur.id+'/team/'+crypto.randomUUID()+'-'+f.name.replace(/[^\w.\-]+/g,'_').slice(-80);
        const up=await sb.storage.from('docs').upload(path,f,{contentType:f.type||undefined});if(up.error){flash(f.name+': '+up.error.message,true);continue;}
        const ins=await sb.from('documents').insert({order_id:cur.id,side:'team',path,name:f.name.slice(0,200),size:f.size,label:label||null,uploaded_by:me.email});if(ins.error){flash(ins.error.message,true);continue;}n++;}
      if(n)flash(n+' file(s) uploaded. The client can download them now.');openOrder(cur.id);}
    const r=e.target.closest('[data-rem]');if(r){await sb.from('reminders').update({done:r.checked}).eq('id',r.dataset.rem);}
  });
  $('adNew').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.target);
    const ref='WZ-'+new Date().toISOString().slice(2,10).replace(/-/g,'')+'-M'+Math.random().toString(36).slice(2,6).toUpperCase();
    const row={order_ref:ref,email:String(f.get('email')).trim().toLowerCase(),customer_name:f.get('name')||null,package:f.get('package'),amount:+f.get('amount'),currency:String(f.get('currency')).toUpperCase()};
    const {data,error}=await sb.from('orders').insert(row).select().single();if(error)return flash(error.message,true);
    await sb.from('order_events').insert({order_id:data.id,status:'paid',note:'Order added by team',created_by:me.email});
    e.target.reset();$('adNewBox').open=false;flash('Order '+ref+' added. The client sees it when they sign in with '+row.email+'.');await loadOrders();openOrder(data.id);});
  $('adOut').addEventListener('click',async()=>{await sb.auth.signOut();location.replace('account.html');});
  gate();
})();
