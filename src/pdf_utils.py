from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch

def generate_pdf(filename, schedule, client_name, principal, term, logo_path, template_path):
    # Create PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    
    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles['Title'],
        fontSize=24,
        alignment=1,  # Center alignment
        spaceAfter=12,
        textColor=colors.blue
    )
    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.leading = 14
    normal_style.spaceAfter = 6

    # Build the PDF content
    content = []

    # Add logo in the center
    if logo_path:
        logo = Image(logo_path, width=2*inch, height=2*inch)  # Adjust size as needed
        logo.hAlign = 'CENTER'
        content.append(logo)
        content.append(Spacer(1, 12))

    # Add client information
    client_info = [
        [Paragraph(f"Nombre de Cliente: {client_name}", normal_style)],
        [Paragraph(f"Monto Total: ${principal:.2f}", normal_style)],
        [Paragraph(f"Plazo: {term} Meses", normal_style)]
    ]
    
    client_table = Table(client_info, colWidths=[3.5 * inch])
    client_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))

    content.append(client_table)
    content.append(Spacer(1, 12))

    # Add schedule details (keeping original table format)
    data = [['Pagos', 'Interes y Servicio', 'Abono a Capital', 'Total a Cancelar', 'Capital Restante']]
    for i, payment in enumerate(schedule, start=1):
        data.append([f"Payment {i}",
                     f"Q{payment['Interes y Servicio']}",
                     f"Q{payment['Abono a Capital']}",
                     f"Q{payment['Total Cancelar']}",
                     f"Q{payment['Capital Restante']}"])

    table = Table(data, colWidths=[1 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch, 1.5 * inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('ALIGN', (0, 1), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    
    content.append(table)

    # Build the PDF
    doc.build(content)
