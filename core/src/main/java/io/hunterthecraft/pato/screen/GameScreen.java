package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;

public class GameScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;

    public GameScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = game.batch;
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.3f, 0.3f, 0.4f, 1);
        batch.begin();
        // Mapa será adicionado depois
        batch.end();
    }

    @Override public void dispose() {}
    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
}
