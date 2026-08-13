"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { bookMeta, parts, allChapters, TOTAL_PAGES } from "@/lib/book-data";

/* ------------------------------------------------------------------ */
/*  Simplex 2D noise (organic aurora movement)                        */
/* ------------------------------------------------------------------ */
function createNoise2D() {
  const grad3 = [
    [1,1,0],[-1,1,0],[1,-1,0],[-1,-1,0],
    [1,0,1],[-1,0,1],[1,0,-1],[-1,0,-1],
    [0,1,1],[0,-1,1],[0,1,-1],[0,-1,-1],
  ];
  const perm = new Uint8Array(512);
  const p = new Uint8Array(256);
  for (let i = 0; i < 256; i++) p[i] = i;
  for (let i = 255; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [p[i], p[j]] = [p[j], p[i]];
  }
  for (let i = 0; i < 512; i++) perm[i] = p[i & 255];

  const dot = (g: number[], x: number, y: number) => g[0] * x + g[1] * y;
  const F2 = 0.5 * (Math.sqrt(3) - 1);
  const G2 = (3 - Math.sqrt(3)) / 6;

  return (xin: number, yin: number): number => {
    const s = (xin + yin) * F2;
    const i = Math.floor(xin + s);
    const j = Math.floor(yin + s);
    const t = (i + j) * G2;
    const X0 = i - t, Y0 = j - t;
    const x0 = xin - X0, y0 = yin - Y0;
    const i1 = x0 > y0 ? 1 : 0;
    const j1 = x0 > y0 ? 0 : 1;
    const x1 = x0 - i1 + G2, y1 = y0 - j1 + G2;
    const x2 = x0 - 1 + 2 * G2, y2 = y0 - 1 + 2 * G2;
    const ii = i & 255, jj = j & 255;
    let n0 = 0, n1 = 0, n2 = 0;
    let t0 = 0.5 - x0 * x0 - y0 * y0;
    if (t0 > 0) { t0 *= t0; n0 = t0 * t0 * dot(grad3[perm[ii + perm[jj]] % 12], x0, y0); }
    let t1 = 0.5 - x1 * x1 - y1 * y1;
    if (t1 > 0) { t1 *= t1; n1 = t1 * t1 * dot(grad3[perm[ii + i1 + perm[jj + j1]] % 12], x1, y1); }
    let t2 = 0.5 - x2 * x2 - y2 * y2;
    if (t2 > 0) { t2 *= t2; n2 = t2 * t2 * dot(grad3[perm[ii + 1 + perm[jj + 1]] % 12], x2, y2); }
    return 70 * (n0 + n1 + n2);
  };
}

/* ------------------------------------------------------------------ */
/*  Organic Aurora Blob Canvas (matching aditiuncut.com)               */
/* ------------------------------------------------------------------ */
function AuroraCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);
    const noise = createNoise2D();

    // Color palette: magenta/pink dominant, cyan/teal edges, hints of lime
    const blobs: { cx: number; cy: number; r: number; g: number; b: number; size: number; speed: number; noiseOffX: number; noiseOffY: number }[] = [
      { cx: 0.5, cy: 0.45, r: 255, g: 50, b: 120, size: 0.35, speed: 0.0003, noiseOffX: 0, noiseOffY: 100 },
      { cx: 0.4, cy: 0.5, r: 0, g: 200, b: 255, size: 0.3, speed: 0.00025, noiseOffX: 50, noiseOffY: 50 },
      { cx: 0.6, cy: 0.4, r: 160, g: 80, b: 255, size: 0.25, speed: 0.00035, noiseOffX: 100, noiseOffY: 0 },
      { cx: 0.5, cy: 0.55, r: 80, g: 255, b: 150, size: 0.2, speed: 0.0004, noiseOffX: 150, noiseOffY: 150 },
      { cx: 0.45, cy: 0.48, r: 255, g: 100, b: 200, size: 0.28, speed: 0.00028, noiseOffX: 200, noiseOffY: 100 },
    ];

    const draw = (timestamp: number) => {
      ctx!.clearRect(0, 0, w, h);
      ctx!.filter = "blur(80px)";

      for (const blob of blobs) {
        const nx = noise(timestamp * blob.speed + blob.noiseOffX, 0) * 0.15;
        const ny = noise(0, timestamp * blob.speed + blob.noiseOffY) * 0.1;
        const x = (blob.cx + nx) * w;
        const y = (blob.cy + ny) * h;
        const radius = Math.max(10, blob.size * Math.min(w, h) * (0.8 + noise(timestamp * blob.speed * 0.5 + blob.noiseOffX, timestamp * blob.speed * 0.5 + blob.noiseOffY) * 0.3));

        const grad = ctx!.createRadialGradient(x, y, 0, x, y, radius);
        grad.addColorStop(0, `rgba(${blob.r},${blob.g},${blob.b},0.35)`);
        grad.addColorStop(0.4, `rgba(${blob.r},${blob.g},${blob.b},0.15)`);
        grad.addColorStop(1, `rgba(${blob.r},${blob.g},${blob.b},0)`);

        ctx!.beginPath();
        ctx!.arc(x, y, radius, 0, Math.PI * 2);
        ctx!.fillStyle = grad;
        ctx!.fill();
      }

      // White-hot center glow
      const cnx = noise(timestamp * 0.0002, 50) * 0.08;
      const cny = noise(50, timestamp * 0.0002) * 0.06;
      const cx = (0.5 + cnx) * w;
      const cy = (0.47 + cny) * h;
      const cr = Math.max(10, Math.min(w, h) * 0.12);
      const centerGrad = ctx!.createRadialGradient(cx, cy, 0, cx, cy, cr);
      centerGrad.addColorStop(0, "rgba(255,255,255,0.12)");
      centerGrad.addColorStop(0.5, "rgba(255,200,255,0.04)");
      centerGrad.addColorStop(1, "rgba(255,200,255,0)");
      ctx!.beginPath();
      ctx!.arc(cx, cy, cr, 0, Math.PI * 2);
      ctx!.fillStyle = centerGrad;
      ctx!.fill();

      ctx!.filter = "none";
      animId = requestAnimationFrame(draw);
    };

    animId = requestAnimationFrame(draw);

    const onResize = () => {
      w = canvas.width = window.innerWidth;
      h = canvas.height = window.innerHeight;
    };
    window.addEventListener("resize", onResize);
    return () => {
      cancelAnimationFrame(animId);
      window.removeEventListener("resize", onResize);
    };
  }, []);

  return <canvas ref={canvasRef} className="absolute inset-0 w-full h-full block" style={{ touchAction: "none" }} />;
}

/* ------------------------------------------------------------------ */
/*  Landing Page                                                        */
/* ------------------------------------------------------------------ */
function LandingPage({ onOpen }: { onOpen: () => void }) {
  const [started, setStarted] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setStarted(true), 100);
    return () => clearTimeout(t);
  }, []);

  const ease = "cubic-bezier(0.16,1,0.3,1)";

  return (
    <div className="relative w-full h-screen bg-[#050505] text-white overflow-hidden">
      <AuroraCanvas />

      {/* Content */}
      <div className="relative z-10 w-full h-full pointer-events-none">
        <div className="flex flex-col items-center justify-center w-full h-full text-center px-6">
          <div className="space-y-4 pointer-events-auto cursor-default z-20">

            {/* Pickup line - main title */}
            {started && (
              <h1
                className="text-4xl md:text-6xl font-light tracking-tight text-white drop-shadow-[0_0_20px_rgba(0,0,0,1)] select-none leading-[1.1]"
                style={{
                  opacity: 0,
                  animation: `fadeInUp 1s ${ease} 0.4s forwards`,
                }}
              >
                Things I Learned
                <br />
                Tokenizing the World
              </h1>
            )}

            {/* Book name */}
            {started && (
              <h2
                className="text-lg md:text-xl text-white/80 font-light tracking-[0.2em] uppercase drop-shadow-[0_0_10px_rgba(0,0,0,1)]"
                style={{
                  opacity: 0,
                  animation: `fadeInUp 1s ${ease} 0.7s forwards`,
                }}
              >
                AVERON — The Programmable Digital Asset Infrastructure
              </h2>
            )}

            {/* Author line with handwritten font */}
            {started && (
              <p
                className="text-xl sm:text-2xl md:text-3xl font-medium tracking-wide drop-shadow-[0_0_15px_rgba(0,0,0,0.8)]"
                style={{
                  fontFamily: "var(--font-caveat)",
                  opacity: 0,
                  animation: `fadeInUp 1s ${ease} 1s forwards`,
                }}
              >
                a book by Rishabh Gupta
              </p>
            )}

            {/* CTA Button */}
            {started && (
              <div className="pt-8" style={{ opacity: 0, animation: `fadeInUp 1s ${ease} 1.3s forwards` }}>
                <button
                  onClick={onOpen}
                  className="px-8 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full text-sm uppercase tracking-[0.2em] transition-colors backdrop-blur-sm text-white/90 hover:text-white cursor-pointer"
                >
                  Start Reading
                </button>
              </div>
            )}

            {/* Edition line */}
            {started && (
              <p
                className="text-[11px] tracking-[0.15em] text-white/30 mt-6"
                style={{
                  opacity: 0,
                  animation: `fadeInUp 1s ${ease} 1.6s forwards`,
                }}
              >
                {bookMeta.edition}
              </p>
            )}

          </div>
        </div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 z-20 pointer-events-none" style={{ background: "linear-gradient(to top, #050505 0%, transparent 100%)" }} />
      <div className="absolute top-0 left-0 right-0 h-24 z-20 pointer-events-none" style={{ background: "linear-gradient(to bottom, #050505 0%, transparent 100%)" }} />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Table of Contents Sidebar                                          */
/* ------------------------------------------------------------------ */
function TableOfContents({ isOpen, onClose, onGoToPage }: { isOpen: boolean; onClose: () => void; onGoToPage: (p: number) => void }) {
  return (
    <>
      {isOpen && <div className="fixed inset-0 bg-black/60 z-40 backdrop-blur-sm lg:hidden" onClick={onClose} />}
      <aside className={`fixed top-0 left-0 z-50 h-full w-80 bg-[#0a0a0a] border-r border-white/[0.06] transform transition-transform duration-300 ease-in-out overflow-hidden ${isOpen ? "translate-x-0" : "-translate-x-full"}`}>
        <div className="flex items-center justify-between p-5 border-b border-white/[0.06]">
          <h2 className="text-xs tracking-[0.2em] uppercase text-white/50">Contents</h2>
          <button onClick={onClose} className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors text-white/50 hover:text-white">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
          </button>
        </div>
        <div className="overflow-y-auto h-[calc(100%-60px)] py-2 px-2 custom-scrollbar">
          {parts.map((part, pi) => (
            <div key={pi} className="mb-4">
              <div className="px-3 py-2 text-[10px] tracking-[0.25em] uppercase text-white/30 font-medium">
                Part {pi + 1} {" - "} {part.title}
              </div>
              {part.chapters.map((ch, ci) => (
                <button key={ci} onClick={() => { onGoToPage(ch.page); onClose(); }} className="w-full text-left px-4 py-2 text-sm text-white/60 hover:text-white hover:bg-white/[0.03] rounded-md transition-all duration-200 truncate">
                  <span className="text-white/25 text-xs mr-2 tabular-nums">{ch.page}</span>
                  {ch.title}
                </button>
              ))}
            </div>
          ))}
        </div>
      </aside>
    </>
  );
}

/* ------------------------------------------------------------------ */
/*  Book Reader                                                         */
/* ------------------------------------------------------------------ */
function BookReader({ onBack }: { onBack: () => void }) {
  const [currentPage, setCurrentPage] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loadedImages, setLoadedImages] = useState<Set<number>>(new Set([0]));
  const [loading, setLoading] = useState(true);
  const imageRefs = useRef<Map<number, HTMLImageElement>>(new Map());

  const goToPage = useCallback((page: number) => {
    setCurrentPage(Math.max(0, Math.min(page, TOTAL_PAGES - 1)));
  }, []);

  const preloadPage = useCallback((pageNum: number) => {
    if (pageNum < 0 || pageNum >= TOTAL_PAGES || loadedImages.has(pageNum)) return;
    const img = new Image();
    img.src = `/book-pages/page_${String(pageNum).padStart(4, "0")}.jpg`;
    img.onload = () => setLoadedImages((prev) => new Set([...prev, pageNum]));
  }, [loadedImages]);

  useEffect(() => { preloadPage(currentPage); preloadPage(currentPage - 1); preloadPage(currentPage + 1); preloadPage(currentPage + 2); }, [currentPage, preloadPage]);
  useEffect(() => { setLoading(true); }, [currentPage]);

  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === "ArrowDown") { e.preventDefault(); goToPage(currentPage + 1); }
      else if (e.key === "ArrowLeft" || e.key === "ArrowUp") { e.preventDefault(); goToPage(currentPage - 1); }
      else if (e.key === "Escape") { onBack(); }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [currentPage, goToPage, onBack]);

  const currentChapter = allChapters.find((c) => currentPage >= c.page && (allChapters[allChapters.indexOf(c) + 1]?.page ?? TOTAL_PAGES) > currentPage);
  const progress = ((currentPage + 1) / TOTAL_PAGES) * 100;

  return (
    <div className="relative w-full h-screen bg-[#050505] text-white overflow-hidden select-none" onContextMenu={(e) => e.preventDefault()} onDragStart={(e) => e.preventDefault()}>
      <header className="fixed top-0 left-0 right-0 z-30 flex items-center justify-between px-4 md:px-6 h-12 bg-[#050505]/90 backdrop-blur-md border-b border-white/[0.04]">
        <div className="flex items-center gap-3">
          <button onClick={onBack} className="flex items-center gap-2 text-white/50 hover:text-white transition-colors text-sm">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" /></svg>
            <span className="hidden sm:inline text-xs tracking-wider uppercase">Back</span>
          </button>
          <div className="w-px h-4 bg-white/10" />
          <button onClick={() => setSidebarOpen(true)} className="flex items-center gap-2 text-white/50 hover:text-white transition-colors text-sm">
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" /></svg>
            <span className="hidden sm:inline text-xs tracking-wider uppercase">Contents</span>
          </button>
        </div>
        <div className="flex items-center gap-2">
          {currentChapter && <span className="hidden md:block text-[11px] text-white/30 tracking-wider truncate max-w-[300px]">{currentChapter.part} {" - "} {currentChapter.title}</span>}
        </div>
        <div className="flex items-center gap-3">
          <span className="text-xs text-white/40 tabular-nums font-mono">{currentPage + 1}<span className="text-white/20"> / {TOTAL_PAGES}</span></span>
        </div>
      </header>
      <div className="fixed top-12 left-0 right-0 z-30 h-[2px] bg-white/[0.03]">
        <div className="h-full bg-gradient-to-r from-cyan-500/60 via-purple-500/60 to-pink-500/60 transition-all duration-300 ease-out" style={{ width: `${progress}%` }} />
      </div>
      <main className="fixed inset-0 pt-14 pb-14 overflow-hidden">
        <div className="w-full h-full flex items-center justify-center overflow-hidden">
          <div className="hidden lg:flex h-full max-w-[48%] items-center justify-center p-4">
            {currentPage > 0 && (
              <div className="relative max-h-full cursor-pointer opacity-60 hover:opacity-90 transition-opacity duration-300" onClick={() => goToPage(currentPage - 1)}>
                <img src={`/book-pages/page_${String(currentPage - 1).padStart(4, "0")}.jpg`} alt="" className="max-h-[88vh] max-w-full object-contain rounded-sm shadow-2xl pointer-events-none" draggable={false} style={{ userSelect: "none", WebkitUserDrag: "none" }} />
              </div>
            )}
          </div>
          <div className="h-full flex items-center justify-center p-2 sm:p-4 lg:max-w-[52%]">
            <div className="relative max-h-full">
              {loading && <div className="absolute inset-0 flex items-center justify-center"><div className="w-6 h-6 border-2 border-white/20 border-t-white rounded-full animate-spin" /></div>}
              <img ref={(el) => { if (el) imageRefs.current.set(currentPage, el); }} src={`/book-pages/page_${String(currentPage).padStart(4, "0")}.jpg`} alt="" className="max-h-[85vh] max-w-full object-contain rounded-sm shadow-2xl pointer-events-none" draggable={false} onLoad={() => setLoading(false)} style={{ userSelect: "none", WebkitUserDrag: "none" }} />
              <div className="absolute inset-0 pointer-events-none flex items-end justify-end p-3">
                <span className="text-[9px] text-white/10 tracking-widest uppercase">{bookMeta.author} {" · "} {bookMeta.title}</span>
              </div>
            </div>
          </div>
          <div className="hidden lg:flex h-full max-w-[48%] items-center justify-center p-4">
            {currentPage < TOTAL_PAGES - 1 && (
              <div className="relative max-h-full cursor-pointer opacity-60 hover:opacity-90 transition-opacity duration-300" onClick={() => goToPage(currentPage + 1)}>
                <img src={`/book-pages/page_${String(currentPage + 1).padStart(4, "0")}.jpg`} alt="" className="max-h-[88vh] max-w-full object-contain rounded-sm shadow-2xl pointer-events-none" draggable={false} style={{ userSelect: "none", WebkitUserDrag: "none" }} />
              </div>
            )}
          </div>
        </div>
      </main>
      <footer className="fixed bottom-0 left-0 right-0 z-30 h-14 flex items-center justify-between px-4 md:px-8 bg-[#050505]/90 backdrop-blur-md border-t border-white/[0.04]">
        <button onClick={() => goToPage(currentPage - 1)} disabled={currentPage === 0} className="flex items-center gap-1.5 text-sm text-white/40 hover:text-white disabled:text-white/10 disabled:cursor-not-allowed transition-colors">
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" /></svg>
          <span className="hidden sm:inline text-xs tracking-wider uppercase">Previous</span>
        </button>
        <div className="flex-1 max-w-xs mx-4 sm:mx-8">
          <input type="range" min={0} max={TOTAL_PAGES - 1} value={currentPage} onChange={(e) => goToPage(parseInt(e.target.value))} className="w-full h-1 bg-white/10 rounded-full appearance-none cursor-pointer accent-white [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-white [&::-webkit-slider-thumb]:shadow-[0_0_8px_rgba(255,255,255,0.3)]" />
        </div>
        <button onClick={() => goToPage(currentPage + 1)} disabled={currentPage === TOTAL_PAGES - 1} className="flex items-center gap-1.5 text-sm text-white/40 hover:text-white disabled:text-white/10 disabled:cursor-not-allowed transition-colors">
          <span className="hidden sm:inline text-xs tracking-wider uppercase">Next</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}><path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" /></svg>
        </button>
      </footer>
      <TableOfContents isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} onGoToPage={goToPage} />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main App                                                            */
/* ------------------------------------------------------------------ */
export default function Home() {
  const [view, setView] = useState<"landing" | "reader">("landing");

  useEffect(() => {
    const prevent = (e: Event) => e.preventDefault();
    document.addEventListener("contextmenu", prevent);
    document.addEventListener("copy", prevent);
    document.addEventListener("dragstart", prevent);
    const style = document.createElement("style");
    style.textContent = "@media print { body { display: none !important; } html::after { content: \"This document is protected and cannot be printed.\"; display: block; text-align: center; padding: 50px; font-size: 24px; color: #333; } } img { -webkit-user-select: none; user-select: none; pointer-events: none; } * { -webkit-user-drag: none; }";
    document.head.appendChild(style);
    const keyHandler = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && ["s", "p", "u", "a", "c"].includes(e.key.toLowerCase())) e.preventDefault();
      if (e.key === "F12" || (e.ctrlKey && e.shiftKey && ["I", "J", "C"].includes(e.key.toUpperCase()))) e.preventDefault();
    };
    window.addEventListener("keydown", keyHandler);
    return () => {
      document.removeEventListener("contextmenu", prevent);
      document.removeEventListener("copy", prevent);
      document.removeEventListener("dragstart", prevent);
      document.head.removeChild(style);
      window.removeEventListener("keydown", keyHandler);
    };
  }, []);

  if (view === "reader") return <BookReader onBack={() => setView("landing")} />;
  return <LandingPage onOpen={() => setView("reader")} />;
}
