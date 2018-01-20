/*
  Generic 5 node topology example
*/
var topologyData = {
    nodes: [
        {"id": 0, "x": 410, "y": 100, "name": "router 1"},
        {"id": 1, "x": 410, "y": 280, "name": "router 2"},
        {"id": 2, "x": 660, "y": 280, "name": "router 3"},
        {"id": 3, "x": 660, "y": 100, "name": "router 4"},
        {"id": 4, "x": 180, "y": 190, "name": "router 5"}
    ],
    links: [
        {"source": 0, "target": 1},
        {"source": 1, "target": 2},
        {"source": 1, "target": 3},
        {"source": 4, "target": 1},
        {"source": 2, "target": 3},
        {"source": 2, "target": 0},
        {"source": 3, "target": 0},
        {"source": 3, "target": 0},
        {"source": 3, "target": 0},
        {"source": 0, "target": 4},
        {"source": 0, "target": 4},
        {"source": 0, "target": 3}
    ]
};

/* EOF */

