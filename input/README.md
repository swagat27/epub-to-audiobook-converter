# Sample EPUB Files for Testing

This directory is where you should place your EPUB files for conversion.

## What files are supported?

- `.epub` files (EPUB format ebooks)
- The EPUB files should be DRM-free for the parser to work correctly

## Example usage:

1. Download or copy your EPUB file here
2. Run the converter:
   ```bash
   python main.py -i input/your_book.epub
   ```

## Where to find EPUB files:

- **Project Gutenberg**: https://www.gutenberg.org (free public domain books)
- **Internet Archive**: https://archive.org
- **Your personal library** (DRM-free purchases)
- **LibGen** or other academic sources
- **Convert from other formats** using tools like Calibre

## Need a test file?

Try downloading a free book from Project Gutenberg:
- Alice's Adventures in Wonderland: https://www.gutenberg.org/ebooks/11
- The Adventures of Sherlock Holmes: https://www.gutenberg.org/ebooks/1661

## Note about DRM:

This tool only works with DRM-free EPUB files. If you have DRM-protected files, you'll need to remove the DRM first using tools like Calibre with DeDRM plugins (make sure you own the books legally).