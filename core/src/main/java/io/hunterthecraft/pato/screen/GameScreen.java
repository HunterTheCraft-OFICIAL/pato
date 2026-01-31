package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.GL20;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;

public class GameScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private Texture placeholderTile; // depois vira array de tiles

    public GameScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = game.batch;
        placeholderTile = new Texture("libgdx.png"); // temporário
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.3f, 0.3f, 0.3f, 1);
        batch.begin();
        // Desenha um grid 5x5 de placeholders
        for (int x = 0; x < 5; x++) {
            for (int y = 0; y < 5; y++) {
                batch.draw(placeholderTile, x * 64, y * 64, 64, 64);
            }
        }
        batch.end();
    }

    @Override
    public void dispose() {
        placeholderTile.dispose();
    }

    // Métodos vazios...
    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
}