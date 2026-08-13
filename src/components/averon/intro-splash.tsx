"use client";

import { motion } from "framer-motion";
import TubesCursor from "./tubes-cursor";

export default function IntroSplash({
  onComplete,
}: {
  onComplete: () => void;
}) {
  return (
    <div className="relative w-full h-screen bg-[#050505] text-white overflow-hidden font-sans">
      <TubesCursor>
        <div className="flex flex-col items-center justify-center w-full h-full gap-6 text-center px-6">
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 1, delay: 0.5 }}
            className="space-y-4 pointer-events-auto cursor-default z-20"
          >
            <h1 className="text-4xl md:text-6xl font-light tracking-tight text-white drop-shadow-[0_0_20px_rgba(0,0,0,1)] select-none font-display">
              Averon
              <br />
              <span className="italic text-white/80">Volume One</span>
            </h1>
            <p className="text-lg md:text-xl text-white/80 font-light tracking-widest uppercase drop-shadow-[0_0_10px_rgba(0,0,0,1)]">
              a book by Rishabh Gupta
            </p>
            <div className="pt-8">
              <button
                onClick={(e) => { e.stopPropagation(); onComplete(); }}
                className="px-8 py-3 bg-white/10 hover:bg-white/20 border border-white/20 rounded-full text-sm uppercase tracking-widest transition-colors backdrop-blur-sm"
              >
                Enter the Protocol
              </button>
            </div>
          </motion.div>
        </div>
      </TubesCursor>
    </div>
  );
}
