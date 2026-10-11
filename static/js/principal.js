/**
 * KotasPay - Scripts de Interatividade da Landing Page
 * Desenvolvido em JavaScript Vanilla (sem dependências externas)
 */

document.addEventListener('DOMContentLoaded', () => {
  // 1. Header Sticky com Efeito Glassmorphism no Scroll
  const cabecalho = document.getElementById('cabecalho-principal');
  if (cabecalho) {
    const atualizarHeaderScroll = () => {
      if (window.scrollY > 20) {
        cabecalho.classList.add('cabecalho--scrolled');
      } else {
        cabecalho.classList.remove('cabecalho--scrolled');
      }
    };
    window.addEventListener('scroll', atualizarHeaderScroll, { passive: true });
    atualizarHeaderScroll();
  }

  // 2. Menu Mobile Toggle
  const btnMenuMobile = document.getElementById('btn-menu-mobile');
  const menuNavegacao = document.getElementById('menu-navegacao');
  if (btnMenuMobile && menuNavegacao) {
    btnMenuMobile.addEventListener('click', () => {
      const estaAberto = btnMenuMobile.classList.toggle('cabecalho__toggle-mobile--ativo');
      menuNavegacao.classList.toggle('cabecalho__navegacao--aberto');
      btnMenuMobile.setAttribute('aria-expanded', estaAberto);
    });

    // Fechar ao clicar em qualquer link de navegação
    menuNavegacao.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        btnMenuMobile.classList.remove('cabecalho__toggle-mobile--ativo');
        menuNavegacao.classList.remove('cabecalho__navegacao--aberto');
        btnMenuMobile.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // 3. Sistema de Abas Interativas (Tabs de Públicos-Alvo)
  const tabBotoes = document.querySelectorAll('.tab-btn');
  const tabPaineis = document.querySelectorAll('.tab-painel');

  const ativarAba = (targetId) => {
    const painelAlvo = document.getElementById(targetId);
    if (!painelAlvo) return;

    tabBotoes.forEach(btn => {
      const ehAlvo = btn.getAttribute('data-target') === targetId;
      btn.classList.toggle('tab-btn--ativo', ehAlvo);
      btn.setAttribute('aria-selected', ehAlvo ? 'true' : 'false');
    });

    tabPaineis.forEach(painel => {
      const ehAlvo = painel.id === targetId;
      if (ehAlvo) {
        painel.removeAttribute('hidden');
        painel.classList.add('tab-painel--ativo');
      } else {
        painel.setAttribute('hidden', '');
        painel.classList.remove('tab-painel--ativo');
      }
    });
  };

  tabBotoes.forEach(botao => {
    botao.addEventListener('click', () => {
      const targetId = botao.getAttribute('data-target');
      ativarAba(targetId);
    });
  });

  // Ativar aba via parâmetro ?aba=associacoes|cooperativas|membros da URL
  const paramsUrl = new URLSearchParams(window.location.search);
  const abaSolicitada = paramsUrl.get('aba');
  const mapaAbas = {
    associacoes: 'tab-painel-associacoes',
    cooperativas: 'tab-painel-cooperativas',
    membros: 'tab-painel-membros'
  };
  if (abaSolicitada && mapaAbas[abaSolicitada]) {
    ativarAba(mapaAbas[abaSolicitada]);
  }

  // 4. Rolagem Suave com Offset para Links Âncora Internos
  document.querySelectorAll('a[href^="#"]').forEach(ancora => {
    ancora.addEventListener('click', (e) => {
      const href = ancora.getAttribute('href');
      if (href && href !== '#' && href.startsWith('#')) {
        const elementoDestino = document.querySelector(href);
        if (elementoDestino) {
          e.preventDefault();
          const alturaHeader = cabecalho ? cabecalho.offsetHeight : 70;
          const elementoPos = elementoDestino.getBoundingClientRect().top + window.scrollY;
          window.scrollTo({
            top: elementoPos - alturaHeader - 20,
            behavior: 'smooth'
          });
        }
      }
    });
  });

  // 5. Máscara Amigável de WhatsApp no Formulário
  const inputWhatsapp = document.getElementById('id_whatsapp');
  if (inputWhatsapp) {
    inputWhatsapp.addEventListener('input', (e) => {
      let valor = e.target.value.replace(/\D/g, '');
      if (valor.length > 11) valor = valor.substring(0, 11);
      
      if (valor.length > 6) {
        valor = `(${valor.substring(0, 2)}) ${valor.substring(2, 7)}-${valor.substring(7)}`;
      } else if (valor.length > 2) {
        valor = `(${valor.substring(0, 2)}) ${valor.substring(2)}`;
      } else if (valor.length > 0) {
        valor = `(${valor}`;
      }
      e.target.value = valor;
    });
  }
});
