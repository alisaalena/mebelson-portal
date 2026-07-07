# polish_galleries.py — запустить ОДИН раз в papke portal/galleries/
# Делает галереи 1 слоя читаемее:
#  1) пояснение к колонке "Цена" (= средняя цена Ozon за 28 дней)
#  2) плашка оборота -> нейтральный серый + подпись "Оборот"
#  3) убирает дублирующуюся цену внизу карточки (она уже в формуле ₽/кг)
#  4) помечает цену в формуле как "ср."
# Цвет строки ₽/кг (зелёный проходит / красный нет) НЕ трогаем — это нужный сигнал.
import glob, io

NOTE = '''<div class="pricenote" style="margin:0 0 10px;padding:9px 14px;background:#fff8e1;border:1px solid #ffe08a;border-radius:8px;font-size:12px;line-height:1.5;color:#7a5b00">
  &#9432; <strong>&laquo;Цена&raquo;</strong> &mdash; средняя цена реальных продаж за 28 дней (из аналитики Ozon), а не цена с карточки. На карточке Ozon одновременно показывает несколько цен: <strong>с Ozon&nbsp;Картой / с банками</strong> (самая низкая), <strong>с другими банками</strong> (выше) и <strong>зачёркнутую цену до скидки</strong> (самая высокая). Средняя цена усредняет фактические сделки за месяц и обычно попадает между акционной и зачёркнутой ценой &mdash; поэтому не совпадает ни с одной отдельной ценой на карточке.
</div>
'''
ANCHOR = '<div class="bar">'

# (искать, заменить, маркер-уже-сделано)
EDITS = [
  ('<span class="bdg" style="background:${d.color}">${d.revenue}</span>',
   '<span class="bdg" style="background:#5b6b7d">Оборот ${d.revenue}</span>',
   'background:#5b6b7d'),
  ('\n        <span>${d.price}</span>', '', None),  # дубль цены — снять
  ('\'na\'}">${d.formula}</span>', '\'na\'}">ср. ${d.formula}</span>', '">ср. ${d.formula}'),
]

changed = 0
for f in glob.glob('*.html'):
    html = io.open(f, encoding='utf-8').read()
    if ANCHOR not in html:            # панели 2 слоя пропускаем
        continue
    orig = html
    if 'class="pricenote"' not in html:
        html = html.replace(ANCHOR, NOTE + ANCHOR, 1)
    for find, repl, marker in EDITS:
        if marker and marker in html:
            continue
        if find in html:
            html = html.replace(find, repl, 1)
    if html != orig:
        io.open(f, 'w', encoding='utf-8').write(html)
        changed += 1
        print('OK:', f)
    else:
        print('skip (всё уже сделано):', f)
print(f'Готово. Обновлено файлов: {changed}')
