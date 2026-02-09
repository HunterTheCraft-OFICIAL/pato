// core/src/io/hunterthecraft/pato/model/ChunkManager.java
package io.hunterthecraft.pato.model;

import java.util.HashMap;
import java.util.Map;

public class ChunkManager {
    private Map<String, Chunk> loadedChunks = new HashMap<>();
    private static final int RENDER_RADIUS = 2;

    public Chunk getChunk(int chunkX, int chunkY) {
        String key = chunkX + "," + chunkY;
        return loadedChunks.computeIfAbsent(key, k -> new Chunk(chunkX, chunkY));
    }

    // ✅ Lida corretamente com coordenadas negativas
    public static int getChunkX(int tileX) {
        return tileX >= 0 ? tileX / Chunk.SIZE : (tileX - Chunk.SIZE + 1) / Chunk.SIZE;
    }

    public static int getChunkY(int tileY) {
        return tileY >= 0 ? tileY / Chunk.SIZE : (tileY - Chunk.SIZE + 1) / Chunk.SIZE;
    }

    public void unloadDistantChunks(int playerChunkX, int playerChunkY) {
        loadedChunks.entrySet().removeIf(entry -> {
            String[] parts = entry.getKey().split(",");
            int cx = Integer.parseInt(parts[0]);
            int cy = Integer.parseInt(parts[1]);
            return Math.abs(cx - playerChunkX) > RENDER_RADIUS || 
                   Math.abs(cy - playerChunkY) > RENDER_RADIUS;
        });
    }
}