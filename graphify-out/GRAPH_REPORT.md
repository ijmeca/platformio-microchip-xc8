# Graph Report - platform-microchip8  (2026-08-02)

## Corpus Check
- 41 files · ~5,539 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 144 nodes · 274 edges · 20 communities (17 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8c002005`
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
- make_executable
- install_pk2cmd_macos.py

## God Nodes (most connected - your core abstractions)
1. `make_executable()` - 14 edges
2. `find_ipecmd()` - 13 edges
3. `find_xc8()` - 13 edges
4. `PICkit3DetectionTests` - 11 edges
5. `discover_dfps()` - 10 edges
6. `build_device_index()` - 10 edges
7. `normalize_dfp_path()` - 9 edges
8. `normalize_xc8_path()` - 8 edges
9. `verify_archive()` - 8 edges
10. `main()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `upload_firmware()` --calls--> `find_ipecmd()`  [INFERRED]
  builder/main.py → scripts/detect_ipecmd.py
- `upload_firmware()` --calls--> `pickit3_command()`  [INFERRED]
  builder/main.py → scripts/detect_ipecmd.py
- `upload_firmware()` --calls--> `find_pickit3()`  [INFERRED]
  builder/main.py → scripts/detect_pickit3.py
- `upload_firmware()` --calls--> `standalone_pickit3_command()`  [INFERRED]
  builder/main.py → scripts/detect_pickit3.py
- `upload_firmware()` --calls--> `find_pk2cmd()`  [INFERRED]
  builder/main.py → scripts/detect_pk2cmd.py

## Import Cycles
- None detected.

## Communities (20 total, 3 thin omitted)

### Community 0 - "pic12f615-blink/src/main.c"
Cohesion: 0.19
Nodes (18): build_device_index(), _deduplicate(), default_dfp_roots(), devices_in_dfp(), discover_dfps(), _find_under_root(), normalize_dfp_path(), normalize_mcu() (+10 more)

### Community 1 - "find_xc8"
Cohesion: 0.24
Nodes (10): _automatic_candidates(), default_ipecmd_roots(), find_ipecmd(), normalize_ipecmd_path(), pickit3_command(), Path, Discovery and command helpers for MPLAB IPE and PICkit 3., semantic_version_key() (+2 more)

### Community 2 - "detect_pickit3.py"
Cohesion: 0.19
Nodes (14): _automatic_candidates(), default_xc8_roots(), find_xc8(), _newest(), normalize_xc8_path(), Path, Discovery and normalization helpers for externally installed MPLAB XC8., Find XC8 in documented priority order. (+6 more)

### Community 3 - "DFPDetectionTests"
Cohesion: 0.33
Nodes (4): Assembly, PICkit3Uploader, STAThread, Type

### Community 4 - "Microchip8Platform"
Cohesion: 0.16
Nodes (11): upload_firmware(), default_pickit3_roots(), find_pickit3(), normalize_pickit3_path(), Path, Discovery and command helpers for the standalone PICkit 3 application., standalone_pickit3_command(), find_pk2cmd() (+3 more)

### Community 19 - "install_pk2cmd_macos.py"
Cohesion: 0.29
Nodes (11): confirm(), install_archive(), main(), parse_args(), Path, require_supported_mac(), sha256(), validate_runtime() (+3 more)

## Knowledge Gaps
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `find_xc8()` connect `detect_pickit3.py` to `pic12f615-blink/src/main.c`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Why does `make_executable()` connect `detect_pickit3.py` to `pic12f615-blink/src/main.c`, `find_xc8`, `Microchip8Platform`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `find_ipecmd()` connect `find_xc8` to `pic12f615-blink/src/main.c`, `Microchip8Platform`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._