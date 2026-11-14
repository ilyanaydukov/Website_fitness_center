from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import date
from typing import List

def generate_equipment_pdf(equipment_list):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30
    )
    
    # Title
    elements.append(Paragraph("Equipment Report", title_style))
    elements.append(Spacer(1, 0.25*inch))
    
    # Table data
    data = [['ID', 'Name', 'Category', 'Purchase Date', 'Last Service', 'Condition']]
    
    for equipment in equipment_list:
        data.append([
            str(equipment.id),
            str(equipment.name) if equipment.name else 'N/A',
            equipment.category.name if equipment.category and equipment.category.name else 'N/A',
            str(equipment.purchase_date) if equipment.purchase_date else 'N/A',
            str(equipment.date_of_last_service) if equipment.date_of_last_service else 'N/A',
            str(equipment.description_of_condition) if equipment.description_of_condition else 'N/A'
        ])
    
    # Create table
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Generated on: {date.today()}", styles['Normal']))
    
    # Build PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_schedule_pdf(workouts, date_from, date_to):
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        
        # Title
        elements.append(Paragraph("Workout Schedule Report", title_style))
        elements.append(Paragraph(f"Period: {date_from} to {date_to}", styles['Heading2']))
        elements.append(Spacer(1, 0.25*inch))
        
        # Table data
        data = [['ID', 'Date', 'Time', 'Room', 'Trainer', 'Service', 'Capacity', 'Registered']]
        
        for workout in workouts:
            # Получаем имя тренера с защитой от None
            trainer_name = 'N/A'
            if workout.trainer and workout.trainer.employee:
                trainer_name = f"{workout.trainer.employee.first_name} {workout.trainer.employee.last_name}"
            elif workout.trainer:
                trainer_name = "Trainer (no employee data)"
            
            # Получаем комнату с защитой от None
            room_name = 'N/A'
            if workout.room:
                room_name = workout.room.name
            
            # Получаем услугу с защитой от None
            service_name = 'N/A'
            if workout.service:
                service_name = workout.service.name
            
            # Форматируем время
            time_str = 'N/A'
            if workout.start_time and workout.end_time:
                time_str = f"{workout.start_time} - {workout.end_time}"
            
            data.append([
                str(workout.id),
                str(workout.workout_date) if workout.workout_date else 'N/A',
                time_str,
                room_name,
                trainer_name,
                service_name,
                str(workout.max_persons_capacity) if workout.max_persons_capacity else 'N/A',
                f"{workout.current_number_of_recorded}/{workout.max_persons_capacity}" 
                if workout.current_number_of_recorded is not None and workout.max_persons_capacity 
                else 'N/A'
            ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(f"Generated on: {date.today()}", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        # Логируем ошибку для отладки
        print(f"Error in generate_schedule_pdf: {e}")
        # Можно также записать в файл лога
        import traceback
        traceback.print_exc()
        # Возвращаем пустой PDF с сообщением об ошибке
        return generate_error_pdf(f"Error generating PDF: {str(e)}")

def generate_error_pdf(error_message):
    """Создает простой PDF с сообщением об ошибке"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph("Error Report", styles['Heading1']))
    elements.append(Spacer(1, 0.5*inch))
    elements.append(Paragraph(f"Error: {error_message}", styles['Normal']))
    elements.append(Paragraph(f"Generated on: {date.today()}", styles['Normal']))
    
    doc.build(elements)
    buffer.seek(0)
    return buffer

def generate_registrations_pdf(registrations, workout_id):
    try:
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=30
        )
        
        # Title
        elements.append(Paragraph(f"Registrations for Workout #{workout_id}", title_style))
        elements.append(Spacer(1, 0.25*inch))
        
        if registrations and len(registrations) > 0:
            workout = registrations[0].workout
            if workout:
                elements.append(Paragraph(f"Workout Details:", styles['Heading2']))
                elements.append(Paragraph(f"Date: {workout.workout_date}", styles['Normal']))
                
                # Время с защитой от None
                time_str = 'N/A'
                if workout.start_time and workout.end_time:
                    time_str = f"{workout.start_time} - {workout.end_time}"
                elements.append(Paragraph(f"Time: {time_str}", styles['Normal']))
                
                # Комната с защитой от None
                room_name = 'N/A'
                if workout.room:
                    room_name = workout.room.name
                elements.append(Paragraph(f"Room: {room_name}", styles['Normal']))
                
                # Тренер с защитой от None
                trainer_name = 'N/A'
                if workout.trainer and workout.trainer.employee:
                    trainer_name = f"{workout.trainer.employee.first_name} {workout.trainer.employee.last_name}"
                elements.append(Paragraph(f"Trainer: {trainer_name}", styles['Normal']))
                
                elements.append(Spacer(1, 0.25*inch))
        
        # Table data
        data = [['ID', 'Client', 'Registration Date', 'Email', 'Phone']]
        
        for registration in registrations:
            client_name = 'N/A'
            client_email = 'N/A'
            client_phone = 'N/A'
            
            if registration.client:
                client_name = f"{registration.client.first_name} {registration.client.last_name}"
                client_email = str(registration.client.email)
                client_phone = str(registration.client.phone) if registration.client.phone else 'N/A'
            
            data.append([
                str(registration.id),
                client_name,
                str(registration.record_date) if registration.record_date else 'N/A',
                client_email,
                client_phone
            ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 0.5*inch))
        elements.append(Paragraph(f"Total Registrations: {len(registrations)}", styles['Heading2']))
        elements.append(Paragraph(f"Generated on: {date.today()}", styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
        
    except Exception as e:
        print(f"Error in generate_registrations_pdf: {e}")
        import traceback
        traceback.print_exc()
        return generate_error_pdf(f"Error generating registrations PDF: {str(e)}")