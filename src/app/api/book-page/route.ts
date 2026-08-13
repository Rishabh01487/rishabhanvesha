import { NextRequest, NextResponse } from 'next/server';
import fs from 'fs';
import path from 'path';

const PAGES_DIR = path.join(process.cwd(), 'book-pages');
const TOTAL_PAGES = 279;

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const pageParam = searchParams.get('page');

  if (!pageParam) {
    return NextResponse.json({ error: 'Page parameter required' }, { status: 400 });
  }

  const pageNum = parseInt(pageParam, 10);
  if (isNaN(pageNum) || pageNum < 0 || pageNum >= TOTAL_PAGES) {
    return NextResponse.json({ error: 'Invalid page number' }, { status: 400 });
  }

  const filePath = path.join(PAGES_DIR, `page_${String(pageNum).padStart(4, '0')}.jpg`);

  if (!fs.existsSync(filePath)) {
    return NextResponse.json({ error: 'Page not found' }, { status: 404 });
  }

  const imageBuffer = fs.readFileSync(filePath);

  return new NextResponse(imageBuffer, {
    status: 200,
    headers: {
      'Content-Type': 'image/jpeg',
      'Cache-Control': 'public, max-age=3600, s-maxage=3600',
      'X-Content-Type-Options': 'nosniff',
      'Content-Disposition': 'inline',
    },
  });
}
