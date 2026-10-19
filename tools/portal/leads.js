// Team admin: Leads pipeline. Loaded on admin.html after admin.js, which signs in and fires 'wizz:admin-ready'.
(function(){
  const $=id=>document.getElementById(id);
  const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const ST={new:'New',contacted:'Contacted',qualified:'Qualified',quoted:'Quote sent',won:'Won',lost:'Lost'};
  const SRC={website:'Website',whatsapp:'WhatsApp',tiktok:'TikTok',instagram:'Instagram',facebook:'Facebook',referral:'Referral',partner:'Partner office',other:'Other'};
  const MARKETS=['United States','United Kingdom','Canada','Estonia','Poland','France','Netherlands','UAE','Saudi Arabia','Oman','Egypt','Malaysia','Thailand','Pakistan','Not sure yet'];
  const LOST=['Price','Chose a competitor','Not eligible','No reply','Changed plans','Other'];
  const today=()=>new Date().toISOString().slice(0,10);
  const addDays=n=>{const d=new Date();d.setDate(d.getDate()+n);return d.toISOString().slice(0,10);};
  const fmtDate=d=>d?new Date(d).toLocaleDateString('en-GB',{day:'numeric',month:'short'}):'';
  const money=(n,c)=>{if(n==null)return '';try{return new Intl.NumberFormat('en-US',{style:'currency',currency:c||'MYR',currencyDisplay:'narrowSymbol',maximumFractionDigits:0}).format(n)}catch(e){return (c||'')+' '+n}};
  let sb=null,me=null,leads=[],cur=null,events=[],quotes=[],CAT=[],draft=null;

  // WhatsApp message templates in the client's language. {name} {market} {ref}
  const TPL={
    first:{label:'First reply',
      en:'Hi {name}, this is the Wizz Smart Services team. Thank you for your enquiry about {market}. To recommend the right setup, could you tell us: 1) your nationality and country of residence, 2) what you will sell or do, and 3) whether you are a single owner or have partners?',
      ar:'مرحباً {name}، معك فريق ويز للخدمات الذكية. شكراً لاستفسارك عن {market}. حتى نرشّح لك الإعداد المناسب، أخبرنا من فضلك: 1) جنسيتك وبلد إقامتك، 2) نشاطك أو ما ستبيعه، 3) هل أنت مالك وحيد أم معك شركاء؟',
      ms:'Hai {name}, ini pasukan Wizz Smart Services. Terima kasih atas pertanyaan anda tentang {market}. Untuk mencadangkan persediaan yang sesuai, boleh beritahu kami: 1) kewarganegaraan dan negara tempat tinggal anda, 2) apa yang anda jual atau lakukan, dan 3) adakah anda pemilik tunggal atau mempunyai rakan kongsi?'},
    ecom:{label:'Own brand or reseller?',
      en:'Thanks {name}. One more question so we prepare the right documents: will you sell your own private brand, or resell products from other brands? And which marketplace are you targeting (Amazon, Shopify, TikTok Shop, Noon...)?',
      ar:'شكراً {name}. سؤال أخير حتى نجهّز المستندات الصحيحة: هل ستبيع علامتك التجارية الخاصة أم تعيد بيع منتجات علامات أخرى؟ وما المنصة التي تستهدفها (أمازون، شوبيفاي، تيك توك شوب، نون...)؟',
      ms:'Terima kasih {name}. Satu lagi soalan supaya kami sediakan dokumen yang betul: adakah anda akan menjual jenama persendirian anda, atau menjual semula produk jenama lain? Dan pasaran dalam talian mana yang anda sasarkan (Amazon, Shopify, TikTok Shop, Noon...)?'},
    quote:{label:'Quote follow-up',
      en:'Hi {name}, just checking you received our quotation ({ref}). Happy to answer any questions or adjust the package. Bank, payment and marketplace approvals are always decided by each provider, and we prepare your application to give it the best chance.',
      ar:'مرحباً {name}، نتأكد فقط من وصول عرض السعر ({ref}). يسعدنا الإجابة عن أي سؤال أو تعديل الباقة. موافقات البنوك ومزودي الدفع والمنصات يقررها كل مزود، ونحن نجهّز طلبك بأفضل شكل ممكن.',
      ms:'Hai {name}, sekadar memastikan anda telah menerima sebut harga kami ({ref}). Kami sedia menjawab sebarang soalan atau menyesuaikan pakej. Kelulusan bank, pembayaran dan pasaran dalam talian sentiasa diputuskan oleh setiap penyedia, dan kami menyediakan permohonan anda sebaik mungkin.'},
    docs:{label:'Ask for documents',
      en:'Great, {name}. To start, please send: a clear passport copy, your full residential address, your national ID number, 2–3 company name choices and a short description of your business. You can also upload files securely in your client account at wizz.com.my/account.html.',
      ar:'ممتاز يا {name}. للبدء أرسل لنا من فضلك: صورة واضحة من جواز السفر، عنوان السكن الكامل، رقم الهوية الوطنية، 2 إلى 3 أسماء مقترحة للشركة ووصفاً قصيراً لنشاطك. ويمكنك رفع الملفات بأمان في حسابك على wizz.com.my/account.html.',
      ms:'Bagus, {name}. Untuk bermula, sila hantar: salinan pasport yang jelas, alamat kediaman penuh, nombor kad pengenalan, 2–3 pilihan nama syarikat dan penerangan ringkas tentang perniagaan anda. Anda juga boleh memuat naik fail dengan selamat dalam akaun pelanggan di wizz.com.my/account.html.'},
    last:{label:'Final check-in',
      en:'Hi {name}, we haven\'t heard back, so we\'ll pause your enquiry for now. If your plans change, just reply here and we\'ll pick it up straight away.',
      ar:'مرحباً {name}، لم يصلنا ردك، لذلك سنوقف استفسارك مؤقتاً. إذا تغيّرت خططك، رد هنا وسنكمل معك فوراً.',
      ms:'Hai {name}, kami belum menerima maklum balas, jadi kami akan menangguhkan pertanyaan anda buat masa ini. Jika rancangan anda berubah, balas sahaja di sini dan kami akan menyambungnya serta-merta.'},
  };
  const fill=(t,l)=>t.replace(/\{name\}/g,(l.name||'').split(/\s+/)[0]).replace(/\{market\}/g,l.market||'your company').replace(/\{ref\}/g,l.ref);

  function flash(m,bad){const x=$('adMsg');x.hidden=false;x.className='ac-msg '+(bad?'bad':'good');x.textContent=m;clearTimeout(flash.t);flash.t=setTimeout(()=>x.hidden=true,4000);}
  async function load(){
    const {data,error}=await sb.from('leads').select('*').order('created_at',{ascending:false}).limit(1000);
    if(error)return flash(error.message,true);leads=data||[];renderStats();renderList();
    if(cur){cur=leads.find(l=>l.id===cur.id)||null;if(cur)renderLead();}
  }
  function isDue(l){return ['new','contacted','qualified','quoted'].includes(l.status)&&l.next_follow_up&&l.next_follow_up<=today();}
  function renderStats(){
    const open=leads.filter(l=>!['won','lost'].includes(l.status));
    const m=new Date().toISOString().slice(0,7);
    const quoted=leads.filter(l=>l.status==='quoted');
    const S=[['New, not contacted',leads.filter(l=>l.status==='new').length,'new'],['Follow-ups due',leads.filter(isDue).length,'due'],['Hot and open',open.filter(l=>l.priority==='hot').length,'hot'],['Quotes waiting',quoted.length,'quoted'],['Won this month',leads.filter(l=>l.status==='won'&&(l.updated_at||'').slice(0,7)===m).length,'won']];
    $('ldStats').innerHTML=S.map(([t,n,k])=>'<button type="button" class="ld-stat" data-q="'+k+'"><b>'+n+'</b><span>'+t+'</span></button>').join('');
  }
  function renderList(){
    const q=$('ldQ').value.trim().toLowerCase(),f=$('ldF').value,s=$('ldS').value;
    const L=leads.filter(l=>(f==='due'?isDue(l):f==='hot'?(l.priority==='hot'&&!['won','lost'].includes(l.status)):f==='open'?!['won','lost'].includes(l.status):(!f||l.status===f))&&(!s||l.source===s)&&(!q||[l.ref,l.name,l.email,l.phone,l.market,l.activity,l.nationality].join(' ').toLowerCase().includes(q)));
    $('ldCount').textContent=L.length+' lead'+(L.length===1?'':'s');
    $('ldList').innerHTML=L.map(l=>{const due=isDue(l);return '<button type="button" class="ad-row'+(cur&&cur.id===l.id?' on':'')+'" data-lead="'+l.id+'"><span class="ld-line"><i class="ld-dot p-'+l.priority+'" title="'+l.priority+'"></i><b>'+esc(l.name)+'</b><span class="ac-badge ls-'+l.status+'">'+ST[l.status]+'</span></span><span class="ad-pk">'+esc([l.market,l.activity].filter(Boolean).join(' · ').slice(0,80))+'</span><small>'+esc(SRC[l.source]||l.source)+' · '+fmtDate(l.created_at)+(l.next_follow_up&&!['won','lost'].includes(l.status)?' · <span class="'+(due?'ld-due':'')+'">follow up '+fmtDate(l.next_follow_up)+'</span>':'')+'</small></button>';}).join('')||'<p class="ac-none">No leads here.</p>';
  }
  async function open(id){
    cur=leads.find(l=>l.id===id);if(!cur)return;renderList();
    const [ev,qs]=await Promise.all([sb.from('lead_events').select('*').eq('lead_id',id).order('created_at',{ascending:false}),sb.from('quotes').select('*').eq('lead_id',id).order('created_at',{ascending:false})]);
    events=ev.data||[];quotes=qs.data||[];draft=null;renderLead();
  }
  function waLink(l,key){const lang=['ar','ms'].includes(l.lang)?l.lang:'en';return 'https://wa.me/'+String(l.phone||'').replace(/\D/g,'')+'?text='+encodeURIComponent(fill(TPL[key][lang],l));}
  function renderLead(){
    const l=cur,F=[['Email',l.email],['WhatsApp',l.phone],['Nationality',l.nationality],['Lives in',l.residence],['Target country',l.market],['Activity',l.activity],['Services',l.services],['Owners',l.owners],['Selling online',l.brand],['Message',l.message],['Language',{en:'English',ar:'Arabic',ms:'Malay'}[l.lang]||l.lang]];
    $('ldDetail').innerHTML='<div class="ad-top"><div><h2>'+esc(l.name)+'</h2><p class="ad-sub ltr">'+esc(l.ref)+' · '+esc(SRC[l.source]||l.source)+' · '+fmtDate(l.created_at)+'</p>'+(l.ref_code?'<p class="ld-hint" style="margin:4px 0 0">Referral code <b class="ltr">'+esc(l.ref_code)+'</b>: RM 100 off orders of RM 1,000+. Add it as a discount line on the quote, then record the 10% in Referrals once the client pays.</p>':'')+'</div><div class="ad-amt"><span class="ld-pri p-'+l.priority+'">'+l.priority.toUpperCase()+'</span><small>score '+l.score+'</small></div></div>'+
      '<section class="ad-box"><h3>Contact on WhatsApp</h3>'+(l.phone?'<div class="ld-tpl">'+Object.keys(TPL).map(k=>'<a class="btn ghost small" target="_blank" rel="noopener" data-tpl="'+k+'" href="'+esc(waLink(l,k))+'">'+TPL[k].label+'</a>').join('')+'</div><p class="ld-hint">Opens WhatsApp with the message ready in the client\'s language. Sending it marks the lead as contacted and sets the next follow-up in 2 days.</p>':'<p class="ac-none">No WhatsApp number. Add one below.</p>')+(l.email?'<p class="ld-hint">Email: <a href="mailto:'+esc(l.email)+'">'+esc(l.email)+'</a></p>':'')+'</section>'+
      '<section class="ad-box"><h3>Pipeline</h3><div class="ld-grid">'+
        '<label>Status<select id="ldSt">'+Object.keys(ST).map(k=>'<option value="'+k+'"'+(k===l.status?' selected':'')+'>'+ST[k]+'</option>').join('')+'</select></label>'+
        '<label>Next follow-up<input type="date" id="ldNext" value="'+esc(l.next_follow_up||'')+'"></label>'+
        '<label>Priority<select id="ldPri">'+['hot','warm','cold'].map(k=>'<option'+(k===l.priority?' selected':'')+'>'+k+'</option>').join('')+'</select></label>'+
        '<label>Handled by<input id="ldWho" value="'+esc(l.assigned_to||'')+'" placeholder="Team member"></label>'+
        '<label>Quote total<input id="ldQT" type="number" min="0" step="1" value="'+esc(l.quote_total??'')+'"></label>'+
        '<label>Currency<select id="ldQC">'+['MYR','USD','GBP','EUR','SAR','AED','OMR'].map(c=>'<option'+(c===(l.quote_currency||'MYR')?' selected':'')+'>'+c+'</option>').join('')+'</select></label>'+
        '<label id="ldLostW"'+(l.status==='lost'?'':' hidden')+'>Lost reason<select id="ldLost"><option value="">Choose</option>'+LOST.map(r=>'<option'+(r===l.lost_reason?' selected':'')+'>'+r+'</option>').join('')+'</select></label>'+
        '<label>WhatsApp<input id="ldPh" value="'+esc(l.phone||'')+'" placeholder="+60..."></label>'+
      '</div><label class="ad-lbl">Notes<textarea id="ldNotes" rows="3">'+esc(l.notes||'')+'</textarea></label>'+
      '<div class="ld-actions"><button class="btn solid small" id="ldSave" type="button">Save</button><label class="ld-chk"><input type="checkbox" id="ldNoMail"'+(l.no_emails?' checked':'')+'> No automatic emails</label></div>'+
      '<p class="ld-hint">Set the status to <b>Quote sent</b> and the system emails the client a polite follow-up after 3 and 7 days, unless the lead is won, lost or set to no emails.</p></section>'+
      '<section class="ad-box" id="ldQuotes"></section>'+
      '<section class="ad-box"><h3>Enquiry</h3><dl class="ad-dl">'+F.filter(([,v])=>v).map(([k,v])=>'<dt>'+k+'</dt><dd>'+esc(v)+'</dd>').join('')+'</dl></section>'+
      '<section class="ad-box"><h3>History</h3><ul class="ad-ev">'+events.map(e=>'<li><b>'+esc(e.kind.replace(/_/g,' '))+'</b>'+(e.note?' · '+esc(e.note):'')+'<small>'+new Date(e.created_at).toLocaleString('en-GB',{day:'numeric',month:'short',hour:'2-digit',minute:'2-digit'})+' · '+esc(e.created_by||'')+'</small></li>').join('')+'</ul></section>';
    renderQuotes();
  }
  // ---------- quotes
  const QURL=q=>location.origin+'/quote.html?t='+q.token;
  const QMSG={en:(n,u)=>'Hi '+n+', here is your quotation from Wizz Smart Services: '+u+' You can review it, download it as a PDF and accept it online. Happy to answer any questions.',
    ar:(n,u)=>'مرحباً '+n+'، هذا عرض السعر من ويز للخدمات الذكية: '+u+' يمكنك مراجعته وتنزيله PDF والموافقة عليه عبر الإنترنت. يسعدنا الإجابة عن أي سؤال.',
    ms:(n,u)=>'Hai '+n+', ini sebut harga anda daripada Wizz Smart Services: '+u+' Anda boleh menyemaknya, memuat turun sebagai PDF dan menerimanya dalam talian. Kami sedia menjawab sebarang soalan.'};
  const QST={draft:'Draft',sent:'Sent',accepted:'Accepted',cancelled:'Cancelled'};
  function priceOf(it,cur){return cur==='USD'?it.usd:cur==='MYR'?it.myr:0;}
  function renderQuotes(){
    const box=$('ldQuotes');if(!box)return;const l=cur;
    const list=quotes.length?'<ul class="ld-qs">'+quotes.map(q=>'<li><b class="ltr">'+esc(q.ref)+'</b> · '+money(q.total,q.currency)+' · <span class="ac-badge ls-'+(q.status==='accepted'?'won':'quoted')+'">'+QST[q.status]+'</span>'+(q.viewed_at?' <small>viewed '+fmtDate(q.viewed_at)+'</small>':' <small>not opened yet</small>')+
      '<span class="ld-qa"><a class="ac-link" href="'+esc(QURL(q))+'" target="_blank" rel="noopener">Open</a><button type="button" class="ac-link" data-qcopy="'+q.id+'">Copy link</button>'+(l.phone?'<a class="ac-link" target="_blank" rel="noopener" data-qwa="'+q.id+'" href="https://wa.me/'+esc(String(l.phone).replace(/\D/g,''))+'?text='+encodeURIComponent((QMSG[q.lang]||QMSG.en)((l.name||'').split(/\s+/)[0],QURL(q)))+'">WhatsApp</a>':'')+(q.client_email?'<button type="button" class="ac-link" data-qmail="'+q.id+'">Email</button>':'')+(q.status==='sent'?'<button type="button" class="ac-link danger" data-qcancel="'+q.id+'">Cancel</button>':'')+'</span></li>').join('')+'</ul>':'<p class="ac-none">No quotes yet.</p>';
    let form='';
    if(draft){
      const groups=[...new Set(CAT.map(c=>c.g))];
      form='<div class="ld-qf"><div class="ld-grid">'+
        '<label>Title (optional)<input id="qTitle" value="'+esc(draft.title)+'" placeholder="e.g. US LLC for Amazon"></label>'+
        '<label>Language<select id="qLang">'+[['en','English'],['ar','Arabic'],['ms','Malay']].map(([k,v])=>'<option value="'+k+'"'+(k===draft.lang?' selected':'')+'>'+v+'</option>').join('')+'</select></label>'+
        '<label>Currency<select id="qCur">'+['MYR','USD','GBP','EUR','SAR','AED','OMR'].map(c=>'<option'+(c===draft.currency?' selected':'')+'>'+c+'</option>').join('')+'</select></label>'+
        '<label>Valid for (days)<input id="qDays" type="number" min="1" max="90" value="'+draft.days+'"></label></div>'+
        '<div class="ad-form"><select id="qPick"><option value="">Add a package or service…</option>'+groups.map(g=>'<optgroup label="'+esc(g)+'">'+CAT.map((c,i)=>c.g===g?'<option value="'+i+'">'+esc(c.name)+(priceOf(c,draft.currency)?' · '+money(priceOf(c,draft.currency),draft.currency):'')+'</option>':'').join('')+'</optgroup>').join('')+'</select><button type="button" class="btn ghost small" id="qCustom">Custom line</button></div>'+
        '<table class="ld-qt"><thead><tr><th>Service</th><th>Qty</th><th>Unit price</th><th></th></tr></thead><tbody>'+draft.items.map((it,i)=>'<tr><td><input data-qi="'+i+'" data-k="name" value="'+esc(it.name)+'"><textarea data-qi="'+i+'" data-k="detail" rows="2" placeholder="What is included">'+esc(it.detail)+'</textarea><label class="ld-chk"><input type="checkbox" data-qi="'+i+'" data-k="from"'+(it.from?' checked':'')+'> show as "from"</label></td><td><input type="number" min="1" data-qi="'+i+'" data-k="qty" value="'+it.qty+'"></td><td><input type="number" min="0" step="1" data-qi="'+i+'" data-k="unit" value="'+it.unit+'"></td><td><button type="button" class="ac-link danger" data-qdel="'+i+'">Remove</button></td></tr>').join('')+'</tbody></table>'+
        '<p class="ld-qtot">Total: <b>'+money(draft.items.reduce((a,it)=>a+(+it.unit||0)*(+it.qty||1),0),draft.currency)+'</b></p>'+
        '<label class="ad-lbl">Note shown to the client (optional)<textarea id="qNotes" rows="2" placeholder="e.g. Government fees for Delaware are paid at cost.">'+esc(draft.notes)+'</textarea></label>'+
        '<div class="ld-actions"><button class="btn solid small" type="button" id="qSave">Create quote</button><button class="btn ghost small" type="button" id="qCancelDraft">Cancel</button></div>'+
        '<p class="ld-hint">Creating the quote sets the lead to Quote sent. The client gets polite follow-up emails after 3 and 7 days unless they accept, or you change the status.</p></div>';
    }
    box.innerHTML='<h3>Quotes</h3>'+list+(draft?form:'<button type="button" class="btn solid small" id="qNew">New quote</button>');
  }
  function syncDraft(){
    if(!draft)return;const g=id=>$(id);
    if(g('qTitle'))draft.title=g('qTitle').value;if(g('qLang'))draft.lang=g('qLang').value;if(g('qDays'))draft.days=+g('qDays').value||14;if(g('qNotes'))draft.notes=g('qNotes').value;
    document.querySelectorAll('[data-qi]').forEach(el=>{const it=draft.items[+el.dataset.qi];if(!it)return;const k=el.dataset.k;it[k]=el.type==='checkbox'?el.checked:(k==='qty'||k==='unit')?(+el.value||0):el.value;});
  }
  async function loadCat(){if(CAT.length)return;try{CAT=await fetch('quote-catalog.json').then(r=>r.json());}catch(e){CAT=[];}}
  async function saveQuote(){
    syncDraft();const items=draft.items.filter(i=>i.name.trim());if(!items.length)return flash('Add at least one service.',true);
    const total=items.reduce((a,it)=>a+(+it.unit||0)*(+it.qty||1),0);
    const vu=addDays(draft.days||14);
    const row={lead_id:cur.id,created_by:me.email,status:'sent',lang:draft.lang,client_name:cur.name,client_email:cur.email,client_phone:cur.phone,client_country:cur.residence||cur.nationality||null,
      title:draft.title.trim()||null,currency:draft.currency,items:items.map(i=>({name:i.name.trim(),detail:(i.detail||'').trim(),qty:+i.qty||1,unit:+i.unit||0,from:!!i.from})),total,valid_until:vu,notes:draft.notes.trim()||null};
    const {data,error}=await sb.from('quotes').insert(row).select().single();if(error)return flash(error.message,true);
    await sb.from('leads').update({status:['won','lost'].includes(cur.status)?cur.status:'quoted',quoted_at:new Date().toISOString(),follow_up_step:0,quote_total:total,quote_currency:draft.currency,next_follow_up:addDays(3)}).eq('id',cur.id);
    await log('quote',data.ref+' · '+money(total,draft.currency));
    flash('Quote '+data.ref+' created. Send it on WhatsApp or by email.');draft=null;await load();open(cur.id);
  }
  async function mailQuote(id){
    const {data:{session}}=await sb.auth.getSession();
    const r=await fetch('/.netlify/functions/send-quote',{method:'POST',headers:{'content-type':'application/json',authorization:'Bearer '+(session&&session.access_token)},body:JSON.stringify({id})});
    const j=await r.json().catch(()=>({}));if(!r.ok)return flash('Email not sent: '+(j.error||r.status),true);
    await log('quote_emailed',j.ref);flash('Quote emailed to '+j.to+'.');open(cur.id);
  }
  async function log(kind,note){await sb.from('lead_events').insert({lead_id:cur.id,kind,note:note||null,created_by:me.email});}
  async function save(){
    const st=$('ldSt').value,prev=cur.status;
    const row={status:st,next_follow_up:$('ldNext').value||null,priority:$('ldPri').value,assigned_to:$('ldWho').value.trim()||null,
      quote_total:$('ldQT').value===''?null:+$('ldQT').value,quote_currency:$('ldQC').value,notes:$('ldNotes').value.trim()||null,
      phone:$('ldPh').value.trim()||null,no_emails:$('ldNoMail').checked,lost_reason:st==='lost'?($('ldLost').value||null):null};
    if(st==='quoted'&&prev!=='quoted'){row.quoted_at=new Date().toISOString();row.follow_up_step=0;if(!$('ldNext').value||$('ldNext').value<=today())row.next_follow_up=addDays(3);}
    if(['won','lost'].includes(st))row.next_follow_up=null;
    const {error}=await sb.from('leads').update(row).eq('id',cur.id);if(error)return flash(error.message,true);
    if(st!==prev)await log('status',ST[prev]+' → '+ST[st]+(row.lost_reason?' ('+row.lost_reason+')':''));
    flash('Lead saved.');await load();open(cur.id);
  }
  function bind(){
    $('ldQ').addEventListener('input',renderList);$('ldF').addEventListener('change',renderList);$('ldS').addEventListener('change',renderList);
    $('ldStats').addEventListener('click',e=>{const b=e.target.closest('[data-q]');if(!b)return;$('ldF').value=b.dataset.q==='new'?'new':b.dataset.q==='quoted'?'quoted':b.dataset.q==='won'?'won':b.dataset.q;renderList();});
    $('ldList').addEventListener('click',e=>{const b=e.target.closest('[data-lead]');if(b)open(b.dataset.lead);});
    $('ldDetail').addEventListener('click',async e=>{
      if(e.target.id==='ldSave')return save();
      if(e.target.id==='qNew'){await loadCat();draft={title:'',lang:['ar','ms'].includes(cur.lang)?cur.lang:'en',currency:cur.quote_currency||'MYR',days:14,notes:'',items:[]};return renderQuotes();}
      if(e.target.id==='qCancelDraft'){draft=null;return renderQuotes();}
      if(e.target.id==='qCustom'){syncDraft();draft.items.push({name:'',detail:'',qty:1,unit:0,from:false});return renderQuotes();}
      if(e.target.dataset.qdel!=null){syncDraft();draft.items.splice(+e.target.dataset.qdel,1);return renderQuotes();}
      if(e.target.id==='qSave')return saveQuote();
      if(e.target.dataset.qcopy){const q=quotes.find(x=>x.id===e.target.dataset.qcopy);try{await navigator.clipboard.writeText(QURL(q));flash('Link copied.');}catch(_){prompt('Copy the link',QURL(q));}return;}
      if(e.target.dataset.qmail){if(confirm('Email this quote to the client now?'))mailQuote(e.target.dataset.qmail);return;}
      if(e.target.dataset.qcancel){if(!confirm('Cancel this quote? The client link will stop working.'))return;await sb.from('quotes').update({status:'cancelled'}).eq('id',e.target.dataset.qcancel);await log('quote_cancelled','');return open(cur.id);}
      if(e.target.dataset.qwa){await log('quote_whatsapp','');}
      const t=e.target.closest('[data-tpl]');if(t){const k=t.dataset.tpl;const row={last_contacted_at:new Date().toISOString()};
        if(cur.status==='new')row.status='contacted';if(k!=='last')row.next_follow_up=addDays(2);if(k==='last'){row.status='lost';row.lost_reason='No reply';row.next_follow_up=null;}
        await sb.from('leads').update(row).eq('id',cur.id);await log('whatsapp',TPL[k].label);setTimeout(()=>{load().then(()=>open(cur.id));},600);}
    });
    $('ldDetail').addEventListener('change',e=>{if(e.target.id==='ldSt')$('ldLostW').hidden=e.target.value!=='lost';
      if(e.target.id==='qPick'&&e.target.value!==''){syncDraft();const c=CAT[+e.target.value];draft.items.push({name:c.name,detail:c.detail,qty:1,unit:priceOf(c,draft.currency)||0,from:!!c.from});renderQuotes();}
      if(e.target.id==='qCur'){syncDraft();draft.currency=e.target.value;renderQuotes();}
      if(e.target.dataset&&e.target.dataset.qi!=null){syncDraft();renderQuotes();}});
    $('ldNew').addEventListener('submit',async e=>{e.preventDefault();const f=new FormData(e.target);
      const row={source:f.get('source'),name:String(f.get('name')).trim(),phone:String(f.get('phone')||'').trim()||null,email:String(f.get('email')||'').trim().toLowerCase()||null,
        market:f.get('market')||null,activity:String(f.get('activity')||'').trim()||null,lang:f.get('lang'),priority:f.get('priority'),status:'contacted',next_follow_up:addDays(1),assigned_to:me.email,last_contacted_at:new Date().toISOString()};
      const {data,error}=await sb.from('leads').insert(row).select().single();if(error)return flash(error.message,true);
      await sb.from('lead_events').insert({lead_id:data.id,kind:'created',note:'Added by team from '+(SRC[row.source]||row.source),created_by:me.email});
      e.target.reset();$('ldNewBox').open=false;flash('Lead '+data.ref+' added.');await load();open(data.id);});
  }
  function initForm(){
    $('ldNewMkt').innerHTML='<option value="">Target country</option>'+MARKETS.map(m=>'<option>'+m+'</option>').join('');
  }
  const start=d=>{if(sb)return;sb=d.sb;me=d.me;initForm();bind();load();};
  if(window.wizzAdmin)start(window.wizzAdmin);
  document.addEventListener('wizz:admin-ready',e=>start(e.detail));
})();
