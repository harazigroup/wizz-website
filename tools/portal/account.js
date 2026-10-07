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

  // ---------- sign in: password (default), email link, create account, forgot / reset password
  const qs=new URLSearchParams(location.search);
  let mode='signin',lastEmail=qs.get('email')||'',note=null;
  const RET=location.origin+'/account.html';
  function card(){
    const box=$('acOutBox');const email=esc(lastEmail);
    const H={signin:T('Sign in to your account','سجّل الدخول إلى حسابك'),signup:T('Create your account','أنشئ حسابك'),link:T('Sign in with an email link','الدخول برابط عبر البريد'),forgot:T('Reset your password','إعادة تعيين كلمة المرور'),reset:T('Choose a new password','اختر كلمة مرور جديدة')}[mode];
    const P={signin:T('Use the email you paid with so your orders appear.','استخدم البريد الإلكتروني الذي دفعت به لتظهر طلباتك.'),signup:T('Use the email you paid with, or the one you\'ll use at checkout. We\'ll send a link to confirm it.','استخدم البريد الذي دفعت به أو الذي ستدفع به. سنرسل رابطاً لتأكيده.'),link:T('No password needed. We\'ll email you a secure link that signs you in.','لا حاجة لكلمة مرور. سنرسل لك رابطاً آمناً لتسجيل الدخول.'),forgot:T('Enter your email and we\'ll send you a link to set a new password.','أدخل بريدك وسنرسل لك رابطاً لتعيين كلمة مرور جديدة.'),reset:T('Pick a password with at least 8 characters.','اختر كلمة مرور من 8 أحرف على الأقل.')}[mode];
    const tabs=(mode==='signin'||mode==='link')?'<div class="ac-tabs" role="tablist"><button type="button" role="tab" data-mode="signin" aria-selected="'+(mode==='signin')+'">'+T('Password','كلمة المرور')+'</button><button type="button" role="tab" data-mode="link" aria-selected="'+(mode==='link')+'">'+T('Email link','رابط عبر البريد')+'</button></div>':'';
    const fEmail=mode!=='reset'?'<label for="acEmail">'+T('Email','البريد الإلكتروني')+'</label><input id="acEmail" type="email" required autocomplete="email" value="'+email+'">':'';
    const fPw=(mode==='signin'||mode==='signup'||mode==='reset')?'<label for="acPass">'+(mode==='signin'?T('Password','كلمة المرور'):T('New password','كلمة مرور جديدة'))+'</label><input id="acPass" type="password" required minlength="'+(mode==='signin'?1:8)+'" autocomplete="'+(mode==='signin'?'current-password':'new-password')+'">':'';
    const fPw2=(mode==='signup'||mode==='reset')?'<label for="acPass2">'+T('Repeat password','أعد كتابة كلمة المرور')+'</label><input id="acPass2" type="password" required minlength="8" autocomplete="new-password"><p class="ac-pwhint">'+T('At least 8 characters.','8 أحرف على الأقل.')+'</p>':'';
    const btn={signin:T('Sign in','تسجيل الدخول'),signup:T('Create account','إنشاء الحساب'),link:T('Email me a sign-in link','أرسل لي رابط الدخول'),forgot:T('Send reset link','أرسل رابط إعادة التعيين'),reset:T('Save new password','حفظ كلمة المرور')}[mode];
    const links={signin:'<div class="ac-row"><button type="button" class="ac-link" data-mode="forgot">'+T('Forgot password?','نسيت كلمة المرور؟')+'</button><span>'+T('New here?','جديد هنا؟')+' <button type="button" class="ac-link" data-mode="signup">'+T('Create an account','أنشئ حساباً')+'</button></span></div>',
      signup:'<div class="ac-row"><span>'+T('Already have an account?','لديك حساب؟')+' <button type="button" class="ac-link" data-mode="signin">'+T('Sign in','تسجيل الدخول')+'</button></span></div>',
      link:'<div class="ac-row"><span>'+T('New here? The link also creates your account.','جديد هنا؟ الرابط يُنشئ حسابك أيضاً.')+'</span></div>',
      forgot:'<div class="ac-row"><button type="button" class="ac-link" data-mode="signin">'+T('Back to sign in','العودة لتسجيل الدخول')+'</button></div>',reset:''}[mode];
    const msg=note?'<p class="ac-msg '+note[0]+'">'+note[1]+'</p>':'';
    box.innerHTML='<p class="eyebrow">'+T('Client account','حساب العميل')+'</p><h1>'+H+'</h1><p class="muted">'+P+'</p>'+tabs+
      '<form id="acForm" class="ac-form" novalidate>'+fEmail+fPw+fPw2+'<button class="btn solid" id="acSend" type="submit"><span class="dot"></span>'+btn+'</button>'+msg+links+'</form>';
  }
  function setMode(m,n){const e=$('acEmail');if(e)lastEmail=e.value.trim();mode=m;note=n||null;card();const f=$('acEmail')&&!$('acEmail').value?$('acEmail'):$('acPass');if(f)f.focus();}
  $('acOutBox').addEventListener('click',e=>{const b=e.target.closest('[data-mode]');if(b){e.preventDefault();setMode(b.dataset.mode);}});
  const friendly=m=>{m=String(m||'');
    if(/invalid login credentials/i.test(m))return T('Email or password is not correct. Try again, or use "Forgot password?".','البريد أو كلمة المرور غير صحيحة. حاول مرة أخرى أو استخدم "نسيت كلمة المرور؟".');
    if(/email not confirmed/i.test(m))return T('Please confirm your email first. Check your inbox for our confirmation link.','يرجى تأكيد بريدك أولاً. تحقق من رسالة التأكيد في بريدك.');
    if(/already registered|already been registered/i.test(m))return T('This email already has an account. Sign in, or use "Forgot password?".','هذا البريد لديه حساب بالفعل. سجّل الدخول أو استخدم "نسيت كلمة المرور؟".');
    if(/rate limit|too many/i.test(m))return T('Too many attempts. Please wait a minute and try again.','محاولات كثيرة. انتظر دقيقة ثم حاول مرة أخرى.');
    if(/weak|at least/i.test(m))return T('Please choose a stronger password (at least 8 characters).','اختر كلمة مرور أقوى (8 أحرف على الأقل).');
    return T('Something went wrong: ','حدث خطأ: ')+esc(m);};
  $('acOutBox').addEventListener('submit',async e=>{e.preventDefault();
    const email=$('acEmail')?$('acEmail').value.trim():'';const pw=$('acPass')?$('acPass').value:'';const pw2=$('acPass2')?$('acPass2').value:'';
    if($('acEmail')&&!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)){note=['bad',T('Please enter a valid email.','يرجى إدخال بريد إلكتروني صحيح.')];lastEmail=email;return card();}
    if((mode==='signup'||mode==='reset')&&(pw.length<8||pw!==pw2)){note=['bad',pw.length<8?T('Use at least 8 characters.','استخدم 8 أحرف على الأقل.'):T('The two passwords don\'t match.','كلمتا المرور غير متطابقتين.')];lastEmail=email;return card();}
    lastEmail=email;const b=$('acSend');b.disabled=true;let r;
    if(mode==='signin'){r=await sb.auth.signInWithPassword({email,password:pw});if(r.error){note=['bad',friendly(r.error.message)];return card();}return;}
    if(mode==='signup'){r=await sb.auth.signUp({email,password:pw,options:{emailRedirectTo:RET}});if(r.error){note=['bad',friendly(r.error.message)];return card();}
      if(r.data&&r.data.session)return; if(r.data&&r.data.user&&r.data.user.identities&&r.data.user.identities.length===0){note=['bad',friendly('already registered')];return card();}
      return setMode('signin',['good',T('Almost done: we sent a confirmation link to ','بقيت خطوة: أرسلنا رابط تأكيد إلى ')+esc(email)+T('. Open it, then you\'re signed in.','. افتحه وسيتم تسجيل دخولك.')]);}
    if(mode==='link'){r=await sb.auth.signInWithOtp({email,options:{emailRedirectTo:RET,shouldCreateUser:true}});if(r.error){note=['bad',friendly(r.error.message)];return card();}
      note=['good',T('Check your email: we sent a sign-in link to ','تحقق من بريدك: أرسلنا رابط الدخول إلى ')+esc(email)+T('. It works once and expires in one hour.','. يعمل مرة واحدة وتنتهي صلاحيته خلال ساعة.')];return card();}
    if(mode==='forgot'){r=await sb.auth.resetPasswordForEmail(email,{redirectTo:RET});if(r.error){note=['bad',friendly(r.error.message)];return card();}
      return setMode('signin',['good',T('If an account exists for ','إذا كان هناك حساب للبريد ')+esc(email)+T(', we\'ve sent a link to set a new password.',' فقد أرسلنا رابطاً لتعيين كلمة مرور جديدة.')]);}
    if(mode==='reset'){r=await sb.auth.updateUser({password:pw});if(r.error){note=['bad',friendly(r.error.message)];return card();}recovering=false;$('acPw').hidden=true;show(true);loadAll();return;}
  });
  // change password while signed in
  function pwCard(){const c=$('acPw');c.innerHTML='<h2>'+T('Change password','تغيير كلمة المرور')+'</h2><form class="ac-form" id="acPwForm"><label for="acNp">'+T('New password','كلمة مرور جديدة')+'</label><input id="acNp" type="password" minlength="8" required autocomplete="new-password"><label for="acNp2">'+T('Repeat password','أعد كتابة كلمة المرور')+'</label><input id="acNp2" type="password" minlength="8" required autocomplete="new-password"><p class="ac-pwhint">'+T('At least 8 characters. You can still sign in with an email link too.','8 أحرف على الأقل. يمكنك أيضاً الدخول برابط البريد.')+'</p><div class="ac-row"><button class="btn solid small" type="submit">'+T('Save password','حفظ كلمة المرور')+'</button><button class="ac-link" type="button" id="acPwX">'+T('Cancel','إلغاء')+'</button></div><p class="ac-msg" id="acPwMsg" hidden></p></form>';}
  $('acPwBtn').addEventListener('click',()=>{const c=$('acPw');if(c.hidden){pwCard();c.hidden=false;$('acNp').focus();}else c.hidden=true;});
  $('acPw').addEventListener('click',e=>{if(e.target.id==='acPwX')$('acPw').hidden=true;});
  $('acPw').addEventListener('submit',async e=>{e.preventDefault();const a=$('acNp').value,b=$('acNp2').value,m=$('acPwMsg');m.hidden=false;
    if(a.length<8||a!==b){m.className='ac-msg bad';m.textContent=a.length<8?T('Use at least 8 characters.','استخدم 8 أحرف على الأقل.'):T('The two passwords don\'t match.','كلمتا المرور غير متطابقتين.');return;}
    const r=await sb.auth.updateUser({password:a});if(r.error){m.className='ac-msg bad';m.innerHTML=friendly(r.error.message);return;}
    m.className='ac-msg good';m.textContent=T('Password saved. Next time you can sign in with your email and password.','تم حفظ كلمة المرور. يمكنك الدخول في المرة القادمة ببريدك وكلمة المرور.');setTimeout(()=>{$('acPw').hidden=true;},2500);});
  $('acOut').addEventListener('click',async()=>{await sb.auth.signOut();location.replace('account.html');});
  let recovering=false;

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
  function show(signed){$('acLoading').hidden=true;$('acIn').hidden=!signed;$('acOutBox').hidden=signed;if(!signed)card();}
  sb.auth.onAuthStateChange((ev,session)=>{const u=session&&session.user;
    if(ev==='PASSWORD_RECOVERY'){recovering=true;user=u;mode='reset';note=null;$('acLoading').hidden=true;$('acIn').hidden=true;$('acOutBox').hidden=false;card();history.replaceState(null,'',location.pathname);return;}
    if(recovering)return;
    if(u&&(!user||user.id!==u.id)){user=u;show(true);loadAll();if(location.hash.includes('access_token'))history.replaceState(null,'',location.pathname);}else if(!u){user=null;show(false);}});
  sb.auth.getSession().then(({data})=>{if(!data.session&&!recovering)show(false);});
  document.addEventListener('wizz:lang',()=>{if(!$('acOutBox').hidden)card();if(!$('acPw').hidden)pwCard();});
  const err=new URLSearchParams(location.hash.slice(1)).get('error_description');if(err){note=['bad',T('That link has expired or was already used. Please request a new one.','انتهت صلاحية الرابط أو استُخدم من قبل. اطلب رابطاً جديداً.')];}
})();
