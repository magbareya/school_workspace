"""Split PDF files into pages or convert them to cropped JPEG images."""

import argparse
import os
from typing import Optional, Sequence

DEFAULT_EXAM_PDFS = [
    "bagrut_questions/exams/2023-899371.pdf",
    "bagrut_questions/exams/2024-899371.pdf",
    "bagrut_questions/exams/2025-899371.pdf",
]


def crop_bottom_pdf(
    pdf_path: str,
    output_folder: str = "cropped_pages",
    crop: bool = False,
    crop_amount: float = 55.0,
) -> None:
    """Split a PDF into single-page PDFs, optionally cropping the bottom margin."""
    import fitz

    if crop_amount < 0:
        raise ValueError("crop_amount must be non-negative")
    os.makedirs(output_folder, exist_ok=True)
    pdf_filename = os.path.splitext(os.path.basename(pdf_path))[0]

    with fitz.open(pdf_path) as doc:
        for i, page in enumerate(doc):
            if crop:
                rect = page.cropbox
                new_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, max(rect.y0 + 1, rect.y1 - crop_amount))
                page.set_cropbox(new_rect)

            with fitz.open() as new_pdf:
                new_pdf.insert_pdf(doc, from_page=i, to_page=i)
                output_path = os.path.join(output_folder, f"{pdf_filename}_page_{i + 1}.pdf")
                new_pdf.save(output_path)
                print(f"Saved: {output_path}")

    print("All pages processed.")


def crop_bottom_white(image, tolerance: int = 245, crop_lines: int = -1):
    """Crop bottom whitespace from a PIL image while keeping full width and clamping bounds."""
    import numpy as np
    from PIL import Image

    if not isinstance(image, Image.Image):
        raise TypeError("image must be a PIL Image")
    gray = np.array(image.convert("L"))
    mask = gray < tolerance  # detect non-white pixels

    if not mask.any():
        return image  # all white, return as-is

    content_rows = np.where(mask.any(axis=1))[0]
    last_row = min(image.height, max(1, int(content_rows[-1]) - crop_lines))
    return image.crop((0, 0, image.width, last_row))


def pdf_to_images(
    pdf_path: str,
    output_folder: str = "pages",
    dpi: int = 300,
    crop: bool = False,
    crop_twice: bool = False,
    skip_first_page: bool = True,
) -> None:
    """Convert PDF pages to JPEG images, optionally skipping cover page and cropping bottom footers."""
    from pdf2image import convert_from_path

    os.makedirs(output_folder, exist_ok=True)
    pages = convert_from_path(pdf_path, dpi=dpi)
    image_filename_prefix = os.path.splitext(os.path.basename(pdf_path))[0].replace("-", "_")

    start_index = 1 if skip_first_page else 0
    for offset, page in enumerate(pages[start_index:]):
        page_num = start_index + offset + 1
        if crop:
            page = crop_bottom_white(page, crop_lines=63)
            if crop_twice:
                page = crop_bottom_white(page, crop_lines=-15)
        output_path = os.path.join(output_folder, f"{image_filename_prefix}_{page_num}.jpg")
        page.convert("RGB").save(output_path, "JPEG")
        print(f"Saved: {output_path}")

    print("All pages processed.")


def main(argv: Optional[Sequence[str]] = None) -> None:
    parser = argparse.ArgumentParser(
        description="Split PDF files into individual pages or cropped JPEG images."
    )
    parser.add_argument(
        "files",
        nargs="*",
        default=DEFAULT_EXAM_PDFS,
        help="PDF file(s) to process.",
    )
    parser.add_argument(
        "--output-dir",
        default="bagrut_questions/exams/pages/",
        help="Output directory for generated pages.",
    )
    parser.add_argument(
        "--mode",
        choices=["images", "pdf"],
        default="images",
        help="Output format: cropped JPEG images or single-page PDFs (default: images).",
    )
    parser.add_argument(
        "--include-first-page",
        action="store_true",
        help="Do not skip page 1 (cover page) when converting to images.",
    )
    args = parser.parse_args(argv)

    prefixes = set()
    for pdf_file in args.files:
        if not os.path.isfile(pdf_file):
            parser.error(f"PDF file not found: {pdf_file}")
        prefix = os.path.splitext(os.path.basename(pdf_file))[0]
        if args.mode == "images":
            prefix = prefix.replace("-", "_")
        if os.path.normcase(prefix) in prefixes:
            parser.error(f"Inputs share the output prefix {prefix!r}")
        prefixes.add(os.path.normcase(prefix))

    for pdf_file in args.files:
        if args.mode == "pdf":
            crop_bottom_pdf(pdf_file, output_folder=args.output_dir, crop=True)
        else:
            pdf_to_images(
                pdf_file,
                output_folder=args.output_dir,
                crop=True,
                crop_twice=True,
                skip_first_page=not args.include_first_page,
            )


if __name__ == "__main__":
    main()
