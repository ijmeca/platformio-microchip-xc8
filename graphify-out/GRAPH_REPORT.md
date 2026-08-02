# Graph Report - platformio-microchip-xc8  (2026-08-01)

## Corpus Check
- 28 files · ~3,643 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 104 nodes · 192 edges · 18 communities (15 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `16b63020`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- find_xc8
- detect_pickit3.py
- DFPDetectionTests
- Microchip8Platform
- BoardManifestTests
- detect_ipecmd.py
- PICkit3Uploader
- test_detection.py

## God Nodes (most connected - your core abstractions)
1. `find_xc8()` - 13 edges
2. `discover_dfps()` - 10 edges
3. `build_device_index()` - 10 edges
4. `normalize_dfp_path()` - 9 edges
5. `find_ipecmd()` - 9 edges
6. `normalize_xc8_path()` - 8 edges
7. `make_executable()` - 8 edges
8. `XC8DetectionTests` - 8 edges
9. `select_dfp_for_mcu()` - 7 edges
10. `find_pickit3()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `upload_firmware()` --calls--> `find_pickit3()`  [INFERRED]
  builder/main.py → scripts/detect_pickit3.py
- `upload_firmware()` --calls--> `standalone_pickit3_command()`  [INFERRED]
  builder/main.py → scripts/detect_pickit3.py
- `upload_firmware()` --calls--> `find_ipecmd()`  [INFERRED]
  builder/main.py → scripts/detect_ipecmd.py
- `upload_firmware()` --calls--> `pickit3_command()`  [INFERRED]
  builder/main.py → scripts/detect_ipecmd.py

## Import Cycles
- None detected.

## Communities (18 total, 3 thin omitted)

### Community 1 - "find_xc8"
Cohesion: 0.19
Nodes (14): _automatic_candidates(), default_xc8_roots(), find_xc8(), _newest(), normalize_xc8_path(), Path, Discovery and normalization helpers for externally installed MPLAB XC8., Find XC8 in documented priority order. (+6 more)

### Community 2 - "detect_pickit3.py"
Cohesion: 0.43
Nodes (6): default_pickit3_roots(), find_pickit3(), normalize_pickit3_path(), Path, Discovery and command helpers for the standalone PICkit 3 application., standalone_pickit3_command()

### Community 6 - "detect_ipecmd.py"
Cohesion: 0.25
Nodes (10): upload_firmware(), _automatic_candidates(), default_ipecmd_roots(), find_ipecmd(), normalize_ipecmd_path(), pickit3_command(), Path, Discovery and command helpers for MPLAB IPE and PICkit 3. (+2 more)

### Community 15 - "PICkit3Uploader"
Cohesion: 0.33
Nodes (4): Assembly, PICkit3Uploader, STAThread, Type

### Community 16 - "test_detection.py"
Cohesion: 0.27
Nodes (16): build_device_index(), _deduplicate(), default_dfp_roots(), devices_in_dfp(), discover_dfps(), _find_under_root(), normalize_dfp_path(), normalize_mcu() (+8 more)

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `find_xc8()` connect `find_xc8` to `test_detection.py`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Why does `discover_dfps()` connect `test_detection.py` to `DFPDetectionTests`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `find_ipecmd()` connect `detect_ipecmd.py` to `test_detection.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._