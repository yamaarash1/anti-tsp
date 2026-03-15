/**
 * GraphResultPanel コンポーネントテスト
 */
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import GraphResultPanel from "@/components/GraphResultPanel";
import { GraphSolveResult } from "@/lib/types";

const mockResult: GraphSolveResult = {
  shortest: { path: ["A", "E", "G", "I", "J"], distance: 10.4 },
  longest: { path: ["A", "B", "E", "H", "G", "I", "F", "C", "D", "J"], distance: 34.5 },
  points: [],
  edges: [],
};

describe("GraphResultPanel", () => {
  test("最短経路ヘッダーに距離が含まれる", () => {
    render(<GraphResultPanel result={mockResult} />);
    expect(screen.getByText(/最短経路.*10\.4/)).toBeInTheDocument();
  });

  test("最長経路ヘッダーに距離が含まれる", () => {
    render(<GraphResultPanel result={mockResult} />);
    expect(screen.getByText(/最長経路.*ビットDP.*34\.5/)).toBeInTheDocument();
  });

  test("最短経路がA → E → G → I → J形式で表示される", () => {
    render(<GraphResultPanel result={mockResult} />);
    expect(screen.getByText("A → E → G → I → J")).toBeInTheDocument();
  });

  test("最長経路がA → B → ... → J形式で表示される", () => {
    render(<GraphResultPanel result={mockResult} />);
    expect(screen.getByText("A → B → E → H → G → I → F → C → D → J")).toBeInTheDocument();
  });

  test("差分24.1が表示される", () => {
    render(<GraphResultPanel result={mockResult} />);
    expect(screen.getByText(/24\.1/)).toBeInTheDocument();
  });

  test("ノード数が表示される", () => {
    render(<GraphResultPanel result={mockResult} />);
    expect(screen.getByText("5 ノード")).toBeInTheDocument();
    expect(screen.getByText("10 ノード")).toBeInTheDocument();
  });

  test("同じ距離の場合、差分0.0が含まれる", () => {
    const sameResult: GraphSolveResult = {
      shortest: { path: ["A", "B"], distance: 3.6 },
      longest: { path: ["A", "B"], distance: 3.6 },
      points: [],
      edges: [],
    };
    render(<GraphResultPanel result={sameResult} />);
    expect(screen.getAllByText(/0\.0/).length).toBeGreaterThanOrEqual(1);
  });
});
