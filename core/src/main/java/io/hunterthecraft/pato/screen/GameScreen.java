// core/src/io/hunterthecraft/pato/screen/GameScreen.java
package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.assets.AssetManager;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;
import io.hunterthecraft.pato.data.TileType;

public class GameScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private AssetManager assetManager;

    private TileType[][] exampleMap = {
        {TileType.AMAZONIA, TileType.AMAZONIA, TileType.RIO_RETO_V, TileType.CAATINGA, TileType.CAATINGA},
        {TileType.CERRADO, TileType.AMAZONIA, TileType.RIO_RETO_V, TileType.CAATINGA, TileType.AREIA_SUDESTE},
        {TileType.CERRADO, TileType.RIO_CURVA_NE, TileType.LAGO_G, TileType.FOZ_N, TileType.AREIA_SUDESTE},
        {TileType.CERRADO, TileType.CRUZAMENTO_P, TileType.PONTA_S, TileType.AMAZONIA, TileType.AMAZONIA},
        {TileType.CAATINGA, TileType.CAATINGA, TileType.CAATINGA, TileType.CERRADO, TileType.CERRADO}
    };

    public GameScreen(PatoGame game, AssetManager assetManager) {
        this.game = game;
        this.assetManager = assetManager;
    }

    @Override
    public void show() {
        batch = game.batch;
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);
        batch.begin();

        int tileSize = 64;
        int mapWidth = exampleMap[0].length;
        int mapHeight = exampleMap.length;

        float offsetX = (Gdx.graphics.getWidth() - mapWidth * tileSize) / 2f;
        float offsetY = (Gdx.graphics.getHeight() - mapHeight * tileSize) / 2f;

        // Primeiro: terreno (sem alpha)
        for (int y = 0; y < mapHeight; y++) {
            for (int x = 0; x < mapWidth; x++) {
                TileType tile = exampleMap[y][x];
                if (!tile.isWater()) {
                    Texture tex = assetManager.get(tile.getAssetPath(), Texture.class);
                    batch.draw(tex, offsetX + x * tileSize, offsetY + y * tileSize);
                }
            }
        }

        // Depois: água (com alpha, por cima)
        for (int y = 0; y < mapHeight; y++) {
            for (int x = 0; x < mapWidth; x++) {
                TileType tile = exampleMap[y][x];
                if (tile.isWater()) {
                    Texture tex = assetManager.get(tile.getAssetPath(), Texture.class);
                    batch.draw(tex, offsetX + x * tileSize, offsetY + y * tileSize);
                }
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
        // AssetManager será descartado pelo jogo principal ou tela anterior
    }
}