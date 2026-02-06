# -*- coding: utf-8 -*-
from fpdf import FPDF
from datetime import datetime

class RelatorioPDF(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, 'Madetech - Relatorio de Performance', align='C')
        self.ln(15)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f'Pagina {self.page_no()}', align='C')

    def titulo_secao(self, titulo):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, titulo, ln=True)
        self.ln(2)

    def subtitulo(self, texto):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, texto, ln=True)

    def texto_normal(self, texto):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 6, texto)
        self.ln(2)

    def texto_destaque(self, texto):
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(39, 174, 96)
        self.multi_cell(0, 6, texto)
        self.ln(2)

    def criar_tabela(self, headers, dados, col_widths):
        # Header da tabela
        self.set_font('Helvetica', 'B', 9)
        self.set_fill_color(41, 128, 185)
        self.set_text_color(255, 255, 255)
        
        for i, header in enumerate(headers):
            self.cell(col_widths[i], 8, header, border=1, fill=True, align='C')
        self.ln()
        
        # Dados da tabela
        self.set_font('Helvetica', '', 9)
        self.set_text_color(50, 50, 50)
        fill = False
        
        for row in dados:
            if fill:
                self.set_fill_color(240, 248, 255)
            else:
                self.set_fill_color(255, 255, 255)
            
            for i, cell in enumerate(row):
                self.cell(col_widths[i], 7, str(cell), border=1, fill=True, align='C')
            self.ln()
            fill = not fill

    def bullet_point(self, texto, cor_verde=False):
        if cor_verde:
            self.set_text_color(39, 174, 96)
            bullet = "+"
        else:
            self.set_text_color(60, 60, 60)
            bullet = "-"
        self.set_font('Helvetica', '', 10)
        x_start = self.get_x()
        self.cell(8, 6, bullet)
        self.set_x(x_start + 8)
        self.multi_cell(0, 6, texto)
        self.set_x(x_start)


# Criar o PDF
pdf = RelatorioPDF()
pdf.add_page()

# Titulo Principal
pdf.set_font('Helvetica', 'B', 24)
pdf.set_text_color(44, 62, 80)
pdf.cell(0, 15, 'Relatorio de Lancamento', align='C', ln=True)

pdf.set_font('Helvetica', '', 12)
pdf.set_text_color(100, 100, 100)
pdf.cell(0, 8, 'www.madetech.com.br', align='C', ln=True)
pdf.cell(0, 6, 'Periodo: 07 Janeiro - 03 Fevereiro 2026 (4 semanas)', align='C', ln=True)
pdf.cell(0, 6, f'Gerado em: {datetime.now().strftime("%d/%m/%Y")}', align='C', ln=True)
pdf.ln(10)

# Linha decorativa
pdf.set_draw_color(41, 128, 185)
pdf.set_line_width(1)
pdf.line(20, pdf.get_y(), 190, pdf.get_y())
pdf.ln(10)

# Resumo Executivo
pdf.titulo_secao('Resumo Executivo')
pdf.texto_normal('Os primeiros resultados do lancamento sao bastante promissores! Em apenas 4 semanas, o site ja demonstra sinais solidos de crescimento e engajamento.')
pdf.ln(3)

# Tabela de Metricas Gerais
headers_resumo = ['Metrica', 'Resultado']
dados_resumo = [
    ['Total de Sessoes', '419 visitas'],
    ['Sessoes Engajadas', '184 (44%)'],
    ['Tempo Medio no Site', '54 segundos'],
    ['Eventos Registrados', '48.943 interacoes'],
    ['Media Diaria', '~15 sessoes/dia']
]
pdf.criar_tabela(headers_resumo, dados_resumo, [95, 95])
pdf.ln(10)

# Campanha de Email
pdf.titulo_secao('Campanha de Email - Primeiros Resultados')
pdf.texto_normal('A campanha de email que iniciamos ja representa 18,6% de todo o trafego do site:')
pdf.ln(2)

pdf.bullet_point('78 sessoes originadas de emails', cor_verde=True)
pdf.bullet_point('26 sessoes engajadas (33% de engajamento)', cor_verde=True)
pdf.bullet_point('Tempo medio de 23 segundos por visita', cor_verde=True)
pdf.ln(3)

pdf.texto_normal('Perspectiva: Para uma campanha inicial, esses numeros sao uma excelente base. A medida que refinamos os titulos e CTAs dos emails, a tendencia e de crescimento no engajamento.')
pdf.ln(5)

# SEO
pdf.titulo_secao('SEO - O Investimento que Vai Render')
pdf.texto_normal('O site foi construido com estrutura SEO completa, e isso ja esta dando sinais positivos:')
pdf.ln(2)

pdf.bullet_point('29 sessoes de Busca Organica em apenas 4 semanas', cor_verde=True)
pdf.bullet_point('65,52% de taxa de engajamento - a MAIOR entre todos os canais!', cor_verde=True)
pdf.bullet_point('Tempo medio de 46s e 186 eventos por sessao', cor_verde=True)
pdf.ln(3)

pdf.subtitulo('Por que isso e excelente?')
pdf.texto_normal('O Google leva em media 3-6 meses para indexar e ranquear um site novo adequadamente. Ja termos 29 visitas organicas com alta qualidade de engajamento indica que:')
pdf.ln(2)

pdf.bullet_point('O site esta sendo indexado corretamente', cor_verde=True)
pdf.bullet_point('O conteudo esta atraindo o publico certo', cor_verde=True)
pdf.bullet_point('A estrutura tecnica de SEO esta funcionando', cor_verde=True)
pdf.ln(3)

pdf.texto_destaque('Projecao: Nos proximos 2-3 meses, esperamos um crescimento significativo no trafego organico a medida que o Google reconheca a autoridade do dominio.')

# Nova pagina para tabela de canais
pdf.add_page()

# Distribuicao por Canal
pdf.titulo_secao('Distribuicao por Canal de Aquisicao')
pdf.ln(3)

headers_canais = ['Canal', 'Sessoes', '% Total', 'Engajamento', 'Tempo']
dados_canais = [
    ['Direct', '285', '68,02%', '47,37%', '1min 03s'],
    ['Email', '78', '18,62%', '33,33%', '23s'],
    ['Unassigned', '33', '7,88%', '0%', '43s'],
    ['Organic Search', '29', '6,92%', '65,52%', '46s'],
    ['Organic Social', '8', '1,91%', '50%', '3s'],
    ['Referral', '1', '0,24%', '0%', '0s']
]
pdf.criar_tabela(headers_canais, dados_canais, [40, 30, 30, 40, 30])
pdf.ln(10)

# Trafego Direto
pdf.titulo_secao('Trafego Direto - Reconhecimento de Marca')
pdf.texto_normal('68% do trafego e direto (285 sessoes), o que significa que as pessoas estao:')
pdf.ln(2)

pdf.bullet_point('Digitando o URL diretamente', cor_verde=True)
pdf.bullet_point('Salvando nos favoritos', cor_verde=True)
pdf.bullet_point('Voltando ao site por conta propria', cor_verde=True)
pdf.ln(3)

pdf.texto_destaque('Isso e um excelente indicador de interesse e retencao para um projeto recem-lancado!')
pdf.ln(8)

# Conclusao
pdf.titulo_secao('Conclusao')
pdf.set_fill_color(232, 245, 233)
pdf.set_draw_color(39, 174, 96)
pdf.rect(15, pdf.get_y(), 180, 45, style='DF')
pdf.set_xy(20, pdf.get_y() + 5)

pdf.set_font('Helvetica', '', 10)
pdf.set_text_color(50, 50, 50)
conclusao = """Para um lancamento de menos de 1 mes, os numeros sao solidos. O investimento em SEO foi estrategico - os frutos virao nos proximos meses quando o Google consolidar o ranqueamento. A campanha de email esta trazendo trafego constante e pode ser otimizada para aumentar conversoes.

Estamos no caminho certo!"""

pdf.multi_cell(170, 6, conclusao)
pdf.ln(15)

# Proximos Passos
pdf.set_y(pdf.get_y() + 10)
pdf.titulo_secao('Proximos Passos Sugeridos')
pdf.bullet_point('Continuar monitorando metricas de SEO', cor_verde=True)
pdf.bullet_point('Otimizar titulos e CTAs dos emails', cor_verde=True)
pdf.bullet_point('Aumentar presenca em redes sociais', cor_verde=True)
pdf.bullet_point('Criar mais conteudo para atrair trafego organico', cor_verde=True)

# Salvar PDF
output_path = 'Relatorio_Madetech.pdf'
pdf.output(output_path)
print(f'Relatorio gerado com sucesso: {output_path}')
