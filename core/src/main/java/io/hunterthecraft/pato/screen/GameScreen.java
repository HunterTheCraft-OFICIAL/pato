// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.data.TileType;
import io.hunterthecraft.pato.model.WorldData;

public class GameScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private WorldData world;
    private Texture[] tileTextures;

    public GameScreen(PatoGame game, WorldData world) {
        this.game = game;
        this.world = world;
    }

    @Override
    public void show() {
        batch = new SpriteBatch();
        // Carrega texturas dos dois biomas
        tileTextures = new Texture[2];
        tileTextures[0] = new Texture(world.biomeA.getAssetPath());
        tileTextures[1] = new Texture(world.biomeB.getAssetPath());
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);

        batch.begin();
        int tileSize = 128; // ← AJUSTADO PARA 128px (tamanho realista)
        float offsetX = (Gdx.graphics.getBackBufferWidth() - world.width * tileSize) / 2f;
        float offsetY = (Gdx.graphics.getBackBufferHeight() - world.height * tileSize) / 2f;

        for (int y = 0; y < world.height; y++) {
            for (int x = 0; x < world.width; x++) {
                TileType tile = world.getTileAt(x, y);
                Texture tex = (tile == world.biomeA) ? tileTextures[0] : tileTextures[1];
                batch.draw(tex, offsetX + x * tileSize, offsetY + y * tileSize);
            }
        }
        batch.end();
    }

    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}

    @Override
    public void dispose() {
        if (tileTextures != null) {
            for (Texture tex : tileTextures) {
                if (tex != null) tex.dispose();
            }
        }
        if (batch != null) batch.dispose();
    }
}