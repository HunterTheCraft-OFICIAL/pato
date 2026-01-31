package io.hunterthecraft.pato.screen;

import com.badlogic.gdx.Gdx;
import com.badlogic.gdx.Screen;
import com.badlogic.gdx.graphics.g2d.SpriteBatch;
import com.badlogic.gdx.utils.ScreenUtils;
import com.badlogic.gdx.InputAdapter;
import io.hunterthecraft.pato.PatoGame;

public class MainMenuScreen extends InputAdapter implements Screen {
    private PatoGame game;
    private SpriteBatch batch;

    public MainMenuScreen(PatoGame game) {
        this.game = game;
    }

    @Override
    public void show() {
        batch = game.batch;
        Gdx.input.setInputProcessor(this);
    }

    @Override
    public void render(float delta) {
        ScreenUtils.clear(0.2f, 0.3f, 0.2f, 1); // verde escuro
        batch.begin();
        // Aqui pode desenhar "PATO - Main Menu"
        batch.end();
    }

    @Override
    public boolean touchDown(int screenX, int screenY, int pointer, int button) {
        // Qualquer toque inicia o jogo (MVP simples)
        game.setScreen(new GameScreen(game));
        return true;
    }

    @Override
    public void dispose() {}

    // Outros métodos vazios...
    @Override public void resize(int width, int height) {}
    @Override public void pause() {}
    @Override public void resume() {}
    @Override public void hide() {}
}