import { PDFDocument, rgb, StandardFonts } from 'pdf-lib'

export const pdfService = {
  /**
   * Генерация PDF отчета по оборудованию
   */
  async generateEquipmentReport(equipmentList) {
    try {
      const pdfDoc = await PDFDocument.create()
      const page = pdfDoc.addPage([595.28, 841.89]) // A4
      const { height } = page.getSize()
      const font = await pdfDoc.embedFont(StandardFonts.Helvetica)
      const boldFont = await pdfDoc.embedFont(StandardFonts.HelveticaBold)
      
      let y = height - 50
      
      // Заголовок
      page.drawText('Отчет по оборудованию фитнес-центра', {
        x: 50,
        y,
        size: 24,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      y -= 40
      
      // Дата генерации
      const currentDate = new Date().toLocaleDateString('ru-RU')
      page.drawText(`Дата генерации: ${currentDate}`, {
        x: 50,
        y,
        size: 12,
        font,
        color: rgb(0.4, 0.4, 0.4),
      })
      y -= 30
      
      // Заголовки таблицы
      const headers = ['ID', 'Название', 'Категория', 'Дата покупки', 'Последнее обслуживание', 'Состояние']
      const columnWidths = [30, 120, 100, 90, 120, 135]
      let x = 30
      
      // Рисуем заголовки
      headers.forEach((header, index) => {
        page.drawText(header, {
          x,
          y,
          size: 10,
          font: boldFont,
          color: rgb(1, 1, 1),
        })
        x += columnWidths[index]
      })
      y -= 20
      
      // Разделительная линия
      page.drawLine({
        start: { x: 30, y },
        end: { x: 565, y },
        thickness: 1,
        color: rgb(0, 0, 0),
      })
      y -= 10
      
      // Данные оборудования
      equipmentList.forEach((equipment, index) => {
        if (y < 100) {
          page = pdfDoc.addPage([595.28, 841.89])
          y = height - 50
        }
        
        const row = [
          equipment.id.toString(),
          equipment.name || 'Не указано',
          equipment.category?.name || 'Не указана',
          equipment.purchase_date ? new Date(equipment.purchase_date).toLocaleDateString('ru-RU') : 'Не указана',
          equipment.date_of_last_service ? new Date(equipment.date_of_last_service).toLocaleDateString('ru-RU') : 'Не указана',
          equipment.description_of_condition || 'Не указано'
        ]
        
        x = 30
        row.forEach((cell, cellIndex) => {
          page.drawText(cell, {
            x,
            y,
            size: 9,
            font,
            color: rgb(0, 0, 0),
            maxWidth: columnWidths[cellIndex] - 5,
          })
          x += columnWidths[cellIndex]
        })
        y -= 15
        
        // Линия между строками
        if (index < equipmentList.length - 1) {
          page.drawLine({
            start: { x: 30, y: y + 5 },
            end: { x: 565, y: y + 5 },
            thickness: 0.5,
            color: rgb(0.8, 0.8, 0.8),
          })
          y -= 5
        }
      })
      
      // Итоги
      y -= 20
      page.drawText(`Всего единиц оборудования: ${equipmentList.length}`, {
        x: 50,
        y,
        size: 12,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      
      const pdfBytes = await pdfDoc.save()
      return pdfBytes
    } catch (error) {
      console.error('Error generating equipment PDF:', error)
      throw error
    }
  },
  
  /**
   * Генерация PDF отчета по расписанию
   */
  async generateScheduleReport(workouts, dateFrom, dateTo) {
    try {
      const pdfDoc = await PDFDocument.create()
      let page = pdfDoc.addPage([595.28, 841.89])
      const { height } = page.getSize()
      const font = await pdfDoc.embedFont(StandardFonts.Helvetica)
      const boldFont = await pdfDoc.embedFont(StandardFonts.HelveticaBold)
      
      let y = height - 50
      
      // Заголовок
      page.drawText('Отчет по расписанию тренировок', {
        x: 50,
        y,
        size: 24,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      y -= 30
      
      // Период
      const periodText = `Период: ${new Date(dateFrom).toLocaleDateString('ru-RU')} - ${new Date(dateTo).toLocaleDateString('ru-RU')}`
      page.drawText(periodText, {
        x: 50,
        y,
        size: 14,
        font,
        color: rgb(0.4, 0.4, 0.4),
      })
      y -= 20
      
      // Дата генерации
      const currentDate = new Date().toLocaleDateString('ru-RU')
      page.drawText(`Дата генерации: ${currentDate}`, {
        x: 50,
        y,
        size: 12,
        font,
        color: rgb(0.4, 0.4, 0.4),
      })
      y -= 40
      
      // Статистика
      const totalWorkouts = workouts.length
      const totalRegistered = workouts.reduce((sum, workout) => sum + workout.current_number_of_recorded, 0)
      const totalCapacity = workouts.reduce((sum, workout) => sum + workout.max_persons_capacity, 0)
      const occupancyRate = totalCapacity > 0 ? Math.round((totalRegistered / totalCapacity) * 100) : 0
      
      const stats = [
        `Всего тренировок: ${totalWorkouts}`,
        `Общее количество записей: ${totalRegistered}`,
        `Средняя заполняемость: ${occupancyRate}%`
      ]
      
      stats.forEach(stat => {
        page.drawText(stat, {
          x: 50,
          y,
          size: 12,
          font,
          color: rgb(0, 0, 0),
        })
        y -= 20
      })
      
      y -= 20
      
      // Заголовки таблицы
      const headers = ['Дата', 'Время', 'Услуга', 'Тренер', 'Зал', 'Записано/Макс']
      const columnWidths = [70, 80, 120, 120, 100, 85]
      let x = 30
      
      // Рисуем заголовки
      headers.forEach((header, index) => {
        page.drawText(header, {
          x,
          y,
          size: 10,
          font: boldFont,
          color: rgb(1, 1, 1),
        })
        x += columnWidths[index]
      })
      y -= 20
      
      // Разделительная линия
      page.drawLine({
        start: { x: 30, y },
        end: { x: 565, y },
        thickness: 1,
        color: rgb(0, 0, 0),
      })
      y -= 10
      
      // Данные тренировок
      workouts.forEach((workout, index) => {
        if (y < 100) {
          page = pdfDoc.addPage([595.28, 841.89])
          y = height - 50
        }
        
        const row = [
          new Date(workout.workout_date).toLocaleDateString('ru-RU'),
          `${workout.start_time} - ${workout.end_time}`,
          workout.service?.name || 'Не указано',
          workout.trainer ? `${workout.trainer.first_name} ${workout.trainer.last_name}` : 'Не указан',
          workout.room?.name || 'Не указан',
          `${workout.current_number_of_recorded}/${workout.max_persons_capacity}`
        ]
        
        x = 30
        row.forEach((cell, cellIndex) => {
          page.drawText(cell, {
            x,
            y,
            size: 9,
            font,
            color: rgb(0, 0, 0),
            maxWidth: columnWidths[cellIndex] - 5,
          })
          x += columnWidths[cellIndex]
        })
        y -= 15
        
        // Линия между строками
        if (index < workouts.length - 1) {
          page.drawLine({
            start: { x: 30, y: y + 5 },
            end: { x: 565, y: y + 5 },
            thickness: 0.5,
            color: rgb(0.8, 0.8, 0.8),
          })
          y -= 5
        }
      })
      
      const pdfBytes = await pdfDoc.save()
      return pdfBytes
    } catch (error) {
      console.error('Error generating schedule PDF:', error)
      throw error
    }
  },
  
  /**
   * Генерация PDF отчета по записям на тренировку
   */
  async generateRegistrationsReport(registrations, workout) {
    try {
      const pdfDoc = await PDFDocument.create()
      const page = pdfDoc.addPage([595.28, 841.89])
      const { height } = page.getSize()
      const font = await pdfDoc.embedFont(StandardFonts.Helvetica)
      const boldFont = await pdfDoc.embedFont(StandardFonts.HelveticaBold)
      
      let y = height - 50
      
      // Заголовок
      page.drawText('Отчет по записям на тренировку', {
        x: 50,
        y,
        size: 24,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      y -= 40
      
      // Информация о тренировке
      if (workout) {
        const workoutInfo = [
          `Тренировка: ${workout.service?.name || 'Не указано'}`,
          `Дата: ${new Date(workout.workout_date).toLocaleDateString('ru-RU')}`,
          `Время: ${workout.start_time} - ${workout.end_time}`,
          `Тренер: ${workout.trainer ? `${workout.trainer.first_name} ${workout.trainer.last_name}` : 'Не указан'}`,
          `Зал: ${workout.room?.name || 'Не указан'}`,
          `Записано: ${workout.current_number_of_recorded}/${workout.max_persons_capacity}`
        ]
        
        workoutInfo.forEach(info => {
          page.drawText(info, {
            x: 50,
            y,
            size: 12,
            font,
            color: rgb(0, 0, 0),
          })
          y -= 20
        })
      }
      
      y -= 30
      
      // Дата генерации
      const currentDate = new Date().toLocaleDateString('ru-RU')
      page.drawText(`Дата генерации: ${currentDate}`, {
        x: 50,
        y,
        size: 12,
        font,
        color: rgb(0.4, 0.4, 0.4),
      })
      y -= 40
      
      // Статистика
      page.drawText(`Всего записей: ${registrations.length}`, {
        x: 50,
        y,
        size: 14,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      y -= 30
      
      if (registrations.length === 0) {
        page.drawText('Нет записей на эту тренировку', {
          x: 50,
          y,
          size: 14,
          font: boldFont,
          color: rgb(0.5, 0.5, 0.5),
        })
      } else {
        // Заголовки таблицы
        const headers = ['№', 'Клиент', 'Телефон', 'Email', 'Дата записи']
        const columnWidths = [30, 150, 120, 170, 100]
        let x = 30
        
        // Рисуем заголовки
        headers.forEach((header, index) => {
          page.drawText(header, {
            x,
            y,
            size: 10,
            font: boldFont,
            color: rgb(1, 1, 1),
          })
          x += columnWidths[index]
        })
        y -= 20
        
        // Разделительная линия
        page.drawLine({
          start: { x: 30, y },
          end: { x: 570, y },
          thickness: 1,
          color: rgb(0, 0, 0),
        })
        y -= 10
        
        // Данные записей
        registrations.forEach((record, index) => {
          if (y < 100) {
            // Можно добавить новую страницу при необходимости
            page.drawText('... продолжение на следующей странице', {
              x: 50,
              y,
              size: 10,
              font,
              color: rgb(0.5, 0.5, 0.5),
            })
            y -= 100
          }
          
          const row = [
            (index + 1).toString(),
            `${record.client?.first_name || ''} ${record.client?.last_name || ''}`.trim() || 'Не указано',
            record.client?.phone || 'Не указан',
            record.client?.email || 'Не указан',
            new Date(record.record_date).toLocaleDateString('ru-RU')
          ]
          
          x = 30
          row.forEach((cell, cellIndex) => {
            page.drawText(cell, {
              x,
              y,
              size: 9,
              font,
              color: rgb(0, 0, 0),
              maxWidth: columnWidths[cellIndex] - 5,
            })
            x += columnWidths[cellIndex]
          })
          y -= 15
          
          // Линия между строками
          if (index < registrations.length - 1) {
            page.drawLine({
              start: { x: 30, y: y + 5 },
              end: { x: 570, y: y + 5 },
              thickness: 0.5,
              color: rgb(0.8, 0.8, 0.8),
            })
            y -= 5
          }
        })
      }
      
      // Подпись
      y -= 40
      page.drawText('Отчет сгенерирован автоматически системой "Фитнес-центр"', {
        x: 50,
        y,
        size: 10,
        font,
        color: rgb(0.4, 0.4, 0.4),
      })
      
      const pdfBytes = await pdfDoc.save()
      return pdfBytes
    } catch (error) {
      console.error('Error generating registrations PDF:', error)
      throw error
    }
  },
  
  /**
   * Генерация PDF для клиента (подписка, посещения)
   */
  async generateClientReport(clientData) {
    try {
      const pdfDoc = await PDFDocument.create()
      const page = pdfDoc.addPage([595.28, 841.89])
      const { height } = page.getSize()
      const font = await pdfDoc.embedFont(StandardFonts.Helvetica)
      const boldFont = await pdfDoc.embedFont(StandardFonts.HelveticaBold)
      
      let y = height - 50
      
      // Заголовок
      page.drawText('Ваша статистика посещений', {
        x: 50,
        y,
        size: 24,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      y -= 40
      
      // Информация о клиенте
      page.drawText(`Клиент: ${clientData.first_name} ${clientData.last_name}`, {
        x: 50,
        y,
        size: 14,
        font: boldFont,
        color: rgb(0, 0, 0),
      })
      y -= 20
      
      page.drawText(`Email: ${clientData.email}`, {
        x: 50,
        y,
        size: 12,
        font,
        color: rgb(0, 0, 0),
      })
      y -= 20
      
      if (clientData.phone) {
        page.drawText(`Телефон: ${clientData.phone}`, {
          x: 50,
          y,
          size: 12,
          font,
          color: rgb(0, 0, 0),
        })
        y -= 20
      }
      
      y -= 20
      
      // Дата генерации
      const currentDate = new Date().toLocaleDateString('ru-RU')
      page.drawText(`Отчет сформирован: ${currentDate}`, {
        x: 50,
        y,
        size: 12,
        font,
        color: rgb(0.4, 0.4, 0.4),
      })
      y -= 40
      
      // Активная подписка
      if (clientData.active_subscription) {
        const sub = clientData.active_subscription
        page.drawText('Активная подписка:', {
          x: 50,
          y,
          size: 14,
          font: boldFont,
          color: rgb(0, 0.5, 0),
        })
        y -= 20
        
        page.drawText(`Тип: ${sub.subscription?.subscription_type || 'Не указан'}`, {
          x: 70,
          y,
          size: 12,
          font,
          color: rgb(0, 0, 0),
        })
        y -= 18
        
        page.drawText(`Действует до: ${new Date(sub.end_action_date).toLocaleDateString('ru-RU')}`, {
          x: 70,
          y,
          size: 12,
          font,
          color: rgb(0, 0, 0),
        })
        y -= 30
      }
      
      // Статистика посещений
      if (clientData.workouts_attended > 0) {
        page.drawText('Статистика посещений:', {
          x: 50,
          y,
          size: 14,
          font: boldFont,
          color: rgb(0, 0, 0),
        })
        y -= 20
        
        page.drawText(`Всего посещений: ${clientData.workouts_attended || 0}`, {
          x: 70,
          y,
          size: 12,
          font,
          color: rgb(0, 0, 0),
        })
        y -= 18
        
        if (clientData.favorite_trainer) {
          page.drawText(`Любимый тренер: ${clientData.favorite_trainer}`, {
            x: 70,
            y,
            size: 12,
            font,
            color: rgb(0, 0, 0),
          })
          y -= 18
        }
        
        if (clientData.favorite_service) {
          page.drawText(`Любимая услуга: ${clientData.favorite_service}`, {
            x: 70,
            y,
            size: 12,
            font,
            color: rgb(0, 0, 0),
          })
          y -= 18
        }
        
        y -= 20
      }
      
      // Предстоящие тренировки
      if (clientData.upcoming_workouts && clientData.upcoming_workouts.length > 0) {
        page.drawText('Предстоящие тренировки:', {
          x: 50,
          y,
          size: 14,
          font: boldFont,
          color: rgb(0, 0, 0),
        })
        y -= 30
        
        clientData.upcoming_workouts.forEach((workout, index) => {
          if (index < 5) { // Ограничиваем 5 записями
            const workoutText = `${new Date(workout.workout_date).toLocaleDateString('ru-RU')} - ${workout.service?.name} (${workout.start_time})`
            page.drawText(workoutText, {
              x: 70,
              y,
              size: 11,
              font,
              color: rgb(0, 0, 0),
              maxWidth: 500,
            })
            y -= 16
          }
        })
      }
      
      // Благодарность
      y -= 40
      page.drawText('Спасибо, что выбираете наш фитнес-центр!', {
        x: 50,
        y,
        size: 14,
        font: boldFont,
        color: rgb(0.2, 0.2, 0.2),
      })
      
      const pdfBytes = await pdfDoc.save()
      return pdfBytes
    } catch (error) {
      console.error('Error generating client PDF:', error)
      throw error
    }
  },
  
  /**
   * Утилита для скачивания PDF
   */
  downloadPDF(pdfBytes, filename = 'report.pdf') {
    try {
      const blob = new Blob([pdfBytes], { type: 'application/pdf' })
      const link = document.createElement('a')
      link.href = window.URL.createObjectURL(blob)
      link.download = filename
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(link.href)
    } catch (error) {
      console.error('Error downloading PDF:', error)
      throw error
    }
  },
  
  /**
   * Утилита для открытия PDF в новой вкладке
   */
  openPDF(pdfBytes) {
    try {
      const blob = new Blob([pdfBytes], { type: 'application/pdf' })
      const url = window.URL.createObjectURL(blob)
      window.open(url, '_blank')
    } catch (error) {
      console.error('Error opening PDF:', error)
      throw error
    }
  }
}

export default pdfService