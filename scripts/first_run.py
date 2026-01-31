"""
Script para executar primeiro ciclo completo do sistema
"""
import sys
import asyncio
from pathlib import Path
from datetime import datetime

# Adiciona o diretório raiz ao Python path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from config.settings import settings
from src.database.connection import SessionLocal
from src.database import repository
from src.collectors.shopee_api import ShopeeAffiliateAPI
from src.collectors.offer_parser import OfferParser
from src.ranking.scorer import ProductScorer
from src.ranking.selector import ProductSelector
from src.content.generator import ContentGenerator
from src.links.shortener import LinkShortener
from src.utils.logger import get_logger

logger = get_logger(__name__)


async def step1_coletar_produtos(db, nicho: str = "tech"):
    """Passo 1: Coleta produtos da Shopee"""
    print(f"\n📥 PASSO 1: Coletando produtos do nicho '{nicho}'...")
    
    api = ShopeeAffiliateAPI()
    parser = OfferParser()
    
    raw_offers = await api.get_product_offers(limit=20)
    
    produtos_salvos = []
    for raw_offer in raw_offers:
        produto_data = parser.parse_offer(raw_offer, nicho)
        
        if not produto_data:
            continue
        
        is_valid, motivo = parser.validar_produto(produto_data)
        if not is_valid:
            continue
        
        # Verifica duplicata
        existing = repository.ProdutoRepository.buscar_por_shopee_id(
            db, produto_data["shopee_id"]
        )
        
        if not existing:
            produto = repository.ProdutoRepository.criar(db, produto_data)
            produtos_salvos.append(produto)
    
    print(f"  ✅ {len(produtos_salvos)} produtos coletados e salvos")
    return produtos_salvos


def step2_rankear_produtos(db, produtos):
    """Passo 2: Ranqueia produtos"""
    print(f"\n⭐ PASSO 2: Ranqueando {len(produtos)} produtos...")
    
    scorer = ProductScorer()
    
    for produto in produtos:
        produto_dict = {
            "shopee_id": produto.shopee_id,
            "comissao_percentual": produto.comissao_percentual,
            "preco_original": produto.preco_original,
            "preco_promocional": produto.preco_promocional,
            "desconto_percentual": produto.desconto_percentual,
            "rating": produto.rating,
            "total_vendas": produto.total_vendas
        }
        
        score, motivo = scorer.calcular_score(produto_dict)
        repository.ProdutoRepository.atualizar_score(db, produto.id, score, motivo)
    
    print(f"  ✅ Produtos ranqueados")


def step3_selecionar_top(db, nicho: str, top_n: int = 5):
    """Passo 3: Seleciona top produtos"""
    print(f"\n🏆 PASSO 3: Selecionando top {top_n} produtos...")
    
    top_produtos = repository.ProdutoRepository.top_ranqueados(db, nicho, top_n)
    
    print(f"  ✅ Top {len(top_produtos)} produtos selecionados:")
    for i, p in enumerate(top_produtos, 1):
        print(f"     {i}. {p.nome[:50]}... (Score: {p.score_ranking:.1f})")
    
    return top_produtos


def step4_gerar_conteudo(db, produtos, canal: str = "grupo"):
    """Passo 4: Gera conteúdo"""
    print(f"\n✍️  PASSO 4: Gerando conteúdo para canal '{canal}'...")
    
    generator = ContentGenerator()
    total_gerado = 0
    
    for produto in produtos:
        produto_dict = {
            "id": produto.id,
            "nome": produto.nome,
            "preco_original": produto.preco_original,
            "preco_promocional": produto.preco_promocional,
            "desconto_percentual": produto.desconto_percentual,
            "nicho": produto.nicho,
            "url_produto": produto.url_produto,
            "imagem_url": produto.imagem_url
        }
        
        # Gera 1 conteúdo por produto
        conteudo = generator.generate_for_canal(
            canal=canal,
            produto=produto_dict
        )
        
        conteudo_data = {
            "produto_id": produto.id,
            "canal": conteudo.get('canal'),
            "formato": conteudo.get('formato'),
            "persona": conteudo.get('persona'),
            "template": conteudo.get('template'),
            "copy_texto": conteudo.get('copy_texto', ''),
            "variacao_numero": 1,
            "aprovado": True  # Auto-aprova para primeiro ciclo
        }
        
        repository.ConteudoRepository.criar(db, conteudo_data)
        total_gerado += 1
    
    print(f"  ✅ {total_gerado} conteúdos gerados")


async def step5_gerar_links(db, produtos):
    """Passo 5: Gera links de afiliado"""
    print(f"\n🔗 PASSO 5: Gerando links de afiliado...")
    
    shortener = LinkShortener()
    total_links = 0
    
    for produto in produtos[:3]:  # Apenas 3 para teste
        try:
            parts = produto.shopee_id.split("_")
            if len(parts) < 2:
                continue
            
            shop_id = parts[0]
            item_id = "_".join(parts[1:])
            
            link_data = await shortener.generate_short_link(
                item_id=item_id,
                shop_id=shop_id,
                canal="grupo",
                nicho=produto.nicho,
                formato="texto",
                campanha="first_run"
            )
            
            if link_data:
                link_data["produto_id"] = produto.id
                repository.LinkRepository.criar(db, link_data)
                total_links += 1
                
        except Exception as e:
            logger.warning(f"Erro ao gerar link para {produto.shopee_id}: {e}")
    
    print(f"  ✅ {total_links} links gerados")


async def main():
    """Executa ciclo completo"""
    print("=" * 70)
    print("SHOPEE AFFILIATE OPS - Primeiro Ciclo Completo")
    print("=" * 70)
    print(f"\n⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    db = SessionLocal()
    
    try:
        # 1. Coleta
        produtos = await step1_coletar_produtos(db, nicho="tech")
        
        if not produtos:
            print("\n❌ Nenhum produto coletado. Verifique as credenciais da Shopee.")
            return
        
        # 2. Ranking
        step2_rankear_produtos(db, produtos)
        
        # 3. Seleção
        top_produtos = step3_selecionar_top(db, nicho="tech", top_n=5)
        
        # 4. Conteúdo
        step4_gerar_conteudo(db, top_produtos, canal="grupo")
        
        # 5. Links
        await step5_gerar_links(db, top_produtos)
        
        print("\n" + "=" * 70)
        print("✨ CICLO COMPLETO FINALIZADO!")
        print("=" * 70)
        print("\n📊 Resumo:")
        print(f"   • Produtos coletados: {len(produtos)}")
        print(f"   • Top produtos: {len(top_produtos)}")
        print(f"   • Conteúdos gerados: {len(top_produtos)}")
        print("\n💡 Próximos passos:")
        print("   1. Acesse http://localhost:8000 para ver a API")
        print("   2. Use os endpoints em /api/products, /api/content, etc")
        print("   3. Configure workflows N8N para automação")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        logger.error(f"Erro no first_run: {e}")
        
    finally:
        db.close()
        print(f"\n⏰ Fim: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")


if __name__ == "__main__":
    asyncio.run(main())
