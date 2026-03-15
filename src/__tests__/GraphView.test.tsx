/**
 * GraphView コンポーネントテスト
 * - SVGが正しくレンダリングされるか
 * - ポイント・エッジが描画されるか
 * - 結果ありの場合に凡例が表示されるか
 */
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import GraphView from "@/components/GraphView";
import { GraphPoint, GraphEdge, GraphSolveResult } from "@/lib/types";

const points: GraphPoint[] = [
  { name: "A", label: "Alpha", x: 0, y: 5 },
  { name: "B", label: "Bravo", x: 2, y: 8 },
  { name: "C", label: "Charlie", x: 5, y: 8 },
];

const edges: GraphEdge[] = [
  { from: "A", to: "B", distance: 3.6 },
  { from: "B", to: "C", distance: 3.0 },
];

describe("GraphView", () => {
  test("ポイント名がSVGに表示される", () => {
    render(<GraphView points={points} edges={edges} />);
    expect(screen.getByText("A")).toBeInTheDocument();
    expect(screen.getByText("B")).toBeInTheDocument();
    expect(screen.getByText("C")).toBeInTheDocument();
  });

  test("エッジの距離ラベルが表示される", () => {
    render(<GraphView points={points} edges={edges} />);
    expect(screen.getByText("3.6")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
  });

  test("結果なしの場合、凡例は表示されない", () => {
    render(<GraphView points={points} edges={edges} />);
    expect(screen.queryByText("始点")).not.toBeInTheDocument();
  });

  test("結果ありの場合、凡例が表示される", () => {
    const result: GraphSolveResult = {
      shortest: { path: ["A", "B", "C"], distance: 6.6 },
      longest: { path: ["A", "B", "C"], distance: 6.6 },
      points,
      edges,
    };
    render(<GraphView points={points} edges={edges} result={result} />);
    expect(screen.getByText("始点")).toBeInTheDocument();
    expect(screen.getByText("終点")).toBeInTheDocument();
    expect(screen.getByText("最短")).toBeInTheDocument();
    expect(screen.getByText("最長")).toBeInTheDocument();
  });

  test("ポイントが空の場合、ローディング表示", () => {
    render(<GraphView points={[]} edges={[]} />);
    expect(screen.getByText("読み込み中...")).toBeInTheDocument();
  });
});
