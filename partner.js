// Partner (B2B office) portal on partner.html. Sign-in happens on account.html (same Supabase session).
// Reads with row-level security: an office sees only its own row, its own orders and the active partner price list.
(function(){
  const SB_URL='https://mzkkhotipmgqczavrfqy.supabase.co';
  const SB_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16a2tob3RpcG1ncWN6YXZyZnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTEzNjA5OTEsImV4cCI6MjEwNjkzNjk5MX0.-RX74vfMP8qedH2F7XvBN4OGj_dL8yEX96VlXO8ONA0';
  const $=id=>document.getElementById(id);
  const ar=()=>document.documentElement.lang==='ar';const T=(en,a)=>ar()?a:en;
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const money=(n,c)=>{try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c||'MYR',currencyDisplay:'code',maximumFractionDigits:2}).format(n)}catch(e){return (c||'')+' '+n}};
  const fmtDate=d=>d?new Date(d).toLocaleDateString(ar()?'ar':'en-GB',{day:'numeric',month:'short',year:'numeric'}):'';
  const STEPS=['submitted','invoiced','paid','in_progress','completed'];
  const LAB={submitted:['Received','تم الاستلام'],invoiced:['Invoice issued','صدرت الفاتورة'],paid:['Paid','مدفوع'],in_progress:['In progress','قيد التنفيذ'],completed:['Completed','مكتمل'],cancelled:['Cancelled','ملغى']};
  const lab=s=>(LAB[s]||[s,s])[ar()?1:0];
  const CAT={formation:['Company formation','تأسيس الشركات'],established:['Established companies','شركات قائمة'],addon:['Add-on services','خدمات إضافية'],visa:['Visas & permits','التأشيرات والتصاريح'],other:['Other services','خدمات أخرى']};
  const cat=c=>(CAT[c]||[c,c])[ar()?1:0];
  const nm=i=>(ar()&&i.name_ar)?i.name_ar:i.name_en;
  const MAX=10*1024*1024, TYPES=['application/pdf','image/jpeg','image/png','image/webp','image/heic','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  const box=$('ptApp');
  if(!window.supabase){box.innerHTML='<p class="ac-msg bad">'+T('The portal could not load. Check your connection and refresh.','تعذّر تحميل البوابة. تحقق من اتصالك وحدّث الصفحة.')+'</p>';return;}
  const sb=window.supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:true,detectSessionInUrl:true,flowType:'implicit'}});
  let user=null,me=null,prices=[],orders=[],docs={},tab='orders',openId=null,cart={},busy=false;
  const flash=(m,bad)=>{const x=$('ptMsg');x.hidden=false;x.className='ac-msg '+(bad?'bad':'good');x.textContent=m;clearTimeout(flash.t);flash.t=setTimeout(()=>x.hidden=true,5000);};

  async function boot(){
    const {data}=await sb.auth.getSession();
    if(!data.session){location.replace('account.html?next=partner');return;}
    user=data.session.user;
    const p=await sb.from('partners').select('*').limit(1);
    me=(p.data||[])[0]||null;
    if(!me||me.status!=='active'){render();return;}
    const h=decodeURIComponent(location.hash.slice(1));
    await load();
    if(h){const o=orders.find(x=>x.ref===h);if(o){openId=o.id;loadDocs(o.id);}}
    render();
  }
  async function load(){
    const [pr,or]=await Promise.all([
      sb.from('partner_prices').select('sku,category,name_en,name_ar,price,currency,sort,note_en,note_ar').order('sort'),
      sb.from('partner_orders').select('*').order('created_at',{ascending:false}).limit(500)]);
    if(pr.error||or.error){flash((pr.error||or.error).message,true);}
    prices=pr.data||[];orders=or.data||[];
  }
  async function loadDocs(id){const {data}=await sb.from('partner_order_docs').select('*').eq('order_id',id).order('created_at');docs[id]=data||[];render();}

  // ---------- render
  function render(){
    if(!me){box.innerHTML='<div class="ac-card pt-gate"><h1>'+T('Partner portal','بوابة الشركاء')+'</h1><p>'+T('This email ('+esc(user.email)+') is not linked to a partner account. Partner accounts are opened by our team after KYC.','هذا البريد ('+esc(user.email)+') غير مرتبط بحساب شريك. نفتح حسابات الشركاء بعد إتمام التحقق (KYC).')+'</p><div class="ac-row"><a class="btn solid" href="partners.html">'+T('Become a partner','كن شريكاً')+'</a><a class="btn ghost" href="account.html">'+T('My client account','حساب العميل')+'</a><button class="ac-link" id="ptOut" type="button">'+T('Sign out','تسجيل الخروج')+'</button></div></div>';return;}
    if(me.status!=='active'){box.innerHTML='<div class="ac-card pt-gate"><h1>'+esc(me.company)+'</h1><p>'+T('Your partner account is paused. Please contact us on WhatsApp.','حساب الشريك موقوف مؤقتاً. يرجى التواصل معنا عبر واتساب.')+'</p><a class="btn wa" href="https://wa.me/601124477685" target="_blank" rel="noopener">WhatsApp</a></div>';return;}
    const due=orders.filter(o=>o.status==='invoiced'),dueTot=sumBy(due);
    box.innerHTML='<div class="ac-top"><div><p class="eyebrow">'+T('Partner portal','بوابة الشركاء')+' · <span class="ltr">'+esc(me.code)+'</span></p><h1>'+esc(me.company)+'</h1><p class="muted">'+T('Signed in as','مسجّل باسم')+' <b class="ltr">'+esc(user.email)+'</b></p></div><div class="ac-actions"><a class="btn ghost small" href="account.html">'+T('Client account','حساب العميل')+'</a><button class="btn ghost small" id="ptOut" type="button">'+T('Sign out','تسجيل الخروج')+'</button></div></div>'+
      '<div class="ld-stats pt-stats"><div class="ld-stat"><b>'+orders.filter(o=>!['completed','cancelled'].includes(o.status)).length+'</b><span>'+T('Open orders','طلبات جارية')+'</span></div><div class="ld-stat"><b>'+due.length+'</b><span>'+T('Invoices to pay','فواتير مستحقة')+(due.length?' · <span class="ltr">'+esc(dueTot)+'</span>':'')+'</span></div><div class="ld-stat"><b>'+orders.filter(o=>o.status==='completed').length+'</b><span>'+T('Completed','مكتملة')+'</span></div></div>'+
      '<div class="ad-tabs" role="tablist">'+[['orders',T('Orders','الطلبات')],['new',T('New order','طلب جديد')],['prices',T('Price list','قائمة الأسعار')],['statement',T('Statement','كشف الحساب')]].map(([k,v])=>'<button type="button" role="tab" data-tab="'+k+'" aria-selected="'+(tab===k)+'">'+v+'</button>').join('')+'</div>'+
      '<div class="pt-body">'+({orders:vOrders,new:vNew,prices:vPrices,statement:vStatement}[tab])()+'</div>';
  }
  const sumBy=list=>{const t={};list.forEach(o=>t[o.currency]=(t[o.currency]||0)+Number(o.total));return Object.entries(t).map(([c,v])=>money(v,c)).join(' + ')||money(0,'MYR');};
  function steps(st){const i=STEPS.indexOf(st);return '<ol class="ac-steps'+(i<0?' off':'')+'">'+STEPS.map((s,k)=>'<li class="'+(i>=0&&k<i?'done':'')+(k===i?' now':'')+'"><span></span><em>'+esc(lab(s))+'</em></li>').join('')+'</ol>';}
  function docList(id,side){const L=(docs[id]||[]).filter(d=>d.side===side);
    if(!L.length)return '<p class="ac-none">'+(side==='wizz'?T('Nothing yet. Company documents will appear here.','لا يوجد شيء بعد. ستظهر مستندات الشركة هنا.'):T('No files uploaded yet.','لم تُرفع ملفات بعد.'))+'</p>';
    return '<ul class="ac-docs">'+L.map(d=>'<li><span class="ac-file">'+esc(d.name)+'<small>'+fmtDate(d.created_at)+(d.size?' · '+Math.max(1,Math.round(d.size/1024))+' KB':'')+'</small></span><button type="button" class="ac-link" data-dl="'+esc(d.path)+'">'+T('Download','تحميل')+'</button>'+(side==='partner'&&['submitted','invoiced','paid'].includes((orders.find(o=>o.id===id)||{}).status)?'<button type="button" class="ac-link danger" data-del="'+d.id+'">'+T('Delete','حذف')+'</button>':'')+'</li>').join('')+'</ul>';}
  function vOrders(){
    if(!orders.length)return '<div class="ac-empty"><h3>'+T('No orders yet','لا توجد طلبات بعد')+'</h3><p>'+T('Place your first order for a client from the New order tab.','قدّم أول طلب لعميلك من تبويب "طلب جديد".')+'</p><button class="btn solid" type="button" data-tab="new">'+T('New order','طلب جديد')+'</button></div>';
    return '<div class="ad-filter"><input id="ptQ" placeholder="'+T('Search client or order number','ابحث باسم العميل أو رقم الطلب')+'" value="'+esc(vOrders.q||'')+'"></div><div class="ac-orders">'+orders.filter(o=>{const q=(vOrders.q||'').toLowerCase();return !q||(o.ref+' '+o.client_name).toLowerCase().includes(q);}).map(o=>{const open=o.id===openId;
      const head='<button type="button" class="ac-head" data-open="'+o.id+'" aria-expanded="'+open+'"><span class="ac-ref ltr">'+esc(o.ref)+'</span><span class="ac-pkg">'+esc(o.client_name)+'<small>'+esc((o.items||[]).map(nm).join(' · '))+'</small></span><span class="ac-meta">'+fmtDate(o.created_at)+' · <span class="ltr">'+money(o.total,o.currency)+'</span></span><span class="ac-badge pt-s-'+o.status+'">'+esc(lab(o.status))+'</span></button>';
      if(!open)return '<article class="ac-order">'+head+'</article>';
      const items='<table class="pt-items"><tbody>'+(o.items||[]).map(i=>'<tr><td>'+esc(nm(i))+'</td><td class="ltr">'+i.qty+' × '+money(i.unit,o.currency)+'</td><td class="ltr">'+money(i.qty*i.unit,o.currency)+'</td></tr>').join('')+'</tbody><tfoot><tr><td>'+T('Total','الإجمالي')+'</td><td></td><td class="ltr">'+money(o.total,o.currency)+'</td></tr></tfoot></table>';
      const client=[o.client_nationality&&T('Nationality: ','الجنسية: ')+o.client_nationality,o.client_country&&T('Lives in: ','يقيم في: ')+o.client_country].filter(Boolean).map(esc).join(' · ');
      return '<article class="ac-order open">'+head+'<div class="ac-body">'+(o.status==='cancelled'?'':steps(o.status))+
        (o.note_to_partner?'<p class="ac-note">'+esc(o.note_to_partner)+'</p>':'')+
        (o.status==='invoiced'?'<p class="ac-warn">'+T('Invoice issued. Please pay by bank transfer or USDT and send us the payment proof on WhatsApp.','صدرت الفاتورة. يرجى الدفع بالتحويل البنكي أو USDT وإرسال إثبات الدفع عبر واتساب.')+'</p>':'')+
        (client?'<p class="muted">'+client+'</p>':'')+items+
        '<div class="ac-row pt-acts">'+(o.invoice_no?'<a class="btn solid small" target="_blank" href="invoice.html?o='+o.id+'">'+T('Invoice','الفاتورة')+' <span class="ltr">'+esc(o.invoice_no)+'</span></a>':'<a class="btn ghost small" target="_blank" href="invoice.html?o='+o.id+'">'+T('Order confirmation','تأكيد الطلب')+'</a>')+'<a class="btn ghost small" target="_blank" rel="noopener" href="https://wa.me/601124477685?text='+encodeURIComponent('Wizz partner '+me.code+', order '+o.ref+': ')+'">WhatsApp</a></div>'+
        '<div class="ac-cols"><section><h3>'+T('Client documents','مستندات العميل')+'</h3><p class="ac-hint">'+T('Passport copy, residential address, national ID number and anything we ask for. PDF, JPG, PNG or Word, up to 10 MB each.','نسخة الجواز وعنوان السكن الكامل ورقم الهوية الوطنية وأي مستند نطلبه. PDF أو JPG أو PNG أو Word، حتى 10 ميغابايت للملف.')+'</p>'+docList(o.id,'partner')+
        (['completed','cancelled'].includes(o.status)?'':'<label class="btn ghost ac-up"><input type="file" multiple data-up="'+o.id+'" accept=".pdf,.jpg,.jpeg,.png,.webp,.heic,.doc,.docx" hidden>'+T('Upload files','رفع ملفات')+'</label><p class="ac-upmsg" id="up-'+o.id+'" hidden></p>')+'</section>'+
        '<section><h3>'+T('From Wizz','من ويز')+'</h3>'+docList(o.id,'wizz')+'</section></div></div></article>';}).join('')+'</div>';
  }
  function vPrices(){
    if(!prices.length)return '<p class="ac-none">'+T('Your price list is being prepared. Please message us on WhatsApp for prices.','قائمة أسعارك قيد الإعداد. يرجى مراسلتنا عبر واتساب للأسعار.')+'</p>';
    const groups={};prices.forEach(p=>(groups[p.category]=groups[p.category]||[]).push(p));
    return '<p class="ac-hint">'+T('Office prices for '+esc(me.company)+'. Prices are our service fees for one client. Please don\'t share this list.','أسعار المكاتب الخاصة بـ '+esc(me.company)+'. الأسعار هي أتعاب خدماتنا لعميل واحد. يرجى عدم مشاركة هذه القائمة.')+'</p>'+
      Object.entries(groups).map(([c,L])=>'<section class="ad-box"><h3>'+esc(cat(c))+'</h3><table class="pt-prices"><tbody>'+L.map(p=>'<tr><td>'+esc(nm(p))+((ar()?p.note_ar:p.note_en)?'<small>'+esc(ar()?p.note_ar:p.note_en)+'</small>':'')+'</td><td class="ltr">'+money(p.price,p.currency)+'</td><td><button type="button" class="ac-link" data-add="'+esc(p.sku)+'">'+T('Order','اطلب')+'</button></td></tr>').join('')+'</tbody></table></section>').join('');
  }
  function vNew(){
    if(!prices.length)return vPrices();
    const groups={};prices.forEach(p=>(groups[p.category]=groups[p.category]||[]).push(p));
    const sel=Object.entries(cart).filter(([,q])=>q>0).map(([s,q])=>({p:prices.find(x=>x.sku===s),q})).filter(x=>x.p);
    const cur=sel.length?sel[0].p.currency:null;
    const tot=sel.reduce((t,x)=>t+x.q*x.p.price,0);
    return '<form id="ptNew" class="pt-new" novalidate><section class="ad-box"><h3>'+T('1. Your client','1. بيانات العميل')+'</h3><p class="ac-hint">'+T('We only deal with your office. The client\'s details are used for the filing.','نتعامل مع مكتبكم فقط، وتُستخدم بيانات العميل في إجراءات التسجيل.')+'</p><div class="pt-grid">'+
      '<label>'+T('Client full name (as in passport)','اسم العميل الكامل (كما في الجواز)')+'<input name="client_name" required maxlength="150" value="'+esc(vNew.d.client_name||'')+'"></label>'+
      '<label>'+T('Nationality','الجنسية')+'<input name="client_nationality" maxlength="80" value="'+esc(vNew.d.client_nationality||'')+'"></label>'+
      '<label>'+T('Country of residence','دولة الإقامة')+'<input name="client_country" maxlength="80" value="'+esc(vNew.d.client_country||'')+'"></label>'+
      '<label class="full">'+T('Notes for our team (optional)','ملاحظات لفريقنا (اختياري)')+'<textarea name="client_notes" maxlength="2000" rows="3">'+esc(vNew.d.client_notes||'')+'</textarea></label></div></section>'+
      '<section class="ad-box"><h3>'+T('2. Services','2. الخدمات')+'</h3>'+Object.entries(groups).map(([c,L])=>'<h4 class="pt-cat">'+esc(cat(c))+'</h4><ul class="pt-pick">'+L.map(p=>{const q=cart[p.sku]||0;const off=cur&&q===0&&p.currency!==cur;return '<li class="'+(q?'on':'')+(off?' off':'')+'"><span>'+esc(nm(p))+'</span><b class="ltr">'+money(p.price,p.currency)+'</b><span class="pt-qty"><button type="button" data-q="-1" data-sku="'+esc(p.sku)+'" aria-label="−"'+(q?'':' disabled')+'>−</button><em class="ltr">'+q+'</em><button type="button" data-q="1" data-sku="'+esc(p.sku)+'" aria-label="+"'+(off?' disabled':'')+'>+</button></span></li>';}).join('')+'</ul>').join('')+'</section>'+
      '<section class="ad-box pt-sum"><h3>'+T('3. Payment','3. الدفع')+'</h3><div class="pt-pay"><label><input type="radio" name="pay_method" value="bank"'+((vNew.d.pay_method||'bank')==='bank'?' checked':'')+'> '+T('Bank transfer','تحويل بنكي')+'</label><label><input type="radio" name="pay_method" value="usdt"'+(vNew.d.pay_method==='usdt'?' checked':'')+'> USDT (TRC-20)</label></div>'+
      '<p class="pt-total">'+T('Total','الإجمالي')+': <b class="ltr">'+(sel.length?money(tot,cur):'–')+'</b></p><p class="ac-hint">'+T('We send you an invoice after you place the order. Work starts once payment is received. Government approvals, bank and platform decisions are made by third parties and are not guaranteed.','نرسل لك فاتورة بعد تقديم الطلب، ويبدأ العمل بعد استلام الدفع. موافقات الجهات الحكومية وقرارات البنوك والمنصات تعود لأطراف أخرى ولا يمكن ضمانها.')+'</p>'+
      '<button class="btn solid" type="submit"'+(busy?' disabled':'')+'><span class="dot"></span>'+T('Place order','تقديم الطلب')+'</button></section></form>';
  }
  vNew.d={};
  function vStatement(){
    const y=new Date().getFullYear(),from=vStatement.f||y+'-01-01',to=vStatement.t||new Date().toISOString().slice(0,10);
    return '<section class="ad-box"><h3>'+T('Account statement','كشف الحساب')+'</h3><p class="ac-hint">'+T('All your orders, invoices and payments for a period, ready to print or save as PDF.','كل طلباتك وفواتيرك ومدفوعاتك خلال فترة، جاهزة للطباعة أو الحفظ PDF.')+'</p><form id="ptSt" class="ad-form"><label>'+T('From','من')+'<input type="date" name="from" value="'+from+'"></label><label>'+T('To','إلى')+'<input type="date" name="to" value="'+to+'"></label><button class="btn solid small" type="submit">'+T('Open statement','عرض الكشف')+'</button></form></section>';
  }

  // ---------- events
  box.addEventListener('click',async e=>{
    const t=e.target.closest('[data-tab]');if(t){tab=t.dataset.tab;render();return;}
    if(e.target.closest('#ptOut')){await sb.auth.signOut();location.replace('account.html');return;}
    const o=e.target.closest('[data-open]');if(o){openId=openId===o.dataset.open?null:o.dataset.open;render();if(openId)loadDocs(openId);return;}
    const a=e.target.closest('[data-add]');if(a){cart={[a.dataset.add]:1};tab='new';render();return;}
    const q=e.target.closest('[data-q]');if(q){keepForm();const s=q.dataset.sku;cart[s]=Math.max(0,Math.min(50,(cart[s]||0)+Number(q.dataset.q)));render();return;}
    const dl=e.target.closest('[data-dl]');if(dl){const w=window.open('','_blank');const {data,error}=await sb.storage.from('partner-docs').createSignedUrl(dl.dataset.dl,60);if(error||!data){if(w)w.close();flash(error?error.message:'Error',true);return;}if(w)w.location=data.signedUrl;else location.href=data.signedUrl;return;}
    const del=e.target.closest('[data-del]');if(del){if(!confirm(T('Delete this file?','حذف هذا الملف؟')))return;const d=(docs[openId]||[]).find(x=>x.id===del.dataset.del);if(!d)return;await sb.storage.from('partner-docs').remove([d.path]);await sb.from('partner_order_docs').delete().eq('id',d.id);loadDocs(openId);}
  });
  box.addEventListener('input',e=>{if(e.target.id==='ptQ'){vOrders.q=e.target.value;const p=e.target.selectionStart;render();const i=$('ptQ');i.focus();try{i.setSelectionRange(p,p)}catch(_){}}});
  function keepForm(){const f=$('ptNew');if(f)vNew.d=Object.fromEntries(new FormData(f));}
  box.addEventListener('submit',async e=>{
    if(e.target.id==='ptSt'){e.preventDefault();const d=Object.fromEntries(new FormData(e.target));vStatement.f=d.from;vStatement.t=d.to;window.open('invoice.html?statement=1&from='+d.from+'&to='+d.to,'_blank');return;}
    if(e.target.id!=='ptNew')return;e.preventDefault();keepForm();const d=vNew.d;
    const items=Object.entries(cart).filter(([,q])=>q>0).map(([sku,qty])=>({sku,qty}));
    if(!String(d.client_name||'').trim()){flash(T('Please enter the client\'s full name.','يرجى إدخال اسم العميل الكامل.'),true);return;}
    if(!items.length){flash(T('Please choose at least one service.','يرجى اختيار خدمة واحدة على الأقل.'),true);return;}
    busy=true;render();
    const {data,error}=await sb.from('partner_orders').insert({partner_id:me.id,client_name:d.client_name.trim(),client_nationality:(d.client_nationality||'').trim()||null,client_country:(d.client_country||'').trim()||null,client_notes:(d.client_notes||'').trim()||null,pay_method:d.pay_method==='usdt'?'usdt':'bank',items}).select().single();
    busy=false;
    if(error){flash(error.message,true);render();return;}
    try{const s=await sb.auth.getSession();await fetch('/.netlify/functions/partner',{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+s.data.session.access_token},body:JSON.stringify({action:'order_new',order_id:data.id})});}catch(_){}
    cart={};vNew.d={};orders.unshift(data);openId=data.id;docs[data.id]=[];tab='orders';render();
    flash(T('Order '+data.ref+' placed. Please upload the client\'s documents below. We\'ll send the invoice shortly.','تم تقديم الطلب '+data.ref+'. يرجى رفع مستندات العميل أدناه، وسنرسل الفاتورة قريباً.'));
  });
  box.addEventListener('change',async e=>{const inp=e.target.closest('[data-up]');if(!inp)return;const id=inp.dataset.up;const msg=$('up-'+id);
    const files=[...inp.files];inp.value='';let ok=0,bad=[];msg.hidden=false;msg.className='ac-upmsg';msg.textContent=T('Uploading…','جارٍ الرفع…');
    for(const f of files){
      if(f.size>MAX||(f.type&&!TYPES.includes(f.type))){bad.push(f.name);continue;}
      const safe=f.name.replace(/[^\w.\-]+/g,'_').slice(-80);const path=id+'/partner/'+crypto.randomUUID()+'-'+safe;
      const up=await sb.storage.from('partner-docs').upload(path,f,{contentType:f.type||undefined,upsert:false});
      if(up.error){bad.push(f.name);continue;}
      const ins=await sb.from('partner_order_docs').insert({order_id:id,side:'partner',path,name:f.name.slice(0,200),size:f.size});
      if(ins.error){await sb.storage.from('partner-docs').remove([path]);bad.push(f.name);continue;}ok++;}
    await loadDocs(id);const m=$('up-'+id);if(m){m.hidden=false;m.className='ac-upmsg '+(bad.length?'bad':'good');
    m.textContent=(ok?T(ok+' file(s) uploaded. ','تم رفع '+ok+' ملف. '):'')+(bad.length?T('Not uploaded (type or size): ','لم يُرفع (النوع أو الحجم): ')+bad.join(', '):'');}});
  document.addEventListener('wizz:lang',render);
  sb.auth.onAuthStateChange((ev)=>{if(ev==='SIGNED_OUT')location.replace('account.html');});
  boot();
})();
