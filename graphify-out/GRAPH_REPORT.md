# Graph Report - platform-microchip8  (2026-08-02)

## Corpus Check
- 37 files · ~4,317 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 111 nodes · 209 edges · 18 communities (16 shown, 2 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `75be9e0e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- pic12f615-blink/src/main.c
- find_xc8
- detect_pickit3.py
- DFPDetectionTests
- Microchip8Platform
- BoardManifestTests
- detect_ipecmd.py

## God Nodes (most connected - your core abstractions)
1. `find_ipecmd()` - 13 edges
2. `find_xc8()` - 13 edges
3. `make_executable()` - 12 edges
4. `discover_dfps()` - 10 edges
5. `build_device_index()` - 10 edges
6. `normalize_dfp_path()` - 9 edges
7. `normalize_xc8_path()` - 8 edges
8. `XC8DetectionTests` - 8 edges
9. `PICkit3DetectionTests` - 8 edges
10. `select_dfp_for_mcu()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `upload_firmware()` --calls--> `find_pickit3()`  [INFERRED]
  builder/main.py → scripts/detect_pickit3.py
- `upload_firmware()` --calls--> `find_ipecmd()`  [INFERRED]
  builder/main.py → scripts/detect_ipecmd.py
- `upload_firmware()` --calls--> `pickit3_command()`  [INFERRED]
  builder/main.py → scripts/detect_ipecmd.py
- `upload_firmware()` --calls--> `standalone_pickit3_command()`  [INFERRED]
  builder/main.py → scripts/detect_pickit3.py

## Import Cycles
- None detected.

## Communities (18 total, 2 thin omitted)

### Community 0 - "pic12f615-blink/src/main.c"
Cohesion: 0.18
Nodes (18): build_device_index(), _deduplicate(), default_dfp_roots(), devices_in_dfp(), discover_dfps(), _find_under_root(), normalize_dfp_path(), normalize_mcu() (+10 more)

### Community 1 - "find_xc8"
Cohesion: 0.22
Nodes (13): upload_firmware(), _automatic_candidates(), default_ipecmd_roots(), find_ipecmd(), normalize_ipecmd_path(), pickit3_command(), Path, Discovery and command helpers for MPLAB IPE and PICkit 3. (+5 more)

### Community 2 - "detect_pickit3.py"
Cohesion: 0.19
Nodes (13): _automatic_candidates(), default_xc8_roots(), find_xc8(), _newest(), normalize_xc8_path(), Path, Discovery and normalization helpers for externally installed MPLAB XC8., Find XC8 in documented priority order. (+5 more)

### Community 3 - "DFPDetectionTests"
Cohesion: 0.33
Nodes (4): Assembly, PICkit3Uploader, STAThread, Type

### Community 4 - "Microchip8Platform"
Cohesion: 0.39
Nodes (5): default_pickit3_roots(), find_pickit3(), normalize_pickit3_path(), Path, Discovery and command helpers for the standalone PICkit 3 application.

## Knowledge Gaps
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `find_xc8()` connect `detect_pickit3.py` to `find_xc8`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `make_executable()` connect `find_xc8` to `detect_pickit3.py`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._