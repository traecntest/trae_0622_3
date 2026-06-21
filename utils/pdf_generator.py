import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from config import EXPORT_DIR, RISK_LEVELS


class PDFGenerator:
    def __init__(self):
        self._register_fonts()

    def _register_fonts(self):
        try:
            font_paths = [
                "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
                "/usr/share/fonts/truetype/arphic/ukai.ttc",
                "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
                "/System/Library/Fonts/PingFang.ttc",
                "C:/Windows/Fonts/msyh.ttc",
            ]
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont('ChineseFont', font_path))
                        break
                    except Exception:
                        continue
        except Exception:
            pass

    def generate_action_card(self, script_name: str, risk_summary: dict, tips: list,
                            user_name: str = "") -> str:
        os.makedirs(EXPORT_DIR, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"防骗行动卡_{timestamp}.pdf"
        filepath = os.path.join(EXPORT_DIR, filename)

        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            leftMargin=2 * cm,
            rightMargin= 2* cm,
            topMargin=2 * cm,
            bottomMargin=2 * cm
        )

        story = []
        styles = getSampleStyleSheet()

        font_name = self._get_font_name()

        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Title'],
            fontName=font_name,
            fontSize=24,
            alignment=TA_CENTER,
            spaceAfter=20,
            textColor=colors.HexColor('#2c3e50')
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=14,
            alignment=TA_CENTER,
            spaceAfter=15,
            textColor=colors.HexColor('#7f8c8d')
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontName=font_name,
            fontSize=16,
            spaceBefore=15,
            spaceAfter=10,
            textColor=colors.HexColor('#2c3e50')
        )

        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=12,
            leading=18,
            spaceAfter=8
        )

        story.append(Paragraph("银盾反诈 · 家庭防骗行动卡", title_style))
        story.append(Paragraph(f"场景：{script_name}", subtitle_style))

        if user_name:
            story.append(Paragraph(f"演练人：{user_name}", subtitle_style))

        story.append(Spacer(1, 0.5 * cm))

        score = risk_summary.get("final_score", 0)
        level_key = risk_summary.get("final_level", "safe")
        level_label = risk_summary.get("final_level_label", "安全")
        level_color = RISK_LEVELS.get(level_key, {}).get("color", "#22c55e")

        score_data = [
            ["风险得分", "风险等级"],
            [str(score), level_label]
        ]
        score_table = Table(score_data, colWidths=[6 * cm, 6 * cm])
        score_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, 1), 18),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f3f5')),
            ('TEXTCOLOR', (1, 1), (1, 1), colors.HexColor(level_color)),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(score_table)

        story.append(Spacer(1, 0.8 * cm))
        story.append(Paragraph("防骗要点", heading_style))

        for i, tip in enumerate(tips, 1):
            story.append(Paragraph(f"{i}. {tip}", normal_style))

        story.append(Spacer(1, 0.8 * cm))

        reminder_data = [
            ["重要提醒"],
            ["• 三不一多原则：未知链接不点击，陌生来电不轻信，个人信息不透露，转账汇款多核实"],
            ["• 全国反诈热线：96110"],
            ["• 如遇诈骗，请立即拨打110报警"]
        ]
        reminder_table = Table(reminder_data, colWidths=[16 * cm])
        reminder_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), font_name),
            ('FONTSIZE', (0, 0), (0, 0), 14),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BACKGROUND', (0, 0), (0, 0), colors.HexColor('#e74c3c')),
            ('TEXTCOLOR', (0, 0), (0, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e74c3c')),
        ]))
        story.append(reminder_table)

        story.append(Spacer(1, 1 * cm))

        date_str = datetime.now().strftime("%Y年%m月%d日")
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontName=font_name,
            fontSize=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#95a5a6')
        )
        story.append(Paragraph(f"生成日期：{date_str} | 银盾反诈彩排室", footer_style))

        doc.build(story)
        return filepath

    def _get_font_name(self):
        if 'ChineseFont' in pdfmetrics.getRegisteredFontNames():
            return 'ChineseFont'
        return 'Helvetica'

    def generate_summary_image(self, script_name: str, risk_summary: dict,
                              tips: list) -> str:
        try:
            from PIL import Image, ImageDraw, ImageFont
            import io

            width, height = 800, 1000
            img = Image.new('RGB', (width, height), color='#ffffff')
            draw = ImageDraw.Draw(img)

            font_path = self._find_chinese_font()
            try:
                title_font = ImageFont.truetype(font_path, 32) if font_path else ImageFont.load_default()
                subtitle_font = ImageFont.truetype(font_path, 18) if font_path else ImageFont.load_default()
                normal_font = ImageFont.truetype(font_path, 16) if font_path else ImageFont.load_default()
            except Exception:
                title_font = ImageFont.load_default()
                subtitle_font = ImageFont.load_default()
                normal_font = ImageFont.load_default()

            draw.rectangle([0, 0, width, 80], fill='#2c3e50')
            draw.text((width // 2 - 180, 25), "银盾反诈 · 防骗行动卡", fill='white', font=title_font)

            y = 110
            draw.text((40, y), f"场景：{script_name}", fill='#333333', font=subtitle_font)
            y += 35

            score = risk_summary.get("final_score", 0)
            level_label = risk_summary.get("final_level_label", "安全")
            level_key = risk_summary.get("final_level", "safe")
            level_color = RISK_LEVELS.get(level_key, {}).get("color", "#22c55e")

            draw.text((40, y), f"风险得分：{score}分", fill=level_color, font=title_font)
            y += 50
            draw.text((40, y), f"风险等级：{level_label}", fill=level_color, font=subtitle_font)
            y += 40

            draw.rectangle([40, y, width - 40, y + 4], fill='#e0e0e0')
            bar_width = int((width - 80) * score / 100)
            draw.rectangle([40, y, 40 + bar_width, y + 4], fill=level_color)
            y += 30

            draw.text((40, y), "防骗要点：", fill='#2c3e50', font=subtitle_font)
            y += 35

            for i, tip in enumerate(tips, 1):
                draw.text((50, y), f"{i}. {tip}", fill='#333333', font=normal_font)
                y += 30

            y += 20
            draw.rectangle([40, y, width - 40, y + 120], fill='#fef2f2', outline='#ef4444', width=2)
            draw.text((60, y + 15), "重要提醒", fill='#dc2626', font=subtitle_font)
            draw.text((60, y + 45), "三不一多：未知链接不点击，陌生来电不轻信", fill='#333333', font=normal_font)
            draw.text((60, y + 70), "个人信息不透露，转账汇款多核实", fill='#333333', font=normal_font)
            draw.text((60, y + 95), "全国反诈热线：96110", fill='#dc2626', font=normal_font)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"防骗卡_{timestamp}.png"
            filepath = os.path.join(EXPORT_DIR, filename)
            img.save(filepath)
            return filepath

        except ImportError:
            return ""

    def _find_chinese_font(self):
        font_paths = [
            "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
            "/usr/share/fonts/truetype/arphic/ukai.ttc",
            "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
            "/System/Library/Fonts/PingFang.ttc",
            "C:/Windows/Fonts/msyh.ttc",
            "C:/Windows/Fonts/simhei.ttf",
        ]
        for path in font_paths:
            if os.path.exists(path):
                return path
        return None
