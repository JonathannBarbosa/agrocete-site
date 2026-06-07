/* AGROCETE — products data + card renderer (shared home/produtos) */
(function(){
  var BASE="https://agrocete-site.s3.sa-east-1.amazonaws.com/images/landing_pages/";
  // line keys: clay = Plantio/enraizamento · leaf = Arranque · tech = Tecnologia
  var P = [
    {n:"GRAP STPRO",      line:"clay", l:"Plantio & enraizamento", id:"grap-stpro",      f:"16_V9KwIXZt7suaQOy.png"},
    {n:"GRAP NOD L+",     line:"clay", l:"Plantio & enraizamento", id:"grap-nod-l",       f:"25_Hrvf3Hs2q1GLslQ.png"},
    {n:"GRAP NOD AL",     line:"clay", l:"Plantio & enraizamento", id:"grap-nod-al",      f:"26_d2MCEgs3aw14m2x.png"},
    {n:"GRAP EXTRA NOD",  line:"clay", l:"Plantio & enraizamento", id:"grap-extra-nod",   f:"51_mtlZymSAIdXR9JG.png"},
    {n:"GRAP NOD PHOS",   line:"clay", l:"Plantio & enraizamento", id:"grap-nod-phos",    f:"58_Bl1DOCQyqQKcoXI.png"},
    {n:"GRAP BeesTRIC",   line:"clay", l:"Plantio & enraizamento", id:"grap-beestric",    f:"101_eInLeJCmMc8trC2.png"},
    {n:"BIOSTAT",         line:"clay", l:"Plantio & enraizamento", id:"biostat",          f:"102_SFBNDeKVy5vEoO9.png"},
    {n:"GRAP GRAD",       line:"leaf", l:"Arranque & crescimento", id:"grap-grad",        f:"23_F37XmlHg4et9agg.png"},
    {n:"GRAP EVIC-S",     line:"leaf", l:"Arranque & crescimento", id:"grap-evic-s",      f:"24_airlDJqy8aJuY6O.png"},
    {n:"GRAP FIELD PRO",  line:"leaf", l:"Arranque & crescimento", id:"grap-field-pro",   f:"60_wU5pzztxVfh6FqI.png"},
    {n:"GRAP BREED PRO",  line:"leaf", l:"Arranque & crescimento", id:"grap-breed-pro",   f:"61_xTsR99xoT7W2h5I.png"},
    {n:"GRAP ORGANO TOP", line:"leaf", l:"Arranque & crescimento", id:"grap-organo-top",  f:"62_GAPf06TRJPsqyyD.png"},
    {n:"GRAP AMYNO 15",   line:"leaf", l:"Arranque & crescimento", id:"grap-amyno-15",    f:"63_NlQioF2xSyKoIVZ.png"},
    {n:"GRAP SUPER GUN",  line:"tech", l:"Tecnologia de aplicação", id:"grap-super-gun",   f:"27_5yHOXkY2GSNl2Fu.png"},
    {n:"GRAP SUPER GUN SR",line:"tech",l:"Tecnologia de aplicação", id:"grap-super-gun-sr",f:"59_Im71SXKDkTmmeCS.png"},
    {n:"GRAP D-LIM",      line:"tech", l:"Tecnologia de aplicação", id:"grap-d-lim",       f:"28_KIBAv2xurLMhPbW.png"},
    {n:"GRAP TECH",       line:"tech", l:"Tecnologia de aplicação", id:"grap-tech",        f:"30_i2nZ1qcInNywOM5.png"},
    {n:"GRAP TECH NR",    line:"tech", l:"Tecnologia de aplicação", id:"grap-tech-nr",     f:"29_1pFpM8GhdShueat.png"},
    {n:"GRAP SWIFT",      line:"tech", l:"Tecnologia de aplicação", id:"grap-swift",       f:"31_MHHQ9refHBJzqb2.png"},
    {n:"ALPHATANK",       line:"tech", l:"Tecnologia de aplicação", id:"alphatank",        f:"95_6pSMwAvguHagSti.png"}
  ];
  P.forEach(function(p){ p.img = BASE + p.f; });
  window.AGRO_PRODUCTS = P;

  window.productCard = function(p){
    var arrow='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
    return ''+
    '<article class="prod-card reveal" data-line="'+p.line+'">'+
      '<div class="pc-media"><image-slot id="prod-'+p.id+'" fit="contain" src="'+p.img+'" placeholder="'+p.n+'"></image-slot></div>'+
      '<div class="pc-bot">'+
        '<span class="pc-line is-'+p.line+'"><span class="dot"></span>'+p.l+'</span>'+
        '<h4>'+p.n+'</h4>'+
        '<a href="#" class="link-arrow pc-link">Saiba mais '+arrow+'</a>'+
      '</div>'+
    '</article>';
  };
})();
