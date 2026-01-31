// core/src/io/hunterthecraft/pato/model/MapTile.java
package io.hunterthecraft.pato.model;

import io.hunterthecraft.pato.data.TileType;

public class MapTile {
    public final int x, y;
    public TileType type;

    public MapTile(int x, int y, TileType type) {
        this.x = x;
        this.y = y;
        this.type = type;
    }
}