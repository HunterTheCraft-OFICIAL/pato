// core/src/main/java/io/hunterthecraft/pato/model/WorldData.java
package io.hunterthecraft.pato.model;

import io.hunterthecraft.pato.data.TileType; // ← agora existe!

public class WorldData {
    public String name = "Mundo Xadrez";
    public long seed = 42;
    public int width = 5;
    public int height = 5;
    public TileType biomeA = TileType.AMAZONIA;
    public TileType biomeB = TileType.CERRADO;

    public TileType getTileAt(int x, int y) {
        return ((x + y) % 2 == 0) ? biomeA : biomeB;
    }
}