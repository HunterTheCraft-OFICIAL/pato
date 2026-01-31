// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.model.GameMap;
import io.hunterthecraft.pato.data.TileType;

public class GameScreen implements Screen {
    private PatoGame game;
    private GameMap map;
    private Texture[] tileTextures = new Texture[TileType.values().length];

    public GameScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        // Carrega texturas
        for (TileType type : TileType.values()) {
            tileTextures[type.ordinal()] = new Texture("tiles/" + type.key + ".png");
        }
        map = new GameMap();
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.2f, 0.2f, 0.3f, 1);
        game.batch.begin();
        for (int x = 0; x < GameMap.WIDTH; x++) {
            for (int y = 0; y < GameMap.HEIGHT; y++) {
                var tile = map.getTile(x, y);
                if (tile != null) {
                    Texture tex = tileTextures[tile.type.ordinal()];
                    game.batch.draw(tex, x * 64, Gdx.graphics.getHeight() - (y + 1) * 64);
                }
            }
        }
        game.batch.end();
    }

    @Override
    public void dispose() {
        for (Texture tex : tileTextures) {
            if (tex != null) tex.dispose();
        }
    }

    // Métodos vazios...
    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
}