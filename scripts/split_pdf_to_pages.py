import os
import fitz
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageEnhance

def crop_bottom_pdf(pdf_path, output_folder="cropped_pages", crop=False, crop_amount=55):
    os.makedirs(output_folder, exist_ok=True)
    doc = fitz.open(pdf_path)
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]
    for i, page in enumerate(doc):
        if crop:
            rect = page.rect
            new_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.y1 - crop_amount)
            page.set_cropbox(new_rect)
        new_pdf = fitz.open()
        new_pdf.insert_pdf(doc, from_page=i, to_page=i)
        output_path = os.path.join(output_folder, f"{pdf_filename}_page_{i+1}.pdf")
        new_pdf.save(output_path)
        new_pdf.close()
        print(f"Saved: {output_path}")
    doc.close()
    print("All pages processed.")


def crop_bottom_white(image, tolerance=245, crop_lines=-1):
    """Crop only bottom white area; keep full width."""
    gray = np.array(image.convert("L"))
    mask = gray < tolerance  # detect non-white pixels

    if not mask.any():
        return image  # all white, return as-is

    # Find last row containing non-white pixels
    content_rows = np.where(mask.any(axis=1))[0]
    # first_row = content_rows[0]
    last_row = content_rows[-1] - crop_lines

    # cropped_image = image.crop((0, first_row, image.width, last_row + 1))
    cropped_image = image.crop((0, 0, image.width, last_row))
    return cropped_image

def pdf_to_images(pdf_path, output_folder='pages', dpi=300, crop=False, crop_twice=False):
    os.makedirs(output_folder, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)
    image_filename_prefix = os.path.splitext(os.path.basename(pdf_path))[0].replace('-', '_')

    for i, page in enumerate(pages[1:]):
        if crop:
            page = crop_bottom_white(page, crop_lines=63)
            if crop_twice:
                page = crop_bottom_white(page, crop_lines=-15)
        output_path = os.path.join(output_folder, f'{image_filename_prefix}_{i + 2}.jpg')
        page.convert("RGB").save(output_path, "JPEG")
        print(f"Saved: {output_path}")

    print("All pages processed.")


def main():
    # pdf_file = "bagrut_exams/2025-899371.PDF"
    pdf_file = "bagrut_exams/2024-899371.pdf"
    pdf_to_images(pdf_file, output_folder="bagrut_exams/pages/", crop=True, crop_twice=True)
    # crop_bottom_pdf(pdf_file, output_folder="bagrut_exams/pages2/", crop=True)


if __name__ == "__main__":
    main()
