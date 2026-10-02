import { useEffect, useRef } from "react";
import "./GridBackground.css";

// Visual tuning for the cursor-reactive grid background.
const CELL_SIZE = 26; // px, full tile size including the thin gap
const GAP = 3; // px, gap between cells
const GLOW_RADIUS = 220; // px, outer radius of the soft cursor glow
const BRIGHT_RADIUS = 150; // px, radius where grid cells visibly brighten
const SMOOTHING = 0.12; // 0-1 lerp factor; higher = snappier cursor follow
const TRAIL_LENGTH = 6; // number of fading trail points behind fast movement
const TRAIL_MIN_DIST = 4; // px movement before a new trail point is recorded

export default function GridBackground() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return undefined;
    const ctx = canvas.getContext("2d");
    if (!ctx) return undefined;

    const reduceMotion =
      typeof window !== "undefined" &&
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    let dpr = Math.min(window.devicePixelRatio || 1, 2);
    let width = 0;
    let height = 0;
    let pattern = null;
    let brightPattern = null;
    let rafId = null;

    const pointer = { x: -9999, y: -9999, has: false };
    const smoothed = { x: -9999, y: -9999 };
    const trail = [];

    function buildTile(cellAlpha) {
      const tile = document.createElement("canvas");
      tile.width = CELL_SIZE * dpr;
      tile.height = CELL_SIZE * dpr;
      const tctx = tile.getContext("2d");
      tctx.scale(dpr, dpr);
      tctx.clearRect(0, 0, CELL_SIZE, CELL_SIZE);
      tctx.fillStyle = `rgba(120, 190, 255, ${cellAlpha})`;
      const cellInner = CELL_SIZE - GAP;
      tctx.fillRect(0, 0, cellInner, cellInner);
      return tile;
    }

    function drawGlow(x, y, radius, alpha) {
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius);
      gradient.addColorStop(0, `rgba(140, 210, 255, ${alpha})`);
      gradient.addColorStop(1, "rgba(140, 210, 255, 0)");
      ctx.globalCompositeOperation = "lighter";
      ctx.fillStyle = gradient;
      ctx.fillRect(x - radius, y - radius, radius * 2, radius * 2);
      ctx.globalCompositeOperation = "source-over";
    }

    function draw() {
      ctx.clearRect(0, 0, width, height);

      ctx.fillStyle = "#070a10";
      ctx.fillRect(0, 0, width, height);

      ctx.fillStyle = pattern;
      ctx.fillRect(0, 0, width, height);

      if (pointer.has && !reduceMotion) {
        for (let i = 0; i < trail.length; i++) {
          const t = trail[i];
          const age = (i + 1) / trail.length;
          drawGlow(t.x, t.y, BRIGHT_RADIUS * 0.6 * age, 0.08 * age);
        }

        drawGlow(smoothed.x, smoothed.y, GLOW_RADIUS, 0.16);

        ctx.save();
        ctx.beginPath();
        ctx.arc(smoothed.x, smoothed.y, BRIGHT_RADIUS, 0, Math.PI * 2);
        ctx.clip();
        ctx.globalCompositeOperation = "lighter";
        ctx.fillStyle = brightPattern;
        ctx.fillRect(
          smoothed.x - BRIGHT_RADIUS,
          smoothed.y - BRIGHT_RADIUS,
          BRIGHT_RADIUS * 2,
          BRIGHT_RADIUS * 2
        );
        ctx.globalCompositeOperation = "source-over";
        ctx.restore();
      }
    }

    function resize() {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      width = window.innerWidth;
      height = window.innerHeight;
      canvas.width = width * dpr;
      canvas.height = height * dpr;
      canvas.style.width = "100%";
      canvas.style.height = "100%";
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

      const dimTile = buildTile(0.05);
      const brightTile = buildTile(0.4);
      pattern = ctx.createPattern(dimTile, "repeat");
      brightPattern = ctx.createPattern(brightTile, "repeat");
      draw();
    }

    function tick() {
      smoothed.x += (pointer.x - smoothed.x) * SMOOTHING;
      smoothed.y += (pointer.y - smoothed.y) * SMOOTHING;

      if (pointer.has) {
        const last = trail[trail.length - 1];
        const dist = last
          ? Math.hypot(smoothed.x - last.x, smoothed.y - last.y)
          : Infinity;
        if (dist > TRAIL_MIN_DIST) {
          trail.push({ x: smoothed.x, y: smoothed.y });
          if (trail.length > TRAIL_LENGTH) trail.shift();
        }
      }

      draw();
      rafId = requestAnimationFrame(tick);
    }

    function handlePointerMove(e) {
      const point = e.touches ? e.touches[0] : e;
      if (!point) return;
      pointer.x = point.clientX;
      pointer.y = point.clientY;
      if (!pointer.has) {
        pointer.has = true;
        smoothed.x = pointer.x;
        smoothed.y = pointer.y;
      }
    }

    function handlePointerLeave() {
      pointer.has = false;
      trail.length = 0;
    }

    function handleVisibility() {
      if (document.hidden) {
        if (rafId) cancelAnimationFrame(rafId);
        rafId = null;
      } else if (!rafId && !reduceMotion) {
        rafId = requestAnimationFrame(tick);
      }
    }

    resize();

    if (reduceMotion) {
      // Static, low-contrast grid only — no animation loop, no tracking.
      window.addEventListener("resize", resize);
      return () => window.removeEventListener("resize", resize);
    }

    rafId = requestAnimationFrame(tick);

    window.addEventListener("resize", resize);
    window.addEventListener("mousemove", handlePointerMove, { passive: true });
    window.addEventListener("touchmove", handlePointerMove, { passive: true });
    window.addEventListener("touchstart", handlePointerMove, { passive: true });
    window.addEventListener("mouseleave", handlePointerLeave);
    window.addEventListener("touchend", handlePointerLeave);
    document.addEventListener("visibilitychange", handleVisibility);

    return () => {
      if (rafId) cancelAnimationFrame(rafId);
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", handlePointerMove);
      window.removeEventListener("touchmove", handlePointerMove);
      window.removeEventListener("touchstart", handlePointerMove);
      window.removeEventListener("mouseleave", handlePointerLeave);
      window.removeEventListener("touchend", handlePointerLeave);
      document.removeEventListener("visibilitychange", handleVisibility);
    };
  }, []);

  return (
    <div className="grid-bg" aria-hidden="true">
      <canvas ref={canvasRef} />
    </div>
  );
}