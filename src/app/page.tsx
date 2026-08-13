"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { bookMeta, parts, allChapters, TOTAL_PAGES, type Part } from "@/lib/book-data";

/* ------------------------------------------------------------------ */
/*  Particle canvas – subtle network-graph effect                     */
/* ------------------------------------------------------------------ */
function ParticleCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animId: number;
    let w = (canvas.width = window.innerWidth);
    let h = (canvas.height = window.innerHeight);

    const particles: { x: number; y: number; vx: number; vy: number; r: number }[] = [];
    const COUNT = Math.min(80, Math.floor((w * h) / 18000));

    for (let i = 0; i < COUNT; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        vx: (Math.random() - 0.5) * 0.3,
        vy: (Math.random() - 0.5) * 0.3,
        r: Math.random() * 1.5 + 0.5,
      });
    }

    const draw = () => {
      ctx!.clearRect(0, 0, w, h);

      for (const p of particles) {
        p.x += p.vx;
        p.y += p.vy;
        if (p.x < 0 || p.x > w) p.vx *= -1;
        if (p.y < 0 || p.y > h) p.vy *= -1;

        ctx!.beginPath();
        ctx!.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx!.fillStyle = "rgba(212,175,55,0.35)";
        ctx!.fill();
      }

      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 140) {
            ctx!.beginPath();
            ctx!.moveTo(particles[i].x, particles[i].y);
            ctx!.lineTo(particles[j].x, particles[j].y);
            ctx!.strokeStyle = `rgba(212,175,55,${0.12 * (1 - dist / 140)})`;
            ctx!.lineWidth = 0.5;
            ctx!.stroke();
          }
        }
      }

      animId = requestAnimationFrame(draw);
    };

    draw();

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

  return (
    <canvas
      ref={canvasRef}
      className="absolute inset-0 w-full h-full block"
      style={{ touchAction: "none" }}
    />
  );
}

/* ------------------------------------------------------------------ */
/*  Landing Page                                                       */
/* ------------------------------------------------------------------ */
function LandingPage({ onOpen }: { onOpen: () => void }) {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 200);
    return () => clearTimeout(t);
  }, []);

  return (
    <div className="relative w-full h-screen bg-[#050505] text-white overflow-hidden font-sans">
      <ParticleCanvas />

      <div className="relative z-10 w-full h-full pointer-events-none">
        <div className="flex flex-col items-center justify-center w-full h-full gap-6 text-center px-6">
          <div
            className="space-y-5 pointer-events-auto cursor-default z-20"
            style={{
              opacity: visible ? 1 : 0,
              transform: visible ? "translateY(0)" : "translateY(16px)",
              transition: "opacity 1.2s ease, transform 1.2s ease",
            }}
          >
            <div className="flex items-center justify-center gap-3 mb-2">
              <span className="text-xs tracking-[0.35em] uppercase text-[#d4af37]/60">
                {bookMeta.series}
              </span>
            </div>

            <h1 className="text-5xl sm:text-6xl md:text-7xl lg:text-8xl font-light tracking-tight drop-shadow-[0_0_30px_rgba(212,175,55,0.15)] select-none leading-[1.1]">
              <span className="text-[#d4af37]">AVERON</span>
            </h1>

            <h2 className="text-lg sm:text-xl md:text-2xl text-white/90 font-light tracking-wide">
              {bookMeta.subtitle}
            </h2>

            <p className="text-sm md:text-base text-white/50 font-light tracking-widest uppercase mt-2">
              {bookMeta.description}
            </p>

            <div className="flex items-center justify-center gap-2 mt-1">
              <div className="w-8 h-px bg-[#d4af37]/40" />
              <span className="text-xs tracking-[0.25em] text-white/40 uppercase">
                by {bookMeta.author}
              </span>
              <div className="w-8 h-px bg-[#d4af37]/40" />
            </div>

            <div className="pt-8">
              <button
                onClick={onOpen}
                className="group px-8 py-3.5 bg-white/[0.06] hover:bg-[#d4af37]/20 border border-[#d4af37]/30 hover:border-[#d4af37]/60 rounded-full text-sm uppercase tracking-[0.2em] transition-all duration-500 backdrop-blur-sm text-[#d4af37]/90 hover:text-[#d4af37]"
              >
                <span className="inline-flex items-center gap-2">
                  Read the Book
                  <svg
                    className="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1"
                    fill="none"
                    viewBox="0 0 24 24"
                    stroke="currentColor"
                    strokeWidth={1.5}
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3"
                    />
                  </svg>
                </span>
              </button>
            </div>

            <p className="text-[10px] text-white/20 tracking-wider mt-6">
              {bookMeta.edition} · {bookMeta.role}
            </p>
          </div>
        </div>
      </div>

      {/* Bottom fade */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#050505] to-transparent z-20" />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Table of Contents Sidebar                                          */
/* ------------------------------------------------------------------ */
function TableOfContents({
  isOpen,
  onClose,
  onGoToPage,
}: {
  isOpen: boolean;
  onClose: () => void;
  onGoToPage: (p: number) => void;
}) {
  return (
    <>
      {/* Backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 backdrop-blur-sm lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`
          fixed top-0 left-0 z-50 h-full w-80 bg-[#0a0a0a] border-r border-white/[0.06]
          transform transition-transform duration-300 ease-in-out overflow-hidden
          ${isOpen ? "translate-x-0" : "-translate-x-full"}
        `}
      >
        <div className="flex items-center justify-between p-5 border-b border-white/[0.06]">
          <h2 className="text-xs tracking-[0.2em] uppercase text-[#d4af37]/80">
            Contents
          </h2>
          <button
            onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors text-white/50 hover:text-white"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <div className="overflow-y-auto h-[calc(100%-60px)] py-2 px-2 custom-scrollbar">
          {parts.map((part, pi) => (
            <div key={pi} className="mb-4">
              <div className="px-3 py-2 text-[10px] tracking-[0.25em] uppercase text-[#d4af37]/50 font-medium">
                Part {pi + 1} — {part.title}
              </div>
              {part.chapters.map((ch, ci) => (
                <button
                  key={ci}
                  onClick={() => {
                    onGoToPage(ch.page);
                    onClose();
                  }}
                  className="w-full text-left px-4 py-2 text-sm text-white/60 hover:text-[#d4af37] hover:bg-white/[0.03] rounded-md transition-all duration-200 truncate"
                >
                  <span className="text-white/25 text-xs mr-2 tabular-nums">
                    {ch.page}
                  </span>
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
/*  Book Reader                                                        */
/* ------------------------------------------------------------------ */
function BookReader({ onBack }: { onBack: () => void }) {
  const [currentPage, setCurrentPage] = useState(0);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [loadedImages, setLoadedImages] = useState<Set<number>>(new Set([0]));
  const [loading, setLoading] = useState(true);
  const containerRef = useRef<HTMLDivElement>(null);
  const imageRefs = useRef<Map<number, HTMLImageElement>>(new Map());

  const goToPage = useCallback((page: number) => {
    setCurrentPage(Math.max(0, Math.min(page, TOTAL_PAGES - 1)));
  }, []);

  const preloadPage = useCallback((pageNum: number) => {
    if (pageNum < 0 || pageNum >= TOTAL_PAGES || loadedImages.has(pageNum)) return;
    const img = new Image();
    img.src = `/api/book-page?page=${pageNum}`;
    img.onload = () => {
      setLoadedImages((prev) => new Set([...prev, pageNum]));
    };
  }, [loadedImages]);

  useEffect(() => {
    preloadPage(currentPage);
    // Preload adjacent pages
    preloadPage(currentPage - 1);
    preloadPage(currentPage + 1);
    preloadPage(currentPage + 2);
  }, [currentPage, preloadPage]);

  useEffect(() => {
    setLoading(true);
  }, [currentPage]);

  // Keyboard navigation
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" || e.key === "ArrowDown") {
        e.preventDefault();
        goToPage(currentPage + 1);
      } else if (e.key === "ArrowLeft" || e.key === "ArrowUp") {
        e.preventDefault();
        goToPage(currentPage - 1);
      } else if (e.key === "Escape") {
        onBack();
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, [currentPage, goToPage, onBack]);

  const currentChapter = allChapters.find(
    (c) => currentPage >= c.page && (allChapters[allChapters.indexOf(c) + 1]?.page ?? TOTAL_PAGES) > currentPage
  );

  const progress = ((currentPage + 1) / TOTAL_PAGES) * 100;

  return (
    <div
      className="relative w-full h-screen bg-[#050505] text-white overflow-hidden select-none"
      onContextMenu={(e) => e.preventDefault()}
      onDragStart={(e) => e.preventDefault()}
    >
      {/* Top bar */}
      <header className="fixed top-0 left-0 right-0 z-30 flex items-center justify-between px-4 md:px-6 h-12 bg-[#050505]/90 backdrop-blur-md border-b border-white/[0.04]">
        <div className="flex items-center gap-3">
          <button
            onClick={onBack}
            className="flex items-center gap-2 text-white/50 hover:text-[#d4af37] transition-colors text-sm"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
            </svg>
            <span className="hidden sm:inline text-xs tracking-wider uppercase">Back</span>
          </button>
          <div className="w-px h-4 bg-white/10" />
          <button
            onClick={() => setSidebarOpen(true)}
            className="flex items-center gap-2 text-white/50 hover:text-[#d4af37] transition-colors text-sm"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
            </svg>
            <span className="hidden sm:inline text-xs tracking-wider uppercase">Contents</span>
          </button>
        </div>

        <div className="flex items-center gap-2">
          {currentChapter && (
            <span className="hidden md:block text-[11px] text-white/30 tracking-wider truncate max-w-[300px]">
              {currentChapter.part} — {currentChapter.title}
            </span>
          )}
        </div>

        <div className="flex items-center gap-3">
          <span className="text-xs text-white/40 tabular-nums font-mono">
            {currentPage + 1}<span className="text-white/20"> / {TOTAL_PAGES}</span>
          </span>
        </div>
      </header>

      {/* Progress bar */}
      <div className="fixed top-12 left-0 right-0 z-30 h-[2px] bg-white/[0.03]">
        <div
          className="h-full bg-gradient-to-r from-[#d4af37]/60 to-[#d4af37] transition-all duration-300 ease-out"
          style={{ width: `${progress}%` }}
        />
      </div>

      {/* Main content area */}
      <main className="fixed inset-0 pt-14 pb-14 overflow-hidden">
        <div
          ref={containerRef}
          className="w-full h-full flex items-center justify-center overflow-hidden"
        >
          {/* Previous page (desktop) */}
          <div className="hidden lg:flex h-full max-w-[48%] items-center justify-center p-4">
            {currentPage > 0 && (
              <div
                className="relative max-h-full cursor-pointer opacity-60 hover:opacity-90 transition-opacity duration-300"
                onClick={() => goToPage(currentPage - 1)}
              >
                <img
                  src={`/api/book-page?page=${currentPage - 1}`}
                  alt=""
                  className="max-h-[88vh] max-w-full object-contain rounded-sm shadow-2xl pointer-events-none"
                  draggable={false}
                  style={{ userSelect: "none", WebkitUserDrag: "none" }}
                />
              </div>
            )}
          </div>

          {/* Current page */}
          <div className="h-full flex items-center justify-center p-2 sm:p-4 lg:max-w-[52%]">
            <div className="relative max-h-full">
              {loading && (
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-6 h-6 border-2 border-[#d4af37]/20 border-t-[#d4af37] rounded-full animate-spin" />
                </div>
              )}
              <img
                ref={(el) => {
                  if (el) imageRefs.current.set(currentPage, el);
                }}
                src={`/api/book-page?page=${currentPage}`}
                alt=""
                className="max-h-[85vh] max-w-full object-contain rounded-sm shadow-2xl pointer-events-none"
                draggable={false}
                onLoad={() => setLoading(false)}
                style={{ userSelect: "none", WebkitUserDrag: "none" }}
              />
              {/* Watermark overlay */}
              <div className="absolute inset-0 pointer-events-none flex items-end justify-end p-3">
                <span className="text-[9px] text-white/10 tracking-widest uppercase">
                  {bookMeta.author} · {bookMeta.title}
                </span>
              </div>
            </div>
          </div>

          {/* Next page (desktop) */}
          <div className="hidden lg:flex h-full max-w-[48%] items-center justify-center p-4">
            {currentPage < TOTAL_PAGES - 1 && (
              <div
                className="relative max-h-full cursor-pointer opacity-60 hover:opacity-90 transition-opacity duration-300"
                onClick={() => goToPage(currentPage + 1)}
              >
                <img
                  src={`/api/book-page?page=${currentPage + 1}`}
                  alt=""
                  className="max-h-[88vh] max-w-full object-contain rounded-sm shadow-2xl pointer-events-none"
                  draggable={false}
                  style={{ userSelect: "none", WebkitUserDrag: "none" }}
                />
              </div>
            )}
          </div>
        </div>
      </main>

      {/* Bottom navigation */}
      <footer className="fixed bottom-0 left-0 right-0 z-30 h-14 flex items-center justify-between px-4 md:px-8 bg-[#050505]/90 backdrop-blur-md border-t border-white/[0.04]">
        <button
          onClick={() => goToPage(currentPage - 1)}
          disabled={currentPage === 0}
          className="flex items-center gap-1.5 text-sm text-white/40 hover:text-[#d4af37] disabled:text-white/10 disabled:cursor-not-allowed transition-colors"
        >
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5L8.25 12l7.5-7.5" />
          </svg>
          <span className="hidden sm:inline text-xs tracking-wider uppercase">Previous</span>
        </button>

        {/* Page slider for mobile */}
        <div className="flex-1 max-w-xs mx-4 sm:mx-8">
          <input
            type="range"
            min={0}
            max={TOTAL_PAGES - 1}
            value={currentPage}
            onChange={(e) => goToPage(parseInt(e.target.value))}
            className="w-full h-1 bg-white/10 rounded-full appearance-none cursor-pointer accent-[#d4af37] [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-[#d4af37] [&::-webkit-slider-thumb]:shadow-[0_0_8px_rgba(212,175,55,0.4)]"
          />
        </div>

        <button
          onClick={() => goToPage(currentPage + 1)}
          disabled={currentPage === TOTAL_PAGES - 1}
          className="flex items-center gap-1.5 text-sm text-white/40 hover:text-[#d4af37] disabled:text-white/10 disabled:cursor-not-allowed transition-colors"
        >
          <span className="hidden sm:inline text-xs tracking-wider uppercase">Next</span>
          <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
          </svg>
        </button>
      </footer>

      {/* Table of Contents sidebar */}
      <TableOfContents
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onGoToPage={goToPage}
      />
    </div>
  );
}

/* ------------------------------------------------------------------ */
/*  Main App                                                           */
/* ------------------------------------------------------------------ */
export default function Home() {
  const [view, setView] = useState<"landing" | "reader">("landing");

  // Anti-piracy: disable right-click, copy, print, drag globally
  useEffect(() => {
    const prevent = (e: Event) => e.preventDefault();
    document.addEventListener("contextmenu", prevent);
    document.addEventListener("copy", prevent);
    document.addEventListener("dragstart", prevent);

    // Disable print via CSS media
    const style = document.createElement("style");
    style.textContent = `
      @media print {
        body { display: none !important; }
        html::after {
          content: "This document is protected and cannot be printed.";
          display: block;
          text-align: center;
          padding: 50px;
          font-size: 24px;
          color: #333;
        }
      }
      img { -webkit-user-select: none; user-select: none; pointer-events: none; }
      * { -webkit-user-drag: none; }
    `;
    document.head.appendChild(style);

    // Disable keyboard shortcuts (Ctrl+S, Ctrl+P, Ctrl+Shift+I, etc.)
    const keyHandler = (e: KeyboardEvent) => {
      if (
        (e.ctrlKey || e.metaKey) &&
        ["s", "p", "u", "a", "c"].includes(e.key.toLowerCase())
      ) {
        e.preventDefault();
      }
      if (e.key === "F12" || (e.ctrlKey && e.shiftKey && ["I", "J", "C"].includes(e.key.toUpperCase()))) {
        e.preventDefault();
      }
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

  if (view === "reader") {
    return <BookReader onBack={() => setView("landing")} />;
  }

  return <LandingPage onOpen={() => setView("reader")} />;
}
