// core/src/io/hunterthecraft/pato/model/ChunkManager.java
package io.hunterthecraft.pato.model;

import java.util.HashMap;
import java.util.Map;

public class ChunkManager {
    private Map<String, Chunk> loadedChunks = new HashMap<>();
    private static final int RENDER_RADIUS = 2; // chunks visíveis

    public Chunk getChunk(int chunkX, chunkY) {
        String key = chunkX + "," + chunkY;
        return loadedChunks.computeIfAbsent(key, k -> new Chunk(chunkX, chunkY));
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