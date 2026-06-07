/* =====================================================================
   AGROCETE — site.js
   Chrome injection (header/footer) · direction switch · i18n · reveals
   · mobile nav · scroll state · vanilla Tweaks panel (host protocol)
   ===================================================================== */
(function(){
  "use strict";

  /* ---------------- i18n dictionary ---------------- */
  var I18N = {
    pt:{
      nav_sobre:"Sobre nós", nav_constr:"Construção da Produtividade", nav_constr_s:"Construção", nav_prod:"Produtos",
      nav_saber:"Saber+Agro", nav_contato:"Contato", nav_inst:"Institucional",
      cta_contato:"Fale com a gente", cta_prod:"Ver produtos",
      inst_proposito:"Propósito, Missão, Visão e Valores", inst_sust:"Sustentabilidade",
      inst_inov:"Inovação", inst_compliance:"Compliance", inst_imprensa:"Imprensa",
      inst_vagas:"Oportunidades", inst_esg:"Política SGI e ESG", inst_canal:"Canal de denúncia",
      ft_links:"Links rápidos", ft_inst:"Institucional", ft_contato:"Contato",
      ft_claim:"Produtividade se constrói. Em cada etapa, desde as raízes.",
      ft_rights:"Agrocete Indústria de Fertilizantes ® 2026. Todos os direitos reservados",
      saiba:"Saiba mais"
    },
    en:{
      nav_sobre:"About us", nav_constr:"Productivity System", nav_constr_s:"System", nav_prod:"Products",
      nav_saber:"Knowledge Hub", nav_contato:"Contact", nav_inst:"Company",
      cta_contato:"Talk to us", cta_prod:"View products",
      inst_proposito:"Purpose, Mission, Vision & Values", inst_sust:"Sustainability",
      inst_inov:"Innovation", inst_compliance:"Compliance", inst_imprensa:"Press",
      inst_vagas:"Careers", inst_esg:"IMS & ESG Policy", inst_canal:"Whistleblower channel",
      ft_links:"Quick links", ft_inst:"Company", ft_contato:"Contact",
      ft_claim:"Productivity is built. At every stage, from the roots up.",
      ft_rights:"Agrocete Indústria de Fertilizantes ® 2026. All rights reserved",
      saiba:"Learn more"
    },
    es:{
      nav_sobre:"Nosotros", nav_constr:"Construcción de Productividad", nav_constr_s:"Construcción", nav_prod:"Productos",
      nav_saber:"Saber+Agro", nav_contato:"Contacto", nav_inst:"Institucional",
      cta_contato:"Habla con nosotros", cta_prod:"Ver productos",
      inst_proposito:"Propósito, Misión, Visión y Valores", inst_sust:"Sostenibilidad",
      inst_inov:"Innovación", inst_compliance:"Compliance", inst_imprensa:"Prensa",
      inst_vagas:"Oportunidades", inst_esg:"Política SGI y ESG", inst_canal:"Canal de denuncias",
      ft_links:"Enlaces rápidos", ft_inst:"Institucional", ft_contato:"Contacto",
      ft_claim:"La productividad se construye. En cada etapa, desde las raíces.",
      ft_rights:"Agrocete Indústria de Fertilizantes ® 2026. Todos los derechos reservados",
      saiba:"Saber más"
    }
  };

  var MARK = '<svg class="mark" viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2C9 8 6 13 6 19a10 10 0 0 0 20 0c0-6-3-11-10-17Zm0 5.6c4.2 4 6 7.4 6 11.4a6 6 0 0 1-5 5.9V14.5a1 1 0 0 0-2 0v10.4a6 6 0 0 1-5-5.9c0-4 1.8-7.4 6-11.4Z"/></svg>';

  // Official Agrocete logo (loaded cross-origin as an image)
  var LOGO_URL = 'https://www.agrocete.com.br/site/images/agrocete/logo-simbolo-grande.svg';
  var LOGO = '<img class="brand-logo" src="'+LOGO_URL+'" alt="Agrocete">';

  var SOCIAL = ''+
    '<a href="https://www.instagram.com/agrocetebrasil/" aria-label="Instagram"><svg viewBox="0 0 24 24"><path d="M12 2.2c3.2 0 3.6 0 4.8.07 1.2.06 1.8.25 2.2.42.6.22 1 .48 1.4.9.43.42.7.82.92 1.4.17.42.36 1 .42 2.2.05 1.2.06 1.6.06 4.8s0 3.6-.06 4.8c-.06 1.2-.25 1.8-.42 2.2-.22.6-.49 1-.92 1.4-.42.43-.8.7-1.4.92-.42.17-1 .36-2.2.42-1.2.05-1.6.06-4.8.06s-3.6 0-4.8-.06c-1.2-.06-1.8-.25-2.2-.42-.6-.22-1-.49-1.4-.92-.43-.42-.7-.8-.92-1.4-.17-.42-.36-1-.42-2.2C2.21 15.6 2.2 15.2 2.2 12s0-3.6.06-4.8c.06-1.2.25-1.8.42-2.2.22-.6.49-1 .92-1.4.42-.43.8-.7 1.4-.92.42-.17 1-.36 2.2-.42C8.4 2.21 8.8 2.2 12 2.2Zm0 3.07A6.73 6.73 0 1 0 18.73 12 6.73 6.73 0 0 0 12 5.27Zm0 11.1A4.37 4.37 0 1 1 16.37 12 4.37 4.37 0 0 1 12 16.37Zm6.99-11.4a1.57 1.57 0 1 1-1.57-1.56 1.57 1.57 0 0 1 1.57 1.57Z"/></svg></a>'+
    '<a href="https://www.linkedin.com/company/agrocete/" aria-label="LinkedIn"><svg viewBox="0 0 24 24"><path d="M4.98 3.5A2.5 2.5 0 1 1 0 3.5a2.5 2.5 0 0 1 4.98 0ZM.5 8.5h4V24h-4V8.5ZM8 8.5h3.83v2.1h.06a4.2 4.2 0 0 1 3.78-2.08c4.04 0 4.79 2.66 4.79 6.12V24h-4v-6.6c0-1.57-.03-3.6-2.2-3.6s-2.53 1.72-2.53 3.49V24H8V8.5Z"/></svg></a>'+
    '<a href="https://www.facebook.com/agrocete/" aria-label="Facebook"><svg viewBox="0 0 24 24"><path d="M24 12a12 12 0 1 0-13.88 11.85v-8.38H7.08V12h3.04V9.36c0-3 1.79-4.67 4.53-4.67 1.31 0 2.69.24 2.69.24v2.95h-1.52c-1.49 0-1.96.93-1.96 1.87V12h3.33l-.53 3.47h-2.8v8.38A12 12 0 0 0 24 12Z"/></svg></a>';

  /* ---------------- Header ---------------- */
  function buildHeader(active){
    var t = '__T__';
    return ''+
    '<header class="hdr" id="hdr"><div class="hdr-inner">'+
      '<a class="brand" href="index.html">'+LOGO+'</a>'+
      '<nav class="nav">'+
        '<a href="sobre.html" data-i="nav_sobre" data-page="sobre">'+t+'</a>'+
        '<a href="construcao.html" data-i="nav_constr_s" data-page="construcao">'+t+'</a>'+
        '<a href="produtos.html" data-i="nav_prod" data-page="produtos">'+t+'</a>'+
        '<a href="saber-mais.html" data-i="nav_saber" data-page="saber">'+t+'</a>'+
        '<div class="nav-has"><a href="#" data-i="nav_inst">'+t+'</a>'+
          '<div class="nav-menu">'+
            '<a href="#" data-i="inst_proposito">'+t+'</a>'+
            '<a href="#" data-i="inst_sust">'+t+'</a>'+
            '<a href="#" data-i="inst_inov">'+t+'</a>'+
            '<a href="#" data-i="inst_compliance">'+t+'</a>'+
            '<a href="#" data-i="inst_imprensa">'+t+'</a>'+
            '<a href="#" data-i="inst_vagas">'+t+'</a>'+
            '<a href="#" data-i="inst_canal">'+t+'</a>'+
          '</div>'+
        '</div>'+
      '</nav>'+
      '<div class="hdr-cta">'+
        '<div class="lang" id="lang">'+
          '<button data-lang="pt">PT</button><button data-lang="en">EN</button><button data-lang="es">ES</button>'+
        '</div>'+
        '<a href="contato.html" class="btn btn-primary" data-i="cta_contato">'+t+'</a>'+
        '<button class="menu-toggle" id="menuToggle" aria-label="Menu"><span></span></button>'+
      '</div>'+
    '</div></header>'+
    '<aside class="drawer" id="drawer">'+
      '<a href="sobre.html" data-i="nav_sobre">'+t+'</a>'+
      '<a href="construcao.html" data-i="nav_constr">'+t+'</a>'+
      '<a href="produtos.html" data-i="nav_prod">'+t+'</a>'+
      '<a href="saber-mais.html" data-i="nav_saber">'+t+'</a>'+
      '<a href="contato.html" data-i="nav_contato">'+t+'</a>'+
      '<a class="drawer-sub" href="#" data-i="inst_canal">'+t+'</a>'+
      '<a class="drawer-sub" href="#" data-i="inst_vagas">'+t+'</a>'+
    '</aside>';
  }

  /* ---------------- Footer ---------------- */
  function buildFooter(){
    var t='__T__';
    return ''+
    '<footer class="ftr"><div class="wrap">'+
      '<div class="ftr-top">'+
        '<div class="ftr-brand">'+
          '<a class="brand" href="index.html">'+MARK+'<span>agrocete</span></a>'+
          '<p class="ftr-claim" data-i="ft_claim">'+t+'</p>'+
          '<div class="social" style="margin-top:28px">'+SOCIAL+'</div>'+
        '</div>'+
        '<div><h5 data-i="ft_links">'+t+'</h5><ul>'+
          '<li><a href="sobre.html" data-i="nav_sobre">'+t+'</a></li>'+
          '<li><a href="construcao.html" data-i="nav_constr">'+t+'</a></li>'+
          '<li><a href="produtos.html" data-i="nav_prod">'+t+'</a></li>'+
          '<li><a href="saber-mais.html" data-i="nav_saber">'+t+'</a></li>'+
          '<li><a href="contato.html" data-i="nav_contato">'+t+'</a></li>'+
        '</ul></div>'+
        '<div><h5 data-i="ft_inst">'+t+'</h5><ul>'+
          '<li><a href="#" data-i="inst_proposito">'+t+'</a></li>'+
          '<li><a href="#" data-i="inst_sust">'+t+'</a></li>'+
          '<li><a href="#" data-i="inst_inov">'+t+'</a></li>'+
          '<li><a href="#" data-i="inst_compliance">'+t+'</a></li>'+
          '<li><a href="#" data-i="inst_esg">'+t+'</a></li>'+
          '<li><a href="#" data-i="inst_canal">'+t+'</a></li>'+
        '</ul></div>'+
        '<div><h5 data-i="ft_contato">'+t+'</h5><ul>'+
          '<li><a href="https://maps.google.com/?q=Rua Anna Scremin 800 Ponta Grossa PR">Rua Anna Scremin, 800<br>Distrito Industrial, Ponta Grossa/PR</a></li>'+
          '<li><a href="tel:+554232281229">+55 (42) 3228-1229</a></li>'+
          '<li><a href="mailto:contato@agrocete.com.br">contato@agrocete.com.br</a></li>'+
        '</ul></div>'+
      '</div>'+
      '<div class="ftr-bottom">'+
        '<span data-i="ft_rights">'+t+'</span>'+
        '<div class="ftr-seals">'+
          '<span class="ftr-seal">GPTW<br>Certified</span>'+
          '<span class="ftr-seal">Together for<br>Sustainability</span>'+
          '<span class="ftr-seal">Selo Clima<br>Paraná</span>'+
        '</div>'+
      '</div>'+
    '</div></footer>';
  }

  /* ---------------- i18n apply ---------------- */
  function applyLang(lang){
    var dict = I18N[lang] || I18N.pt;
    document.documentElement.setAttribute('lang', lang==='pt'?'pt-BR':lang);
    document.querySelectorAll('[data-i]').forEach(function(el){
      var k = el.getAttribute('data-i');
      if(dict[k]!=null) el.innerHTML = dict[k];
    });
    document.querySelectorAll('#lang button, .langset button').forEach(function(b){
      b.classList.toggle('on', b.getAttribute('data-lang')===lang);
    });
    localStorage.setItem('agro_lang_v2', lang);
  }

  /* ---------------- Direction ---------------- */
  function applyDir(dir){
    document.documentElement.setAttribute('data-dir', dir);
    localStorage.setItem('agro_dir_v2', dir);
  }

  /* ---------------- Reveal on scroll (rect-based, robust) ---------------- */
  function initReveal(){
    var els = [].slice.call(document.querySelectorAll('.reveal'));
    if(document.documentElement.getAttribute('data-motion')==='off'){
      els.forEach(function(e){e.classList.add('in')}); return;
    }
    function check(){
      var vh = window.innerHeight || document.documentElement.clientHeight;
      els = els.filter(function(e){
        var r = e.getBoundingClientRect();
        if(r.top < vh*0.92 && r.bottom > -40){ e.classList.add('in'); return false; }
        return true;
      });
    }
    check();
    requestAnimationFrame(check);
    window.addEventListener('scroll', check, {passive:true});
    window.addEventListener('resize', check);
    // safety net: ensure nothing stays hidden
    setTimeout(function(){ els.forEach(function(e){e.classList.add('in')}); }, 2600);
  }

  /* ---------------- Header scroll state + mobile nav ---------------- */
  function initChrome(){
    var hdr = document.getElementById('hdr');
    var onScroll = function(){ if(hdr) hdr.setAttribute('data-scrolled', window.scrollY>20?'true':'false'); };
    onScroll(); window.addEventListener('scroll', onScroll, {passive:true});

    var mt = document.getElementById('menuToggle');
    if(mt) mt.addEventListener('click', function(){ document.body.classList.toggle('nav-open'); });
    document.querySelectorAll('#drawer a').forEach(function(a){
      a.addEventListener('click', function(){ document.body.classList.remove('nav-open'); });
    });
    document.querySelectorAll('#lang button, .langset button').forEach(function(b){
      b.addEventListener('click', function(){ applyLang(b.getAttribute('data-lang')); });
    });

    // active nav
    var active = document.body.getAttribute('data-page');
    if(active) document.querySelectorAll('.nav a[data-page="'+active+'"]').forEach(function(a){a.classList.add('active');});
  }

  /* ---------------- Tweaks panel (vanilla, host protocol) ---------------- */
  var TWEAKS = {
    dir:   {label:'Direção', type:'radio', options:[['raizes','Raízes'],['sistema','Sistema'],['terra','Terra']], def:'raizes'},
    accent:{label:'Cor de acento', type:'swatch', options:['#044F8B','#179E57','#B16A40','#3E6E89','#5C8A3A'], def:'#044F8B'},
    font:  {label:'Fonte de título', type:'radio', options:[['clean','Schibsted'],['display','Bricolage'],['neutral','Hanken']], def:'clean'},
    motion:{label:'Animação', type:'toggle', def:true},
    density:{label:'Respiro', type:'radio', options:[['compact','Compacto'],['comfy','Padrão'],['airy','Arejado']], def:'comfy'}
  };
  var FONTMAP = {clean:'"Schibsted Grotesk", system-ui, sans-serif', display:'"Bricolage Grotesque", system-ui, sans-serif', neutral:'"Hanken Grotesk", system-ui, sans-serif'};
  var WEIGHTMAP = {clean:'600', display:'700', neutral:'700'};
  // each direction has a natural font + accent — switching dir adopts them
  var DIR_FONT = {raizes:'clean', sistema:'display', terra:'display'};
  var DIR_ACCENT = {raizes:'#044F8B', sistema:'#179E57', terra:'#B16A40'};

  function readTweaks(){
    var s = {}; try{ s = JSON.parse(localStorage.getItem('agro_tweaks_v2')||'{}'); }catch(e){}
    for(var k in TWEAKS){ if(s[k]==null) s[k]=TWEAKS[k].def; }
    return s;
  }
  function writeTweaks(s){ localStorage.setItem('agro_tweaks_v2', JSON.stringify(s)); }

  function applyTweaks(s){
    applyDir(s.dir);
    var r = document.documentElement.style;
    r.setProperty('--accent', s.accent);
    r.setProperty('--font-display', FONTMAP[s.font]);
    r.setProperty('--display-weight', WEIGHTMAP[s.font]);
    document.documentElement.setAttribute('data-motion', s.motion?'on':'off');
    if(!s.motion){ document.querySelectorAll('.reveal').forEach(function(e){e.classList.add('in')}); }
    var pad = s.density==='compact'?'.72':(s.density==='airy'?'1.25':'1');
    r.setProperty('--density', pad);
  }

  function buildTweaksPanel(){
    var wrap = document.createElement('div');
    wrap.id='tweaksPanel';
    wrap.innerHTML = '<div class="tw-head"><strong>Tweaks</strong><button id="twClose" aria-label="Fechar">×</button></div><div class="tw-body" id="twBody"></div>';
    document.body.appendChild(wrap);
    var body = wrap.querySelector('#twBody');
    var s = readTweaks();

    Object.keys(TWEAKS).forEach(function(key){
      var cfg = TWEAKS[key];
      var sec = document.createElement('div'); sec.className='tw-sec';
      sec.innerHTML = '<label class="tw-label">'+cfg.label+'</label>';
      var ctrl;
      if(cfg.type==='radio'){
        ctrl=document.createElement('div'); ctrl.className='tw-seg'; ctrl.dataset.tw=key;
        cfg.options.forEach(function(o){
          var b=document.createElement('button'); b.textContent=o[1]; b.dataset.val=o[0];
          b.className = s[key]===o[0]?'on':'';
          b.onclick=function(){
            s[key]=o[0];
            if(key==='dir'){ s.font=DIR_FONT[o[0]]; s.accent=DIR_ACCENT[o[0]]; }
            writeTweaks(s); applyTweaks(s);
            ctrl.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x.dataset.val===o[0])});
            if(key==='dir') syncControls(s);
          };
          ctrl.appendChild(b);
        });
      } else if(cfg.type==='swatch'){
        ctrl=document.createElement('div'); ctrl.className='tw-swatches';
        cfg.options.forEach(function(c){
          var b=document.createElement('button'); b.style.background=c; b.dataset.val=c;
          b.className = s[key]===c?'on':'';
          b.onclick=function(){ s[key]=c; writeTweaks(s); applyTweaks(s); ctrl.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x.dataset.val===c)}); };
          ctrl.appendChild(b);
        });
      } else if(cfg.type==='toggle'){
        ctrl=document.createElement('button'); ctrl.className='tw-toggle'+(s[key]?' on':'');
        ctrl.innerHTML='<span></span>';
        ctrl.onclick=function(){ s[key]=!s[key]; writeTweaks(s); applyTweaks(s); ctrl.classList.toggle('on',s[key]); };
      }
      sec.appendChild(ctrl); body.appendChild(sec);
    });

    wrap.querySelector('#twClose').onclick=function(){ setPanel(false); };
  }

  // reflect programmatic state changes (e.g. dir-driven font/accent) in the controls
  function syncControls(s){
    var fc=document.querySelector('[data-tw="font"]');
    if(fc) fc.querySelectorAll('button').forEach(function(x){x.classList.toggle('on',x.dataset.val===s.font)});
    document.querySelectorAll('.tw-swatches button').forEach(function(x){x.classList.toggle('on',x.dataset.val===s.accent)});
  }

  var panelOpen=false;
  function setPanel(open){ panelOpen=open; var p=document.getElementById('tweaksPanel'); if(p) p.classList.toggle('open',open); }

  // host protocol: listen for tweaks visibility toggle
  window.addEventListener('message', function(e){
    var d=e.data; if(!d||typeof d!=='object') return;
    if(d.type==='tweaks:visibility'||d.type==='omelette:tweaks'){ setPanel(!!d.visible); }
    if(d.type==='tweaks:toggle'){ setPanel(!panelOpen); }
  });

  /* ---------------- Boot ---------------- */
  function boot(){
    var active = document.body.getAttribute('data-page')||'';
    // inject chrome
    var headerHost = document.getElementById('site-header');
    if(headerHost) headerHost.outerHTML = buildHeader(active);
    var footerHost = document.getElementById('site-footer');
    if(footerHost) footerHost.outerHTML = buildFooter();

    var lang = localStorage.getItem('agro_lang_v2')||'pt';
    applyLang(lang);
    applyTweaks(readTweaks());
    buildTweaksPanel();
    initChrome();
    initReveal();
  }

  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
