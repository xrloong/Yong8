# Yong8
以限制滿足問題來建構漢字字形（Use Constraint Satisfaction Problem to Construct Hanzi Glyph）。

受到 iOS 的 Auto Layout 和 Android 的 ConstraintLayout 的啟發，可以把類似技術用於漢字的構形。Auto Layout 和 ConstraintLayout 在描述版面佈局時，會描述將每個部件的限制（如描述置中、在某個部件的右方多少位置），並將之轉化為線性規劃的問題。

Inspired by iOS Auto Layout and Android ConstraintLayout, we may apply such technique for HanZi glyph. Auto Layout and ConstraintLayout describes a layout be describe constraints between each component (for example, being at center, or be at the right of another component with some distance), and convert it to be a linear programming problem.

類似的，可以將漢字構形看做筆劃和部件的佈局問題，而筆劃間和部件間有各種限制條件。

Similarly, we may treat Hanzi glyph as layouting problem of strokes and components, and there are many constraints between strokes and between components.

本計劃目的即為開發以限制滿足問題來描述漢字構形的技術。

The goal of the project is to develop such technique to describe Hanzi glyph by constraint satisfaction problem.

安裝
====

* 第三方函式庫（Third-party libraries）
```console
$ pip3 install <<package-name>>
```

|   solver  | PIP package |
| :-------: | :---------: |
| cassowary |  cassowary  |
|   cvxpy   |    cvxpy    |
|   dreal   |    dreal    |
|   gekko   |    gekko    |
|    pulp   |    PuLP     |
|     z3    |  z3-solver  |

測試
====
```console
$ sh test.sh
```

範例（Examples）
====
```console
$ PYTHONPATH=".:solvers/gekko" python3 examples/<<example>>.py
```

目前的範例有：

| 漢字 |    範例    |
| :--: | :--------: |
|  一  |  U4E00.py  |
|  十  |  U5341.py  |
|  土  |  U5341.py  |
|  士  |  U5341.py  |


