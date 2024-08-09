from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfgen import canvas
from PyPDF2 import PdfReader, PdfWriter
import os

def generate_pdf(filename, schedule, client_name, principal, months, logo_path=None, template_path=None):
    # Create a temporary PDF with the loan data
    temp_pdf = filename.replace(".pdf", "_temp.pdf")
    pdf = SimpleDocTemplate(temp_pdf, pagesize=A4)
    elements = []

    # Add client info
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Cliente: {client_name}", styles['Title']))
    elements.append(Paragraph(f"Monto de Crédito: ${principal:.2f}", styles['Normal']))
    elements.append(Paragraph(f"Plazo de Pagos: {months} meses", styles['Normal']))
    elements.append(Paragraph(" ", styles['Normal']))  # Add some space

    # Prepare the table data
    table_data = [['Mes', 'Interes y Servicios', 'Abono a Capital', 'Total a Cancelar', 'Capital Restante']]

    for i, payment in enumerate(schedule, start=1):
        table_data.append([
            f"{i}",
            f"${payment['Interes y Servicio']:.2f}",
            f"${payment['Abono a Capital']:.2f}",
            f"${payment['Total Cancelar']:.2f}",
            f"${payment['Capital Restante']:.2f}",
        ])

    # Create the table
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build the temporary PDF
    pdf.build(elements)

    # Merge the temporary PDF with the template
    if template_path and os.path.exists(template_path):
        template_pdf = PdfReader(template_path)
        temp_pdf_reader = PdfReader(temp_pdf)
        output_pdf = PdfWriter()

        # Overlay each page
        for page in template_pdf.pages:
            temp_page = temp_pdf_reader.pages[0]  # Assuming one page of data for now
            page.merge_page(temp_page)
            output_pdf.add_page(page)

        with open(filename, 'wb') as output_file:
            output_pdf.write(output_file)
        
        # Clean up the temporary PDF
        os.remove(temp_pdf)
    else:
        # If no template, just rename the temp PDF to final filename
        os.rename(temp_pdf, filename)
