"use client";

import { motion } from "framer-motion";
import ShootingStar from "./shooting-star";

export default function MainPage({
  onEnter,
}: {
  onEnter?: () => void;
}) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.2, ease: "easeInOut" }}
      className="flex w-dvw h-dvh justify-center items-center bg-black overflow-hidden relative"
    >
      {/* Radial white glow + starfield twinkle */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_center,rgba(255,255,255,0.15)_0%,rgba(0,0,0,0)_80%)]" />
        <div className="stars absolute inset-0" />
      </div>

      {/* Three shooting stars with neon colors */}
      <ShootingStar
        starColor="#9E00FF"
        trailColor="#2EB9DF"
        minSpeed={15}
        maxSpeed={35}
        minDelay={1000}
        maxDelay={3000}
        className="pointer-events-none"
      />
      <ShootingStar
        starColor="#FF0099"
        trailColor="#FFB800"
        minSpeed={10}
        maxSpeed={25}
        minDelay={2000}
        maxDelay={4000}
        className="pointer-events-none"
      />
      <ShootingStar
        starColor="#00FF9E"
        trailColor="#00B8FF"
        minSpeed={20}
        maxSpeed={40}
        minDelay={1500}
        maxDelay={3500}
        className="pointer-events-none"
      />

      {/* Centered content */}
      <motion.div
        className="z-50 text-center space-y-4 items-center flex flex-col max-w-2xl px-4"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.88, delay: 1.5 }}
      >
        <p className="text-5xl md:text-7xl z-50 text-white font-handwriting leading-tight drop-shadow-[0_0_20px_rgba(0,0,0,1)]">
          Averon
        </p>
        <p className="text-3xl md:text-4xl z-50 text-white/90 font-handwriting translate-y-[-10px] drop-shadow-[0_0_15px_rgba(0,0,0,1)]">
          a book by Rishabh Gupta
        </p>
        <p
          onClick={onEnter}
          className="text-sm font-medium z-50 hover:scale-110 transition-transform bg-white text-black rounded-full px-6 py-3 cursor-pointer text-center mt-4"
        >
          Start Reading
        </p>

        {/* Pickup line 1 */}
        <motion.p
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 2.4 }}
          className="mt-12 max-w-md mx-auto text-lg md:text-2xl text-white/70 font-handwriting italic leading-snug drop-shadow-[0_0_15px_rgba(0,0,0,1)]"
        >
          This is where I document everything I learn while building Averon and researching the future of real-world asset tokenization
        </motion.p>

        {/* Pickup line 2 */}
        <motion.p
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 3.2 }}
          className="mt-4 max-w-sm mx-auto text-base md:text-lg text-white/50 font-handwriting leading-snug drop-shadow-[0_0_15px_rgba(0,0,0,1)]"
        >
          Built from first principles. Documented with curiosity. Shared through Averon.
        </motion.p>
      </motion.div>
    </motion.div>
  );
}
