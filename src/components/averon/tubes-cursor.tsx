"use client";

import { useEffect, useRef, useState } from "react";

type TubesApi = {
  tubes: {
    setColors: (colors: string[]) => void;
    setLightsColors: (colors: string[]) => void;
  };
};

type TubesOpts = {
  tubes: {
    colors: string[];
    lights: {
      intensity: number;
      colors: string[];
    };
  };
};

declare global {
  interface Window {
    __tubes1Factory?: (canvas: HTMLCanvasElement, opts: TubesOpts) => TubesApi;
  }
}

const CDN_URL =
  "https://cdn.jsdelivr.net/npm/threejs-components@0.0.19/build/cursors/tubes1.min.js";

function randColors(n: number): string[] {
  return Array.from({ length: n }, () => {
    const hex = Math.floor(Math.random() * 16777215)
      .toString(16)
      .padStart(6, "0");
    return `#${hex}`;
  });
}

function loadTubesModule(): Promise<void> {
  return new Promise((resolve, reject) => {
    if (window.__tubes1Factory) {
      resolve();
      return;
    }
    const id = "tubes1-loader";
    const existing = document.getElementById(id) as HTMLScriptElement | null;
    if (existing) {
      existing.addEventListener("load", () => resolve());
      existing.addEventListener("error", () =>
        reject(new Error("tubes1 load error"))
      );
      return;
    }
    const s = document.createElement("script");
    s.id = id;
    s.type = "module";
    s.textContent = `
      import factory from "${CDN_URL}";
      window.__tubes1Factory = factory;
      window.dispatchEvent(new Event("tubes1-ready"));
    `;
    s.addEventListener("error", () => reject(new Error("tubes1 script error")));
    window.addEventListener("tubes1-ready", () => resolve(), { once: true });
    document.head.appendChild(s);
    setTimeout(() => {
      if (window.__tubes1Factory) resolve();
      else reject(new Error("tubes1 load timeout"));
    }, 8000);
  });
}

export default function TubesCursor({
  children,
  className = "",
  enableClickInteraction = true,
}: {
  children?: React.ReactNode;
  className?: string;
  enableClickInteraction?: boolean;
}) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const apiRef = useRef<TubesApi | null>(null);
  const [loaded, setLoaded] = useState(false);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      if (!canvasRef.current) return;
      try {
        await loadTubesModule();
        if (cancelled || !canvasRef.current) return;
        const factory = window.__tubes1Factory;
        if (!factory) throw new Error("Tubes1 factory not found on window");
        apiRef.current = factory(canvasRef.current, {
          tubes: {
            colors: ["#f967fb", "#53bc28", "#6958d5"],
            lights: {
              intensity: 200,
              colors: ["#83f36e", "#fe8a2e", "#ff008a", "#60aed5"],
            },
          },
        });
        setLoaded(true);
      } catch (err) {
        console.error("TubesCursor load failed:", err);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div
      className={`relative w-full h-full min-h-[400px] overflow-hidden bg-background ${className}`}
      onClick={() => {
        if (!enableClickInteraction || !apiRef.current) return;
        apiRef.current.tubes.setColors(randColors(3));
        apiRef.current.tubes.setLightsColors(randColors(4));
      }}
    >
      <canvas
        ref={canvasRef}
        className="absolute inset-0 w-full h-full block"
        style={{ touchAction: "none" }}
      />
      {!loaded && <div className="stars absolute inset-0" aria-hidden="true" />}
      <div className="relative z-10 w-full h-full pointer-events-none">
        {children}
      </div>
    </div>
  );
}
