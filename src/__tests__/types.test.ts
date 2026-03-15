/**
 * 型定義の整合性テスト
 * GraphSolveResultの構造が正しいかコンパイル時に検証
 */
import {
  GraphPoint,
  GraphEdge,
  GraphPath,
  GraphSolveResult,
} from "@/lib/types";

describe("Type definitions", () => {
  test("GraphPoint has required fields", () => {
    const point: GraphPoint = { name: "A", x: 0, y: 5 };
    expect(point.name).toBe("A");
    expect(point.x).toBe(0);
    expect(point.y).toBe(5);
  });

  test("GraphPoint with optional label", () => {
    const point: GraphPoint = { name: "A", label: "Alpha", x: 0, y: 5 };
    expect(point.label).toBe("Alpha");
  });

  test("GraphEdge has required fields", () => {
    const edge: GraphEdge = { from: "A", to: "B", distance: 3.6 };
    expect(edge.from).toBe("A");
    expect(edge.to).toBe("B");
    expect(edge.distance).toBe(3.6);
  });

  test("GraphPath has path and distance", () => {
    const path: GraphPath = { path: ["A", "E", "G", "I", "J"], distance: 10.4 };
    expect(path.path).toHaveLength(5);
    expect(path.distance).toBe(10.4);
  });

  test("GraphSolveResult has all required fields", () => {
    const result: GraphSolveResult = {
      shortest: { path: ["A", "E", "G", "I", "J"], distance: 10.4 },
      longest: { path: ["A", "B", "E", "H", "G", "I", "F", "C", "D", "J"], distance: 34.5 },
      points: [{ name: "A", x: 0, y: 5 }],
      edges: [{ from: "A", to: "B", distance: 3.6 }],
    };
    expect(result.shortest.distance).toBeLessThan(result.longest.distance);
    expect(result.points).toHaveLength(1);
    expect(result.edges).toHaveLength(1);
  });
});
