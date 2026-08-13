"use client";

import { useEffect, useRef, useState } from "react";

type ShootingState = {
  id: number;
  x: number;
  y: number;
  angle: number;
  scale: number;
  speed: number;
  distance: number;
};

function randomEdge(): { x: number; y: number; angle: number } {
  const e = Math.floor(Math.random() * 4);
  const t = Math.random() * window.innerWidth;
  switch (e) {
    case 0: return { x: t, y: 0, angle: 45 };
    case 1: return { x: window.innerWidth, y: t, angle: 135 };
    case 2: return { x: t, y: window.innerHeight, angle: 225 };
    case 3: return { x: 0, y: t, angle: 315 };
    default: return { x: 0, y: 0, angle: 45 };
  }
}

export default function ShootingStar({
  minSpeed = 10,
  maxSpeed = 30,
  minDelay = 1200,
  maxDelay = 4200,
  starColor = "#9E00FF",
  trailColor = "#2EB9DF",
  starWidth = 10,
  starHeight = 1,
  className = "",
}: {
  minSpeed?: number;
  maxSpeed?: number;
  minDelay?: number;
  maxDelay?: number;
  starColor?: string;
  trailColor?: string;
  starWidth?: number;
  starHeight?: number;
  className?: string;
}) {
  const [star, setStar] = useState<ShootingState | null>(null);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    let mounted = true;
    const spawn = () => {
      if (!mounted) return;
      const { x, y, angle } = randomEdge();
      setStar({
        id: Date.now(), x, y, angle, scale: 1,
        speed: Math.random() * (maxSpeed - minSpeed) + minSpeed,
        distance: 0,
      });
      const next = Math.random() * (maxDelay - minDelay) + minDelay;
      timerRef.current = setTimeout(spawn, next);
    };
    spawn();
    return () => { mounted = false; if (timerRef.current) clearTimeout(timerRef.current); };
  }, [minSpeed, maxSpeed, minDelay, maxDelay]);

  useEffect(() => {
    if (!star) return;
    let raf = 0;
    const tick = () => {
      setStar((prev) => {
        if (!prev) return null;
        const nx = prev.x + prev.speed * Math.cos((prev.angle * Math.PI) / 180);
        const ny = prev.y + prev.speed * Math.sin((prev.angle * Math.PI) / 180);
        const nd = prev.distance + prev.speed;
        const ns = 1 + nd / 100;
        if (nx < -20 || nx > window.innerWidth + 20 || ny < -20 || ny > window.innerHeight + 20) return null;
        return { ...prev, x: nx, y: ny, distance: nd, scale: ns };
      });
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [star?.id]);

  const gid = useRef(`grad-${Math.random().toString(36).slice(2, 9)}`).current;

  return (
    <svg className={`w-full h-full absolute inset-0 z-0 ${className}`} aria-hidden="true">
      {star && (
        <rect
          key={star.id}
          x={star.x}
          y={star.y}
          width={starWidth * star.scale}
          height={starHeight}
          fill={`url(#${gid})`}
          transform={`rotate(${star.angle}, ${star.x + (starWidth * star.scale) / 2}, ${star.y + starHeight / 2})`}
        />
      )}
      <defs>
        <linearGradient id={gid} x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{ stopColor: trailColor, stopOpacity: 0 }} />
          <stop offset="100%" style={{ stopColor: starColor, stopOpacity: 1 }} />
        </linearGradient>
      </defs>
    </svg>
  );
}
