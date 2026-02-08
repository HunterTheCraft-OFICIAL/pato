// core/src/io/hunterthecraft/pato/model/WorldData.java
package io.hunterthecraft.pato.model;

import io.hunterthecraft.pato.data.TileType;

public class WorldData {
    public String name;
    public long seed;
    public int width = 5;
    public int height = 5;
    public TileType biomeA = TileType.AMAZONIA;
    public TileType biomeB = TileType.CERRADO;

    // Padrão xadrez
    public TileType getTileAt(int x, int y) {
        return ((x + y) % 2 == 0) ? biomeA : biomeB;
    }
}