package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.Texture;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import io.hunterthecraft.pato.PatoGame;

public class LoadingScreen implements Screen {
    private PatoGame game;
    private SpriteBatch batch;
    private Texture logo;

    public LoadingScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = game.batch;
        // Carregue assets pesados aqui (ex: tileset, fontes)
        logo = new Texture("libgdx.png"); // placeholder

        // Simula carregamento (em 2 segundos vai pro menu)
        Gdx.app.postRunnable(() -> {
            game.setScreen(new MainMenuScreen(game));
            dispose(); // libera loading
        });
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.1f, 0.1f, 0.15f, 1);
        batch.begin();
        batch.draw(logo, 140, 210);
        batch.end();
    }

    @Override
    public void dispose() {
        if (logo != null) logo.dispose();
    }

    // Métodos vazios obrigatórios
    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
}