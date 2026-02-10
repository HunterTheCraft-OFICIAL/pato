// core/src/io/hunterthecraft/pato/renderer/WorldRenderer.java
package io.hunterthecraft.pato.renderer;

import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.Disposable;
import io.hunterthecraft.pato.data.TileType;
import io.hunterthecraft.pato.model.Chunk;
import io.hunterthecraft.pato.model.ChunkManager;

public class WorldRenderer implements Disposable {
    private SpriteBatch batch; // ← Agora é worldBatch
    private Texture[] tileTextures;
    private ChunkManager chunkManager;
    private static final int TILE_SIZE = 128;

    public WorldRenderer(SpriteBatch batch) {
        this.batch = batch; // ← Recebe worldBatch
        this.chunkManager = new ChunkManager();
        loadTextures();
    }

    private void loadTextures() {
        tileTextures = new Texture[2];
        tileTextures[0] = new Texture("tiles/debug_amazonia.png");
        tileTextures[1] = new Texture("tiles/debug_cerrado.png");
    }

    public void render(float cameraX, float cameraY, float zoom) {
        int centerTileX = (int) (cameraX / TILE_SIZE);
        int centerTileY = (int) (cameraY / TILE_SIZE);
        
        int centerChunkX = ChunkManager.getChunkX(centerTileX);
        int centerChunkY = ChunkManager.getChunkY(centerTileY);

        int radius = 2;
        for (int cy = centerChunkY - radius; cy <= centerChunkY + radius; cy++) {
            for (int cx = centerChunkX - radius; cx <= centerChunkX + radius; cx++) {
                Chunk chunk = chunkManager.getChunk(cx, cy);
                for (int y = 0; y < Chunk.SIZE; y++) {
                    for (int x = 0; x < Chunk.SIZE; x++) {
                        TileType tile = chunk.getTile(x, y);
                        int globalX = cx * Chunk.SIZE + x;
                        int globalY = cy * Chunk.SIZE + y;
                        Texture tex = (tile == TileType.AMAZONIA) ? tileTextures[0] : tileTextures[1];
                        batch.draw(tex, globalX * TILE_SIZE, globalY * TILE_SIZE, TILE_SIZE, TILE_SIZE);
                    }
                }
            }
        }

        chunkManager.unloadDistantChunks(centerChunkX, centerChunkY);
    }

    public ChunkManager getChunkManager() {
        return chunkManager;
    }

    @Override
    public void dispose() {
        if (tileTextures != null) {
            for (Texture t : tileTextures) if (t != null) t.dispose();
        }
    }
}