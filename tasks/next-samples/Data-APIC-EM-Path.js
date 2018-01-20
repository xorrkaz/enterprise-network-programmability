/*
  APIC-EM Path Trace Example - single layer, linear topology
*/
var topologyData = {
    nodes: [
        {"id": 0, "x": 050, "y": 100, "name": "65.1.1.46"},
        {"id": 1, "x": 100, "y": 50, "name": "AP7081.059f.19ca"},
        {"id": 2, "x": 150, "y": 100, "name": "CAMPUS-Access1"},
        {"id": 3, "x": 200, "y": 50, "name": "CAMPUS-Dist1"},
        {"id": 4, "x": 250, "y": 100, "name": "Campus-WLC-5508"},
        {"id": 5, "x": 300, "y": 50, "name": "CAMPUS-Dist1"},
        {"id": 6, "x": 350, "y": 100, "name": "CAMPUS-Core2"},
        {"id": 7, "x": 400, "y": 50, "name": "CAMPUS-Router1"},
        {"id": 8, "x": 450, "y": 100, "name": "Unknown Device"},
        {"id": 9, "x": 500, "y": 50, "name": "Branch-Router2"},
        {"id": 10, "x": 550, "y": 100, "name": "Branch-Access1"},
        {"id": 11, "x": 600, "y": 50, "name": "207.1.10.20"}
    ],
    links: [
        {"source": 0, "target": 1},
        {"source": 1, "target": 2},
        {"source": 2, "target": 3},
        {"source": 3, "target": 4},
        {"source": 4, "target": 5},
        {"source": 5, "target": 6},
        {"source": 6, "target": 7},
        {"source": 7, "target": 8},
        {"source": 8, "target": 9},
        {"source": 9, "target": 10},
        {"source": 10, "target": 11}
    ]
};
/* EOF */