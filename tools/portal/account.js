(function(){
  const SB_URL='https://mzkkhotipmgqczavrfqy.supabase.co';
  const SB_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im16a2tob3RpcG1ncWN6YXZyZnF5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTEzNjA5OTEsImV4cCI6MjEwNjkzNjk5MX0.-RX74vfMP8qedH2F7XvBN4OGj_dL8yEX96VlXO8ONA0';
  const $=id=>document.getElementById(id);
  const ar=()=>document.documentElement.lang==='ar';const T=(en,a)=>ar()?a:en;
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const STEPS=['paid','docs_needed','review','filed','registered','delivered'];
  const LABEL={paid:['Paid','تم الدفع'],docs_needed:['Documents needed','بانتظار المستندات'],review:['Under review','قيد المراجعة'],filed:['Filed','تم التقديم'],registered:['Company registered','تم تسجيل الشركة'],delivered:['Delivered','تم التسليم'],on_hold:['On hold','متوقف مؤقتاً'],cancelled:['Cancelled','ملغى']};
  const lab=s=>(LABEL[s]||[s,s])[ar()?1:0];
  const fmtMoney=(n,c)=>{try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c,currencyDisplay:'narrowSymbol'}).format(n)}catch(e){return c+' '+n}};
  const fmtDate=d=>new Date(d).toLocaleDateString(ar()?'ar':'en-GB',{day:'numeric',month:'short',year:'numeric'});
  const MAX=10*1024*1024, TYPES=['application/pdf','image/jpeg','image/png','image/webp','image/heic','application/msword','application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
  if(!window.supabase){$('acLoading').hidden=true;$('acErr').hidden=false;$('acErr').textContent=T('The account service could not load. Check your connection and refresh.','تعذّر تحميل خدمة الحساب. تحقق من اتصالك وحدّث الصفحة.');return;}
  const sb=window.supabase.createClient(SB_URL,SB_KEY,{auth:{persistSession:true,detectSessionInUrl:true,flowType:'implicit'}});
  let user=null,orders=[],openId=null,docs={},events={},rems={};

  // ---------- sign in
  const qs=new URLSearchParams(location.search);if(qs.get('email'))$('acEmail').value=qs.get('email');
  $('acForm').addEventListener('submit',async e=>{e.preventDefault();const email=$('acEmail').value.trim();if(!email)return;
    const b=$('acSend');b.disabled=true;$('acFormMsg').hidden=true;
    const {error}=await sb.auth.signInWithOtp({email,options:{emailRedirectTo:location.origin+'/account.html',shouldCreateUser:true}});
    b.disabled=false;
    if(error){$('acFormMsg').hidden=false;$('acFormMsg').className='ac-msg bad';$('acFormMsg').textContent=T('We couldn\'t send the email: ','تعذّر إرسال البريد: ')+error.message;return;}
    $('acForm').hidden=true;$('acSent').hidden=false;$('acSentTo').textContent=email;});
  $('acAgain').addEventListener('click',()=>{$('acSent').hidden=true;$('acForm').hidden=false;});
  $('acOut').addEventListener('click',async()=>{await sb.auth.signOut();location.replace('account.html');});

  // ---------- data
  async function loadAll(){
    const {data,error}=await sb.from('orders').select('id,order_ref,package,items,amount,currency,status,client_note,created_at,onboarding_at').order('created_at',{ascending:false});
    if(error){showErr(error.message);return;}
    orders=data||[];render();
    const {data:adm}=await sb.from('admins').select('email').limit(1);$('acAdmin').hidden=!(adm&&adm.length);
  }
  async function loadOrder(id){
    const [d,e,r]=await Promise.all([
      sb.from('documents').select('*').eq('order_id',id).order('created_at'),
      sb.from('order_events').select('*').eq('order_id',id).order('created_at'),
      sb.from('reminders').select('*').eq('order_id',id).eq('done',false).order('due_date')]);
    docs[id]=d.data||[];events[id]=e.data||[];rems[id]=r.data||[];render();
  }
  function showErr(m){$('acErr').hidden=false;$('acErr').textContent=m;}

  // ---------- render
  function steps(st){const i=STEPS.indexOf(st);return '<ol class="ac-steps'+(i<0?' off':'')+'">'+STEPS.map((s,k)=>'<li class="'+(i>=0&&k<i?'done':'')+(k===i?' now':'')+'"><span></span><em>'+esc(lab(s))+'</em></li>').join('')+'</ol>';}
  function docList(id,side){const L=(docs[id]||[]).filter(d=>d.side===side);
    if(!L.length)return '<p class="ac-none">'+(side==='team'?T('Nothing yet. We\'ll add your company documents here.','لا يوجد شيء بعد. سنضيف مستندات شركتك هنا.'):T('No files uploaded yet.','لم تُرفع ملفات بعد.'))+'</p>';
    return '<ul class="ac-docs">'+L.map(d=>'<li><span class="ac-file">'+esc(d.name)+'<small>'+fmtDate(d.created_at)+(d.size?' · '+Math.max(1,Math.round(d.size/1024))+' KB':'')+'</small></span><button type="button" class="ac-link" data-dl="'+esc(d.path)+'">'+T('Download','تحميل')+'</button>'+(side==='client'?'<button type="button" class="ac-link danger" data-del="'+d.id+'">'+T('Delete','حذف')+'</button>':'')+'</li>').join('')+'</ul>';}
  function render(){
    if(!user)return;
    $('acWho').textContent=user.email;
    const box=$('acOrders');
    if(!orders.length){box.innerHTML='<div class="ac-empty"><h3>'+T('No orders yet','لا توجد طلبات بعد')+'</h3><p>'+T('We couldn\'t find an order paid with this email. If you used a different email at checkout, sign in with that one, or message us on WhatsApp.','لم نجد طلباً مدفوعاً بهذا البريد. إذا استخدمت بريداً آخر عند الدفع فسجّل الدخول به، أو راسلنا على واتساب.')+'</p><a class="btn solid" href="packages.html">'+T('See packages','عرض الباقات')+'</a></div>';return;}
    box.innerHTML=orders.map(o=>{const open=o.id===openId;
      const head='<button type="button" class="ac-head" data-open="'+o.id+'" aria-expanded="'+open+'"><span class="ac-ref ltr">'+esc(o.order_ref)+'</span><span class="ac-pkg">'+esc(o.package)+'</span><span class="ac-meta">'+fmtDate(o.created_at)+' · <span class="ltr">'+fmtMoney(o.amount,o.currency)+'</span></span><span class="ac-badge s-'+o.status+'">'+esc(lab(o.status))+'</span></button>';
      if(!open)return '<article class="ac-order">'+head+'</article>';
      const ev=(events[o.id]||[]).slice().reverse().map(e=>'<li><b>'+esc(e.status?lab(e.status):T('Update','تحديث'))+'</b>'+(e.note?' · '+esc(e.note):'')+'<small>'+fmtDate(e.created_at)+'</small></li>').join('');
      const rm=(rems[o.id]||[]).map(r=>'<li><b>'+esc(r.title)+'</b><small>'+T('Due ','الموعد ')+fmtDate(r.due_date)+'</small></li>').join('');
      return '<article class="ac-order open">'+head+'<div class="ac-body">'+steps(o.status)+
        (o.client_note?'<p class="ac-note">'+esc(o.client_note)+'</p>':'')+
        (!o.onboarding_at?'<p class="ac-warn">'+T('We still need your onboarding details. Please complete the form on the confirmation page, or send them to us on WhatsApp.','ما زلنا نحتاج بيانات التسجيل. أكمل النموذج في صفحة التأكيد أو أرسلها لنا عبر واتساب.')+'</p>':'')+
        '<div class="ac-cols"><section><h3>'+T('Your documents','مستنداتك')+'</h3><p class="ac-hint">'+T('Passport copy, proof of identity and anything we ask for. PDF, JPG, PNG or Word, up to 10 MB each.','نسخة الجواز وإثبات الهوية وأي مستند نطلبه. PDF أو JPG أو PNG أو Word، حتى 10 ميغابايت للملف.')+'</p>'+docList(o.id,'client')+
        '<label class="btn ghost ac-up"><input type="file" multiple data-up="'+o.id+'" accept=".pdf,.jpg,.jpeg,.png,.webp,.heic,.doc,.docx" hidden>'+T('Upload files','رفع ملفات')+'</label><p class="ac-upmsg" id="up-'+o.id+'" hidden></p></section>'+
        '<section><h3>'+T('From Wizz','من ويز')+'</h3>'+docList(o.id,'team')+'</section></div>'+
        (rm?'<section class="ac-rem"><h3>'+T('Upcoming deadlines','المواعيد القادمة')+'</h3><ul>'+rm+'</ul></section>':'')+
        (ev?'<section class="ac-ev"><h3>'+T('History','السجل')+'</h3><ul>'+ev+'</ul></section>':'')+
        '</div></article>';}).join('');
  }
  document.addEventListener('wizz:lang',render);

  // ---------- actions
  $('acOrders').addEventListener('click',async e=>{
    const o=e.target.closest('[data-open]');if(o){openId=openId===o.dataset.open?null:o.dataset.open;render();if(openId)loadOrder(openId);return;}
    const dl=e.target.closest('[data-dl]');if(dl){const w=window.open('','_blank');const {data,error}=await sb.storage.from('docs').createSignedUrl(dl.dataset.dl,60);if(error||!data){if(w)w.close();alert(error?error.message:'Error');return;}if(w)w.location=data.signedUrl;else location.href=data.signedUrl;return;}
    const del=e.target.closest('[data-del]');if(del){if(!confirm(T('Delete this file?','حذف هذا الملف؟')))return;const d=(docs[openId]||[]).find(x=>x.id===del.dataset.del);if(!d)return;
      await sb.storage.from('docs').remove([d.path]);await sb.from('documents').delete().eq('id',d.id);loadOrder(openId);}
  });
  $('acOrders').addEventListener('change',async e=>{const inp=e.target.closest('[data-up]');if(!inp)return;const id=inp.dataset.up;const msg=$('up-'+id);
    const files=[...inp.files];inp.value='';let ok=0,bad=[];msg.hidden=false;msg.className='ac-upmsg';msg.textContent=T('Uploading…','جارٍ الرفع…');
    for(const f of files){
      if(f.size>MAX||(f.type&&!TYPES.includes(f.type))){bad.push(f.name);continue;}
      const safe=f.name.replace(/[^\w.\-]+/g,'_').slice(-80);const path=id+'/client/'+crypto.randomUUID()+'-'+safe;
      const up=await sb.storage.from('docs').upload(path,f,{contentType:f.type||undefined,upsert:false});
      if(up.error){bad.push(f.name);continue;}
      const ins=await sb.from('documents').insert({order_id:id,side:'client',path,name:f.name.slice(0,200),size:f.size,uploaded_by:user.email});
      if(ins.error){await sb.storage.from('docs').remove([path]);bad.push(f.name);continue;}ok++;}
    msg.className='ac-upmsg '+(bad.length?'bad':'good');
    msg.textContent=(ok?T(ok+' file(s) uploaded. ','تم رفع '+ok+' ملف. '):'')+(bad.length?T('Not uploaded (type or size): ','لم يُرفع (النوع أو الحجم): ')+bad.join(', '):'');
    loadOrder(id);});

  // ---------- session
  function show(signed){$('acLoading').hidden=true;$('acIn').hidden=!signed;$('acOutBox').hidden=signed;}
  sb.auth.onAuthStateChange((ev,session)=>{const u=session&&session.user;if(u&&(!user||user.id!==u.id)){user=u;show(true);loadAll();if(location.hash.includes('access_token'))history.replaceState(null,'',location.pathname);}else if(!u){user=null;show(false);}});
  sb.auth.getSession().then(({data})=>{if(!data.session)show(false);});
  const err=new URLSearchParams(location.hash.slice(1)).get('error_description');if(err){$('acFormMsg').hidden=false;$('acFormMsg').className='ac-msg bad';$('acFormMsg').textContent=T('That sign-in link has expired or was already used. Request a new one.','انتهت صلاحية رابط الدخول أو استُخدم من قبل. اطلب رابطاً جديداً.');}
})();
