import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

def create_invoice(quantities, total_price, chocolates):
    invoice_id = f"invoice_{int(os.urandom(4).hex(), 16)}.pdf"
    invoice_path = os.path.join('invoices', invoice_id)

    doc = SimpleDocTemplate(invoice_path, pagesize=A4)
    data = [['Sr. No.', 'Product', 'Quantity', 'Price']]
    sr_no = 1
    for choco, qty in quantities.items():
        if qty > 0:  # Only add to invoice if quantity is greater than 0
            data.append([str(sr_no), chocolates[choco]['name'], str(qty), f'{qty * chocolates[choco]['price']} Rs'])
            sr_no += 1
    data.append(['', '', 'Total', f'{total_price} Rs'])

    table = Table(data, style=[
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 14),  # Increase font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 18),  # Increase bottom padding
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    styles = getSampleStyleSheet()
    centered_style = ParagraphStyle(name='Centered', parent=styles['Normal'], alignment=TA_CENTER)
    company_name = Paragraph("<b>Swiss-IN</b>", styles['Heading1'])
    contact_details = Paragraph("<b>Contact Details:</b> <br/>Address: 123 Chocolate Lane, Ahmedabad, Gujarat, India<br/>Phone: +91 1234567890<br/>Email: info@swissin.com", styles['BodyText'])

    content = [company_name, Spacer(1, 10), contact_details, Spacer(1, 10), table, Spacer(1, 10), Paragraph("Thank you for your purchase!", centered_style)]

    doc.build(content)
    return invoice_id
