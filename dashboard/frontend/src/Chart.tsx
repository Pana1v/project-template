import { useEffect, useRef } from "react";
import uPlot from "uplot";
import "uplot/dist/uPlot.min.css";

// One line chart. data = [x values, y values].
export function Chart({ title, data, height = 220 }: { title: string; data: number[][]; height?: number }) {
  const wrap = useRef<HTMLDivElement>(null);
  const plot = useRef<uPlot | null>(null);

  useEffect(() => {
    const el = wrap.current!;
    plot.current = new uPlot(
      {
        width: Math.max(200, el.clientWidth),
        height,
        scales: { x: { time: false } },
        axes: [{ stroke: "currentColor" }, { stroke: "currentColor", size: 56 }],
        series: [{ label: "step" }, { label: title, stroke: "#2a9d8f", width: 1.5, points: { show: false } }],
      },
      data as uPlot.AlignedData,
      el,
    );
    const ro = new ResizeObserver(() => plot.current?.setSize({ width: el.clientWidth, height }));
    ro.observe(el);
    return () => {
      ro.disconnect();
      plot.current?.destroy();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [title, height]);

  useEffect(() => plot.current?.setData(data as uPlot.AlignedData), [data]);

  return (
    <section className="panel">
      <h3>{title}</h3>
      <div ref={wrap} />
    </section>
  );
}
