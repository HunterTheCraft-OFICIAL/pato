// core/src/io/hunterthecraft/pato/model/GameMap.java
package io.hunterthecraft.pato.model;

import io.hunterthecraft.pato.data.TileType;
import java.util.Random;

public class GameMap {
    public static final int WIDTH = 10;
    public static final int HEIGHT = 10;
    private MapTile[][] tiles = new MapTile[WIDTH][HEIGHT];
    private Random random = new Random();

    public GameMap() {
        generate();
    }

    private void generate() {
        TileType[] types = TileType.values();
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++) {
                TileType randomType = types[random.nextInt(types.length)];
                tiles[x][y] = new MapTile(x, y, randomType);
            }
        }
    }

    public MapTile getTile(int x, int y) {
        if (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT) {
            return tiles[x][y];
        }
        return null;
    }
}