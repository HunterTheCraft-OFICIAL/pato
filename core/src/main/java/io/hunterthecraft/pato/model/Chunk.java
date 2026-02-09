// core/src/io/hunterthecraft/pato/model/Chunk.java
package io.hunterthecraft.pato.model;

import io.hunterthecraft.pato.data.TileType;

public class Chunk {
    public static final int SIZE = 16;
    public final int chunkX, chunkY;
    private TileType[][] tiles = new TileType[SIZE][SIZE];

    public Chunk(int chunkX, int chunkY) { // ← CONFIRME: "int chunkY"
        this.chunkX = chunkX;
        this.chunkY = chunkY;
        generate();
    }

    private void generate() {
        for (int y = 0; y < SIZE; y++) {
            for (int x = 0; x < SIZE; x++) {
                int globalX = chunkX * SIZE + x;
                int globalY = chunkY * SIZE + y;
                tiles[x][y] = ((globalX + globalY) % 2 == 0) 
                    ? TileType.AMAZONIA 
                    : TileType.CERRADO;
            }
        }
    }

    public TileType getTile(int x, int y) {
        return tiles[x][y];
    }
}