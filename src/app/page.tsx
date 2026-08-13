"use client";

import { useState, useEffect, useCallback, useRef } from "react";
import { bookMeta, parts, allChapters, TOTAL_PAGES } from "@/lib/book-data";
import IntroSplash from "@/components/averon/intro-splash";
import MainPage from "@/components/averon/main-page";

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
  const [loading, setLoading] = useState(true);
  const imageRefs = useRef<Map<number, HTMLImageElement>>(new Map());

  const goToPage = useCallback((page: number) => {
    setCurrentPage(Math.max(0, Math.min(page, TOTAL_PAGES - 1)));
  }, []);

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
                <span className="text-[9px] text-white/10 tracking-widest uppercase">{bookMeta.author} {" \u00b7 "} {bookMeta.title}</span>
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
  const [view, setView] = useState<"splash" | "main" | "reader">("splash");

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

  if (view === "reader") return <BookReader onBack={() => setView("main")} />;
  if (view === "main") return <MainPage onEnter={() => setView("reader")} />;
  return <IntroSplash onComplete={() => setView("main")} />;
}
