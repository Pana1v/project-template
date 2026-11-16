import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { Chart } from "./Chart";
import "./styles.css";

type Row = Record<string, number>;

function App() {
  const [runs, setRuns] = useState<string[]>([]);
  const [run, setRun] = useState<string>("");
  const [rows, setRows] = useState<Row[]>([]);

  // Refresh the run list every 5 s so new runs show up without a reload.
  useEffect(() => {
    const load = () =>
      fetch("/api/runs")
        .then((r) => r.json())
        .then((list: string[]) => {
          setRuns(list);
          setRun((cur) => cur || list[0] || "");
        })
        .catch(() => {});
    load();
    const t = setInterval(load, 5000);
    return () => clearInterval(t);
  }, []);

  // Stream the selected run: the backend sends all rows first, then new ones as they land.
  useEffect(() => {
    setRows([]);
    if (!run) return;
    const ws = new WebSocket(`${location.protocol === "https:" ? "wss" : "ws"}://${location.host}/ws/${encodeURIComponent(run)}`);
    ws.onmessage = (e) => setRows((prev) => prev.concat(JSON.parse(e.data)));
    return () => ws.close();
  }, [run]);

  // Union over all rows: a metric first logged later still gets a chart.
  const keys = [...new Set(rows.flatMap((r) => Object.keys(r).filter((k) => k !== "step" && typeof r[k] === "number")))];
  const steps = rows.map((r, i) => r.step ?? i);

  return (
    <main>
      <header>
        <h1>project-template</h1>
        <select value={run} onChange={(e) => setRun(e.target.value)} aria-label="Run">
          {runs.map((r) => (
            <option key={r}>{r}</option>
          ))}
        </select>
      </header>
      {!runs.length && <p>No runs yet. Start one with <code>make demo</code>.</p>}
      <div className="grid">
        {keys.map((k) => (
          <Chart key={k} title={k} data={[steps, rows.map((r) => r[k])]} />
        ))}
      </div>
    </main>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
