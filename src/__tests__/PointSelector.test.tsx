/**
 * PointSelector コンポーネントテスト
 * - ドロップダウンが表示されるか
 * - 同一始点終点で警告が出るか
 * - ボタンの活性/非活性制御
 */
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import "@testing-library/jest-dom";
import PointSelector from "@/components/PointSelector";

// fetchGraphPointsをモック
jest.mock("@/lib/api", () => ({
  fetchGraphPoints: jest.fn().mockResolvedValue([
    { name: "A", label: "Alpha", x: 0, y: 5 },
    { name: "B", label: "Bravo", x: 2, y: 8 },
    { name: "C", label: "Charlie", x: 5, y: 8 },
  ]),
}));

describe("PointSelector", () => {
  const mockOnSolve = jest.fn();

  beforeEach(() => {
    mockOnSolve.mockClear();
  });

  test("ドロップダウンにポイントが表示される", async () => {
    render(<PointSelector onSolve={mockOnSolve} loading={false} />);
    await waitFor(() => {
      expect(screen.getAllByText("A (Alpha)")).toHaveLength(2); // 始点・終点に各1つ
    });
  });

  test("経路計算ボタンが表示される", async () => {
    render(<PointSelector onSolve={mockOnSolve} loading={false} />);
    await waitFor(() => {
      expect(screen.getByText("経路計算")).toBeInTheDocument();
    });
  });

  test("loading中はボタンが計算中...になる", async () => {
    render(<PointSelector onSolve={mockOnSolve} loading={true} />);
    await waitFor(() => {
      expect(screen.getByText("計算中...")).toBeInTheDocument();
    });
  });

  test("同一ポイント選択で警告表示", async () => {
    const user = userEvent.setup();
    render(<PointSelector onSolve={mockOnSolve} loading={false} />);

    await waitFor(() => {
      expect(screen.getAllByText("A (Alpha)")).toHaveLength(2);
    });

    // 始点と終点を同じにする
    const selects = screen.getAllByRole("combobox");
    await user.selectOptions(selects[0], "A");
    await user.selectOptions(selects[1], "A");

    expect(screen.getByText("始点と終点は異なるポイントを選んでください")).toBeInTheDocument();
  });
});
